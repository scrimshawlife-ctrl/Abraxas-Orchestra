"""
intent — dual-named stage (Tree of Life)

mechanical: intent
symbolic:   kether
ALLOWED:    Validate goals, limits, entry contract
FORBIDDEN:  I/O, scoring, persistence, emission
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Intent:
    source: str
    max_items: int = 100
    require_score: float = 0.0


def accept(source: str, *, max_items: int = 100) -> Intent:
    """kether — fail closed before any intake."""
    src = (source or "").strip()
    if not src:
        raise ValueError("intent: source is required")
    if max_items < 1:
        raise ValueError("intent: max_items must be >= 1")
    return Intent(source=src, max_items=max_items)
