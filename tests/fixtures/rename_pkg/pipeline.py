"""Pipeline that imports the symbolic-named module."""

from __future__ import annotations

from . import nigredo


def run(source: str) -> dict[str, str]:
    return nigredo.pull(source)
