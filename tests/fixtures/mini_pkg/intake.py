"""Raw force intake — mechanical: intake."""

from __future__ import annotations


def pull(source: str) -> dict[str, str]:
    return {"source": source, "stage": "intake"}
