# Completion checklist — v0.3.2

Use this page to decide when the skill package is **frozen** for Hermes/OpenClaw use (private or public).

Public debut packaging: [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).  
Active plan: [`ANALYZE_OPTIMIZE_PLAN.md`](ANALYZE_OPTIMIZE_PLAN.md) (Phases A–C shipped).

## Automated (must be green on `main`)

| Gate | Command | Expected |
|------|---------|----------|
| Smoke | `bash scripts/smoke.sh` | `SMOKE OK` |
| Unit tests | included in smoke | 40+ tests OK |
| CLI integrity | `python3 scripts/orchestra.py check` | `CHECK OK — Orchestra 0.3.2` |
| Frameworks | `python3 scripts/orchestra.py list` | 11 keys |
| Path jail | `bash install.sh --dry-run --target /etc/orchestra` | non-zero exit |
| Analyze fixture | `… analyze --path tests/fixtures/mini_pkg -f tree-of-life` | exit 0, `CLEAN` |

## Engineering surface (done on `main`)

- [x] Canonical loci: `schemas/frameworks.v1.json`
- [x] CLI: `check` | `list` | `structure` | `project` | `diagram` | `analyze` | `optimize`
- [x] Analyze → map → optimize plan (0.2.0)
- [x] Optimize apply + refresh + boundary promote + `--steps` (0.3.x)
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
- [ ] Optional: annotated tag `v0.3.2` (see `docs/DEPLOY.md` / `PUBLIC_RELEASE.md`)
- [ ] Optional: photographic `assets/hero.jpg` (see `assets/README.md`)
- [ ] Optional: GitHub Release + registry submit (`docs/COMMUNITY.md`)

## Explicitly deferred

See `docs/ROADMAP.md` — multi-language analyze, network install, pytest coverage gates, ritual/network runtime, dedicated OpenClaw branch.

## After freeze

Treat schema, CLI, and install layout as a **stable contract**.

- Corpus expansion: edit `schemas/frameworks.v1.json` + `references/` + tests (CONTRIBUTING checklist); no major bump required for additive frameworks.
- Contract change (CLI flags, schema required fields, install paths): bump version and CHANGELOG.

Public debut (license + registry): see [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).
