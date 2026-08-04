# Changelog

All notable changes to Abraxas Orchestra will be recorded here.

The format follows Keep a Changelog principles. Versions follow Semantic Versioning.

Narrative release notes: [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md).

## [0.1.2] — 2026-08-04

### Added
- `docs/DEPLOY.md` — explicit ordered deployment next steps (Hermes/OpenClaw)
- `tests/test_orchestra.py` — stdlib unittest suite (14 tests)
- `scripts/smoke.sh` — check + tests + demo + install dry-run
- `.github/workflows/ci.yml` — Python 3.11/3.12 CI
- `docs/ROADMAP.md` — done vs deferred production bar
- `CONTRIBUTING.md` — smoke gate + framework-add checklist
- `schemas/frameworks.v1.json` — canonical framework loci (single source of truth)
- `docs/RELEASE_NOTES.md` — narrative release notes for operators and agents
- `docs/SECURITY.md` — local threat model
- `references/enochian-cli-loci.md` — Enochian CLI table companion
- `assets/hero.svg` — text-safe README hero (JPEG remains optional)

### Fixed
- Enochian-chaos example regenerated with dual-named module stubs on disk
- SKILL.md / DESIGN.md version aligned to 0.1.2
- Installer best-effort stage of `assets/`

### Changed
- Reference depth pass across frameworks + CLI loci tables
- CLI loads `schemas/frameworks.v1.json` at startup (no embedded FRAMEWORKS dict)
- Installer requires `schemas/frameworks.v1.json` and `references/enochian-cli-loci.md`
- Manifest lists frameworks schema path

## [0.1.1] — 2026-08-04

### Fixed
- Correspondence schema enum expanded to all 11 frameworks + `composite`
- Schema allows `overlay_note` on mappings
- Installer requires all framework reference files

### Added
- Hermes/OpenClaw packaging surface, agent posture, examples

## [0.1.0] — 2026-08-04

First public design surface. Corpus open for expansion.
