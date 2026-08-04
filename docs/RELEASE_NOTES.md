# Release notes

Narrative notes for operators and agents. Machine changelog: [`CHANGELOG.md`](../CHANGELOG.md).

## 0.1.2 — 2026-08-04

Private Hermes/OpenClaw **production bar** for skill packaging.

### Highlights

| Theme | What landed |
|-------|-------------|
| Single source of truth | `schemas/frameworks.v1.json` drives CLI loci |
| Packaging | Smoke script, 17 unit tests, CI 3.11/3.12, atomic install |
| Deploy | Ordered path in `docs/DEPLOY.md` |
| Freeze checklist | `docs/COMPLETION.md` |
| Examples | Signal-forager + Enochian/Chaos runnable pipelines |

### Frameworks (v0.1.2)

Eleven maps: Tree of Life, alchemical stages, Elder Futhark, planetary spheres, I Ching (curated), Solomonic, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic.

### Examples

- Signal-forager: full Tree/alchemical pipeline with `ValidationError` / `StageError`
- Enochian + Chaos: session pipeline (seal → call → edge → inverse → bus → results gate)
- Soft-fail helpers: `run_forage_safe` / `run_session_safe`

### Upgrade from 0.1.1 / 0.1.0

1. Pull `main` (or a tag once published)
2. `bash scripts/smoke.sh`
3. Re-install with `bash install.sh` (or OpenClaw `--target`)

### Operator residuals

- Default README hero is `assets/hero.svg` (in-repo). Optional photographic `assets/hero.jpg` is operator-local
- Annotated tag is operator-local:

```bash
git tag -a v0.1.2 -m "Orchestra 0.1.2 production-ready private skill"
git push origin v0.1.2
```

### Out of scope

OSI public-hub listing, runtime ritual systems, network integrations, multi-agent product orchestration.

## 0.1.1 — 2026-08-04

Schema enum expanded to all frameworks; installer requires framework refs; packaging surface.

## 0.1.0 — 2026-08-04

First design surface. Corpus open for expansion.
