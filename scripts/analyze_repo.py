"""Read-only repository analyze for Abraxas Orchestra (Phase A).

Stdlib only. Walks a local Python tree, builds an import graph, optionally
maps nodes onto frameworks.v1 loci with fail-closed strength scoring.
"""

from __future__ import annotations

import ast
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

SKIP_DIRS = frozenset({
    ".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "node_modules",
    ".tox", ".mypy_cache", ".ruff_cache", "dist", "build", ".eggs",
    ".pytest_cache", ".cursor", ".orchestra-backups",
})

# First path segment after root that indicates a system tree (POSIX).
SYSTEM_TOP = frozenset({
    "etc", "usr", "bin", "sbin", "boot", "dev", "proc", "sys",
    "lib", "lib64", "System", "Windows", "root",
})

STRENGTH_RANK = {"STRONG": 3, "ADEQUATE": 2, "WEAK": 1, "FORCED": 0}


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def path_jail_ok(path: Path, *, allow_system: bool = False) -> tuple[bool, str]:
    """Refuse filesystem root and classic system prefixes (installer spirit)."""
    try:
        resolved = path.expanduser().resolve()
    except OSError as exc:
        return False, f"unresolvable path: {exc}"
    if not resolved.exists():
        return False, f"path does not exist: {resolved}"
    if not resolved.is_dir():
        return False, f"path is not a directory: {resolved}"
    if allow_system:
        return True, ""
    if resolved == Path("/"):
        return False, "refusing to analyze filesystem root /"
    parts = resolved.parts
    # Absolute POSIX: ('/', 'etc', ...) or ('/', 'usr', ...)
    if len(parts) >= 2 and parts[0] == "/" and parts[1] in SYSTEM_TOP:
        return False, f"refusing system path: {resolved}"
    return True, ""


def _module_id(root: Path, py_file: Path) -> str:
    rel = py_file.relative_to(root)
    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = Path(parts[-1]).stem
    if not parts:
        return root.name or "root"
    return ".".join(parts)


def _pkg_parts(root: Path, py_file: Path) -> list[str]:
    """Package parts for the directory containing py_file, relative to root."""
    rel = py_file.parent.relative_to(root)
    if str(rel) == ".":
        return []
    return list(rel.parts)


def _collect_py_files(root: Path, *, max_depth: int | None, max_files: int) -> list[Path]:
    files: list[Path] = []
    root = root.resolve()

    def walk(current: Path, depth: int) -> None:
        if len(files) >= max_files:
            return
        if max_depth is not None and depth > max_depth:
            return
        try:
            entries = sorted(current.iterdir(), key=lambda p: p.name)
        except OSError:
            return
        for entry in entries:
            if len(files) >= max_files:
                return
            name = entry.name
            if entry.is_dir():
                if name in SKIP_DIRS or name.startswith("."):
                    continue
                walk(entry, depth + 1)
            elif entry.is_file() and entry.suffix == ".py":
                files.append(entry)

    walk(root, 0)
    return files[:max_files]


def _resolve_import(
    *,
    root: Path,
    current_file: Path,
    module: str | None,
    level: int,
    name: str | None,
    known: set[str],
) -> str | None:
    """Best-effort resolve to a known module id, else absolute/external name."""
    if level > 0:
        pkg = _pkg_parts(root, current_file)
        up = level - 1
        if up > len(pkg):
            base: list[str] = []
        else:
            base = pkg[: len(pkg) - up] if up else list(pkg)
        suffix: list[str] = []
        if module:
            suffix = module.split(".")
        elif name:
            suffix = [name]
        candidate = ".".join(base + suffix)
        if not candidate:
            return None
        if candidate in known:
            return candidate
        # Prefer longest known prefix
        parts = candidate.split(".")
        for i in range(len(parts), 0, -1):
            cand = ".".join(parts[:i])
            if cand in known:
                return cand
        return candidate

    if module:
        if module in known:
            return module
        parts = module.split(".")
        for i in range(len(parts), 0, -1):
            cand = ".".join(parts[:i])
            if cand in known:
                return cand
        return module
    return name


