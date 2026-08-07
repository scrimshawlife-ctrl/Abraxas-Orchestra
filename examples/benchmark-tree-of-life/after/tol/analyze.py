"""
analyze — dual-named stage (Tree of Life)

mechanical: analyze
symbolic:   hod
ALLOWED:    Score, filter, decompose intake
FORBIDDEN:  File/network I/O, persistence, operator emission
"""

from __future__ import annotations

from typing import Any

from .intent import Intent


def score(intent: Intent, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """hod — scored records only."""
    out: list[dict[str, Any]] = []
    for row in rows:
        w = float(row.get("weight") or 0.0)
        if w < intent.require_score:
            continue
        out.append({
            **row,
            "score": w,
            "stage": "analyze",
            "symbolic": "hod",
        })
    return out
