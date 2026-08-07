"""
intake — dual-named stage (Tree of Life)

mechanical: intake
symbolic:   chokmah
locus:      Raw force intake

Owns: pull raw records only. No scoring, no persistence.
"""

from __future__ import annotations

from typing import Any

from intent import Intent


def pull(intent: Intent) -> list[dict[str, Any]]:
    """chokmah — load raw force bounded by intent (demo: synthetic rows)."""
    # Demo intake: in production, open intent.source (file/API).
    raw = [
        {"id": i, "text": f"event-{i}", "weight": (i % 5) / 4.0}
        for i in range(intent.max_items)
    ]
    return raw[: intent.max_items]
