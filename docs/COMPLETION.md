# Completion checklist — v0.3.1

Use this page to decide when the skill package is **frozen** for Hermes/OpenClaw use (private or public).

Public debut packaging: [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).
Analyze → optimize plan (shipped): [`ANALYZE_OPTIMIZE_PLAN.md`](ANALYZE_OPTIMIZE_PLAN.md).

## Automated (must be green on `main`)

| Gate | Command | Expected |
|------|---------|----------|
| Smoke | `bash scripts/smoke.sh` | `SMOKE OK` |
| Unit tests | included in smoke | 40 tests OK |
| CLI integrity | `python3 scripts/orchestra.py check` | `CHECK OK — Orchestra 0.3.1` |
| Frameworks | `python3 scripts/orchestra.py list` | 11 keys |
| Path jail (install) | `bash install.sh --dry-run --target /etc/orchestra` | non-zero exit |
| Analyze fixture | `python3 scripts/orchestra.py analyze --path tests/fixtures/mini_pkg --out /tmp/orch-an` | `analysis.json` written |
| Optimize plan | `python3 scripts/orchestra.py optimize --from /tmp/orch-an/analysis.json --out /tmp/orch-plan` | plan written, no tree writes |

## Engineering surface (done on `main`)

- [x] Canonical loci: `schemas/frameworks.v1.json`
- [x] CLI: `check` / `list` / `structure` / `project` / `diagram`
- [x] CLI: `analyze` (Phase A) + `optimize` plan (Phase B)
- [x] CLI: `optimize --apply --confirm` (+ `--refresh`) (Phase C / C+)
- [x] Schemas: `analysis.v1`, `optimize-plan.v1`
- [x] Auto diagram HTML/JSON/Mermaid on structure/project/analyze `--out`
- [x] Atomic installer (Hermes + OpenClaw `--target`) with path jail
- [x] Signal-forager + Enochian/Chaos examples with structured errors
- [x] CI workflow (Python 3.11 / 3.12)
- [x] Apache-2.0 LICENSE + NOTICE
- [x] Security docs for apply write surface
- [x] Installer VERSION aligned to package VERSION

## Operator gates (local)

- [ ] One successful install on your host (`docs/DEPLOY.md` steps 2–4)
- [ ] Optional: annotated tag `v0.3.1` (see `docs/DEPLOY.md`)
- [ ] Optional: photographic `assets/hero.jpg` (SVG already ships)
- [ ] Optional: GitHub Release + registry submit (`docs/COMMUNITY.md`)

## Explicitly deferred past 0.3.1

See `docs/ROADMAP.md` — multi-language analyze, broader safe_apply, pytest coverage gates, ritual/network runtime, dedicated OpenClaw branch.

## After freeze

Treat schema, CLI, and install layout as a **stable contract**.

- Corpus expansion: edit `schemas/frameworks.v1.json` + `references/` + tests; no major bump required for additive frameworks.
- New mutating apply actions: bump minor/major per ROADMAP; update SECURITY.
- Contract change (CLI flags, schema required fields, install paths): bump version and CHANGELOG.

Public debut (license + registry): see [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).
