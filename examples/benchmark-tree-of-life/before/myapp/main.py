"""
main — orchestrates flat tangle; no early intent contract.
"""

from __future__ import annotations

from typing import Any

from myapp.helpers import score
from myapp.stuff import dump
from myapp.utils import load


def run(source: str = "demo", *, max_items: int = 12) -> dict[str, Any]:
    """
    Flat control flow: always loads and scores even when source is empty.

    Same happy-path payload shape as the staged after/ tree for max_items,
    but structure does not enforce locus contracts.
    """
    data = load(source, max_items=max_items)
    out = score(data, require_score=0.0)
    result = dump(out)
    # Drop demo-only marker for parity comparison
    result.pop("_via", None)
    return result
