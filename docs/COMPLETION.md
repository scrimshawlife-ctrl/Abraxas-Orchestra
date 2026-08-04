# Completion checklist — v0.1.2

Use this page to decide when the skill package is **frozen** for private Hermes/OpenClaw use.

## Automated (must be green on `main`)

| Gate | Command | Expected |
|------|---------|----------|
| Smoke | `bash scripts/smoke.sh` | `SMOKE OK` |
| Unit tests | included in smoke | 17 tests OK |
| CLI integrity | `python3 scripts/orchestra.py check` | `CHECK OK — Orchestra 0.1.2` |
| Frameworks | `python3 scripts/orchestra.py do list-frameworks` | 11 keys |

## Engineering surface (done on `main`)

- [x] Canonical loci: `schemas/frameworks.v1.json`
- [x] CLI: `check` / `structure` / `project` / `list-frameworks`
- [x] Atomic installer (Hermes + OpenClaw `--target`)
- [x] Signal-forager pipeline + structured errors
- [x] Enochian + Chaos pipeline + structured errors
- [x] CI workflow (Python 3.11 / 3.12)
- [x] Human + agent docs (README, SKILL, DEPLOY, SECURITY, RELEASE_NOTES)
- [x] Text-safe hero: `assets/hero.svg`

## Operator gates (local — not blocking private install)

- [ ] One successful install on your host (`docs/DEPLOY.md` steps 2–4)
- [ ] Optional: annotated tag `v0.1.2` (see `docs/DEPLOY.md` § Optional)
- [ ] Optional: photographic `assets/hero.jpg` (see `assets/README.md`)
- [ ] Close tracking issue for residuals when tag/hero decided

## Explicitly deferred past 0.1.2

See `docs/ROADMAP.md` — OSI relicense, pytest gates, ritual/network runtime, dedicated OpenClaw branch.

## After freeze

Treat schema, CLI, and install layout as a **stable contract**.

- Corpus expansion: edit `schemas/frameworks.v1.json` + `references/` + tests (CONTRIBUTING checklist); no major bump required for additive frameworks.
- Contract change (CLI flags, schema required fields, install paths): bump version and CHANGELOG.
