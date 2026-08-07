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


def _collect_source_files(
    root: Path,
    *,
    extensions: frozenset[str] | set[str],
    max_depth: int | None,
    max_files: int,
) -> list[Path]:
    files: list[Path] = []
    root = root.resolve()
    exts = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in extensions}

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
            elif entry.is_file() and entry.suffix.lower() in exts:
                files.append(entry)

    walk(root, 0)
    return files[:max_files]


def _collect_py_files(root: Path, *, max_depth: int | None, max_files: int) -> list[Path]:
    """Backward-compatible collector for Python only."""
    return _collect_source_files(
        root, extensions={".py"}, max_depth=max_depth, max_files=max_files
    )


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


def _norm_ident(s: str) -> str:
    """Normalize identifiers for fuzzy mechanical match (hyphen/underscore/case)."""
    return re.sub(r"[^a-z0-9]+", "", s.lower())


# Common software-role tokens → conceptual families used only to boost matching
# against existing locus tokens/notes. Never invents symbolic names.
_ROLE_SYNONYMS: dict[str, frozenset[str]] = {
    # intake / edge
    "ingest": frozenset({"intake", "ingest", "raw", "edge", "signal", "pull", "fetch", "load"}),
    "intake": frozenset({"intake", "ingest", "raw", "edge", "signal", "pull", "fetch", "load"}),
    "loader": frozenset({"intake", "ingest", "load", "raw"}),
    "reader": frozenset({"intake", "ingest", "load", "read"}),
    "parser": frozenset({"intake", "constraint", "schema", "parse", "form"}),
    "cli": frozenset({"intake", "human", "surface", "entry", "intent"}),
    "main": frozenset({"intent", "entry", "init", "sovereign"}),
    "entrypoint": frozenset({"intent", "entry", "init", "edge"}),
    "entry": frozenset({"intent", "entry", "init", "edge", "domain"}),
    # constraint / schema
    "schema": frozenset({"constraint", "schema", "type", "form", "validate"}),
    "validator": frozenset({"constraint", "schema", "validate", "judgment"}),
    "policy": frozenset({"constraint", "governance", "policy", "boundary"}),
    "auth": frozenset({"constraint", "protection", "boundary", "binding"}),
    "guard": frozenset({"constraint", "protection", "boundary", "guard"}),
    # analysis / transform
    "analyzer": frozenset({"analyze", "analysis", "score", "illuminate", "transform"}),
    "scorer": frozenset({"analyze", "score", "illuminate", "judgment"}),
    "transform": frozenset({"transform", "analyze", "purify", "fire"}),
    "worker": frozenset({"task", "executive", "transform", "agent"}),
    "handler": frozenset({"task", "executive", "handler", "agent"}),
    "processor": frozenset({"transform", "analyze", "process", "task"}),
    # store / memory
    "repo": frozenset({"store", "memory", "repository", "inherited", "yesod"}),
    "repository": frozenset({"store", "memory", "repository", "yesod"}),
    "cache": frozenset({"store", "memory", "cache"}),
    "db": frozenset({"store", "memory", "database"}),
    "database": frozenset({"store", "memory", "database"}),
    "state": frozenset({"store", "memory", "state"}),
    # output / surface
    "emit": frozenset({"output", "emit", "export", "surface", "outcome", "malkuth"}),
    "export": frozenset({"output", "export", "emit", "outcome", "malkuth"}),
    "render": frozenset({"output", "render", "surface", "human", "malkuth"}),
    "writer": frozenset({"output", "write", "emit", "surface", "malkuth"}),
    "response": frozenset({"output", "response", "comms", "surface"}),
    "api": frozenset({"surface", "comms", "convention", "human", "output"}),
    # control / intent
    "orchestrator": frozenset({"intent", "sovereign", "governance", "core", "synthesis"}),
    "controller": frozenset({"governance", "executive", "control", "core"}),
    "gateway": frozenset({"edge", "boundary", "intake", "comms", "bus"}),
    "bus": frozenset({"bus", "comms", "cross", "domain", "relation"}),
    "router": frozenset({"comms", "bus", "route", "cross", "domain"}),
    # adversarial / judgment
    "critic": frozenset({"adversarial", "judgment", "critique", "conflict"}),
    "judge": frozenset({"judgment", "adversarial", "just"}),
    "filter": frozenset({"purify", "constraint", "filter", "adversarial"}),
}

