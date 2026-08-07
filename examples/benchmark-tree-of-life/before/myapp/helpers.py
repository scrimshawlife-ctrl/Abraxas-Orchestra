"""
helpers — scoring mixed with dump helpers (tangled).
"""

from __future__ import annotations

from typing import Any

# Cycle: helpers → stuff → utils → helpers
from myapp import stuff  # noqa: F401


def reweight(weight: float) -> float:
    """Tiny score transform — should live only in analyze."""
    return float(weight)


def score(rows: list[dict[str, Any]], require_score: float = 0.0) -> list[dict[str, Any]]:
    """Score/filter, then peek at stuff for store-shaped fields (cross-cut)."""
    out: list[dict[str, Any]] = []
    for row in rows:
        w = float(row.get("weight") or 0.0)
        if w < require_score:
            continue
        item = {
            **row,
            "score": w,
            "stage": "analyze",
            "symbolic": "hod",
        }
        # Helpers knows about store markers — mixed locus
        item = stuff.stamp_partial(item)
        out.append(item)
    return out
