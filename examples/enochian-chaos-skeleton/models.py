"""Shared types for the Enochian + Chaos Magic session skeleton."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class PipelineError(Exception):
    """Base error for Enochian session pipeline failures."""

    def __init__(self, stage: str, message: str, *, details: dict[str, Any] | None = None) -> None:
        self.stage = stage
        self.details = details or {}
        super().__init__(f"[{stage}] {message}")


class ValidationError(PipelineError):
    """Invalid inputs before or during a stage."""


class StageError(PipelineError):
    """Unexpected failure inside a pipeline stage."""


class EpistemicLabel(str, Enum):
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    SPECULATIVE = "SPECULATIVE"


class Domain(str, Enum):
    AIR = "air"  # east / analysis / messaging
    FIRE = "fire"  # south / transformation
    WATER = "water"  # west / memory / flux
    EARTH = "earth"  # north / persistence


@dataclass(frozen=True)
class Provenance:
    source: str
    method: str
    timestamp: str
    skill: str = "orchestra-enochian-chaos/0.1.2"


@dataclass
class RootTruthSeal:
    """Session authority seal (sigillum_dei_aemeth)."""

    session_id: str
    operator: str
    valid: bool
    reason: str
    provenance: Provenance


@dataclass
class DomainEntryToken:
    """Invocation / domain-entry token (enochian_call)."""

    call_id: str
    domains: list[Domain]
    seal_session_id: str
    accepted: bool
    reason: str


@dataclass
class EdgeItem:
    """Material gateway unit (aethyr_tex)."""

    id: str
    domain: Domain
    payload: dict[str, Any]
    density: float
    source: str
    received_at: str


@dataclass
class BusMessage:
    """Cross-domain coordination message (tablet_of_union)."""

    id: str
    from_domain: Domain
    to_domain: Domain | None
    body: str
    weight: float


@dataclass
class InverseFinding:
    """Adversarial / fail-mode surface (cacodemon_mirror)."""

    item_id: str
    kept: bool
    reason: str
    label: EpistemicLabel


@dataclass
class SovereignContract:
    """Apex intent / pure contract (aethyr_lil)."""

    intent_id: str
    statement: str
    max_items: int
    allowed_domains: list[Domain]
    min_density: float


@dataclass
class SessionReport:
    """Concrete session emission."""

    session_id: str
    intent_id: str
    seal_valid: bool
    accepted_calls: int
    edge_count: int
    bus_count: int
    kept: list[dict[str, Any]]
    rejected_count: int
    summary: str
    provenance: Provenance
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "intent_id": self.intent_id,
            "seal_valid": self.seal_valid,
            "accepted_calls": self.accepted_calls,
            "edge_count": self.edge_count,
            "bus_count": self.bus_count,
            "kept": self.kept,
            "rejected_count": self.rejected_count,
            "summary": self.summary,
            "provenance": asdict(self.provenance),
            "meta": self.meta,
        }
