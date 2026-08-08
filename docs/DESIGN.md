# Abraxas Orchestra — Design

**Status**: Executable skill surface  
**Version target**: 0.8.0  
**Hosts**: Hermes, OpenClaw  
**Repository**: https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra

## Intent

Structure software architecture using traditional correspondence systems as hierarchical maps. Emit dual-named modules (mechanical primary, symbolic secondary) with recoverable provenance. Fail closed on weak mappings. Preserve human sovereignty over forced correspondences. Analyze local trees (Python AST; other languages via import-surface token parsers) and emit optimize plans without silent mutation. Guided **wizard** plans resolve argv for Hermes Desktop (chat → `--answers`) without freestyle flags.

## Core contracts

1. **Dual naming** — Every structural unit carries a mechanical identifier and an optional symbolic locus.
2. **Provenance** — Correspondence tables declare strength (`STRONG` / `ADEQUATE` / `WEAK` / `FORCED`) and notes.
3. **Pragmatic projection** — Oversized or forced maps collapse under `project` with an explicit projection note.
4. **Open corpus** — Framework tables expand without breaking the CLI contract.
5. **Agent posture** — Implementation rules live in `references/agent-posture.md` (smallest working layer, no invented loci).
6. **Observed first** — `analyze` records OBSERVED import structure; mappings never invent loci outside `schemas/frameworks.v1.json`.
7. **Human sovereignty** — Optimize mutates the tree only with `--apply --confirm`; dry-run is the default apply path.
8. **Guided path** — `wizard` is print-only by default; Desktop agents collect answers in chat and pass `--answers` (no interactive stdin); `confirm_apply` only when the operator approved gated renames.

## Executable surface (v0.8.0)

CLI entry: `python3 scripts/orchestra.py` — commands registered on `CommandRouter` (`scripts/orchestra_router.py`): **meta** (check, list, wizard), **emit** (structure, project, diagram), **repo** (analyze, optimize). Legacy `do <cmd>` prefix still accepted.

**Hermes / OpenClaw:** the same groups are the agent routing contract in `SKILL.md` and `references/agent-posture.md`. Agents pick a group first, then a command — not freehand architecture. When unsure, prefer **meta** `wizard` (Desktop: chat collect → `--answers` → print-only, then `--run` on approval).

| Command | Role |
|---------|------|
| `check` | Integrity: frameworks load, schema validate, skill root |
| `list` | List frameworks |
| `wizard` | Guided plan from `--answers` / `--preset`; print-only default; `--run` dispatches in-process |
| `structure` | Emit dual-named skeleton + correspondence table; auto diagram on `--out` |
| `project` | Collapse oversized / forced maps before emit |
| `diagram` | Graph-only HTML / JSON / Mermaid emission |
| `analyze` | Read-only OBSERVED import graph (`--lang` python AST; js/ts/go/rust/ruby AST-grade token parsers; `auto`); optional `-f` map |
| `optimize` | Plan only by default from `analysis.json` |
| `optimize --apply` | Dry-run of `safe_apply` mechanical moves |
| `optimize --apply --confirm` | Gated writes after backup (rename / promote / flatten); optional `--steps` / `--actions` / `--refresh` |

Also:

- Schema validation inside `check`
- Atomic installer (`install.sh`) with dry-run, path jail, rollback
- Smoke script + stdlib unit tests + CI
- Semver parity: `scripts/bump_version.py` + `docs/SEMVER.md`

## Framework data source

Canonical loci live in `schemas/frameworks.v1.json`. The CLI loads this file at startup via `_load_frameworks()`. Markdown under `references/` is progressive-disclosure documentation and must stay aligned with the JSON when frameworks change.

## Related docs

- [`RELEASE_NOTES.md`](RELEASE_NOTES.md)
- [`DEPLOY.md`](DEPLOY.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`SECURITY.md`](SECURITY.md) — live threat model and write surfaces
- [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md) — audit history + 0.4.0 addendum
- [`ANALYZE_OPTIMIZE_PLAN.md`](ANALYZE_OPTIMIZE_PLAN.md) — analyze → optimize design (shipped)
- [`CHANGELOG.md`](../CHANGELOG.md)
