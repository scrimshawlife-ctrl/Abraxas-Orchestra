# Release notes

Narrative notes for operators and agents. Machine changelog: [`CHANGELOG.md`](../CHANGELOG.md).

## 0.1.3 — 2026-08-04

**Public debut packaging** with security hardening.

### Security
- Installer path jail + system-prefix deny list
- No `eval` in install execution path
- Apache-2.0 LICENSE + NOTICE
- `.github/SECURITY.md` + `docs/SECURITY_AUDIT.md`

### Upgrade from 0.1.2
1. Pull `main` or tag `v0.1.3`
2. `bash scripts/smoke.sh`
3. Re-install (`bash install.sh`); note new refusal of outside-`$HOME` targets

### Public registries
Eligible under Apache-2.0. Follow `docs/PUBLIC_RELEASE.md` and `docs/COMMUNITY.md`.

## 0.1.2 — 2026-08-04

Private Hermes/OpenClaw **production bar** for skill packaging.

### Highlights

| Theme | What landed |
|-------|-------------|
| Single source of truth | `schemas/frameworks.v1.json` drives CLI loci |
| Packaging | Smoke script, unit tests, CI 3.11/3.12, atomic install |
| Deploy | Ordered path in `docs/DEPLOY.md` |
| Freeze checklist | `docs/COMPLETION.md` |
| Examples | Signal-forager + Enochian/Chaos runnable pipelines |

### Examples

- Signal-forager: full Tree/alchemical pipeline with `ValidationError` / `StageError`
- Enochian + Chaos: session pipeline (seal → call → edge → inverse → bus → results gate)
- Soft-fail helpers: `run_forage_safe` / `run_session_safe`

### Operator residuals (0.1.2)

- Default README hero is `assets/hero.svg`
- Annotated tag optional

## 0.1.1 — 2026-08-04

Schema enum expanded; installer requires framework refs; packaging surface.

## 0.1.0 — 2026-08-04

First design surface. Corpus open for expansion.
