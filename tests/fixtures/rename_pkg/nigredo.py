"""Chaos / putrefaction intake — symbolic nigredo → mechanical raw_ingest."""

from __future__ import annotations


def pull(source: str) -> dict[str, str]:
    return {"source": source, "stage": "nigredo"}
