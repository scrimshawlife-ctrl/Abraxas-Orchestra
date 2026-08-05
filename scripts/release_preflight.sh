#!/usr/bin/env bash
# Operator preflight before tagging a release. Stdlib + bash only.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> smoke"
bash scripts/smoke.sh

echo "==> version parity (semver)"
python3 scripts/bump_version.py check
V="$(python3 scripts/bump_version.py show)"
echo "VERSION=$V"

echo "==> path jail (install)"
set +e
bash install.sh --dry-run --target /etc/orchestra >/dev/null 2>&1
icode=$?
set -e
test "$icode" -ne 0
echo "install jail OK (exit $icode)"

echo "==> path jail (analyze)"
set +e
python3 scripts/orchestra.py analyze --path /etc >/dev/null 2>&1
acode=$?
set -e
test "$acode" -eq 2
echo "analyze jail OK (exit $acode)"

echo "==> license surface"
test -f LICENSE && test -f NOTICE && test -f .github/SECURITY.md
echo "license OK"

echo ""
echo "PREFLIGHT OK — ready to tag v${V}"
echo "  git tag -a v${V} -m \"Orchestra ${V}\""
echo "  git push origin v${V}"
