# Pragmatic Projections

When a pure symbolic map would harm maintainability, type safety, testability, or cognitive load, Orchestra **projects** rather than forces.

Projections are always recorded. Never silent.

## When to project

| Trigger | Typical action |
|---------|----------------|
| Map has more loci than the concern set needs | Collapse to framework **core set** |
| Concern has no clean locus | Mark `FORCED` or drop under `do project` |
| Two frameworks compete for the same concern | Pick primary; optional Chaos overlay; do not dual-primary |
| Nested maps exceed review capacity | Flatten to ≤6 mechanical modules |
| Symbolic name would become public API | Keep mechanical primary; symbolic in docs only |

## `do project` semantics (CLI)

1. Drop loci whose notes start with `FORCED`
2. If remaining count > 6 and the framework defines `core_collapse`, keep only those mechanical names
3. Write the projection note into `correspondence-table.json` → `pragmatic_projection`
4. Status stays `CLEAN` if only clean loci remain after drop; otherwise prior forced status may already have failed `do structure`

## Core collapse sets (aligned with CLI)

| Framework | Core mechanical names |
|-----------|------------------------|
| tree-of-life | intent, synthesis, output |
| alchemical-stages | raw_ingest, illuminate, coagulate |
| elder-futhark | signal_intake, just_judgment, human_surface |
| planetary-spheres | boundary, core, comms |
| iching-hexagrams | init, harmony, completion |
| solomonic | sovereign, executive, task_agent |
| peircean-signs | trace, convention, inference |
| numogram | init, threshold, completion |
| sacred-geometry | nested_core, shared_zone |
| enochian | edge_intake, domain_entry, sovereign_intent |
| chaos-magic | paradigm_switch, intent_token, outcome_gate |

## Dual-naming under projection

Projection **must not** invent new symbolic loci. It only selects or drops existing rows.

```text
# BEFORE (oversized Tree map)
intent, intake, constraint, expand, adversarial, synthesis, persist, analyze, store, output

# AFTER do project (core collapse)
intent / kether
synthesis / tiphareth
output / malkuth
# projection note: Collapsed N non-core loci to framework core set.
```

## Operator sovereignty

- Accept projection when maintainability wins
- Reject and expand core set only by editing `FRAMEWORKS` + this table + schema together
- Never treat projection as auto-canon into Abraxas

## Strength after projection

| Strength | Meaning post-project |
|----------|----------------------|
| STRONG / ADEQUATE | Retained clean locus |
| FORCED | Should have been dropped by `do project`; if still present, operator must review |
| WEAK | Prefer explicit human acceptance before implement |

## Related

- CLI: `scripts/orchestra.py` → `_apply_pragmatic_projection`
- Schema: `schemas/correspondence-table.v1.schema.json` field `pragmatic_projection`
- Agent posture: `references/agent-posture.md` (smallest working layer first)
