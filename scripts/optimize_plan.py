"""Optimize plan synthesis from Orchestra analysis artifacts (Phase B/C).

Default: plan-only (no tree writes). Phase C apply lives in optimize_apply.py.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STRENGTH_RANK = {"STRONG": 3, "ADEQUATE": 2, "WEAK": 1, "FORCED": 0}


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_analysis(path: str | Path) -> dict[str, Any]:
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f"analysis file not found: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("schema") != "orchestra-analysis.v1":
        raise ValueError(
            f"expected schema orchestra-analysis.v1, got {data.get('schema')!r}"
        )
    return data


def build_optimize_plan(
    analysis: dict[str, Any],
    *,
    from_analysis: str,
    min_strength: str = "ADEQUATE",
    version: str,
) -> dict[str, Any]:
    """Emit ordered refactor plan for mappings ≥ min_strength; block the rest."""
    if min_strength not in STRENGTH_RANK:
        raise ValueError(f"bad min_strength: {min_strength}")

    threshold = STRENGTH_RANK[min_strength]
    nodes_by_id = {n["id"]: n for n in analysis.get("nodes") or []}
    edges = analysis.get("edges") or []
    internal_edges = [e for e in edges if not e.get("external")]

    steps: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    step_n = 0

    for m in analysis.get("mappings") or []:
        strength = m.get("strength", "WEAK")
        node_id = m.get("node_id") or m.get("mechanical_name")
        locus = m.get("symbolic_locus") or m.get("symbolic_name") or ""
        mech = m.get("mechanical_name") or ""

        if STRENGTH_RANK.get(strength, 0) < threshold or strength == "FORCED":
            blocked.append({
                "targets": [node_id] if node_id else [],
                "reason": (
                    "FORCED mapping blocks optimize"
                    if strength == "FORCED"
                    else f"strength {strength} below min_strength {min_strength}"
                ),
                "strength": strength,
            })
            continue

        # suggest_rename when observed leaf differs from framework mechanical name
        leaf = (node_id or "").split(".")[-1]
        if leaf and mech and leaf != mech:
            step_n += 1
            steps.append({
                "id": f"step-{step_n}",
                "action": "suggest_rename",
                "targets": [node_id],
                "locus": f"{mech}/{locus}",
                "strength": strength,
                "safe_apply": False,
                "notes": (
                    f"Optional dual-name alignment: observed `{leaf}` maps to "
                    f"mechanical `{mech}` (symbolic `{locus}`). Mechanical filesystem "
                    f"names stay unless operator requests rename."
                ),
            })

        node = nodes_by_id.get(node_id) if node_id else None

        # suggest_boundary for STRONG/ADEQUATE mapped modules
        step_n += 1
        steps.append({
            "id": f"step-{step_n}",
            "action": "suggest_boundary",
            "targets": [node_id],
            "locus": f"{mech}/{locus}",
            "strength": strength,
            "safe_apply": False,
            "notes": (
                f"Treat `{node_id}` as package boundary aligned to locus "
                f"`{mech}` ({locus}). Keep public API mechanical."
            ),
        })

        # suggest_flatten for single-file packages (inverse of promote)
        if node and node.get("kind") == "package":
            rel = node.get("path") or ""
            if rel.endswith("__init__.py"):
                step_n += 1
                steps.append({
                    "id": f"step-{step_n}",
                    "action": "suggest_flatten",
                    "targets": [node_id],
                    "locus": f"{mech}/{locus}",
                    "strength": strength,
                    "safe_apply": False,
                    "notes": (
                        f"Optional flatten: `{node_id}` is a package path "
                        f"`{rel}`. If it contains only `__init__.py`, apply may "
                        f"collapse it to a flat module."
                    ),
                })

    # suggest_extract for observed import edges between two mapped nodes
    mapped_ids = {
        m.get("node_id")
        for m in analysis.get("mappings") or []
        if m.get("node_id")
        and STRENGTH_RANK.get(m.get("strength", "WEAK"), 0) >= threshold
        and m.get("strength") != "FORCED"
    }
    seen_pairs: set[tuple[str, str]] = set()
    for e in internal_edges:
        a, b = e.get("from"), e.get("to")
        if not a or not b or a not in mapped_ids or b not in mapped_ids:
            continue
        pair = (a, b)
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        if a not in nodes_by_id or b not in nodes_by_id:
            continue
        step_n += 1
        steps.append({
            "id": f"step-{step_n}",
            "action": "suggest_extract",
            "targets": [a, b],
            "locus": "import-flow",
            "strength": "ADEQUATE",
            "safe_apply": False,
            "notes": (
                f"Observed import edge `{a}` → `{b}`. Consider an explicit stage "
                f"boundary / interface between these modules if the flow grows."
            ),
        })

    plan = {
        "schema": "orchestra-optimize-plan.v1",
        "from_analysis": from_analysis,
        "min_strength": min_strength,
        "steps": steps,
        "blocked": blocked,
        "provenance": {
            "operator": "orchestra-cli",
            "timestamp": _utc_now(),
            "skill_version": version,
            "kind": "INFERRED",
            "analysis_status": analysis.get("status"),
            "analysis_path": analysis.get("path"),
        },
    }
    # Annotate concrete mechanical steps as safe_apply when eligible (Phase C+).
    try:
        from optimize_apply import enrich_safe_steps
        plan = enrich_safe_steps(plan, analysis)
    except Exception:
        pass
    return plan


def plan_to_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Orchestra optimize plan",
        "",
        f"From: `{plan.get('from_analysis')}`",
        f"Min strength: `{plan.get('min_strength')}`",
        f"Generated: {plan.get('provenance', {}).get('timestamp', '')}",
        "",
        "## Steps",
        "",
    ]
    steps = plan.get("steps") or []
    if not steps:
        lines.append("_Empty plan — nothing met the strength threshold._")
        lines.append("")
    else:
        for s in steps:
            lines.append(f"### {s['id']} — `{s['action']}`")
            lines.append(f"- targets: {', '.join(f'`{t}`' for t in s.get('targets') or [])}")
            lines.append(f"- locus: `{s.get('locus', '')}`")
            lines.append(f"- strength: `{s.get('strength')}`")
            lines.append(f"- safe_apply: `{s.get('safe_apply')}`")
            if s.get("notes"):
                lines.append(f"- notes: {s['notes']}")
            lines.append("")

    lines += ["## Blocked", ""]
    blocked = plan.get("blocked") or []
    if not blocked:
        lines.append("_None._")
        lines.append("")
    else:
        for b in blocked:
            targets = ", ".join(f"`{t}`" for t in b.get("targets") or []) or "(none)"
            lines.append(f"- {targets}: {b.get('reason')} (strength `{b.get('strength')}`)")
        lines.append("")

    lines += [
        "## Notes",
        "",
        "- Plan-only by default — the analyzed repository is not modified.",
        "- `optimize --apply` is dry-run; `optimize --apply --confirm` writes "
        "only `safe_apply: true` steps (rename / promote / flatten) with backup.",
        "- `suggest_extract` stays advisory (`safe_apply: false`).",
        "- Select steps with `--steps step-1,step-3` or `--actions suggest_rename`.",
        "",
    ]
    return "\n".join(lines)


def write_plan_artifacts(plan: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "optimize-plan.json").write_text(
        json.dumps(plan, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "OPTIMIZE.md").write_text(plan_to_markdown(plan), encoding="utf-8")
