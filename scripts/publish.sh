#!/usr/bin/env bash
# Operator publish helper for Abraxas Orchestra.
# Does NOT create the GitHub Release UI draft (paste body from docs/RELEASE_BODY_v0.3.2.md).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

V="$(tr -d '[:space:]' < VERSION)"
echo "==> publishing line: ${V}"

echo "==> preflight"
bash scripts/release_preflight.sh

if git rev-parse "v${V}" >/dev/null 2>&1; then
  echo "tag v${V} already exists locally"
else
  git tag -a "v${V}" -m "Orchestra ${V}"
  echo "created local tag v${V}"
fi

echo ""
echo "Next (requires your credentials):"
echo "  git push origin main"
echo "  git push origin v${V}"
echo ""
echo "Then GitHub → Releases → Create release from tag v${V}"
echo "Paste body from: docs/RELEASE_BODY_v${V}.md"
echo ""
echo "Host install:"
echo "  bash install.sh --dry-run && bash install.sh"
echo "  python3 ~/.hermes/skills/orchestra/scripts/orchestra.py check"