def _imports_from_ast(
    tree: ast.AST,
    *,
    root: Path,
    current_file: Path,
    known: set[str],
) -> list[tuple[str, bool]]:
    found: list[tuple[str, bool]] = []
    self_id = _module_id(root, current_file)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                target = _resolve_import(
                    root=root,
                    current_file=current_file,
                    module=alias.name,
                    level=0,
                    name=None,
                    known=known,
                )
                if target:
                    found.append((target, target not in known))
        elif isinstance(node, ast.ImportFrom):
            mod = node.module
            level = node.level or 0
            if level == 0 and mod is None:
                continue
            if mod is not None or level == 0:
                target = _resolve_import(
                    root=root,
                    current_file=current_file,
                    module=mod,
                    level=level,
                    name=None,
                    known=known,
                )
                if target:
                    found.append((target, target not in known))
                continue
            # from . import name, name2
            for alias in node.names:
                if alias.name == "*":
                    continue
                target = _resolve_import(
                    root=root,
                    current_file=current_file,
                    module=None,
                    level=level,
                    name=alias.name,
                    known=known,
                )
                if target:
                    found.append((target, target not in known))

    seen: set[str] = set()
    out: list[tuple[str, bool]] = []
    for t, ext in found:
        if t == self_id or t in seen:
            continue
        seen.add(t)
        out.append((t, ext))
    return out


def _tokenize(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9_]+", text.lower()) if t and len(t) > 1}


def _map_node_to_locus(
    node: dict[str, Any],
    loci: list[tuple[str, str, str]],
    *,
    source_text: str = "",
) -> dict[str, Any] | None:
    """Score best locus match. Never invents symbolic names."""
    nid = node["id"]
    leaf = nid.split(".")[-1]
    tokens = _tokenize(nid + " " + source_text)
    best: tuple[int, tuple[str, str, str], str] | None = None

    for mech, sym, note in loci:
        mech_l = mech.lower()
        sym_l = sym.lower()
        note_toks = _tokenize(note)
        if leaf == mech_l or nid.lower() == mech_l or leaf == sym_l:
            strength = "STRONG"
        elif mech_l in tokens or mech_l in nid.lower().split("."):
            strength = "ADEQUATE"
        elif tokens & (_tokenize(mech) | _tokenize(sym) | note_toks):
            strength = "WEAK"
        else:
            continue
        rank = STRENGTH_RANK[strength]
        if best is None or rank > best[0]:
            best = (rank, (mech, sym, note), strength)

    if best is None:
        return None
    _, (mech, sym, note), strength = best
    return {
        "functional_concern": note or mech,
        "mechanical_name": mech,
        "symbolic_name": sym,
        "symbolic_locus": sym,
        "strength": strength,
        "notes": note,
        "node_id": nid,
    }


def _suggest_frameworks(
    nodes: list[dict[str, Any]],
    frameworks: dict[str, dict[str, Any]],
) -> list[str]:
    leaves = {n["id"].split(".")[-1].lower() for n in nodes}
    scored: list[tuple[int, str]] = []
    for key, meta in frameworks.items():
        mechs = {m.lower() for m, _, _ in meta.get("default_loci") or []}
        hit = len(leaves & mechs)
        if hit:
            scored.append((hit, key))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [k for _, k in scored[:5]]


def _error_analysis(
    *,
    path: str,
    lang: str,
    framework: str | None,
    overlay: str | None,
    version: str,
    error: str,
) -> dict[str, Any]:
    return {
        "schema": "orchestra-analysis.v1",
        "path": path,
        "language": lang,
        "framework": framework,
        "secondary_overlay": overlay,
        "status": "NOT_COMPUTABLE",
        "nodes": [],
        "edges": [],
        "mappings": [],
        "provenance": {
            "operator": "orchestra-cli",
            "timestamp": _utc_now(),
            "skill_version": version,
            "kind": "OBSERVED",
            "error": error,
        },
    }


