"""
store — dual-named stage (Tree of Life)

mechanical: store
symbolic:   yesod
locus:      Foundation / substrate

Owns: durable substrate write. No scoring logic.
"""

from __future__ import annotations

from typing import Any


def persist(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """yesod — attach foundation markers (demo: in-memory stamp)."""
    return [{**r, "stored": True, "stage": "store", "symbolic": "yesod"} for r in rows]
