#!/usr/bin/env python3
"""
Abraxas Orchestra — CLI entrypoint (v0.2 executable surface)

Minimal, fail-closed, dual-naming skeleton emitter + repo analyze/optimize plan.
Stdlib only. No external dependencies.

Commands: check | list | structure | project | diagram | analyze | optimize
Legacy: do <command> still accepted.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "0.3.2"
SKILL_ROOT = Path(__file__).resolve().parent.parent

def _load_frameworks() -> dict[str, dict[str, Any]]:
    path = SKILL_ROOT / "schemas" / "frameworks.v1.json"
    if not path.exists():
        raise SystemExit(f"MISSING frameworks schema: {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    frameworks: dict[str, dict[str, Any]] = {}
    for key, meta in raw.get("frameworks", {}).items():
        loci = []
        for row in meta.get("default_loci", []):
            loci.append((row["mechanical"], row["symbolic"], row.get("note") or ""))
        frameworks[key] = {
            "title": meta["title"],
            "reference": meta["reference"],
            "default_loci": loci,
            "core_collapse": list(meta.get("core_collapse") or []),
        }
    return frameworks


FRAMEWORKS: dict[str, dict[str, Any]] = _load_frameworks()


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
