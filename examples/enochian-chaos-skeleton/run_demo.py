#!/usr/bin/env python3
"""Runnable Enochian + Chaos Magic session demo."""

from __future__ import annotations

import json
from pathlib import Path

from models import Domain
from pipeline import run_session

OUT = Path(__file__).resolve().parent / "_demo_out"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    edge_items = [
        {
            "id": "e1",
            "domain": "air",
            "density": 0.8,
            "payload": {"text": "analysis packet from east watchtower"},
        },
        {
            "id": "e2",
            "domain": "fire",
            "density": 0.7,
            "payload": {"text": "transform spark"},
        },
        {
            "id": "e3",
            "domain": "water",
            "density": 0.15,
            "payload": {"text": "too thin flux"},
        },
        {
            "id": "e4",
            "domain": "earth",
            "density": 0.6,
            "payload": {"text": "persist block"},
        },
        {
            "id": "e5",
            "domain": "air",
            "density": 0.9,
            "payload": {"text": ""},
        },
    ]

    report = run_session(
        session_id="sess-demo-001",
        operator="orchestra-demo",
        intent_id="intent-enochian-demo",
        statement="Open four Watchtowers; keep dense cross-domain material only.",
        edge_items=edge_items,
        domains=[Domain.AIR, Domain.FIRE, Domain.WATER, Domain.EARTH],
        min_density=0.2,
        max_items=8,
        report_path=str(OUT / "report.json"),
    )

    print(report.summary)
    print(json.dumps(report.meta.get("results_gate"), indent=2))
    print(f"wrote {OUT / 'report.json'}")
    return 0 if report.meta.get("results_gate", {}).get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
