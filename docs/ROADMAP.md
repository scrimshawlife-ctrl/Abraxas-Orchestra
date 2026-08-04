# Roadmap and production readiness

## Done (v0.1.1 → v0.1.2 engineering)

| Item | Notes |
|------|--------|
| 11-framework open corpus | Including Enochian seals + Chaos Magic |
| CLI structure / project / check | Stdlib only |
| Schema validation in `check` | Sample tables per framework |
| Atomic installer | Hermes + OpenClaw `--target` |
| Signal-forager example | Runnable pipeline |
| Enochian + Chaos example | Structure + Mermaid |
| Agent posture | Non-framework build rules |
| Human/agent docs | README, COMMUNITY, SKILL frontmatter |
| **Automated tests** | `tests/test_orchestra.py` (12 tests) |
| **Smoke script** | `scripts/smoke.sh` |
| **CI** | `.github/workflows/ci.yml` |
| **Deploy guide** | `docs/DEPLOY.md` |

## Explicitly deferred

| Item | Reason |
|------|--------|
| OSI relicense | Operator decision (blocks some public hubs) |
| Dedicated `openclaw` git branch | Install path already works via `--target` |
| pytest / coverage gates | Stdlib unittest is enough for v0.1 |
| Runtime ritual / network integrations | Out of skill scope |
| Multi-agent orchestration product | Separate Abraxas systems |
| CLI loci loaded from references | Dual-source drift risk accepted for v0.1 |

## Production readiness bar (skill package)

A release is production-ready for **private Hermes/OpenClaw install** when:

1. `bash scripts/smoke.sh` exits 0  
2. `VERSION` matches manifest + CHANGELOG section  
3. No undeclared network or secrets in CLI path  
4. Fail-closed paths covered by tests (unknown framework, same overlay)  
5. Installer `--dry-run` succeeds  

Public registry listing additionally requires license compatibility (`docs/COMMUNITY.md`).

## Closed in follow-up (post-0.1.2 hygiene)

| Item | Notes |
|------|--------|
| SKILL.md version → 0.1.2 | Frontmatter aligned |
| DESIGN.md version → 0.1.2 | Target strings aligned |
| Enochian-chaos module stubs | Dual-named `__init__.py` regenerated |
| Installer stages `assets/` | Best-effort copy |
| CONTRIBUTING.md | Local smoke + framework checklist |

Still operator-local: **`assets/hero.jpg` binary push**, optional `v0.1.2` tag (see `docs/DEPLOY.md`).

## Closed in depth pass (continue-as-recommended)

| Item | Notes |
|------|--------|
| Pragmatic projections expanded | Core collapse table aligned with CLI |
| Alchemy / Tree / Planetary / I Ching depth | CLI loci tables + failure modes / Four Worlds |
| Example unit tests | signal-forager files, enochian stubs, demo report shape |
| Deploy tag instructions | Optional `v0.1.2` pin |

## Next steps for deployment

Follow **`docs/DEPLOY.md`** in order:

0. Preconditions (Python 3.11+, smoke green)
1. Local validation
2. Choose Hermes vs OpenClaw target
3. Dry-run → install
4. Post-install `check` / smoke on the installed copy
5. Wire host skill discovery and reload session
6. First real structure emission with human review of FORCED maps
7. Upgrade path: pull → smoke → reinstall
8. Optional: relicense / public hub (not required for private deploy)
