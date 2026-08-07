"""
store — dual-named stage (Tree of Life)

mechanical: store
symbolic:   yesod
ALLOWED:    Persist foundation/substrate state
FORBIDDEN:  New scoring rules, raw intake, final packaging
"""

from __future__ import annotations

from typing import Any


def persist(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """yesod — in-memory foundation stamp."""
    return [
        {**r, "stored": True, "stage": "store", "symbolic": "yesod"}
        for r in rows
    ]
