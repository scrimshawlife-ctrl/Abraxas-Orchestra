# Abraxas Orchestra — Design

**Status**: Executable skill surface  
**Version target**: 0.1.2  
**Hosts**: Hermes, OpenClaw

## Intent

Structure software architecture using traditional correspondence systems as hierarchical maps. Emit dual-named modules (mechanical primary, symbolic secondary) with recoverable provenance. Fail closed on weak mappings. Preserve human sovereignty over forced correspondences.

## Core contracts

1. **Dual naming** — Every structural unit carries a mechanical identifier and an optional symbolic locus.
2. **Provenance** — Correspondence tables declare strength (`STRONG` / `ADEQUATE` / `WEAK` / `FORCED`) and notes.
3. **Pragmatic projection** — Oversized or forced maps collapse under `do project` with an explicit projection note.
4. **Open corpus** — Framework tables expand without breaking the CLI contract.
5. **Agent posture** — Implementation rules live in `references/agent-posture.md` (smallest working layer, no invented loci).

## Executable surface (v0.1.2)

- CLI: `check`, `do list-frameworks`, `do structure`, `do project`
- Schema validation inside `check` (v0.1.2)
- Atomic installer with dry-run and rollback
- Smoke script + stdlib unit tests + CI

## Framework data source

Canonical loci live in `schemas/frameworks.v1.json`. The CLI loads this file at startup via `_load_frameworks()`. Markdown under `references/` is progressive-disclosure documentation and must stay aligned with the JSON when frameworks change.

## Related docs

- [`RELEASE_NOTES.md`](RELEASE_NOTES.md)
- [`DEPLOY.md`](DEPLOY.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`SECURITY.md`](SECURITY.md)
- [`CHANGELOG.md`](../CHANGELOG.md)
