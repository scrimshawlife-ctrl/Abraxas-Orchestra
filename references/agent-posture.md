# Agent posture — code implementation rules

Non-framework rules for filling Orchestra skeletons. Apply after structure emission, before or while writing production code.

## Principles

1. **Smallest working layer first** — implement the minimal path that satisfies the current concern set.
2. **Mechanical names are public API** — symbolic names stay in docs, comments, and correspondence tables unless the operator requests otherwise.
3. **No invented loci** — if a concern has no clean map, mark `FORCED` and stop; do not fabricate Sephirot, Aethyrs, or runes.
4. **Deps first** — establish types, schemas, and boundaries before generative or scoring logic.
5. **Fail closed** — prefer explicit reject paths over silent drop.
6. **Provenance** — OBSERVED / INFERRED / SPECULATIVE labels on scores and claims.

## Layered growth

```text
agent_posture: layered-growth | simple-current | no-stopgap | deps-first
```

Do not invent a symbolic locus in Tree of Life / Enochian / etc. for these rules.

Framework loci for structure emission: `schemas/frameworks.v1.json` (do not invent symbolic names absent from that table).
