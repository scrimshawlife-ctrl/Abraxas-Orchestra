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
