"""
adversarial — dual-named module

mechanical: adversarial
symbolic:   geburah
locus:      Severity / filtering
"""

from __future__ import annotations

import re
from typing import Iterable

from models import ConstrainedSignal, FilteredSignal


_NOISE_PATTERNS = [
    re.compile(r"^\s*$"),
    re.compile(r"^(.)\1{8,}$"),
    re.compile(r"https?://\S+$", re.I),
]


def _is_noise(text: str) -> str | None:
    if len(text) < 8:
        return "too_short"
    for pat in _NOISE_PATTERNS:
        if pat.match(text):
            return f"noise_pattern:{pat.pattern}"
    return None


def filter_signals(
    signals: list[ConstrainedSignal],
    *,
    min_weight: float = 0.1,
    require_tags: Iterable[str] | None = None,
    query_terms: Iterable[str] | None = None,
) -> list[FilteredSignal]:
    """Adversarial pass: drop noise, under-weight, tag-mismatched, query-irrelevant."""
    req = {t.lower() for t in (require_tags or [])}
    terms = [t.lower() for t in (query_terms or []) if t.strip()]
    out: list[FilteredSignal] = []

    seen_text: set[str] = set()
    for sig in signals:
        if sig.weight < min_weight:
            out.append(FilteredSignal(sig, False, f"weight_below_min:{sig.weight}"))
            continue
        noise = _is_noise(sig.text)
        if noise:
            out.append(FilteredSignal(sig, False, noise))
            continue
        key = sig.text.lower().strip()
        if key in seen_text:
            out.append(FilteredSignal(sig, False, "duplicate_text"))
            continue
        seen_text.add(key)
        if req:
            tagset = {t.lower() for t in sig.tags}
            if not req.issubset(tagset):
                out.append(FilteredSignal(sig, False, "missing_required_tags"))
                continue
        if terms:
            blob = key
            if not any(t in blob for t in terms):
                out.append(FilteredSignal(sig, False, "query_terms_absent"))
                continue
        out.append(FilteredSignal(sig, True, "ok"))
    return out
