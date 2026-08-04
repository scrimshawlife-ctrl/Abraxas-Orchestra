# Numogram Correspondence

Eighth framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide zone separation, syzygetic polarity, time-circuit processes, and provenance annotation. They are not runtime rules.

The Numogram (CCRU / Hyperstition tradition) is a decimal diagram of zones, syzygies, gates, and time-circuits. For software architecture it supplies a compact, non-hierarchical yet highly structured map of polar pairs, directed currents, and cyclic process.

## Ten Zones → Domain / State Classes

| Zone | Traditional / hyperstitional force              | Architectural role                                      | Typical modules / packages                          |
|------|-------------------------------------------------|---------------------------------------------------------|-----------------------------------------------------|
| 0    | Void, intensive continuum, undivided            | Undifferentiated substrate, pure potential, null base   | `void/`, `potential/`, `null_base/`                 |
| 1    | Unity, initiation, first difference             | Initiation, singular entry, first differentiation       | `init/`, `entry/`, `first_diff/`                    |
| 2    | Duality, coupling, binary tension               | Pairing, binary tension, dual systems                   | `dual/`, `pair/`, `binary_tension/`                 |
| 3    | Triplicity, synthesis of difference             | Triadic synthesis, mediation, three-body resolution     | `triad/`, `mediate/`, `synthesis_3/`                |
| 4    | Quaternity, stability, structured order         | Stable structure, ordered foundation, fourfold          | `structure/`, `stable_order/`, `quaternity/`        |
| 5    | Threshold, tipping, intensive peak              | Threshold, tipping point, intensive maximum             | `threshold/`, `tipping/`, `intensive/`              |
| 6    | Resonance, feedback, doubled triad              | Feedback, resonance, amplified mediation                | `feedback/`, `resonance/`, `amplify/`               |
| 7    | Complication, excess, overload                  | Excess, complication, overload regimes                  | `excess/`, `complicate/`, `overload/`               |
| 8    | Consolidation, doubled quaternity               | Consolidation, dense structure, doubled order           | `consolidate/`, `dense_order/`                      |
| 9    | Completion, return, intensive continuum again   | Completion, return to continuum, final intensity        | `completion/`, `return/`, `final_intensity/`        |

## Syzygies → Balanced Polar Pairs

Syzygies are the five zone-pairs that sum to 9. They form the primary polarities of the diagram.

| Syzygy   | Zones | Traditional force                          | Architectural polarity role                                      |
|----------|-------|--------------------------------------------|------------------------------------------------------------------|
| 0 ↔ 9    | 0 / 9 | Void ↔ Completion                          | Potential ↔ Final intensity; open continuum ↔ closed return      |
| 1 ↔ 8    | 1 / 8 | Initiation ↔ Consolidation                 | Singular entry ↔ dense consolidation                             |
| 2 ↔ 7    | 2 / 7 | Duality ↔ Excess                           | Binary tension ↔ overload / complication                         |
| 3 ↔ 6    | 3 / 6 | Triad ↔ Resonance                          | Mediation ↔ amplified feedback                                   |
| 4 ↔ 5    | 4 / 5 | Structure ↔ Threshold                       | Stable order ↔ tipping / intensive peak                          |

## Time-Circuit → Directed Process Cycle

```
1 (init) → 2 (dual tension) → 3 (mediate) → 4 (structure)
    ↑                                           ↓
9 (return) ← 8 (consolidate) ← 7 (excess) ← 6 (feedback) ← 5 (threshold)
```

Use the time-circuit when a system needs an explicit cyclic regime rather than a linear alchemical stage sequence.

## Gates → Explicit Interfaces / Currents

Gates become explicit interface modules between polar or sequential domains. A gate should declare both its source zone and destination zone.

## Dual-Naming Pattern

```
# mechanical: tipping_point
# symbolic:   zone_5_threshold  (Numogram — Zone 5)
```

## Practical Projection Notes

- The syzygies are the highest-leverage architectural extract.
- Zones 0 and 9 form a continuum pair useful for open potential ↔ final intensity.
- Numogram structure is non-hierarchical; it complements Tree of Life or Solomonic rank ladders.

Load this file when Numogram zones, syzygies, time-circuits, or gates are selected as primary or secondary framework.

## CLI default loci (mechanical → symbolic)

| Mechanical | Symbolic | Note |
|------------|----------|------|
| `potential` | `zone_0` | Void / pure potential |
| `init` | `zone_1` | First differentiation |
| `structure` | `zone_4` | Stable order |
| `threshold` | `zone_5` | Tipping / intensive peak |
| `feedback` | `zone_6` | Resonance / amplify |
| `completion` | `zone_9` | Return / final intensity |

Core collapse for `do project`: **`init`, `threshold`, `completion`**.

Canonical machine table: `schemas/frameworks.v1.json`.
