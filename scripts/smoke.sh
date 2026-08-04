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

echo "==> analyze scripts/ (real tree) + optimize dry-run"
SELF_OUT="$(mktemp -d "${TMPDIR:-/tmp}/orchestra-self.XXXXXX")"
# Allow exit 1 (WEAK_MAPPINGS) — analysis still succeeded
set +e
python3 scripts/orchestra.py analyze \
  --path scripts \
  -f alchemical-stages \
  --out "$SELF_OUT" >/dev/null
acode=$?
set -e
test "$acode" -eq 0 -o "$acode" -eq 1
test -f "$SELF_OUT/analysis.json"
python3 scripts/orchestra.py optimize --from "$SELF_OUT/analysis.json" --apply >/dev/null
rm -rf "$SELF_OUT"

echo "==> signal-forager demo"
python3 examples/signal-forager-skeleton/run_demo.py >/dev/null

echo "==> install dry-run"
bash install.sh --dry-run >/dev/null

echo "==> enochian-chaos demo"
( cd examples/enochian-chaos-skeleton && python3 run_demo.py >/dev/null )
echo "SMOKE OK"
