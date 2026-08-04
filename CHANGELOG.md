# Changelog

All notable changes to Abraxas Orchestra will be recorded here.

The format follows Keep a Changelog principles. Versions follow Semantic Versioning.

## [0.1.2] — 2026-08-04

### Added
- `tests/test_orchestra.py` — stdlib unittest suite (check, structure, fail-closed, disk emit, schema enum)
- `scripts/smoke.sh` — check + tests + demo + install dry-run
- `.github/workflows/ci.yml` — Python 3.11/3.12 CI
- `docs/ROADMAP.md` — done vs deferred production bar

### Fixed
- Enochian-chaos example regenerated with dual-named module stubs on disk

## [0.1.1] — 2026-08-04

### Fixed
- Correspondence schema enum expanded to all 11 frameworks + `composite`
- Schema allows `overlay_note` on mappings (matches CLI emission)
- `orchestra check` emits sample tables and validates against schema for every framework
- Installer requires all framework reference files (not only Tree/Alchemy)
- Installer stages `LICENSE`, `examples`, and itself

### Added
- README rewritten: How to use (humans + agents), definition of done, safety
- `docs/COMMUNITY.md` — community-skills compliance checklist and license gap
- SKILL.md frontmatter: version, license, openclaw/hermes metadata, when-not-to-use
- `references/agent-posture.md` — coding-agent build rules
- Proprietary `LICENSE` and `.gitignore`
- Example: `examples/enochian-chaos-skeleton/`
- Mermaid diagrams for Enochian + Chaos overlay
- Hermes/OpenClaw coding-agent packaging surface

## [0.1.0] — 2026-08-04

First public design surface. Corpus open for expansion.
