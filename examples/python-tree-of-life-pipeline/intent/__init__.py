"""
intent — dual-named stage (Tree of Life)

mechanical: intent
symbolic:   kether
locus:      System intent / entry contract

Owns: what the run is allowed to do (goals, limits). No I/O.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Intent:
    """kether — entry contract for one pipeline run."""

    source: str
    max_items: int = 100
    require_score: float = 0.0


def accept(source: str, *, max_items: int = 100) -> Intent:
    """Validate and freeze operator intent before any intake."""
    src = (source or "").strip()
    if not src:
        raise ValueError("intent: source is required")
    if max_items < 1:
        raise ValueError("intent: max_items must be >= 1")
    return Intent(source=src, max_items=max_items)
