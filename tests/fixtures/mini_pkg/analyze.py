"""Analytical decomposition — mechanical: analyze."""

from __future__ import annotations

from . import intake


def score(payload: dict[str, str]) -> dict[str, str]:
    base = intake.pull(payload.get("source", "default"))
    return {**base, "stage": "analyze", "score": "1"}
