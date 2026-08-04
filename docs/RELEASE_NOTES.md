# Release notes

Narrative notes for operators and agents. Machine changelog: [`CHANGELOG.md`](../CHANGELOG.md).

## 0.3.1 — 2026-08-04

Apply hardening + import-graph refresh.

- `--refresh` with `--apply --confirm` re-runs `analyze` and writes beside the backup
- Destination collisions demoted; vacate-first rename ordering
- Smoke covers `scripts/` analyze + optimize dry-run

## 0.3.0 — 2026-08-04

**Optimize apply (Phase C)** — gated mutation.

- `optimize --apply` = dry-run of `safe_apply` mechanical renames
- `optimize --apply --confirm` writes after backup (`--backup-dir`, default under analyzed root)
- FORCED mappings refuse apply; boundary/extract steps stay advisory
- Restore notes: `RESTORE.md` in the backup directory

## 0.2.0 — 2026-08-04

Repo **analyze → map → optimize (plan)**.

- `analyze --path DIR` observes a local Python import graph (stdlib `ast`), optional `-f` mapping onto `frameworks.v1.json`, diagram bundle on `--out`.
- `optimize --from analysis.json` emits `optimize-plan.json` + `OPTIMIZE.md` without modifying the analyzed tree.

Plan: [`ANALYZE_OPTIMIZE_PLAN.md`](ANALYZE_OPTIMIZE_PLAN.md).

## 0.1.6 — 2026-08-04

Automatic diagrammatic emission.

`structure` / `project --out DIR` always writes:

- `architecture.html`
- `architecture.json`
- `architecture.mmd` (Mermaid)

Agents: when Mermaid or a code diagram is needed for Orchestra-mapped work, emit via CLI — do not invent separate graphs.

## 0.1.5 — 2026-08-04

Diagrammatic emission via `diagram` / `diagrammit`.

## 0.1.4 — 2026-08-04

Simplified command structure.

## 0.1.3 — 2026-08-04

Public debut packaging + security hardening.

## 0.1.0 — 2026-08-04

First design surface.
