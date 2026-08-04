"""
output — dual-named module

mechanical: output
symbolic:   malkuth
locus:      Concrete manifestation
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from models import ForageReport, Provenance, ScoredSignal


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_report(
    *,
    intent_id: str,
    kept: list[ScoredSignal],
    rejected_count: int,
    query: str,
) -> ForageReport:
    labels: dict[str, int] = {}
    for s in kept:
        labels[s.label.value] = labels.get(s.label.value, 0) + 1
    summary = (
        f"query={query!r} kept={len(kept)} rejected={rejected_count} "
        f"labels={labels}"
    )
    return ForageReport(
        intent_id=intent_id,
        kept=kept,
        rejected_count=rejected_count,
        summary=summary,
        provenance=Provenance(
            source="output.build_report",
            method="malkuth_emit",
            timestamp=_utc_now(),
        ),
        meta={"label_counts": labels, "query": query},
    )


def emit_json(report: ForageReport, path: str | Path | None = None) -> dict[str, Any]:
    """Emit report as dict; optionally write JSON file."""
    data = report.to_dict()
    if path is not None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


def emit_text(report: ForageReport) -> str:
    lines = [
        f"ForageReport intent_id={report.intent_id}",
        f"summary: {report.summary}",
        f"provenance: {report.provenance.source} @ {report.provenance.timestamp}",
        "",
        "kept signals:",
    ]
    for s in report.kept:
        lines.append(
            f"  [{s.label.value}] score={s.score:.3f} id={s.signal.id} "
            f"src={s.signal.source} :: {s.signal.text[:80]}"
        )
    return "\n".join(lines) + "\n"
