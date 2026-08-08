# Agent posture — code implementation under Orchestra

Hermes/OpenClaw agents using this skill must follow the same **command router** as the CLI:
**meta** · **emit** · **repo** (`scripts/orchestra_router.py` / `SKILL.md`).

## Route first

| User intent | Group | Default command |
|-------------|-------|-----------------|
| Is the skill healthy? What maps exist? | **meta** | `check` / `list` |
| Unsure which path / flags; Desktop chat collect | **meta** | `wizard` |
| New dual-named layout or diagram from a framework | **emit** | `structure` or `diagram` |
| Oversized map needs collapse | **emit** | `project` |
| Observe / map / refactor an existing tree | **repo** | `analyze` then `optimize` |

Do not freestyle architecture Mermaid or invent loci outside the framework tables.
Prefer **meta** `wizard` (chat → `--answers` → print-only, then `--run` on approval) over freestyle argv when unsure.

## Naming

- Mechanical names are the public API and filesystem names.
- Symbolic names live in docstrings, comments, and correspondence tables — not as sole public identifiers unless the operator requested that.

## Fail-closed

- Do not invent symbolic loci absent from `schemas/frameworks.v1.json` / `references/`.
- Prefer `NOT_COMPUTABLE` or explicit `FORCED` over decorative false precision.

## Provenance

- Tag OBSERVED / INFERRED / SPECULATIVE when scoring or promoting structure into larger Abraxas systems.
- No silent collapse of oversized maps — use **emit** `project` for pragmatic projection.

## Optimize by the map (not rename-only)

Scaffold folders are not enough. After **emit** `structure` / `project`, implement domain logic
so each package only does the work of its locus:

- **intent / kether** — contracts and limits; no I/O  
- **intake / chokmah** — raw pull; no scoring  
- **analyze / hod** — score/filter; no persist/emit  
- **store / yesod** — substrate; no new scoring rules  
- **output / malkuth** — final manifestation  

Cross-stage calls should follow the map’s one-way edges (see
`examples/python-tree-of-life-pipeline/`). Structure is the control plane that
*optimizes* the code, not a label glued onto a tangle.

## Layered growth

```text
agent_posture: layered-growth | simple-current | no-stopgap | deps-first
```

Do not invent a symbolic locus in Tree of Life / Enochian / etc. for these rules.

Framework loci for structure emission: `schemas/frameworks.v1.json` (do not invent symbolic names absent from that table).

## Diagrammatic emission (mandatory when mapping structure)

When emitting dual-named skeletons or when a Mermaid/architecture diagram would help:

- Use **emit** `structure` / `project --out` or `diagram` — never freehand a graph that invents loci.
- Consume `architecture.mmd` for Mermaid embeds; `architecture.json` for agent hops.
- HTML is for human review; JSON is the source of truth for nodes/edges/flows.

If you would write a Mermaid block for Orchestra-mapped code, emit via the CLI first and embed `architecture.mmd`.

## Repo path discipline

- **repo** `analyze` before any rename discussion on an existing tree.
- **repo** `optimize` is plan-only unless the operator confirms `--apply --confirm`.
- Never apply FORCED/WEAK maps silently.
