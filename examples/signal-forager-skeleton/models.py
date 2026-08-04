"""Shared types for the signal-forager skeleton."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class EpistemicLabel(str, Enum):
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    SPECULATIVE = "SPECULATIVE"


@dataclass(frozen=True)
class Provenance:
    source: str
    method: str
    timestamp: str
    skill: str = "orchestra-signal-forager/0.1.0"


@dataclass
class RawSignal:
    """Untyped intake unit (Chokmah / Nigredo)."""

    id: str
    payload: dict[str, Any]
    source: str
    received_at: str


@dataclass
class ConstrainedSignal:
    """Schema-validated signal (Binah / Albedo)."""

    id: str
    text: str
    tags: list[str]
    weight: float
    source: str
    received_at: str
    provenance: Provenance


@dataclass
class FilteredSignal:
    """Post-adversarial signal (Geburah)."""

    signal: ConstrainedSignal
    keep: bool
    reason: str


@dataclass
class ScoredSignal:
    """Synthesized judgment unit (Tiphareth)."""

    signal: ConstrainedSignal
    score: float
    label: EpistemicLabel
    notes: str = ""


@dataclass
class ForageReport:
    """Concrete output (Malkuth)."""

    intent_id: str
    kept: list[ScoredSignal]
    rejected_count: int
    summary: str
    provenance: Provenance
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        def _sig(s: ScoredSignal) -> dict[str, Any]:
            return {
                "id": s.signal.id,
                "text": s.signal.text,
                "tags": s.signal.tags,
                "weight": s.signal.weight,
                "source": s.signal.source,
                "score": s.score,
                "label": s.label.value,
                "notes": s.notes,
            }

        return {
            "intent_id": self.intent_id,
            "kept": [_sig(s) for s in self.kept],
            "rejected_count": self.rejected_count,
            "summary": self.summary,
            "provenance": asdict(self.provenance),
            "meta": self.meta,
        }
