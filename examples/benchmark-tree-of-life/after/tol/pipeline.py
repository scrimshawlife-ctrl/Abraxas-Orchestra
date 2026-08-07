"""
pipeline — one-way flow along the Tree of Life map.
"""

from __future__ import annotations

from typing import Any

from .analyze import score
from .intent import accept
from .intake import pull
from .output import emit
from .store import persist


def run(source: str = "demo", *, max_items: int = 12) -> dict[str, Any]:
    """Staged control plane: intent first, then one-way stages."""
    intent = accept(source, max_items=max_items)
    raw = pull(intent)
    scored = score(intent, raw)
    saved = persist(scored)
    return emit(saved)
