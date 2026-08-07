# Roadmap

## Active implementation plan

Repo **analyze → map → optimize** (shipped): [`ANALYZE_OPTIMIZE_PLAN.md`](ANALYZE_OPTIMIZE_PLAN.md).

Version policy: [`SEMVER.md`](SEMVER.md) · bump tool: `scripts/bump_version.py`.

---

## Done (0.1.x surface)

- Eleven-framework corpus + `schemas/frameworks.v1.json`
- CLI: `check` | `list` | `structure` | `project` | `diagram`
- Auto diagram on `structure`/`project --out` (HTML + JSON + Mermaid)
- Atomic installer with path jail
- Apache-2.0 public packaging + security audit docs
- Runnable examples (signal-forager, enochian-chaos)

## Shipped

| Phase | Version | Command | Scope |
|-------|---------|---------|-------|
| A | 0.2.0 | `analyze` | Read-only repo graph + optional framework map |
| B | 0.2.0 | `optimize` | Plan only from analysis artifact |
| C | 0.3.0 | `optimize --apply --confirm` | Gated mechanical renames + backup |
| C+ | 0.3.1 | `--refresh` + apply hardening | Post-apply re-analyze; collision/vacate ordering |
| CI | 0.3.1 | Actions | version-parity, path-jail, smoke 3.11/3.12, `ci-ok` |
| Semver | 0.3.1+ | `bump_version.py` | Policy + parity tool + CI check |
| C++ | 0.4.0 | promote / flatten / `--steps` / `--actions` | Broader mechanical `safe_apply` |
| Hardening | 0.4.1 | integrity CI + apply split + framework-fit | Anti-truncation floors; enrich/rewrite modules |
| Mapping | 0.4.2 | deeper analyze heuristics | Role synonyms, compounds, docstring signals |
| Soft coverage | 0.4.3 | `coverage-soft` CI job | Import + linkage + in-process report (no floor) |

## Next

- Use `docs/SEMVER.md` + `scripts/bump_version.py` for all releases
- Optional branch protection without admin bypass (`docs/CI.md`)
- Multi-language analyze (see Deferred)
- Broader safe_apply that invents file content (explicit MAJOR / operator request)

## Deferred

- Multi-language analyze beyond Python
- Network install / remote repo fetch
- Coverage **floors** as hard CI requirement (soft report exists since 0.4.3)
- Ritual/network runtime systems
- Dedicated OpenClaw fork branch
