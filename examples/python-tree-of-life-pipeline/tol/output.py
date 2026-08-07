"""
output — dual-named stage (Tree of Life)

mechanical: output
symbolic:   malkuth
locus:      Concrete manifestation

Owns: final emission shape for operators/agents. No intake or store rules.
"""

from __future__ import annotations

from typing import Any


def emit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """malkuth — concrete manifestation of the pipeline result."""
    return {
        "count": len(rows),
        "items": rows,
        "stage": "output",
        "symbolic": "malkuth",
        "status": "OK",
    }
