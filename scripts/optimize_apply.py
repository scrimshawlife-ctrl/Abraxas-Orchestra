"""Gated optimize apply for Abraxas Orchestra (Phase C+).

--apply alone is dry-run. Writes require --apply --confirm.
Only steps with safe_apply=true are executed (rename / promote / flatten).
Stdlib only. No network. Path jail under the analyzed root.

Implementation split:
- optimize_enrich.py  — safe_apply marking / collision checks
- optimize_rewrite.py — import rewrites after renames
- this module         — backup, mutate, report, restore docs
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from analyze_repo import SYSTEM_TOP
from optimize_enrich import (
    SAFE_ACTIONS,
    collision_error,
    enrich_safe_renames,
    enrich_safe_steps,
    forced_blocks_apply,
    package_only_init,
    under_root,
    validate_apply_root,
)
from optimize_rewrite import rewrite_imports_in_tree

# Re-export public surface used by orchestra.py / optimize_plan.py / tests
__all__ = [
    "SAFE_ACTIONS",
    "apply_optimize_plan",
    "collision_error",
    "enrich_safe_renames",
    "enrich_safe_steps",
    "validate_apply_root",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
    block = forced_blocks_apply(analysis, plan)
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
        if not under_root(src, root) or not under_root(dest, root):
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
        if not under_root(src, root) or not under_root(dest, root):
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
            if under_root(dest, root)
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
        if not under_root(src, root) or not under_root(dest, root):
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
        if not dry_run and not package_only_init(src.parent):
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
            if under_root(dest, root)
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

    import_touches = rewrite_imports_in_tree(root, id_map, dry_run=dry_run)
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
