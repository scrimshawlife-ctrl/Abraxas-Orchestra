"""
intake — dual-named module

mechanical: intake
symbolic:   chokmah
locus:      Raw force intake
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable
from uuid import uuid4

from models import RawSignal


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _as_payload(item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        return dict(item)
    if isinstance(item, str):
        return {"text": item}
    return {"text": str(item)}


def ingest(
    items: Iterable[Any],
    *,
    source: str = "anonymous",
) -> list[RawSignal]:
    """Ingest raw items into RawSignal list. No schema enforcement."""
    now = _utc_now()
    out: list[RawSignal] = []
    for item in items:
        payload = _as_payload(item)
        sid = str(payload.get("id") or uuid4())
        src = str(payload.get("source") or source)
        out.append(
            RawSignal(
                id=sid,
                payload=payload,
                source=src,
                received_at=now,
            )
        )
    return out
