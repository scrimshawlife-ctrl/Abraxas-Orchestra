"""Safe-apply step enrichment for Orchestra optimize (rename/promote/flatten).

Stdlib only. Marks plan steps with safe_apply and move descriptors.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from analyze_repo import SYSTEM_TOP, path_jail_ok

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SAFE_ACTIONS = frozenset({"suggest_rename", "suggest_boundary", "suggest_flatten"})


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


# Public names for other optimize_* modules
under_root = _under_root
node_by_id = _node_by_id
package_only_init = _package_only_init
rewrite_module_id = _rewrite_module_id
forced_blocks_apply = _forced_blocks_apply
