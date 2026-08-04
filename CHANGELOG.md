# Changelog

All notable changes to Abraxas Orchestra will be recorded here.

The format follows Keep a Changelog principles. Versions follow Semantic Versioning.

## [0.1.2] — 2026-08-04

### Added
- `docs/DEPLOY.md` — explicit ordered deployment next steps (Hermes/OpenClaw)
- `tests/test_orchestra.py` — stdlib unittest suite
- `scripts/smoke.sh` — check + tests + demo + install dry-run
- `.github/workflows/ci.yml` — Python 3.11/3.12 CI
- `docs/ROADMAP.md` — done vs deferred production bar
- `CONTRIBUTING.md` — smoke gate + framework-add checklist
- `schemas/frameworks.v1.json` — canonical framework loci (single source of truth)

### Fixed
- Enochian-chaos example regenerated with dual-named module stubs on disk
- SKILL.md / DESIGN.md version aligned to 0.1.2
- Installer best-effort stage of `assets/`

### Changed
- Reference depth pass across frameworks + CLI loci tables
- Tests: example skeletons + demo report shape + frameworks JSON parity (13 tests)
- Deploy: optional release-tag instructions
- CONTRIBUTING: edit `frameworks.v1.json` when adding frameworks

## [0.1.1] — 2026-08-04

### Fixed
- Correspondence schema enum expanded to all 11 frameworks + `composite`
- Schema allows `overlay_note` on mappings
- Installer requires all framework reference files

### Added
- Hermes/OpenClaw packaging surface, agent posture, examples

## [0.1.0] — 2026-08-04

First public design surface. Corpus open for expansion.
