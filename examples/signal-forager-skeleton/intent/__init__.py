"""
intent — dual-named module

mechanical: intent
symbolic:   kether
locus:      System intent / entry contract
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class SignalForageIntent:
    """Kether-level entry contract for a single forage run."""

    query: str
    domains: list[str] = field(default_factory=list)
    max_signals: int = 50
    min_weight: float = 0.1
    require_tags: list[str] = field(default_factory=list)
    intent_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=_utc_now)
    notes: str = ""

    def validate(self) -> None:
        if not self.query or not self.query.strip():
            raise ValueError("intent.query must be non-empty")
        if self.max_signals < 1:
            raise ValueError("intent.max_signals must be >= 1")
        if not (0.0 <= self.min_weight <= 1.0):
            raise ValueError("intent.min_weight must be in [0, 1]")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def create_intent(
    query: str,
    *,
    domains: list[str] | None = None,
    max_signals: int = 50,
    min_weight: float = 0.1,
    require_tags: list[str] | None = None,
    notes: str = "",
) -> SignalForageIntent:
    """Build and validate a forage intent."""
    intent = SignalForageIntent(
        query=query.strip(),
        domains=list(domains or []),
        max_signals=max_signals,
        min_weight=min_weight,
        require_tags=list(require_tags or []),
        notes=notes,
    )
    intent.validate()
    return intent
