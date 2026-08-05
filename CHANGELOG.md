# Changelog

All notable changes to Abraxas Orchestra will be recorded here.

The format follows Keep a Changelog principles. Versions follow Semantic Versioning.

Narrative release notes: [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md).

## [0.4.0] — 2026-08-05

### Added
- `suggest_boundary` safe apply: promote `module.py` → `module/__init__.py` when stem matches mechanical name
- `suggest_flatten` plan + safe apply: collapse single-file packages `leaf/__init__.py` → `leaf.py`
- `optimize --steps` — apply only listed step ids (still must be `safe_apply`)
- `optimize --actions` — filter by action name (`suggest_rename`, `suggest_boundary`, `suggest_flatten`)
- Schema `schemas/optimize-apply.v1.schema.json`

### Changed
- Apply path runs renames → promotes → flattens; collision demotion covers all three move kinds
- Docs aligned: ANALYZE_OPTIMIZE_PLAN (Phase C++), SECURITY / SECURITY_AUDIT, COMPLETION, ROADMAP, PUBLIC_RELEASE, DEPLOY, CONTRIBUTING

## [0.3.2] — 2026-08-04

### Added
- Semantic versioning policy (`docs/SEMVER.md`)
- `scripts/bump_version.py` — show / check / patch / minor / major / set
- CI `version-parity` runs `bump_version.py check`
- `tests/test_semver.py`

### Changed
- `release_preflight.sh` uses semver parity check
- CONTRIBUTING documents bump classes (framework=PATCH, capability=MINOR, break=MAJOR)

## [0.3.1] — 2026-08-04

### Fixed
- Packaging drift: `install.sh` VERSION aligned to 0.3.1; README quick-start flat CLI; COMPLETION checklist refreshed

### Added
- `optimize --apply --confirm --refresh` re-analyzes the tree and writes refreshed `analysis.json` beside the backup
- Vacate-first ordering when a rename destination is another rename’s source
- Destination-collision demotion in plan enrichment
- Analyze skips `.orchestra-backups/`; smoke analyzes `scripts/` + optimize dry-run

## [0.3.0] — 2026-08-04

### Added
- `optimize --apply` dry-run; `--apply --confirm` performs gated mechanical renames with backup
- Import lines rewritten with `as <old>` aliases so call sites stay valid
- `RESTORE.md` + `apply-report.json` written under `--backup-dir`
- Fixture `tests/fixtures/rename_pkg/` for apply tests

### Security
- Apply path jail under analyzed root; refuse FORCED analysis; system backup-dir denied

## [0.2.0] — 2026-08-04

### Added
- `analyze` — read-only Python repo import graph + optional fail-closed framework map
- `optimize` — plan-only refactor suggestions from `analysis.json` (no tree writes)
- Schemas: `analysis.v1`, `optimize-plan.v1`
- Fixture `tests/fixtures/mini_pkg/`

## [0.1.6] — 2026-08-04

### Added
- Automatic diagram emission on `structure`/`project --out`: HTML + JSON + Mermaid (`.mmd`)
- Skill contract: agents must use Orchestra diagram output instead of ad-hoc Mermaid when mapping structure

## [0.1.5] — 2026-08-04

### Added
- `diagram` / `diagrammit` — interactive HTML + agent JSON (`nodes`, `edges`, `flows`)

## [0.1.4] — 2026-08-04

### Changed
- CLI simplified: top-level `check` | `list` | `structure` | `project`

## [0.1.3] — 2026-08-04

### Security
- Path jail; Apache-2.0; audit docs

## [0.1.0] — 2026-08-04

First design surface.
