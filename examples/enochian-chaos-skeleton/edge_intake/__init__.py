"""
edge_intake — material gateway / edge intake

mechanical: edge_intake
symbolic:   aethyr_tex
locus:      Material gateway / edge intake
Overlay:    overlay:chaos-magic/chaos_shift (Paradigm engine / framework select)

Accepts dense edge material only for domains opened by domain_entry.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from models import Domain, DomainEntryToken, EdgeItem


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ingest_edge(
    token: DomainEntryToken,
    items: list[dict[str, Any]],
    *,
    source: str = "edge_feed",
) -> tuple[list[EdgeItem], list[dict[str, Any]]]:
    """Ingest edge payloads; reject items outside opened domains."""
    accepted: list[EdgeItem] = []
    rejected: list[dict[str, Any]] = []
    if not token.accepted:
        for i, raw in enumerate(items):
            rejected.append({"index": i, "reason": f"token refused: {token.reason}", "raw": raw})
        return accepted, rejected

    allowed = set(token.domains)
    for i, raw in enumerate(items):
        domain_raw = str(raw.get("domain", "")).lower().strip()
        try:
            domain = Domain(domain_raw)
        except ValueError:
            rejected.append({"index": i, "reason": f"unknown domain: {domain_raw}", "raw": raw})
            continue
        if domain not in allowed:
            rejected.append({"index": i, "reason": f"domain not opened: {domain.value}", "raw": raw})
            continue
        density = float(raw.get("density", 0.0))
        item_id = str(raw.get("id") or f"edge-{i}")
        accepted.append(
            EdgeItem(
                id=item_id,
                domain=domain,
                payload=dict(raw.get("payload") or {}),
                density=density,
                source=source,
                received_at=_utc(),
            )
        )
    return accepted, rejected
