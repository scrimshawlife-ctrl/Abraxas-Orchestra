#!/usr/bin/env python3
"""CLI entry for the Tree-of-Life optimized pipeline example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure parent of `tol` package is on path when run as a script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from tol.pipeline import run  # noqa: E402


def main() -> int:
    result = run("demo-source", max_items=8)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
