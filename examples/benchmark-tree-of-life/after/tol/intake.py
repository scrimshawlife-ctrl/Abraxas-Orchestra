"""
intake — dual-named stage (Tree of Life)

mechanical: intake
symbolic:   chokmah
ALLOWED:    Pull raw records bounded by intent
FORBIDDEN:  Scoring, filtering policy, durable store, final emission
"""

from __future__ import annotations

from typing import Any

from .intent import Intent


def pull(intent: Intent) -> list[dict[str, Any]]:
    """chokmah — synthetic raw force only."""
    return [
        {
            "id": i,
            "text": f"event-{i}",
            "weight": (i % 5) / 4.0,
            "source": intent.source,
        }
        for i in range(intent.max_items)
    ]
