"""
output — dual-named stage (Tree of Life)

mechanical: output
symbolic:   malkuth
ALLOWED:    Shape concrete manifestation for operators
FORBIDDEN:  Intake, analysis rules, low-level store protocols
"""

from __future__ import annotations

from typing import Any


def emit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """malkuth — final payload."""
    return {
        "count": len(rows),
        "items": rows,
        "stage": "output",
        "symbolic": "malkuth",
        "status": "OK",
    }
