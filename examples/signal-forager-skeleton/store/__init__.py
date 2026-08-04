"""
store — dual-named module

mechanical: store
symbolic:   yesod
locus:      Foundation / substrate
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models import ScoredSignal


class SignalStore:
    """In-memory store with optional JSON persistence."""

    def __init__(self) -> None:
        self._by_id: dict[str, ScoredSignal] = {}

    def put_many(self, signals: list[ScoredSignal]) -> int:
        for s in signals:
            self._by_id[s.signal.id] = s
        return len(signals)

    def get(self, signal_id: str) -> ScoredSignal | None:
        return self._by_id.get(signal_id)

    def all(self) -> list[ScoredSignal]:
        return list(self._by_id.values())

    def clear(self) -> None:
        self._by_id.clear()

    def save_json(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload: list[dict[str, Any]] = []
        for s in self.all():
            payload.append(
                {
                    "id": s.signal.id,
                    "text": s.signal.text,
                    "tags": s.signal.tags,
                    "weight": s.signal.weight,
                    "source": s.signal.source,
                    "score": s.score,
                    "label": s.label.value,
                    "notes": s.notes,
                }
            )
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def load_json(self, path: str | Path) -> int:
        from models import ConstrainedSignal, EpistemicLabel, Provenance

        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        count = 0
        for row in data:
            sig = ConstrainedSignal(
                id=row["id"],
                text=row["text"],
                tags=list(row.get("tags") or []),
                weight=float(row.get("weight", 1.0)),
                source=row.get("source", "store"),
                received_at=row.get("received_at", ""),
                provenance=Provenance(
                    source="store.load_json",
                    method="reload",
                    timestamp=row.get("received_at", ""),
                ),
            )
            scored = ScoredSignal(
                signal=sig,
                score=float(row.get("score", 0.0)),
                label=EpistemicLabel(row.get("label", "SPECULATIVE")),
                notes=row.get("notes", "reloaded"),
            )
            self._by_id[scored.signal.id] = scored
            count += 1
        return count
