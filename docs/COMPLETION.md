# Completion checklist — v0.3.2

Use this page to decide when the skill package is **frozen** for Hermes/OpenClaw use (private or public).

Public debut packaging: [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).
Analyze → optimize plan (shipped): [`ANALYZE_OPTIMIZE_PLAN.md`](ANALYZE_OPTIMIZE_PLAN.md).
Version policy: [`SEMVER.md`](SEMVER.md).
Publish helper: `scripts/publish.sh` · Release body: [`RELEASE_BODY_v0.3.2.md`](RELEASE_BODY_v0.3.2.md).
Release automation: [`.github/workflows/release.yml`](../.github/workflows/release.yml).

## Automated (must be green on `main`)

| Gate | Command | Expected |
|------|---------|----------|
| Smoke | `bash scripts/smoke.sh` | `SMOKE OK` |
| Unit tests | included in smoke | 40+ tests OK |
| CLI integrity | `python3 scripts/orchestra.py check` | `CHECK OK — Orchestra 0.3.2` |
| Frameworks | `python3 scripts/orchestra.py list` | 11 keys |
| Path jail (install) | `bash install.sh --dry-run --target /etc/orchestra` | non-zero exit |
| Semver | `python3 scripts/bump_version.py check` | parity OK |
| CI | `.github/workflows/ci.yml` | `version-parity` + `path-jail` + `smoke` (3.11/3.12) → `ci-ok` |
| Release | `.github/workflows/release.yml` | Tag `v*` → Release (tag must match VERSION) |
| Analyze fixture | `python3 scripts/orchestra.py analyze --path tests/fixtures/mini_pkg --out /tmp/orch-an` | `analysis.json` written |
| Optimize plan | `python3 scripts/orchestra.py optimize --from /tmp/orch-an/analysis.json --out /tmp/orch-plan` | plan written, no tree writes |

## Engineering surface (done on `main`)

- [x] Canonical loci: `schemas/frameworks.v1.json`
- [x] CLI: `check` / `list` / `structure` / `project` / `diagram`
- [x] CLI: `analyze` + `optimize` plan + gated apply
- [x] Auto diagram HTML/JSON/Mermaid on `--out`
- [x] Atomic installer with path jail
- [x] CI + semver tooling
- [x] Automated GitHub Release on `v*` tag push
- [x] Apache-2.0 + security docs

## Operator gates (publish)

- [ ] `bash scripts/release_preflight.sh` green on your machine
- [ ] Host install: `bash install.sh --dry-run && bash install.sh` then `check`
- [ ] Tag: `bash scripts/publish.sh` then `git push origin v0.3.2`
- [ ] Confirm Actions **release** workflow green (creates GitHub Release)
- [ ] Optional: branch protection requiring **`ci-ok`** (`docs/CI.md`)
- [ ] Optional: registry submit (`docs/COMMUNITY.md`)

## Explicitly deferred past 0.3.2

See `docs/ROADMAP.md`.
