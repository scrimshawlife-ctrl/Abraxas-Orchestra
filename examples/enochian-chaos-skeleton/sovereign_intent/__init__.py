"""
sovereign_intent — apex intent / pure contract

mechanical: sovereign_intent
symbolic:   aethyr_lil
locus:      Apex intent / pure contract
Overlay:    overlay:chaos-magic/results_metric (Results eval gate)

Holds the session contract and applies the Chaos results gate.
"""

from __future__ import annotations

from models import Domain, SovereignContract


def make_contract(
    intent_id: str,
    statement: str,
    *,
    max_items: int = 8,
    allowed_domains: list[Domain] | None = None,
    min_density: float = 0.2,
) -> SovereignContract:
    domains = allowed_domains or [Domain.AIR, Domain.FIRE, Domain.WATER, Domain.EARTH]
    return SovereignContract(
        intent_id=intent_id,
        statement=statement.strip(),
        max_items=max_items,
        allowed_domains=list(domains),
        min_density=min_density,
    )


def results_gate(
    contract: SovereignContract,
    kept_count: int,
    rejected_count: int,
) -> dict[str, object]:
    """Chaos outcome gate: pass if any kept item under contract caps."""
    ok = kept_count > 0 and kept_count <= contract.max_items
    return {
        "pass": ok,
        "intent_id": contract.intent_id,
        "kept": kept_count,
        "rejected": rejected_count,
        "max_items": contract.max_items,
        "statement": contract.statement,
        "note": "results_metric gate" if ok else "results_metric fail — no kept items or over max",
    }
