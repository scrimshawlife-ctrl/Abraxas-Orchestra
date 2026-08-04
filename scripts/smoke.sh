#!/usr/bin/env bash
# Full production smoke: check + unit tests + example demos + install dry-run
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> orchestra check"
python3 scripts/orchestra.py check

echo "==> unit tests"
python3 -m unittest discover -s tests -v

echo "==> signal-forager demo"
python3 examples/signal-forager-skeleton/run_demo.py >/dev/null

echo "==> install dry-run"
bash install.sh --dry-run >/dev/null

echo "==> enochian-chaos demo"
( cd examples/enochian-chaos-skeleton && python3 run_demo.py >/dev/null )
echo "SMOKE OK"
