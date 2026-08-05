"""Gated optimize apply for Abraxas Orchestra (Phase C+).

--apply alone is dry-run. Writes require --apply --confirm.
Only steps with safe_apply=true are executed (rename / promote / flatten).
Stdlib only. No network. Path jail under the analyzed root.
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from analyze_repo import SYSTEM_TOP, path_jail_ok

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SAFE_ACTIONS = frozenset({"suggest_rename", "suggest_boundary", "suggest_flatten"})


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _under_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def validate_apply_root(analysis_path: str | Path) -> tuple[Path, str]:
    """Return (resolved_root, error). error empty on success."""
    root = Path(analysis_path).expanduser()
    ok, reason = path_jail_ok(root, allow_system=False)
    if not ok:
        return root, reason
    root = root.resolve()
    parts = root.parts
    if root == Path("/") or (
        len(parts) >= 2 and parts[0] == "/" and parts[1] in SYSTEM_TOP
    ):
        return root, f"refusing system path: {root}"
    return root, ""


def _node_by_id(analysis: dict[str, Any], node_id: str) -> dict[str, Any] | None:
    for n in analysis.get("nodes") or []:
        if n.get("id") == node_id:
            return n
    return None


def _package_only_init(pkg_dir: Path) -> bool:
    """True when package dir has only __init__.py (+ caches)."""
    if not pkg_dir.is_dir():
        return False
    extras: list[Path] = []
    for child in pkg_dir.iterdir():
        if child.name == "__pycache__" or child.name.endswith(".pyc"):
            continue
        if child.name == "__init__.py" and child.is_file():
            continue
        extras.append(child)
    return (pkg_dir / "__init__.py").is_file() and not extras


def enrich_safe_renames(
    plan: dict[str, Any],
    analysis: dict[str, Any],
) -> dict[str, Any]:
    """Backward-compatible alias for enrich_safe_steps."""
    return enrich_safe_steps(plan, analysis)


def enrich_safe_steps(
    plan: dict[str, Any],
    analysis: dict[str, Any],
) -> dict[str, Any]:
    """Mark mechanical rename / promote / flatten steps safe_apply when valid."""
    root = Path(analysis["path"]).resolve()
    steps: list[dict[str, Any]] = []

    # Pass 1 — renames
    for step in plan.get("steps") or []:
        s = dict(step)
        if s.get("action") != "suggest_rename":
            steps.append(s)
            continue
        targets = s.get("targets") or []
        if len(targets) != 1:
            s["safe_apply"] = False
            steps.append(s)
            continue
        node = _node_by_id(analysis, targets[0])
        if not node:
            s["safe_apply"] = False
            steps.append(s)
            continue
        locus = s.get("locus") or ""
        mech = locus.split("/")[0] if locus else ""
        if not mech or not _IDENT.match(mech):
            s["safe_apply"] = False
            steps.append(s)
            continue
        if s.get("strength") not in {"STRONG", "ADEQUATE"}:
            s["safe_apply"] = False
            steps.append(s)
            continue
        rel = node.get("path") or ""
        src = (root / rel).resolve()
        if not _under_root(src, root) or not src.exists():
            s["safe_apply"] = False
            steps.append(s)
            continue
        if node.get("kind") == "package":
            dest = (src.parent.parent / mech / "__init__.py").resolve()
            dest_dir = dest.parent
        else:
            dest = (src.parent / f"{mech}.py").resolve()
            dest_dir = dest.parent
        if not _under_root(dest, root):
            s["safe_apply"] = False
            steps.append(s)
            continue
        if dest == src:
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + " (already aligned — skip)"
            steps.append(s)
            continue
        if dest.exists() or (node.get("kind") == "package" and dest_dir.exists()):
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + " (destination exists — blocked)"
            steps.append(s)
            continue
        s["safe_apply"] = True
        s["rename"] = {
            "from_path": str(src.relative_to(root)),
            "to_path": str(dest.relative_to(root)),
            "from_id": node["id"],
            "to_id": _rewrite_module_id(node["id"], mech),
            "kind": node.get("kind", "module"),
        }
        steps.append(s)

    # Effective paths after planned renames (for boundary promotion / flatten)
    effective_path: dict[str, str] = {}
    effective_id: dict[str, str] = {}
    for s in steps:
        ren = s.get("rename") or {}
        if s.get("safe_apply") and ren:
            effective_path[ren["from_id"]] = ren["to_path"]
            effective_id[ren["from_id"]] = ren["to_id"]

    # Pass 2 — package boundary promotion: module.py → module/__init__.py
    for i, step in enumerate(steps):
        if step.get("action") != "suggest_boundary":
            continue
        s = dict(step)
        targets = s.get("targets") or []
        if len(targets) != 1 or s.get("strength") not in {"STRONG", "ADEQUATE"}:
            s["safe_apply"] = False
            steps[i] = s
            continue
        node_id = targets[0]
        node = _node_by_id(analysis, node_id)
        if not node:
            s["safe_apply"] = False
            steps[i] = s
            continue
        rel = effective_path.get(node_id) or node.get("path") or ""
        mid = effective_id.get(node_id) or node_id
        leaf = mid.split(".")[-1]
        if not leaf or not _IDENT.match(leaf):
            s["safe_apply"] = False
            steps[i] = s
            continue
        if rel.endswith("__init__.py") or node.get("kind") == "package":
            if rel.endswith("__init__.py"):
                s["safe_apply"] = False
                s["notes"] = (s.get("notes") or "") + " (already a package — skip)"
                steps[i] = s
                continue
        src = (root / rel).resolve()
        planned = node_id in effective_path
        if not planned and (not _under_root(src, root) or not src.exists()):
            s["safe_apply"] = False
            steps[i] = s
            continue
        if not rel.endswith(".py") or rel.endswith("__init__.py"):
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + " (not a promotable module file)"
            steps[i] = s
            continue
        stem = Path(rel).stem
        if stem != leaf:
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + (
                f" (stem `{stem}` != mechanical `{leaf}` — rename first)"
            )
            steps[i] = s
            continue
        dest = (root / Path(rel).parent / leaf / "__init__.py").resolve()
        if not _under_root(dest, root):
            s["safe_apply"] = False
            steps[i] = s
            continue
        if dest.exists() or dest.parent.exists():
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + " (package dir exists — blocked)"
            steps[i] = s
            continue
        s["safe_apply"] = True
        s["promote"] = {
            "from_path": rel.replace("\\", "/"),
            "to_path": str(dest.relative_to(root)).replace("\\", "/"),
            "module_id": mid,
            "kind": "package_promote",
        }
        s["notes"] = (s.get("notes") or "") + (
            f" Safe apply: promote `{Path(rel).name}` → `{leaf}/__init__.py`."
        )
        steps[i] = s

    # Pass 3 — flatten single-file packages: leaf/__init__.py → leaf.py
    for i, step in enumerate(steps):
        if step.get("action") != "suggest_flatten":
            continue
        s = dict(step)
        targets = s.get("targets") or []
        if len(targets) != 1 or s.get("strength") not in {"STRONG", "ADEQUATE"}:
            s["safe_apply"] = False
            steps[i] = s
            continue
        node_id = targets[0]
        node = _node_by_id(analysis, node_id)
        if not node:
            s["safe_apply"] = False
            steps[i] = s
            continue
        rel = effective_path.get(node_id) or node.get("path") or ""
        mid = effective_id.get(node_id) or node_id
        leaf = mid.split(".")[-1]
        if not leaf or not _IDENT.match(leaf):
            s["safe_apply"] = False
            steps[i] = s
            continue
        if not rel.endswith("__init__.py") and node.get("kind") != "package":
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + " (not a package — skip)"
            steps[i] = s
            continue
        if not rel.endswith("__init__.py"):
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + " (expected __init__.py path)"
            steps[i] = s
            continue
        src = (root / rel).resolve()
        planned = node_id in effective_path
        if not planned and (not _under_root(src, root) or not src.exists()):
            s["safe_apply"] = False
            steps[i] = s
            continue
        pkg_dir = src.parent
        if not planned and not _package_only_init(pkg_dir):
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + (
                " (package has siblings — flatten blocked)"
            )
            steps[i] = s
            continue
        dest = (pkg_dir.parent / f"{leaf}.py").resolve()
        if not _under_root(dest, root):
            s["safe_apply"] = False
            steps[i] = s
            continue
        if dest.exists():
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + " (destination exists — blocked)"
            steps[i] = s
            continue
        if Path(rel).parent.name != leaf:
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + (
                f" (dir `{Path(rel).parent.name}` != mechanical `{leaf}`)"
            )
            steps[i] = s
            continue
        s["safe_apply"] = True
        s["flatten"] = {
            "from_path": rel.replace("\\", "/"),
            "to_path": str(dest.relative_to(root)).replace("\\", "/"),
            "module_id": mid,
            "kind": "package_flatten",
        }
        s["notes"] = (s.get("notes") or "") + (
            f" Safe apply: flatten `{leaf}/__init__.py` → `{leaf}.py`."
        )
        steps[i] = s

    # Fail-closed: demote colliding destinations across rename + promote + flatten
    dest_owners: dict[str, str] = {}
    for s in steps:
        move = s.get("rename") or s.get("promote") or s.get("flatten") or {}
        if not s.get("safe_apply") or not move:
            continue
        dest = move.get("to_path")
        if not dest:
            continue
        if dest in dest_owners:
            s["safe_apply"] = False
            s["notes"] = (s.get("notes") or "") + (
                f" (destination collision with {dest_owners[dest]} — blocked)"
            )
            for prev in steps:
                if prev.get("id") == dest_owners[dest] and prev.get("safe_apply"):
                    prev["safe_apply"] = False
                    prev["notes"] = (prev.get("notes") or "") + (
                        f" (destination collision with {s.get('id')} — blocked)"
                    )
        else:
            dest_owners[dest] = s.get("id") or dest

    out = dict(plan)
    out["steps"] = steps
    return out


def collision_error(plan: dict[str, Any]) -> str | None:
    """Return error if safe steps claim the same destination."""
    tos: dict[str, str] = {}
    for s in plan.get("steps") or []:
        move = s.get("rename") or s.get("promote") or s.get("flatten") or {}
        if not s.get("safe_apply") or not move:
            continue
        dest = move.get("to_path")
        if not dest:
            continue
        if dest in tos:
            return f"destination collision: {tos[dest]} and {s.get('id')} both target {dest}"
        tos[dest] = s.get("id") or dest
    return None


def _rewrite_module_id(old_id: str, new_leaf: str) -> str:
    parts = old_id.split(".")
    parts[-1] = new_leaf
    return ".".join(parts)


def _forced_blocks_apply(analysis: dict[str, Any], plan: dict[str, Any]) -> str | None:
    if analysis.get("status") == "FORCED_CORRESPONDENCE":
        return "analysis status FORCED_CORRESPONDENCE blocks apply"
    for m in analysis.get("mappings") or []:
        if m.get("strength") == "FORCED":
            return f"FORCED mapping present ({m.get('node_id') or m.get('mechanical_name')})"
    for b in plan.get("blocked") or []:
        if b.get("strength") == "FORCED":
            return "FORCED entries in plan.blocked — refuse apply"
    return None


def _rewrite_import_line(line: str, id_map: dict[str, str]) -> str:
    """Rewrite module names on import lines; keep `as old` aliases so call sites stay valid."""
    stripped = line.lstrip()
    if not (stripped.startswith("import ") or stripped.startswith("from ")):
        return line
    new_line = line
    for old, new in sorted(id_map.items(), key=lambda x: -len(x[0])):
        leaf_old = old.split(".")[-1]
        leaf_new = new.split(".")[-1]
        m = re.match(
            rf"^(\s*from\s+\.+\s+import\s+)({re.escape(leaf_old)})(\s*(?:#.*)?)$",
            new_line,
        )
        if m and leaf_old != leaf_new:
            new_line = f"{m.group(1)}{leaf_new} as {leaf_old}{m.group(3)}"
            continue
        new_line = re.sub(
            rf"(from\s+\.+)({re.escape(leaf_old)})(\s+import\b)",
            rf"\1{leaf_new}\3",
            new_line,
        )
        replaced = re.sub(
            rf"(?<![\w.]){re.escape(old)}(?=[\s.,\\]|$)",
            new,
            new_line,
        )
        if replaced != new_line and " as " not in replaced:
            bare = re.match(
                rf"^(\s*import\s+)({re.escape(new)})(\s*(?:#.*)?)$",
                replaced,
            )
            if bare and leaf_old != leaf_new:
                replaced = f"{bare.group(1)}{new} as {leaf_old}{bare.group(3)}"
        new_line = replaced
    return new_line


def _rewrite_imports_in_tree(
    root: Path,
    id_map: dict[str, str],
    *,
    dry_run: bool,
) -> list[str]:
    """Rewrite import module names for renamed modules. Returns touched rel paths."""
    touched: list[str] = []
    if not id_map:
        return touched
    for py in root.rglob("*.py"):
        if any(
            part in {".venv", "venv", "__pycache__", ".git", ".orchestra-backups"}
            for part in py.parts
        ):
            continue
        if not _under_root(py, root):
            continue
        try:
            text = py.read_text(encoding="utf-8")
        except OSError:
            continue
        lines = text.splitlines(keepends=True)
        changed = False
        out_lines: list[str] = []
        for line in lines:
            rewritten = _rewrite_import_line(line, id_map)
            if rewritten != line:
                changed = True
            out_lines.append(rewritten)
        if not changed:
            continue
        rel = str(py.relative_to(root))
        touched.append(rel)
        if not dry_run:
            py.write_text("".join(out_lines), encoding="utf-8")
    return touched


def _backup_file(src: Path, backup_dir: Path, root: Path) -> Path:
    rel = src.relative_to(root)
    dest = backup_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    return dest


def apply_optimize_plan(
    analysis: dict[str, Any],
    plan: dict[str, Any],
    *,
    confirm: bool = False,
    backup_dir: str | Path | None = None,
    version: str,
    refresh: bool = False,
    frameworks: dict[str, dict[str, Any]] | None = None,
    step_ids: list[str] | None = None,
    actions_filter: list[str] | None = None,
) -> tuple[dict[str, Any], int]:
    """
    Apply safe_apply rename / package-promote / flatten steps.

    confirm=False → dry-run (exit 0, no writes).
    confirm=True → backup + mutate.
    refresh=True (with confirm) → re-analyze tree after successful writes.
    step_ids → only apply listed step ids (still must be safe_apply).
    actions_filter → only apply listed action names (e.g. suggest_rename).
    """
    root_raw = analysis.get("path")
    if not root_raw:
        return {
            "schema": "orchestra-optimize-apply.v1",
            "status": "NOT_COMPUTABLE",
            "error": "analysis missing path",
            "actions": [],
        }, 2

    root, err = validate_apply_root(root_raw)
    if err:
        return {
            "schema": "orchestra-optimize-apply.v1",
            "status": "NOT_COMPUTABLE",
            "error": err,
            "actions": [],
        }, 2

    if actions_filter:
        bad = [a for a in actions_filter if a not in SAFE_ACTIONS]
        if bad:
            return {
                "schema": "orchestra-optimize-apply.v1",
                "status": "NOT_COMPUTABLE",
                "error": f"unknown --actions value(s): {', '.join(bad)}",
                "actions": [],
            }, 2

    plan = enrich_safe_steps(plan, {**analysis, "path": str(root)})
    block = _forced_blocks_apply(analysis, plan)
    if block:
        return {
            "schema": "orchestra-optimize-apply.v1",
            "status": "NOT_COMPUTABLE",
            "error": block,
            "actions": [],
            "dry_run": not confirm,
        }, 2

    dry_run = not confirm
    actions: list[dict[str, Any]] = []
    id_map: dict[str, str] = {}

    bdir: Path | None = None
    if confirm:
        if backup_dir:
            bdir = Path(backup_dir).expanduser().resolve()
        else:
            bdir = (root / ".orchestra-backups" / _utc_now().replace(":", "")).resolve()
        parts = bdir.parts
        if bdir == Path("/") or (
            len(parts) >= 2 and parts[0] == "/" and parts[1] in SYSTEM_TOP
        ):
            return {
                "schema": "orchestra-optimize-apply.v1",
                "status": "NOT_COMPUTABLE",
                "error": f"refusing system backup-dir: {bdir}",
                "actions": [],
            }, 2
        bdir.mkdir(parents=True, exist_ok=True)

    selected = set(step_ids) if step_ids else None
    action_set = set(actions_filter) if actions_filter else None
    safe_steps = [s for s in plan.get("steps") or [] if s.get("safe_apply")]
    if selected is not None:
        safe_steps = [s for s in safe_steps if s.get("id") in selected]
    if action_set is not None:
        safe_steps = [s for s in safe_steps if s.get("action") in action_set]
    skipped = [
        s["id"]
        for s in plan.get("steps") or []
        if not s.get("safe_apply")
        or (selected is not None and s.get("id") not in selected)
        or (action_set is not None and s.get("action") not in action_set)
    ]

    rename_steps = [
        s for s in safe_steps if s.get("action") == "suggest_rename" and s.get("rename")
    ]
    promote_steps = [
        s for s in safe_steps if s.get("action") == "suggest_boundary" and s.get("promote")
    ]
    flatten_steps = [
        s for s in safe_steps if s.get("action") == "suggest_flatten" and s.get("flatten")
    ]

    pending_from = {
        (s.get("rename") or {}).get("from_path")
        for s in rename_steps
        if (s.get("rename") or {}).get("from_path")
    }

    def _rename_order(step: dict[str, Any]) -> tuple[int, str]:
        ren = step.get("rename") or {}
        to_p = ren.get("to_path") or ""
        vacate_first = 1 if to_p in pending_from else 0
        return (vacate_first, ren.get("from_path") or "")

    rename_steps = sorted(rename_steps, key=_rename_order)

    for step in rename_steps:
        rename = step.get("rename") or {}
        src = (root / rename["from_path"]).resolve()
        dest = (root / rename["to_path"]).resolve()
        if not _under_root(src, root) or not _under_root(dest, root):
            actions.append({
                "step_id": step["id"],
                "action": "suggest_rename",
                "status": "blocked",
                "reason": "path escapes analyzed root",
            })
            continue
        if not src.exists():
            actions.append({
                "step_id": step["id"],
                "action": "suggest_rename",
                "status": "blocked",
                "reason": f"source missing: {rename['from_path']}",
            })
            continue
        dest_rel = rename["to_path"]
        if dest.exists():
            if dry_run and dest_rel in pending_from:
                pass
            elif dest_rel in pending_from:
                actions.append({
                    "step_id": step["id"],
                    "action": "suggest_rename",
                    "status": "blocked",
                    "reason": f"destination still occupied: {rename['to_path']}",
                })
                continue
            else:
                actions.append({
                    "step_id": step["id"],
                    "action": "suggest_rename",
                    "status": "blocked",
                    "reason": f"destination exists: {rename['to_path']}",
                })
                continue

        entry: dict[str, Any] = {
            "step_id": step["id"],
            "action": "suggest_rename",
            "from_path": rename["from_path"],
            "to_path": rename["to_path"],
            "from_id": rename.get("from_id"),
            "to_id": rename.get("to_id"),
            "status": "would_apply" if dry_run else "applied",
        }

        if not dry_run and bdir is not None:
            if rename.get("kind") == "package":
                entry["backup"] = str(
                    _backup_file(src.parent, bdir, root).relative_to(bdir)
                )
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src.parent), str(dest.parent))
            else:
                entry["backup"] = str(_backup_file(src, bdir, root).relative_to(bdir))
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dest))
            id_map[rename["from_id"]] = rename["to_id"]
            pending_from.discard(rename["from_path"])
        elif dry_run:
            id_map[rename["from_id"]] = rename["to_id"]

        actions.append(entry)

    # Package promotion after renames (module.py → module/__init__.py)
    for step in promote_steps:
        promote = step.get("promote") or {}
        from_rel = promote["from_path"]
        for a in actions:
            if a.get("status") in {"applied", "would_apply"} and a.get("from_path") == from_rel:
                from_rel = a.get("to_path") or from_rel
                break
            if (
                a.get("status") in {"applied", "would_apply"}
                and a.get("to_id") == promote.get("module_id")
            ):
                from_rel = a.get("to_path") or from_rel
                break
        src = (root / from_rel).resolve()
        dest = (root / promote["to_path"]).resolve()
        if from_rel != promote["from_path"]:
            leaf = Path(from_rel).stem
            dest = (root / Path(from_rel).parent / leaf / "__init__.py").resolve()
        if not _under_root(src, root) or not _under_root(dest, root):
            actions.append({
                "step_id": step["id"],
                "action": "suggest_boundary",
                "status": "blocked",
                "reason": "path escapes analyzed root",
            })
            continue
        if not dry_run and not src.exists():
            actions.append({
                "step_id": step["id"],
                "action": "suggest_boundary",
                "status": "blocked",
                "reason": f"source missing: {from_rel}",
            })
            continue
        if not dry_run and (dest.exists() or dest.parent.exists()):
            actions.append({
                "step_id": step["id"],
                "action": "suggest_boundary",
                "status": "blocked",
                "reason": f"package dir exists: {dest.parent.relative_to(root)}",
            })
            continue
        to_rel = (
            str(dest.relative_to(root)).replace("\\", "/")
            if _under_root(dest, root)
            else promote["to_path"]
        )
        entry = {
            "step_id": step["id"],
            "action": "suggest_boundary",
            "from_path": str(Path(from_rel)).replace("\\", "/"),
            "to_path": to_rel,
            "module_id": promote.get("module_id"),
            "status": "would_apply" if dry_run else "applied",
        }
        if not dry_run and bdir is not None:
            entry["backup"] = str(_backup_file(src, bdir, root).relative_to(bdir))
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))
        actions.append(entry)

    # Flatten after promote (leaf/__init__.py → leaf.py)
    for step in flatten_steps:
        flatten = step.get("flatten") or {}
        from_rel = flatten["from_path"]
        for a in actions:
            if a.get("status") in {"applied", "would_apply"} and a.get("from_path") == from_rel:
                from_rel = a.get("to_path") or from_rel
                break
            if (
                a.get("status") in {"applied", "would_apply"}
                and a.get("to_id") == flatten.get("module_id")
            ):
                from_rel = a.get("to_path") or from_rel
                break
        src = (root / from_rel).resolve()
        dest = (root / flatten["to_path"]).resolve()
        if from_rel != flatten["from_path"]:
            # Renamed package __init__ — recompute flat sibling
            if from_rel.endswith("__init__.py"):
                leaf = Path(from_rel).parent.name
                dest = (root / Path(from_rel).parent.parent / f"{leaf}.py").resolve()
            else:
                leaf = Path(from_rel).stem
                dest = (root / Path(from_rel).parent / f"{leaf}.py").resolve()
        if not _under_root(src, root) or not _under_root(dest, root):
            actions.append({
                "step_id": step["id"],
                "action": "suggest_flatten",
                "status": "blocked",
                "reason": "path escapes analyzed root",
            })
            continue
        if not dry_run and not src.exists():
            actions.append({
                "step_id": step["id"],
                "action": "suggest_flatten",
                "status": "blocked",
                "reason": f"source missing: {from_rel}",
            })
            continue
        if not dry_run and not _package_only_init(src.parent):
            actions.append({
                "step_id": step["id"],
                "action": "suggest_flatten",
                "status": "blocked",
                "reason": "package has siblings — flatten blocked",
            })
            continue
        if not dry_run and dest.exists():
            actions.append({
                "step_id": step["id"],
                "action": "suggest_flatten",
                "status": "blocked",
                "reason": f"destination exists: {dest.relative_to(root)}",
            })
            continue
        to_rel = (
            str(dest.relative_to(root)).replace("\\", "/")
            if _under_root(dest, root)
            else flatten["to_path"]
        )
        entry = {
            "step_id": step["id"],
            "action": "suggest_flatten",
            "from_path": str(Path(from_rel)).replace("\\", "/"),
            "to_path": to_rel,
            "module_id": flatten.get("module_id"),
            "status": "would_apply" if dry_run else "applied",
        }
        if not dry_run and bdir is not None:
            pkg_dir = src.parent
            entry["backup"] = str(_backup_file(pkg_dir, bdir, root).relative_to(bdir))
            shutil.move(str(src), str(dest))
            # Remove emptied package dir (and leftover caches)
            try:
                for child in list(pkg_dir.iterdir()):
                    if child.name == "__pycache__":
                        shutil.rmtree(child)
                    elif child.suffix == ".pyc":
                        child.unlink(missing_ok=True)
                if not any(pkg_dir.iterdir()):
                    pkg_dir.rmdir()
            except OSError:
                pass
        actions.append(entry)

    import_touches = _rewrite_imports_in_tree(root, id_map, dry_run=dry_run)
    applied_n = sum(1 for a in actions if a.get("status") in {"applied", "would_apply"})
    report: dict[str, Any] = {
        "schema": "orchestra-optimize-apply.v1",
        "status": "DRY_RUN" if dry_run else "APPLIED",
        "dry_run": dry_run,
        "root": str(root),
        "backup_dir": str(bdir) if bdir else None,
        "selected_step_ids": sorted(selected) if selected is not None else None,
        "selected_actions": sorted(action_set) if action_set is not None else None,
        "actions": actions,
        "skipped_step_ids": skipped,
        "import_rewrites": import_touches,
        "refresh": None,
        "provenance": {
            "operator": "orchestra-cli",
            "timestamp": _utc_now(),
            "skill_version": version,
            "kind": "OBSERVED" if not dry_run else "INFERRED",
        },
    }

    if refresh and confirm and applied_n > 0 and frameworks is not None:
        from analyze_repo import analyze_path, write_analysis_artifacts

        refreshed, rcode = analyze_path(
            root,
            frameworks=frameworks,
            version=version,
            framework=analysis.get("framework"),
            overlay=analysis.get("secondary_overlay"),
            lang=analysis.get("language") or "python",
        )
        refresh_dir = bdir if bdir is not None else root / ".orchestra-backups" / "refresh"
        refresh_dir.mkdir(parents=True, exist_ok=True)
        write_analysis_artifacts(refreshed, refresh_dir, version=version)
        report["refresh"] = {
            "status": refreshed.get("status"),
            "exit_code": rcode,
            "nodes": len(refreshed.get("nodes") or []),
            "edges": len(refreshed.get("edges") or []),
            "mappings": len(refreshed.get("mappings") or []),
            "out": str(refresh_dir / "analysis.json"),
        }
    elif refresh and not confirm:
        report["refresh"] = {
            "status": "SKIPPED",
            "reason": "refresh requires --apply --confirm",
        }
    elif refresh and applied_n == 0:
        report["refresh"] = {
            "status": "SKIPPED",
            "reason": "no applied steps",
        }

    if confirm and bdir is not None:
        (bdir / "apply-report.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        (bdir / "RESTORE.md").write_text(
            _restore_doc(report),
            encoding="utf-8",
        )
    return report, 0


def _restore_doc(report: dict[str, Any]) -> str:
    lines = [
        "# Orchestra optimize apply — restore",
        "",
        f"Backup dir: `{report.get('backup_dir')}`",
        f"Root: `{report.get('root')}`",
        f"Generated: {report.get('provenance', {}).get('timestamp', '')}",
        "",
        "## Restore steps",
        "",
        "1. Stop writers touching the analyzed tree.",
        "2. For each applied action below, move the backup path back over the destination.",
        "3. Re-run `analyze` to verify the graph.",
        "",
        "## Actions",
        "",
    ]
    for a in report.get("actions") or []:
        if a.get("status") != "applied":
            continue
        lines.append(
            f"- [{a.get('action')}] restore `{a.get('backup')}` → `{a.get('from_path')}` "
            f"(undo `{a.get('from_path')}` → `{a.get('to_path')}`)"
        )
    if not any(a.get("status") == "applied" for a in report.get("actions") or []):
        lines.append("_No applied steps._")
    lines.append("")
    return "\n".join(lines)
