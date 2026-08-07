#!/usr/bin/env python3
"""
Orchestrated pipeline — optimized *by* Tree of Life stages, not only named after them.

Flow (mechanical · symbolic):
  intent (kether) → intake (chokmah) → analyze (hod) → store (yesod) → output (malkuth)

Each stage has one job. Cross-stage calls are one-way along the map.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow `python3 pipeline.py` from this directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze import score
from intent import accept
from intake import pull
from output import emit
from store import persist


def run(source: str = "demo", *, max_items: int = 12) -> dict:
    """Execute the dual-named stage chain; structure is the control plane."""
    intent = accept(source, max_items=max_items)       # kether — contract first
    raw = pull(intent)                                 # chokmah — raw force only
    scored = score(intent, raw)                        # hod — analysis only
    saved = persist(scored)                            # yesod — foundation only
    return emit(saved)                                 # malkuth — manifestation


def main() -> int:
    result = run("demo-source", max_items=8)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