_NOISE_SUFFIXES = (
    "_module",
    "_service",
    "_handler",
    "_manager",
    "_mgr",
    "_util",
    "_utils",
    "_helper",
    "_helpers",
    "_impl",
    "_api",
    "_cli",
    "_core",
    "_lib",
    "_pkg",
    "_package",
    "module",
    "service",
    "handler",
    "manager",
)


def _split_ident_tokens(ident: str) -> set[str]:
    """Split snake/kebab/camel identifiers into lowercase tokens."""
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", ident)
    s = s.replace("-", "_").replace(".", "_")
    return {t for t in s.lower().split("_") if t and len(t) > 1}


def _strip_noise_suffix(leaf: str) -> str:
    """Remove common boilerplate suffixes for mechanical comparison."""
    low = leaf.lower()
    for suf in _NOISE_SUFFIXES:
        if low.endswith(suf) and len(low) > len(suf) + 2:
            return low[: -len(suf)].rstrip("_")
    return low


def _expand_role_tokens(tokens: set[str]) -> set[str]:
    """Expand known role *keys* only (not every token) into conceptual families."""
    expanded: set[str] = set()
    for t in tokens:
        syns = _ROLE_SYNONYMS.get(t)
        if syns:
            expanded |= set(syns)
    return expanded


def _extract_source_signals(source_text: str) -> set[str]:
    """Tokenize docstring first lines + def/class names from source prefix."""
    if not source_text:
        return set()
    tokens = _tokenize(source_text[:2000])
    # Module docstring: first triple-quoted block
    m = re.search(r'^\s*(?:"""|\'\'\')([\s\S]*?)(?:"""|\'\'\')', source_text)
    if m:
        tokens |= _tokenize(m.group(1)[:400])
    for name in re.findall(r"\b(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", source_text[:2000]):
        tokens |= _split_ident_tokens(name)
        tokens.add(name.lower())
    return tokens


def _locus_token_set(mech: str, sym: str, note: str) -> set[str]:
    return _tokenize(mech) | _tokenize(sym) | _tokenize(note) | _split_ident_tokens(mech)


