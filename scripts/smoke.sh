#!/usr/bin/env bash
# Full production smoke: check + unit tests + example demos + install dry-run
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> orchestra check"
python3 scripts/orchestra.py check

echo "==> unit tests"
python3 -m unittest discover -s tests -v

echo "==> analyze fixture"
ANALYZE_OUT="$(mktemp -d "${TMPDIR:-/tmp}/orchestra-analyze.XXXXXX")"
python3 scripts/orchestra.py analyze \
  --path tests/fixtures/mini_pkg \
  -f tree-of-life \
  --out "$ANALYZE_OUT" >/dev/null
test -f "$ANALYZE_OUT/analysis.json"
python3 scripts/orchestra.py optimize --from "$ANALYZE_OUT/analysis.json" --out "$ANALYZE_OUT/plan" >/dev/null
test -f "$ANALYZE_OUT/plan/optimize-plan.json"
rm -rf "$ANALYZE_OUT"

echo "==> signal-forager demo"
python3 examples/signal-forager-skeleton/run_demo.py >/dev/null

echo "==> install dry-run"
bash install.sh --dry-run >/dev/null

echo "==> enochian-chaos demo"
( cd examples/enochian-chaos-skeleton && python3 run_demo.py >/dev/null )
echo "SMOKE OK"
