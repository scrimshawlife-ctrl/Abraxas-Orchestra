"""
utils — mixed intake + light scoring (tangled).

Deliberately violates single-locus design: loads raw rows *and*
applies weight tweaks that belong in analyze.
"""

from __future__ import annotations

from typing import Any

# Cycle: utils → helpers → stuff → utils (structure smell)
from myapp import helpers  # noqa: F401 — imported for side-effect cycle


def load(source: str, max_items: int = 12) -> list[dict[str, Any]]:
    """Load raw events *and* pre-score weights (mixed responsibility)."""
    # No intent gate: empty source still runs full work.
    label = source if source else "anonymous"
    rows: list[dict[str, Any]] = []
    for i in range(max(max_items, 0)):
        weight = (i % 5) / 4.0
        # Scoring logic embedded in intake path
        weight = helpers.reweight(weight)
        rows.append({"id": i, "text": f"event-{i}", "weight": weight, "source": label})
    return rows