def _score_locus_match(
    *,
    leaf: str,
    nid: str,
    tokens: set[str],
    role_tokens: set[str],
    path_segs: set[str],
    mech: str,
    sym: str,
    note: str,
) -> tuple[str, int] | None:
    """
    Return (strength, secondary_score) or None if no match.

    secondary_score breaks ties within the same strength (higher is better).
    Never invents loci — only ranks existing framework rows.
    """
    leaf_l = leaf.lower()
    leaf_n = _norm_ident(leaf)
    leaf_stem = _strip_noise_suffix(leaf_l)
    leaf_stem_n = _norm_ident(leaf_stem)
    leaf_parts = _split_ident_tokens(leaf) | _split_ident_tokens(leaf_stem)
    nid_l = nid.lower()
    nid_parts = set(nid_l.split("."))

    mech_l = mech.lower()
    sym_l = sym.lower()
    mech_n = _norm_ident(mech)
    sym_n = _norm_ident(sym)
    mech_parts = _split_ident_tokens(mech)
    locus_toks = _locus_token_set(mech, sym, note)
    note_toks = _tokenize(note)

    # --- STRONG: exact / normalized identity ---
    if (
        leaf_l == mech_l
        or nid_l == mech_l
        or leaf_l == sym_l
        or leaf_n == mech_n
        or leaf_n == sym_n
        or leaf_stem == mech_l
        or leaf_stem_n == mech_n
        or leaf_stem_n == sym_n
    ):
        return "STRONG", 100

    secondary = 0

    # --- ADEQUATE: path segment, compound, containment, multi-token ---
    adequate = False
    if mech_l in tokens or mech_l in nid_parts or mech_n in path_segs:
        adequate = True
        secondary += 40
    if mech_n and mech_n in leaf_n:
        adequate = True
        secondary += 35
    if leaf_n and leaf_n in mech_n and len(leaf_n) >= 4:
        adequate = True
        secondary += 30
    # Note: do not treat leaf ∈ path_segs as a signal — every module is its own path segment.
    # Whole mechanical token is a leaf part: user_intake ↔ intake / edge_intake
    if mech_parts and mech_parts <= (leaf_parts | tokens):
        adequate = True
        secondary += 20 + 5 * len(mech_parts)
    elif mech_parts and (mech_parts & leaf_parts):
        # partial compound: edge_intake leaf vs edge_intake mech (subset)
        if len(mech_parts & leaf_parts) >= max(1, len(mech_parts) - 1):
            adequate = True
            secondary += 15 + 5 * len(mech_parts & leaf_parts)
    # Leaf ends with mechanical name: foo_intake → intake
    if len(mech_l) >= 4 and (leaf_l.endswith(mech_l) or leaf_stem.endswith(mech_l)):
        adequate = True
        secondary += 28
    if len(mech_l) >= 4 and (leaf_l.startswith(mech_l) or leaf_stem.startswith(mech_l)):
        adequate = True
        secondary += 22
    # Role synonyms (from known role *keys* only) hit locus tokens
    role_hits = role_tokens & locus_toks
    if mech_l in role_tokens or mech_n in {_norm_ident(x) for x in role_tokens}:
        # Direct hit on this mechanical name via synonym expansion
        adequate = True
        secondary += 32 + 4 * len(role_hits)
    elif len(role_hits) >= 2:
        adequate = True
        secondary += 16 + 3 * len(role_hits)
    elif len(role_hits) == 1 and (mech_parts & role_tokens):
        adequate = True
        secondary += 12

    if adequate:
        # Boost for docstring/note alignment
        secondary += min(15, 3 * len(tokens & note_toks))
        return "ADEQUATE", secondary

    # --- WEAK: single-token / loose overlap ---
    plain_hits = tokens & locus_toks
    role_only = role_tokens & locus_toks
    if plain_hits or role_only:
        secondary = 2 * len(plain_hits) + len(role_only)
        return "WEAK", secondary
    return None


def _map_node_to_locus(
    node: dict[str, Any],
    loci: list[tuple[str, str, str]],
    *,
    source_text: str = "",
) -> dict[str, Any] | None:
    """Score best locus match. Never invents symbolic names."""
    nid = node["id"]
    leaf = nid.split(".")[-1]
    base_tokens = _tokenize(nid + " " + source_text) | _split_ident_tokens(leaf)
    base_tokens |= _extract_source_signals(source_text)
    role_tokens = _expand_role_tokens(base_tokens)
    path_segs = {_norm_ident(p) for p in nid.lower().split(".") if p}

    best: tuple[int, int, tuple[str, str, str], str] | None = None
    # (strength_rank, secondary, locus_tuple, strength)

    for mech, sym, note in loci:
        scored = _score_locus_match(
            leaf=leaf,
            nid=nid,
            tokens=base_tokens,
            role_tokens=role_tokens,
            path_segs=path_segs,
            mech=mech,
            sym=sym,
            note=note,
        )
        if scored is None:
            continue
        strength, secondary = scored
        rank = STRENGTH_RANK[strength]
        cand = (rank, secondary, (mech, sym, note), strength)
        if best is None or cand[:2] > best[:2]:
            best = cand

    if best is None:
        return None
    _, secondary, (mech, sym, note), strength = best
    return {
        "functional_concern": note or mech,
        "mechanical_name": mech,
        "symbolic_name": sym,
        "symbolic_locus": sym,
        "strength": strength,
        "notes": note,
        "node_id": nid,
        "match_score": secondary,
    }


