#!/usr/bin/env bash
# Regenerate this example skeleton from the Orchestra CLI.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$(cd "$(dirname "$0")" && pwd)"
python3 "$ROOT/scripts/orchestra.py" do structure \
  -f tree-of-life \
  -o alchemical-stages \
  -c "intent,intake,constraint,adversarial,synthesis,store,output" \
  --out "$OUT"
echo "Regenerated under $OUT"
