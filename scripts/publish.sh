#!/usr/bin/env bash
# Operator publish helper for Abraxas Orchestra.
# Pushing the tag triggers .github/workflows/release.yml (GitHub Release).
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
echo "Push the tag to trigger .github/workflows/release.yml:"
echo "  git push origin v${V}"
echo "Actions will smoke-test and create the GitHub Release."
echo "Notes source: docs/RELEASE_BODY_v${V}.md (if present)"
echo ""
echo "Host install:"
echo "  bash install.sh --dry-run && bash install.sh"
echo "  python3 ~/.hermes/skills/orchestra/scripts/orchestra.py check"
