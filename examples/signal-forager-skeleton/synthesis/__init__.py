"""
synthesis — dual-named module

mechanical: synthesis
symbolic:   tiphareth
locus:      Central judgment / scoring
"""

from __future__ import annotations

from models import (
    ConstrainedSignal,
    EpistemicLabel,
    FilteredSignal,
    ScoredSignal,
)


def _score_signal(sig: ConstrainedSignal, query_terms: list[str]) -> tuple[float, EpistemicLabel, str]:
    text_l = sig.text.lower()
    term_hits = sum(1 for t in query_terms if t and t in text_l)
    tag_bonus = min(0.2, 0.05 * len(sig.tags))
    term_bonus = min(0.3, 0.1 * term_hits)
    score = max(0.0, min(1.0, sig.weight + tag_bonus + term_bonus))

    concrete_sources = ("feed", "api", "log", "sensor", "archive")
    src_l = sig.source.lower()
    if any(s in src_l for s in concrete_sources) and score >= 0.5:
        label = EpistemicLabel.OBSERVED
        notes = "concrete source + adequate score"
    elif term_hits > 0 and score >= 0.35:
        label = EpistemicLabel.INFERRED
        notes = f"term_hits={term_hits}"
    else:
        label = EpistemicLabel.SPECULATIVE
        notes = "weak match or soft source"

    return score, label, notes


def synthesize(
    filtered: list[FilteredSignal],
    *,
    query: str = "",
    max_signals: int = 50,
) -> list[ScoredSignal]:
    """Score kept signals and return top max_signals by score desc."""
    terms = [t.lower() for t in query.split() if len(t) > 2]
    scored: list[ScoredSignal] = []
    for f in filtered:
        if not f.keep:
            continue
        score, label, notes = _score_signal(f.signal, terms)
        scored.append(
            ScoredSignal(signal=f.signal, score=score, label=label, notes=notes)
        )
    scored.sort(key=lambda s: s.score, reverse=True)
    return scored[:max_signals]
