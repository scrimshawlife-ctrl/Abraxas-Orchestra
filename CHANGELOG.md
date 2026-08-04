# Changelog

All notable changes to Abraxas Orchestra will be recorded here.

The format follows Keep a Changelog principles. Versions follow Semantic Versioning.

Narrative release notes: [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md).

## [0.1.3] — 2026-08-04

### Security
- Installer path jail: refuse system prefixes and targets outside `$HOME` (escape: `--allow-outside-home`)
- Installer no longer uses `eval` for install operations (`run_cmd` argv form)
- Public coordinated disclosure policy: `.github/SECURITY.md`
- Audit record: `docs/SECURITY_AUDIT.md`

### Changed
- License: **Apache-2.0** (public hub eligibility) + `NOTICE`
- Version alignment across VERSION / SKILL / manifest / CLI / installer

### Added
- `docs/PUBLIC_RELEASE.md` — public debut packaging checklist
- Installer path-refusal unit tests

## [0.1.2] — 2026-08-04

### Added
- Production packaging: smoke, tests, CI, DEPLOY, COMPLETION, runnable examples
- Structured pipeline errors on both examples
- Canonical `schemas/frameworks.v1.json`

### Fixed
- Enochian-chaos placeholders replaced with session logic
- Version alignment to 0.1.2

## [0.1.1] — 2026-08-04

### Fixed
- Schema enum expanded to all 11 frameworks + `composite`

### Added
- Hermes/OpenClaw packaging surface

## [0.1.0] — 2026-08-04

First public design surface. Corpus open for expansion.