def analyze_path(
    path: str | Path,
    *,
    frameworks: dict[str, dict[str, Any]],
    version: str,
    framework: str | None = None,
    overlay: str | None = None,
    lang: str = "python",
    max_depth: int | None = None,
    max_files: int = 2000,
    allow_system: bool = False,
) -> tuple[dict[str, Any], int]:
    """Analyze a local directory. Returns (analysis_dict, exit_code 0|1|2)."""
    root = Path(path).expanduser()
    ok, reason = path_jail_ok(root, allow_system=allow_system)
    if not ok:
        return _error_analysis(
            path=str(root), lang=lang, framework=framework,
            overlay=overlay, version=version, error=reason,
        ), 2

    root = root.resolve()
    if lang != "python":
        return _error_analysis(
            path=str(root), lang=lang, framework=framework,
            overlay=overlay, version=version,
            error=f"unsupported language for v1: {lang}",
        ), 2

    if framework and framework not in frameworks:
        return _error_analysis(
            path=str(root), lang=lang, framework=framework,
            overlay=overlay, version=version,
            error=f"unknown framework: {framework}",
        ), 2

    if overlay and overlay not in frameworks:
        return _error_analysis(
            path=str(root), lang=lang, framework=framework,
            overlay=overlay, version=version,
            error=f"unknown overlay: {overlay}",
        ), 2

    py_files = _collect_py_files(root, max_depth=max_depth, max_files=max_files)
    if not py_files:
        return _error_analysis(
            path=str(root), lang=lang, framework=framework,
            overlay=overlay, version=version,
            error="empty tree — no Python files found",
        ), 2

    id_for_file = {f: _module_id(root, f) for f in py_files}
    known = set(id_for_file.values())

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    source_by_id: dict[str, str] = {}

    for f in py_files:
        mid = id_for_file[f]
        rel = str(f.relative_to(root))
        kind = "package" if f.name == "__init__.py" else "module"
        parse_error = None
        imports: list[str] = []
        try:
            text = f.read_text(encoding="utf-8")
            source_by_id[mid] = text[:2000]
            tree = ast.parse(text, filename=str(f))
            for target, external in _imports_from_ast(
                tree, root=root, current_file=f, known=known
            ):
                imports.append(target)
                edges.append({
                    "from": mid,
                    "to": target,
                    "kind": "import",
                    "provenance": "OBSERVED",
                    "external": external,
                })
        except SyntaxError as exc:
            parse_error = f"SyntaxError: {exc.msg} (line {exc.lineno})"
            source_by_id[mid] = ""
        except OSError as exc:
            parse_error = f"OSError: {exc}"
            source_by_id[mid] = ""

        nodes.append({
            "id": mid,
            "path": rel,
            "kind": kind,
            "provenance": "OBSERVED",
            "imports": imports,
            "parse_error": parse_error,
        })

    mappings: list[dict[str, Any]] = []
    candidate_frameworks: list[str] = []
    status = "OBSERVED_ONLY"
    exit_code = 0

    if framework:
        loci = list(frameworks[framework]["default_loci"])
        overlay_notes: list[str] = []
        if overlay and overlay in frameworks:
            o_loci = frameworks[overlay]["default_loci"]
            for i, _ in enumerate(loci):
                if i < len(o_loci):
                    _, o_sym, o_note = o_loci[i]
                    overlay_notes.append(f"overlay:{overlay}/{o_sym} ({o_note})")
        used_loci: set[str] = set()
        mech_set = {m for m, _, _ in loci}
        for node in nodes:
            leaf = node["id"].split(".")[-1]
            # Skip package __init__ nodes that are not themselves a locus name
            if node["kind"] == "package" and leaf not in mech_set:
                continue
            m = _map_node_to_locus(
                node, loci, source_text=source_by_id.get(node["id"], "")
            )
            if m is None:
                continue
            if m["mechanical_name"] in used_loci and m["strength"] == "WEAK":
                continue
            used_loci.add(m["mechanical_name"])
            if overlay_notes:
                try:
                    idx = [x[0] for x in loci].index(m["mechanical_name"])
                    if idx < len(overlay_notes):
                        m["overlay_note"] = overlay_notes[idx]
                except ValueError:
                    pass
            mappings.append(m)

        forced = sum(1 for m in mappings if m["strength"] == "FORCED")
        weak = sum(1 for m in mappings if m["strength"] == "WEAK")
        if forced:
            status = "FORCED_CORRESPONDENCE"
            exit_code = 1
        elif weak:
            status = "WEAK_MAPPINGS"
            exit_code = 1
        else:
            status = "CLEAN"
            exit_code = 0
    else:
        candidate_frameworks = _suggest_frameworks(nodes, frameworks)

    analysis: dict[str, Any] = {
        "schema": "orchestra-analysis.v1",
        "path": str(root),
        "language": lang,
        "framework": framework,
        "secondary_overlay": overlay,
        "status": status,
        "nodes": nodes,
        "edges": edges,
        "mappings": mappings,
        "provenance": {
            "operator": "orchestra-cli",
            "timestamp": _utc_now(),
            "skill_version": version,
            "kind": "OBSERVED",
        },
    }
    if candidate_frameworks:
        analysis["candidate_frameworks"] = candidate_frameworks
        analysis["provenance"]["kind"] = "SPECULATIVE"
    return analysis, exit_code


