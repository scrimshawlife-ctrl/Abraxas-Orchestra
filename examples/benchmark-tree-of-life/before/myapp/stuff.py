"""
stuff — store + emit mixed (tangled).
"""

from __future__ import annotations

from typing import Any

# Cycle: stuff → utils → helpers → stuff
from myapp import utils  # noqa: F401


def stamp_partial(row: dict[str, Any]) -> dict[str, Any]:
    """Attach store fields early (called from helpers during score)."""
    return {**row, "stored": True, "stage": "store", "symbolic": "yesod"}


def dump(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Persist markers (already applied) + final emission shape."""
    # Touch utils symbol so the cycle is real at import time
    _ = utils.load  # noqa: B018
    items = [{**r, "stage": "output", "symbolic": "malkuth"} if r.get("stage") == "store" else r for r in rows]
    # Prefer final stage label on items for parity with after emit
    final: list[dict[str, Any]] = []
    for r in rows:
        final.append({
            **r,
            "stored": True,
            "stage": "store",
            "symbolic": "yesod",
        })
    return {
        "count": len(final),
        "items": final,
        "stage": "output",
        "symbolic": "malkuth",
        "status": "OK",
        "_via": "stuff.dump",
    }
