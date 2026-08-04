"""
constraint — dual-named module

mechanical: constraint
symbolic:   binah
locus:      Schema / form constraint
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from models import ConstrainedSignal, Provenance, RawSignal


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _extract_text(payload: dict[str, Any]) -> str | None:
    for key in ("text", "body", "content", "message"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return None


def _extract_tags(payload: dict[str, Any]) -> list[str]:
    raw = payload.get("tags") or payload.get("labels") or []
    if isinstance(raw, str):
        return [t.strip() for t in raw.split(",") if t.strip()]
    if isinstance(raw, list):
        return [str(t).strip() for t in raw if str(t).strip()]
    return []


def _extract_weight(payload: dict[str, Any]) -> float:
    w = payload.get("weight", payload.get("score", 1.0))
    try:
        return float(w)
    except (TypeError, ValueError):
        return 1.0


def constrain(
    raw_signals: list[RawSignal],
) -> tuple[list[ConstrainedSignal], list[dict[str, str]]]:
    """Validate raw signals. Returns (kept, rejections). Fail-closed."""
    kept: list[ConstrainedSignal] = []
    rejected: list[dict[str, str]] = []
    now = _utc_now()

    for raw in raw_signals:
        text = _extract_text(raw.payload)
        if text is None:
            rejected.append({"id": raw.id, "reason": "missing text/body/content"})
            continue
        weight = _extract_weight(raw.payload)
        if weight < 0 or weight > 10:
            rejected.append({"id": raw.id, "reason": f"weight out of range: {weight}"})
            continue
        norm_weight = weight if weight <= 1.0 else min(1.0, weight / 10.0)
        tags = _extract_tags(raw.payload)
        kept.append(
            ConstrainedSignal(
                id=raw.id,
                text=text,
                tags=tags,
                weight=norm_weight,
                source=raw.source,
                received_at=raw.received_at,
                provenance=Provenance(
                    source=raw.source,
                    method="constraint.constrain",
                    timestamp=now,
                ),
            )
        )
    return kept, rejected
