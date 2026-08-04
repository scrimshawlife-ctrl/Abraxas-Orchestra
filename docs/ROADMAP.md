# Roadmap

## Active implementation plan

Repo **analyze → map → optimize** (Cursor-ready): [`ANALYZE_OPTIMIZE_PLAN.md`](ANALYZE_OPTIMIZE_PLAN.md).

---

## Done (0.1.x surface)

- Eleven-framework corpus + `schemas/frameworks.v1.json`
- CLI: `check` | `list` | `structure` | `project` | `diagram`
- Auto diagram on `structure`/`project --out` (HTML + JSON + Mermaid)
- Atomic installer with path jail
- Apache-2.0 public packaging + security audit docs
- Runnable examples (signal-forager, enochian-chaos)

## Shipped in 0.2.0

| Phase | Command | Scope |
|-------|---------|-------|
| A | `analyze` | Read-only repo graph + optional framework map |
| B | `optimize` | Plan only from analysis artifact |

## Next

| Phase | Command | Scope |
|-------|---------|-------|
| C | `optimize --apply --confirm` | Gated mutation + backup → `0.3.0` |

## Deferred

- Multi-language analyze beyond Python
- Network install / remote repo fetch
- pytest coverage gates as hard CI requirement
- Ritual/network runtime systems
- Dedicated OpenClaw fork branch
