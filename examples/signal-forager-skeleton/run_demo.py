#!/usr/bin/env python3
"""
Demo runner for the signal-forager skeleton.

Usage (from this directory):
  python3 run_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from output import emit_text
from pipeline import run_forage


DEMO_ITEMS = [
    {"text": "Market signal: commodity volatility rising in energy sector", "tags": ["market", "energy"], "weight": 0.8, "source": "feed"},
    {"text": "Gossip about celebrity unrelated to query", "tags": ["noise"], "weight": 0.2, "source": "scraped"},
    {"text": "API log: energy futures spread widened overnight", "tags": ["market", "energy", "log"], "weight": 0.9, "source": "api"},
    {"text": "aaaaaaa", "tags": [], "weight": 0.5, "source": "scraped"},
    {"text": "Short", "weight": 0.9},
    {"text": "Inferred link between energy stress and transport delays", "tags": ["energy", "transport"], "weight": 0.6, "source": "analyst"},
    "plain string about energy grid frequency anomaly detected",
    {"text": "https://example.com/only-url", "weight": 0.7},
    {"text": "Duplicate energy futures spread widened overnight", "tags": ["market"], "weight": 0.5, "source": "feed"},
    {"body": "Alternate field: energy storage auction cleared below forecast", "tags": ["energy", "auction"], "weight": 0.75, "source": "archive"},
]


def main() -> int:
    out_dir = ROOT / "_demo_out"
    out_dir.mkdir(exist_ok=True)

    report, scored, store = run_forage(
        "energy market stress signals",
        DEMO_ITEMS,
        source="demo_feed",
        max_signals=10,
        min_weight=0.15,
        persist_path=str(out_dir / "store.json"),
        report_path=str(out_dir / "report.json"),
    )

    print(emit_text(report))
    print(f"stored={len(store.all())} artifacts → {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
