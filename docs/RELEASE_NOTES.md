# Release notes

Narrative notes for operators and agents. Machine changelog: [`CHANGELOG.md`](../CHANGELOG.md).

## 0.2.0 — 2026-08-04

Repo **analyze → map → optimize (plan)**.

- `analyze --path DIR` observes a local Python import graph (stdlib `ast`), optional `-f` mapping onto `frameworks.v1.json`, diagram bundle on `--out`.
- `optimize --from analysis.json` emits `optimize-plan.json` + `OPTIMIZE.md` without modifying the analyzed tree.
- Phase C (`optimize --apply`) remains deferred; the flag is refused.

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
