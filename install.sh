#!/usr/bin/env bash
# Abraxas Orchestra — atomic installer (v0.1)
# Installs to ~/.hermes/skills/orchestra by default.
# Supports --dry-run, --rollback, --target DIR.

set -euo pipefail

VERSION="0.1.2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_TARGET="${HOME}/.hermes/skills/orchestra"
BACKUP_ROOT="${HOME}/.hermes/receipts/orchestra-backups"

DRY_RUN=0
ROLLBACK=0
TARGET="$DEFAULT_TARGET"

usage() {
  cat <<EOF
Abraxas Orchestra installer v${VERSION}

Usage: ./install.sh [options]

Options:
  --dry-run          Show actions without writing
  --target DIR       Install to DIR (default: ${DEFAULT_TARGET})
  --rollback         Restore most recent backup for target
  -h, --help         Show this help

EOF
}

log()  { printf '==> %s\n' "$*"; }
warn() { printf '!!  %s\n' "$*" >&2; }
die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)   DRY_RUN=1; shift ;;
    --target)    TARGET="$2"; shift 2 ;;
    --rollback)  ROLLBACK=1; shift ;;
    -h|--help)   usage; exit 0 ;;
    *)           die "unknown option: $1" ;;
  esac
done

run() {
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '[dry-run] %s\n' "$*"
  else
    eval "$@"
  fi
}

validate_source() {
  log "Validating source at ${SCRIPT_DIR}"
  local required=(
    "SKILL.md"
    "orchestra.manifest.yaml"
    "VERSION"
    "scripts/orchestra.py"
    "schemas/correspondence-table.v1.schema.json"
    "schemas/frameworks.v1.json"
  )
  for f in "${required[@]}"; do
    [[ -f "${SCRIPT_DIR}/${f}" ]] || die "missing required file: ${f}"
  done

  local refs=(
    "references/tree-of-life-mappings.md"
    "references/alchemical-stages.md"
    "references/elder-futhark.md"
    "references/planetary-spheres.md"
    "references/iching-hexagrams.md"
    "references/solomonic.md"
    "references/peircean-signs.md"
    "references/numogram.md"
    "references/sacred-geometry.md"
    "references/enochian.md"
    "references/chaos-magic.md"
  )
  for f in "${refs[@]}"; do
    [[ -f "${SCRIPT_DIR}/${f}" ]] || die "missing framework reference: ${f}"
  done

  if ! python3 "${SCRIPT_DIR}/scripts/orchestra.py" check >/dev/null 2>&1; then
    python3 -c "import ast; ast.parse(open('${SCRIPT_DIR}/scripts/orchestra.py').read())" \
      || die "scripts/orchestra.py failed syntax check"
  fi
  log "Source validation OK"
}

do_rollback() {
  local latest
  latest="$(ls -1dt "${BACKUP_ROOT}"/*/ 2>/dev/null | head -1 || true)"
  [[ -n "$latest" ]] || die "no backups found under ${BACKUP_ROOT}"
  log "Rolling back from ${latest}"
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '[dry-run] rm -rf %s && cp -a %s %s\n' "$TARGET" "$latest" "$TARGET"
  else
    rm -rf "$TARGET"
    mkdir -p "$(dirname "$TARGET")"
    cp -a "$latest" "$TARGET"
  fi
  log "Rollback complete"
}

backup_existing() {
  if [[ ! -d "$TARGET" ]]; then
    return 0
  fi
  local stamp
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  local dest="${BACKUP_ROOT}/${stamp}"
  log "Backing up existing install to ${dest}"
  run "mkdir -p '${BACKUP_ROOT}'"
  run "cp -a '${TARGET}' '${dest}'"
}

atomic_install() {
  local staging
  staging="$(mktemp -d "${TMPDIR:-/tmp}/orchestra-install.XXXXXX")"
  log "Staging into ${staging}"

  run "cp -a '${SCRIPT_DIR}/SKILL.md' '${staging}/'"
  run "cp -a '${SCRIPT_DIR}/orchestra.manifest.yaml' '${staging}/'"
  run "cp -a '${SCRIPT_DIR}/VERSION' '${staging}/'"
  run "cp -a '${SCRIPT_DIR}/README.md' '${staging}/'" 2>/dev/null || true
  run "cp -a '${SCRIPT_DIR}/CHANGELOG.md' '${staging}/'" 2>/dev/null || true
  run "cp -a '${SCRIPT_DIR}/LICENSE' '${staging}/'" 2>/dev/null || true
  run "cp -a '${SCRIPT_DIR}/scripts' '${staging}/'"
  run "cp -a '${SCRIPT_DIR}/references' '${staging}/'"
  run "cp -a '${SCRIPT_DIR}/schemas' '${staging}/'"
  run "cp -a '${SCRIPT_DIR}/docs' '${staging}/'" 2>/dev/null || true
  run "cp -a '${SCRIPT_DIR}/examples' '${staging}/'" 2>/dev/null || true
  run "cp -a '${SCRIPT_DIR}/assets' '${staging}/'" 2>/dev/null || true
  run "cp -a '${SCRIPT_DIR}/tests' '${staging}/'" 2>/dev/null || true
  run "cp -a '${SCRIPT_DIR}/install.sh' '${staging}/'" 2>/dev/null || true

  run "chmod +x '${staging}/scripts/orchestra.py'"
  run "chmod +x '${staging}/scripts/smoke.sh'" 2>/dev/null || true
  run "chmod +x '${staging}/install.sh'" 2>/dev/null || true

  log "Activating at ${TARGET}"
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '[dry-run] mkdir -p %s && rm -rf %s && mv %s %s\n' \
      "$(dirname "$TARGET")" "$TARGET" "$staging" "$TARGET"
    rm -rf "$staging"
  else
    mkdir -p "$(dirname "$TARGET")"
    rm -rf "$TARGET"
    mv "$staging" "$TARGET"
  fi
}

if [[ $ROLLBACK -eq 1 ]]; then
  do_rollback
  exit 0
fi

validate_source
backup_existing
atomic_install

log "Installed Abraxas Orchestra ${VERSION} → ${TARGET}"
log "Try: python3 ${TARGET}/scripts/orchestra.py do list-frameworks"
log "     python3 ${TARGET}/scripts/orchestra.py do structure -f tree-of-life"
log "     python3 ${TARGET}/scripts/orchestra.py check"
log "     bash ${TARGET}/scripts/smoke.sh"
