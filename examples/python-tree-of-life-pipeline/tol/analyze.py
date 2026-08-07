"""
analyze — dual-named stage (Tree of Life)

mechanical: analyze
symbolic:   hod
locus:      Analytical decomposition

Owns: scoring / filtering only. No I/O, no mutation of store.
"""

from __future__ import annotations

from typing import Any

from .intent import Intent


def score(intent: Intent, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """hod — decompose raw intake into scored records."""
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
