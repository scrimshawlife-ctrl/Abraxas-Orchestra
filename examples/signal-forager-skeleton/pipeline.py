"""
Pipeline orchestrator — Tree of Life path through the signal forager.

Kether (intent) → Chokmah (intake) → Binah (constraint) → Geburah (adversarial)
→ Tiphareth (synthesis) → Yesod (store) → Malkuth (output)
"""

from __future__ import annotations

from typing import Any, Iterable

from adversarial import filter_signals
from constraint import constrain
from intake import ingest
from intent import SignalForageIntent, create_intent
from models import ForageReport, ScoredSignal
from output import build_report, emit_json
from store import SignalStore
from synthesis import synthesize


def run_forage(
    query: str,
    items: Iterable[Any],
    *,
    source: str = "demo_feed",
    domains: list[str] | None = None,
    max_signals: int = 20,
    min_weight: float = 0.1,
    require_tags: list[str] | None = None,
    store: SignalStore | None = None,
    persist_path: str | None = None,
    report_path: str | None = None,
) -> tuple[ForageReport, list[ScoredSignal], SignalStore]:
    """Execute one full forage cycle. Deterministic given identical inputs."""
    intent = create_intent(
        query,
        domains=domains,
        max_signals=max_signals,
        min_weight=min_weight,
        require_tags=require_tags,
    )
    return run_forage_with_intent(
        intent,
        items,
        source=source,
        store=store,
        persist_path=persist_path,
        report_path=report_path,
    )


def run_forage_with_intent(
    intent: SignalForageIntent,
    items: Iterable[Any],
    *,
    source: str = "demo_feed",
    store: SignalStore | None = None,
    persist_path: str | None = None,
    report_path: str | None = None,
) -> tuple[ForageReport, list[ScoredSignal], SignalStore]:
    intent.validate()

    raw = ingest(items, source=source)
    constrained, schema_rejected = constrain(raw)

    query_terms = [t for t in intent.query.split() if len(t) > 2]
    filtered = filter_signals(
        constrained,
        min_weight=intent.min_weight,
        require_tags=intent.require_tags,
        query_terms=query_terms,
    )
    adv_rejected = sum(1 for f in filtered if not f.keep)

    scored = synthesize(
        filtered,
        query=intent.query,
        max_signals=intent.max_signals,
    )

    store = store or SignalStore()
    store.put_many(scored)
    if persist_path:
        store.save_json(persist_path)

    rejected_total = len(schema_rejected) + adv_rejected
    report = build_report(
        intent_id=intent.intent_id,
        kept=scored,
        rejected_count=rejected_total,
        query=intent.query,
    )
    if report_path:
        emit_json(report, report_path)

    return report, scored, store