def _suggest_frameworks(
    nodes: list[dict[str, Any]],
    frameworks: dict[str, dict[str, Any]],
) -> list[str]:
    """Rank frameworks by leaf/token overlap with mechanical loci and notes."""
    leaves = {n["id"].split(".")[-1].lower() for n in nodes}
    leaf_norms = {_norm_ident(x) for x in leaves}
    leaf_tokens: set[str] = set()
    for n in nodes:
        leaf = n["id"].split(".")[-1]
        leaf_tokens |= _split_ident_tokens(leaf)
        leaf_tokens |= _expand_role_tokens(_split_ident_tokens(leaf) | {leaf.lower()})

    scored: list[tuple[int, str]] = []
    for key, meta in frameworks.items():
        loci = meta.get("default_loci") or []
        mechs = {m.lower() for m, _, _ in loci}
        mech_norms = {_norm_ident(m) for m in mechs}
        score = 10 * len(leaves & mechs)
        score += 6 * len(leaf_norms & mech_norms)
        locus_bag: set[str] = set()
        for m, s, note in loci:
            locus_bag |= _locus_token_set(m, s, note)
        score += 2 * len(leaf_tokens & locus_bag)
        if score:
            scored.append((score, key))
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

    # Multi-language support (stdlib regex extractors + Python AST)
    from analyze_langs import (
        SUPPORTED_LANGS,
        extensions_for_lang,
        extract_edges_for_file,
        language_for_path,
        module_id_for_file,
        normalize_lang,
    )

    lang_key = normalize_lang(lang)
    if lang_key not in SUPPORTED_LANGS:
        return _error_analysis(
            path=str(root), lang=lang, framework=framework,
            overlay=overlay, version=version,
            error=(
                f"unsupported language: {lang} "
                f"(supported: {', '.join(sorted(SUPPORTED_LANGS))})"
            ),
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

    exts = extensions_for_lang(lang_key)
    source_files = _collect_source_files(
        root, extensions=exts, max_depth=max_depth, max_files=max_files
    )
    if not source_files:
        return _error_analysis(
            path=str(root), lang=lang, framework=framework,
            overlay=overlay, version=version,
            error=f"empty tree — no source files found for language={lang_key}",
        ), 2

    # Build ids with per-file language
    file_lang: dict[Path, str] = {}
    id_for_file: dict[Path, str] = {}
    for f in source_files:
        fl = language_for_path(f) or "python"
        file_lang[f] = fl
        if fl == "python":
            id_for_file[f] = _module_id(root, f)
        else:
            id_for_file[f] = module_id_for_file(root, f, fl)
    known = set(id_for_file.values())

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    source_by_id: dict[str, str] = {}
    languages_seen: set[str] = set()

    for f in source_files:
        mid = id_for_file[f]
        fl = file_lang[f]
        languages_seen.add(fl)
        rel = str(f.relative_to(root))
        kind = "package" if (fl == "python" and f.name == "__init__.py") else "module"
        parse_error = None
        imports: list[str] = []
        try:
            text = f.read_text(encoding="utf-8")
            source_by_id[mid] = text[:2000]
            if fl == "python":
                tree = ast.parse(text, filename=str(f))
                pairs = _imports_from_ast(
                    tree, root=root, current_file=f, known=known
                )
            else:
                pairs = extract_edges_for_file(
                    lang=fl,
                    text=text,
                    root=root,
                    current=f,
                    known=known,
                    self_id=mid,
                )
            for target, external in pairs:
                imports.append(target)
                edges.append({
                    "from": mid,
                    "to": target,
                    "kind": "import",
                    "provenance": "OBSERVED",
                    "external": external,
                    "language": fl,
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
            "language": fl,
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

    # Report requested language; when auto, also list observed languages
    reported_lang = lang_key
    if lang_key == "auto" and len(languages_seen) == 1:
        reported_lang = next(iter(languages_seen))
    elif lang_key == "auto":
        reported_lang = "auto"

    analysis: dict[str, Any] = {
        "schema": "orchestra-analysis.v1",
        "path": str(root),
        "language": reported_lang,
        "languages": sorted(languages_seen),
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
