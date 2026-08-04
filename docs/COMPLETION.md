# Completion checklist — v0.1.3

Use this page to decide when the skill package is **frozen** for Hermes/OpenClaw use (private or public).

Public debut packaging: [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).

## Automated (must be green on `main`)

| Gate | Command | Expected |
|------|---------|----------|
| Smoke | `bash scripts/smoke.sh` | `SMOKE OK` |
| Unit tests | included in smoke | 19 tests OK |
| CLI integrity | `python3 scripts/orchestra.py check` | `CHECK OK — Orchestra 0.1.3` |
| Frameworks | `python3 scripts/orchestra.py do list-frameworks` | 11 keys |
| Path jail | `bash install.sh --dry-run --target /etc/orchestra` | non-zero exit |

## Engineering surface (done on `main`)

- [x] Canonical loci: `schemas/frameworks.v1.json`
- [x] CLI: `check` / `structure` / `project` / `list-frameworks`
- [x] Atomic installer (Hermes + OpenClaw `--target`)
- [x] Installer path jail + `--allow-outside-home` escape
- [x] Signal-forager pipeline + structured errors
- [x] Enochian + Chaos pipeline + structured errors
- [x] CI workflow (Python 3.11 / 3.12)
- [x] Human + agent docs (README, SKILL, DEPLOY, SECURITY, RELEASE_NOTES)
- [x] Text-safe hero: `assets/hero.svg`
- [x] Apache-2.0 LICENSE + NOTICE (public eligibility)
- [x] Security audit + `.github/SECURITY.md`

## Operator gates (local)

- [ ] One successful install on your host (`docs/DEPLOY.md` steps 2–4)
- [ ] Optional: annotated tag `v0.1.3` (see `docs/DEPLOY.md` / `PUBLIC_RELEASE.md`)
- [ ] Optional: photographic `assets/hero.jpg` (see `assets/README.md`)
- [ ] Optional: GitHub Release + registry submit (`docs/COMMUNITY.md`)

## Explicitly deferred past 0.1.3

See `docs/ROADMAP.md` — pytest coverage gates, ritual/network runtime, dedicated OpenClaw branch.

## After freeze

Treat schema, CLI, and install layout as a **stable contract**.

- Corpus expansion: edit `schemas/frameworks.v1.json` + `references/` + tests (CONTRIBUTING checklist); no major bump required for additive frameworks.
- Contract change (CLI flags, schema required fields, install paths): bump version and CHANGELOG.

Public debut (license + registry): see [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).
