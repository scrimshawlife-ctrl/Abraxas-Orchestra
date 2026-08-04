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
| **Automated tests** | `tests/test_orchestra.py` (14 tests) |
| **Smoke script** | `scripts/smoke.sh` |
| **CI** | `.github/workflows/ci.yml` |
| **Deploy guide** | `docs/DEPLOY.md` |
| **Release notes** | `docs/RELEASE_NOTES.md` |
| **Security notes** | `docs/SECURITY.md` |
| **Canonical loci JSON** | `schemas/frameworks.v1.json` (CLI loads at startup) |
| **Text-safe hero** | `assets/hero.svg` |

## Explicitly deferred

| Item | Reason |
|------|--------|
| OSI relicense | Operator decision (blocks some public hubs) |
| Dedicated `openclaw` git branch | Install path already works via `--target` |
| pytest / coverage gates | Stdlib unittest is enough for v0.1 |
| Runtime ritual / network integrations | Out of skill scope |
| Multi-agent orchestration product | Separate Abraxas systems |

## Production readiness bar (skill package)

A release is production-ready for **private Hermes/OpenClaw install** when:

1. `bash scripts/smoke.sh` exits 0  
2. `VERSION` matches manifest + CHANGELOG section  
3. No undeclared network or secrets in CLI path  
4. Fail-closed paths covered by tests (unknown framework, same overlay)  
5. Installer `--dry-run` succeeds  

Public registry listing additionally requires license compatibility (`docs/COMMUNITY.md`).

## Closed gap pass (docs + loci parity)

| Item | Notes |
|------|--------|
| CLI loads `schemas/frameworks.v1.json` | No embedded FRAMEWORKS dict |
| CLI default loci on framework refs | Aligned with JSON |
| `docs/RELEASE_NOTES.md` | Narrative 0.1.2 notes |
| `docs/SECURITY.md` | Local threat model |

Hero: **`assets/hero.svg`** ships in-repo (text-safe). Optional photographic `hero.jpg` still operator-local. Optional `v0.1.2` tag still operator-local.

## Next steps for deployment

Follow **`docs/DEPLOY.md`** in order.

See also: [`RELEASE_NOTES.md`](RELEASE_NOTES.md) · [`CHANGELOG.md`](../CHANGELOG.md) · [`SECURITY.md`](SECURITY.md).