def analysis_to_diagram_graph(analysis: dict[str, Any], *, version: str) -> dict[str, Any]:
    """Convert analysis to orchestra-diagram.v1 (import topology)."""
    map_by_node = {
        m.get("node_id"): m
        for m in (analysis.get("mappings") or [])
        if m.get("node_id")
    }
    nodes = []
    for n in analysis.get("nodes") or []:
        m = map_by_node.get(n["id"])
        mech = (m or {}).get("mechanical_name") or n["id"].split(".")[-1]
        sym = (m or {}).get("symbolic_name") or n["id"]
        nodes.append({
            "id": n["id"],
            "mechanical": mech,
            "symbolic": sym,
            "label": f"{mech} · {sym}",
            "note": (m or {}).get("notes") or n.get("path") or "",
            "order": len(nodes),
            "provenance": n.get("provenance", "OBSERVED"),
        })
    edges = []
    for i, e in enumerate(analysis.get("edges") or []):
        if e.get("external"):
            continue
        edges.append({
            "id": f"e-{i}-{e['from']}-{e['to']}",
            "from": e["from"],
            "to": e["to"],
            "kind": e.get("kind", "import"),
        })
    return {
        "schema": "orchestra-diagram.v1",
        "framework": analysis.get("framework") or "observed",
        "secondary_overlay": analysis.get("secondary_overlay"),
        "nodes": nodes,
        "edges": edges,
        "flows": [{
            "id": "import-topology",
            "name": "observed import topology",
            "steps": [n["id"] for n in nodes],
        }],
        "provenance": {
            "operator": "orchestra-cli",
            "timestamp": _utc_now(),
            "skill_version": version,
            "kind": "OBSERVED",
        },
    }


def write_analysis_artifacts(
    analysis: dict[str, Any],
    out_dir: Path,
    *,
    version: str,
    html_fn: Callable[[dict[str, Any]], str] | None = None,
) -> None:
    """Write analysis.json, optional correspondence table, and diagram bundle."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "analysis.json").write_text(
        json.dumps(analysis, indent=2) + "\n", encoding="utf-8"
    )

    if analysis.get("framework") and analysis.get("mappings"):
        status = analysis["status"]
        if status == "OBSERVED_ONLY":
            status = "CLEAN"
        table = {
            "framework": analysis["framework"],
            "secondary_overlay": analysis.get("secondary_overlay"),
            "status": status,
            "mappings": [
                {k: v for k, v in m.items() if k != "node_id"}
                for m in analysis["mappings"]
            ],
            "pragmatic_projection": None,
            "provenance": analysis.get("provenance"),
        }
        (out_dir / "correspondence-table.json").write_text(
            json.dumps(table, indent=2) + "\n", encoding="utf-8"
        )

    graph = analysis_to_diagram_graph(analysis, version=version)
    if html_fn is None:
        from diagram_emit import _html_diagram
        html_fn = _html_diagram
    from diagram_mermaid import write_diagram_files
    write_diagram_files(out_dir, graph, html=html_fn(graph), quiet=True)
