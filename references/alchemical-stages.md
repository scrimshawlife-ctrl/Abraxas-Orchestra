# Alchemical Stages Correspondence

Secondary overlay framework for Abraxas Orchestra v0.1. Especially useful for pipelines, refinement loops, agent improvement cycles, and data transformation sequences.

## Four Classical Stages

| Stage        | Traditional process                          | Software / pipeline mapping                                      | Typical invariants / failure modes                          |
|--------------|----------------------------------------------|------------------------------------------------------------------|-------------------------------------------------------------|
| Nigredo      | Blackening, putrefaction, chaos, death of form | Raw intake, chaos, unfiltered data, initial decomposition        | High entropy, missing schema, noisy signals, incomplete records |
| Albedo       | Whitening, washing, separation, purification  | Separation, cleaning, schema enforcement, noise removal          | Over-filtering, loss of signal, false purity claims         |
| Citrinitas   | Yellowing, solar illumination, insight        | Insight generation, pattern recognition, illumination, scoring   | Premature insight, hallucinated patterns, weak evidence     |
| Rubedo       | Reddening, coagulation, fixed gold, completion | Final synthesis, production of stable work, coagulation of result | Premature coagulation, unstable final form, missing proof   |

## Direction and Discipline

The stages are sequential by nature. Skipping a stage requires explicit justification and is marked as a forced transition.

Typical healthy flow for a forecasting or signal pipeline:

```
Nigredo (ingest + chaos) 
  → Albedo (clean + constrain) 
    → Citrinitas (illuminate + score) 
      → Rubedo (coagulate + emit)
```

## Dual-Naming Pattern

```
# mechanical: raw_ingest
# symbolic:   nigredo_putrefaction
```

```
# mechanical: purify_and_schema
# symbolic:   albedo_separation
```

```
# mechanical: pattern_illuminate
# symbolic:   citrinitas_insight
```

```
# mechanical: final_coagulate
# symbolic:   rubedo_completion
```

## Practical Notes

- Nigredo modules should tolerate high entropy and avoid early judgment.
- Albedo modules own schema validation and should fail closed on malformed input.
- Citrinitas modules produce scored or illuminated artifacts; they must declare evidence strength.
- Rubedo modules produce the stable external surface; they should be the only place where side-effects that leave the system boundary are allowed (unless the operator explicitly permits otherwise).

When used as a secondary overlay on Tree of Life, map stages onto vertical movement through the Worlds or onto specific Path sequences. Record the dual mapping in the correspondence table.

## Extended dual-naming table (CLI-aligned)

| Mechanical | Symbolic | Stage | Architectural intent |
|------------|----------|-------|----------------------|
| `raw_ingest` | `nigredo` | Nigredo | Chaos intake; untyped feeds; high-entropy buffers |
| `purify` | `albedo` | Albedo | Schema wash; separation; reject malformed |
| `illuminate` | `citrinitas` | Citrinitas | Scoring; pattern recognition; insight artifacts |
| `coagulate` | `rubedo` | Rubedo | Stable emission; sealed report; production form |

## Sub-stage refinements (optional, not in CLI default)

| Sub-label | Parent | Use when |
|-----------|--------|----------|
| `calcination` | Nigredo | Aggressive reduction of source volume |
| `dissolution` | Nigredo | Soften rigid schemas before re-form |
| `separation` | Albedo | Split signal vs noise streams |
| `conjunction` | Albedo→Citrinitas | Recombine cleaned streams |
| `fermentation` | Citrinitas | Iterative improvement / agent loops |
| `distillation` | Citrinitas | Extract high-value scores only |
| `coagulation` | Rubedo | Final fixed product |

Use sub-labels only in docs or secondary overlays. Default CLI emission stays the four classical stages.

## Pipeline mapping (signal forager)

```text
intent     → (contract; often Tree Kether, not alchemical)
intake     → nigredo / raw_ingest
constraint → albedo / purify
synthesis  → citrinitas / illuminate
output     → rubedo / coagulate
```

Adversarial and store stages often stay on the **primary** map (Tree Geburah / Yesod) while alchemy overlays the refine arc.

## Failure modes by stage

| Stage | Software smell | Mitigation |
|-------|----------------|------------|
| Nigredo | Unbounded ingest, no provenance | Hard size/time budgets; SEED labels |
| Albedo | Schema that deletes signal | Keep reject ledger; never silent drop |
| Citrinitas | Score without evidence | Require OBSERVED/INFERRED tags |
| Rubedo | Ship unstable artifact | Gate on tests + operator accept |

## Related

- Primary hierarchical alternative: `references/tree-of-life-mappings.md`
- Projection rules: `references/pragmatic-projections.md`

## CLI default loci (mechanical → symbolic)

| Mechanical | Symbolic | Note |
|------------|----------|------|
| `raw_ingest` | `nigredo` | Chaos / putrefaction intake |
| `purify` | `albedo` | Separation / schema wash |
| `illuminate` | `citrinitas` | Insight / scoring |
| `coagulate` | `rubedo` | Final stable emission |

Core collapse for `do project`: **`raw_ingest`, `illuminate`, `coagulate`**.

Canonical machine table: `schemas/frameworks.v1.json`.
