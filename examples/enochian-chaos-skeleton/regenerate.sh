#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$ROOT/scripts/orchestra.py" do structure \
  -f enochian \
  -o chaos-magic \
  -c "edge_intake,domain_entry,root_truth_seal,cross_domain_bus,inverse_capability,sovereign_intent" \
  --out "$(cd "$(dirname "$0")" && pwd)"
