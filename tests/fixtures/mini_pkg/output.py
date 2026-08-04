"""Concrete manifestation — mechanical: output."""

from __future__ import annotations

from . import analyze, store


def emit(source: str) -> dict[str, str]:
    scored = analyze.score({"source": source})
    return store.persist({**scored, "stage": "output"})
