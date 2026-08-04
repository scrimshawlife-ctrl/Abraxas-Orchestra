"""
Signal forager pipeline — dual-named Tree of Life / alchemical stages.

intent (Kether) → intake (Chokmah/Nigredo) → constraint (Binah/Albedo)
→ adversarial (Geburah) → synthesis (Tiphareth/Citrinitas)
→ store (Yesod) → output (Malkuth/Rubedo)
"""

from __future__ import annotations

import logging
from typing import Any, Iterable

from adversarial import filter_signals
from constraint import constrain
from intake import ingest
from intent import SignalForageIntent, create_intent
from models import ForageReport, PipelineError, ScoredSignal, StageError, ValidationError
from output import build_report, emit_json
from store import SignalStore
from synthesis import synthesize

log = logging.getLogger("orchestra.forager.pipeline")


def _validate_forage_inputs(
    items: Iterable[Any] | None,
    source: str,
    max_signals: int,
    min_weight: float,
) -> list[Any]:
    if items is None:
        raise ValidationError("input", "items is required (use [] for empty feed)")
    try:
        material = list(items)
    except TypeError as exp:
        raise ValidationError("input", f"items is not iterable: {exp}") from exp
    if not isinstance(source, str) or not source.strip():
        raise ValidationError("input", "source must be a non-empty string")
    if not isinstance(max_signals, int) or max_signals < 1:
        raise ValidationError(
            "input",
            "max_signals must be an integer >= 1",
            details={"max_signals": max_signals},
        )
    if not isinstance(min_weight, (int, float)) or min_weight < 0:
        raise ValidationError(
            "input",
            "min_weight must be a number >= 0",
            details={"min_weight": min_weight},
        )
    return material


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
    if not isinstance(query, str) or not query.strip():
        raise ValidationError("intent", "query must be a non-empty string")
    try:
        intent = create_intent(
            query,
            domains=domains,
            max_signals=max_signals,
            min_weight=min_weight,
            require_tags=require_tags,
        )
    except Exception as exp:
        raise StageError("intent", f"create_intent failed: {exp}") from exp
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
    """
    Execute forage with a pre-built intent.

    Raises:
        ValidationError: bad inputs
        StageError: stage failure
        PipelineError: other pipeline failures
    """
    try:
        intent.validate()
    except Exception as exp:
        raise ValidationError("intent", f"intent invalid: {exp}") from exp

    material = _validate_forage_inputs(
        items, source, intent.max_signals, intent.min_weight
    )

    try:
        raw = ingest(material, source=source)
    except Exception as exp:
        raise StageError("intake", f"ingest failed: {exp}") from exp

    try:
        constrained, schema_rejected = constrain(raw)
    except Exception as exp:
        raise StageError("constraint", f"constrain failed: {exp}") from exp

    query_terms = [t for t in intent.query.split() if len(t) > 2]
    try:
        filtered = filter_signals(
            constrained,
            min_weight=intent.min_weight,
            require_tags=intent.require_tags,
            query_terms=query_terms,
        )
    except Exception as exp:
        raise StageError("adversarial", f"filter_signals failed: {exp}") from exp

    adv_rejected = sum(1 for f in filtered if not f.keep)

    try:
        scored = synthesize(
            filtered,
            query=intent.query,
            max_signals=intent.max_signals,
        )
    except Exception as exp:
        raise StageError("synthesis", f"synthesize failed: {exp}") from exp

    store = store or SignalStore()
    try:
        store.put_many(scored)
        if persist_path:
            store.save_json(persist_path)
    except OSError as exp:
        raise StageError(
            "store",
            f"persist failed: {exp}",
            details={"path": persist_path},
        ) from exp
    except Exception as exp:
        raise StageError("store", f"store failed: {exp}") from exp

    rejected_total = len(schema_rejected) + adv_rejected
    try:
        report = build_report(
            intent_id=intent.intent_id,
            kept=scored,
            rejected_count=rejected_total,
            query=intent.query,
        )
    except Exception as exp:
        raise StageError("output", f"build_report failed: {exp}") from exp

    if report_path:
        try:
            emit_json(report, report_path)
        except OSError as exp:
            raise StageError(
                "output",
                f"emit_json failed: {exp}",
                details={"path": report_path},
            ) from exp
        except Exception as exp:
            raise StageError("output", f"emit_json failed: {exp}") from exp

    return report, scored, store


def run_forage_safe(
    *args: Any,
    **kwargs: Any,
) -> tuple[
    tuple[ForageReport, list[ScoredSignal], SignalStore] | None,
    PipelineError | None,
]:
    """Soft-fail wrapper: returns (result, None) or (None, error)."""
    try:
        return run_forage(*args, **kwargs), None
    except PipelineError as exp:
        log.error("forage failed at %s: %s", exp.stage, exp)
        return None, exp
