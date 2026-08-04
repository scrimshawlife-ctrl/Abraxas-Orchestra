# Agent posture — code implementation under Orchestra

When implementing code structured by this skill:

## Naming

- Mechanical names are the public API and filesystem names.
- Symbolic names live in docstrings, comments, and correspondence tables — not as sole public identifiers unless the operator requested that.

## Fail-closed

- Do not invent symbolic loci absent from `schemas/frameworks.v1.json` / `references/`.
- Prefer `NOT_COMPUTABLE` or explicit `FORCED` over decorative false precision.

## Provenance

- Tag OBSERVED / INFERRED / SPECULATIVE when scoring or promoting structure into larger Abraxas systems.
- No silent collapse of oversized maps — use `project` for pragmatic projection.

## Layered growth

```text
agent_posture: layered-growth | simple-current | no-stopgap | deps-first
```

Do not invent a symbolic locus in Tree of Life / Enochian / etc. for these rules.

Framework loci for structure emission: `schemas/frameworks.v1.json` (do not invent symbolic names absent from that table).

## Diagrammatic emission (mandatory when mapping structure)

When emitting dual-named skeletons or when a Mermaid/architecture diagram would help:

- Use `structure`/`project --out` or `diagram` — never freehand a graph that invents loci.
- Consume `architecture.mmd` for Mermaid embeds; `architecture.json` for agent hops.
- HTML is for human review; JSON is the source of truth for nodes/edges/flows.

If you would write a Mermaid block for Orchestra-mapped code, emit via the CLI first and embed `architecture.mmd`.
