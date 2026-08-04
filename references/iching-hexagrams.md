# I Ching Hexagrams — Curated Set for State Machines

Fifth framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide discrete state naming, transition rules, and provenance annotation. They are not runtime rules.

The full I Ching contains 64 hexagrams. For architectural use a curated high-signal subset is more practical.

## Curated Hexagram Set (selected)

| Hex # | Name (English) | Architectural state role | Suggested pairing |
|-------|----------------|--------------------------|-------------------|
| 1 | The Creative | Pure initiation | `init` / `qian_creative` |
| 5 | Waiting | Deliberate accumulation | `wait` / `xu_waiting` |
| 6 | Conflict | Open polarity | `conflict` / `song_conflict` |
| 11 | Peace | Balanced flow | `harmony` / `tai_peace` |
| 24 | Return | Cyclic renewal | `return` / `fu_return` |
| 49 | Revolution | Regime change | `revolution` / `ge_revolution` |
| 63 | After Completion | Ordered finish | `completion` / `jiji_completion` |

## Dual-Naming Pattern

```
# mechanical: deliberate_wait
# symbolic:   xu_waiting  (I Ching — 5 Waiting)
```

## Practical Projection Notes

- Use the curated set as named states in a state machine or regime tracker.
- The set is deliberately incomplete; expand when a real system needs a missing regime (mark SPECULATIVE until tabled).

Load this file when I Ching hexagrams are selected as primary or secondary framework for discrete state work.

## CLI default loci (mechanical → symbolic)

| Mechanical | Symbolic | Regime |
|------------|----------|--------|
| init | qian_creative | Pure start |
| wait | xu_waiting | Accumulate |
| conflict | song_conflict | Open polarity |
| harmony | tai_peace | Balanced flow |
| return | fu_return | Cyclic renewal |
| revolution | ge_revolution | Regime change |
| completion | jiji_completion | Ordered finish |

Core collapse: **init, harmony, completion**.

## Related

- Projection: `references/pragmatic-projections.md`

Canonical machine table: `schemas/frameworks.v1.json`.
