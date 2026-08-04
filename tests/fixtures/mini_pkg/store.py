"""Foundation / substrate — mechanical: store."""

from __future__ import annotations


def persist(record: dict[str, str]) -> dict[str, str]:
    return {**record, "stored": "yes"}
