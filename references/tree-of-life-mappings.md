# Tree of Life Correspondence Tables

Primary hierarchical framework for Abraxas Orchestra v0.1.

These mappings are design references. They guide skeleton generation and provenance annotation. They are not runtime rules.

## Four Worlds → Abstraction Strata

| World       | Traditional role                  | Software mapping                                      | Typical contents                                      |
|-------------|-----------------------------------|-------------------------------------------------------|-------------------------------------------------------|
| Atziluth    | Emanation / pure archetypes       | Intent & domain language                              | High-level contracts, pure interfaces, intent schemas |
| Briah       | Creation / intellectual form      | Architecture & schemas                                | Type definitions, module contracts, governance schemas|
| Yetzirah    | Formation / subtle structure      | Concrete modules & algorithms                         | Implementations, pure functions, transformation logic |
| Assiah      | Action / material manifestation   | Runtime, side-effects, persistence, deployment        | I/O, databases, network, observability, entrypoints   |

Direction of emanation is downward (Atziluth → Assiah). Upward leakage is restricted and must be explicit.

## Sephirot → Architectural Roles

| Sephira     | Number | Traditional force          | Architectural role                                      | Typical modules / packages                          |
|-------------|--------|----------------------------|---------------------------------------------------------|-----------------------------------------------------|
| Kether      | 1      | Crown / pure will          | System intent, top-level oracle interface, entry contract | `intent/`, `oracle_contract/`                       |
| Chokmah     | 2      | Wisdom / pure force        | Raw intake, generative force, unfiltered signal         | `intake/`, `force/`, `raw_signal/`                    |
| Binah       | 3      | Understanding / form       | Constraint, schema enforcement, boundary definition     | `schema/`, `constraint/`, `form/`                   |
| Chesed      | 4      | Mercy / expansion          | Generative exploration, broadening, permissive growth   | `expand/`, `explore/`, `generative/`                |
| Geburah     | 5      | Severity / strength        | Adversarial filtering, severity, pruning, stress        | `adversarial/`, `filter/`, `severity/`              |
| Tiphareth   | 6      | Beauty / harmony           | Central synthesis, balanced judgment, scoring           | `synthesis/`, `judgment/`, `brier/`, `core/`        |
| Netzach     | 7      | Victory / endurance        | Pattern persistence, long-lived memory, endurance       | `persist/`, `memory/`, `endurance/`                 |
| Hod         | 8      | Splendor / intellect       | Analytical decomposition, communication, intellect      | `analyze/`, `decompose/`, `comms/`                  |
| Yesod       | 9      | Foundation                 | Data substrate, foundation store, intermediate image    | `store/`, `foundation/`, `substrate/`               |
| Malkuth     | 10     | Kingdom / manifestation    | Concrete outputs, reports, side-effects, human surface  | `output/`, `report/`, `runtime/`, `side_effects/`   |

## Paths (selected high-value interfaces)

Paths are explicit dependency or transformation directions. Only the most architecturally useful are listed here for v0.1.

| Path letters | Connects          | Architectural meaning                                      |
|--------------|-------------------|------------------------------------------------------------|
| א (Aleph)    | Kether–Chokmah    | Intent → raw force intake                                  |
| ב (Beth)     | Kether–Binah      | Intent → form / schema constraint                          |
| ג (Gimel)    | Kether–Tiphareth  | Direct will → central synthesis (rare, high-stakes)        |
| ד (Daleth)   | Chokmah–Binah     | Force ↔ Form polarity                                      |
| ה (Heh)      | Chokmah–Tiphareth | Generative force into balanced judgment                    |
| ו (Vav)      | Binah–Tiphareth   | Constrained form into synthesis                            |
| ז (Zayin)    | Binah–Geburah     | Understanding → severity / pruning                         |
| ח (Cheth)    | Binah–Chesed      | Understanding → expansion                                  |
| ט (Teth)     | Chesed–Geburah    | Expansion ↔ Severity polarity (classic balance axis)       |
| י (Yod)      | Chesed–Tiphareth  | Mercy / expansion into synthesis                           |
| כ (Kaph)     | Geburah–Tiphareth | Severity into synthesis                                    |
| ל (Lamed)    | Tiphareth–Netzach | Synthesis → enduring pattern                               |
| מ (Mem)      | Tiphareth–Hod     | Synthesis → analytical intellect                           |
| נ (Nun)      | Netzach–Hod       | Endurance ↔ Analysis polarity                              |
| ס (Samekh)   | Tiphareth–Yesod   | Synthesis → foundation / substrate                         |
| ע (Ayin)     | Netzach–Yesod     | Enduring pattern into foundation                           |
| פ (Peh)      | Hod–Yesod         | Analysis into foundation                                   |
| צ (Tzaddi)   | Netzach–Malkuth   | Enduring pattern into manifestation                        |
| ק (Qoph)     | Yesod–Malkuth     | Foundation → concrete output                               |
| ר (Resh)     | Hod–Malkuth       | Analysis → concrete output                                 |
| ש (Shin)     | Tiphareth–Malkuth | Direct synthesis → manifestation (high-visibility path)    |
| ת (Tav)      | Yesod–Malkuth     | Foundation completion                                      |

In code, Paths become explicit adapter modules, interface packages, or typed transformation functions. Directionality is preserved in import graphs and documentation.

## Practical Projection Notes

- Not every system needs all ten Sephirot. Collapse unused Sephirot into neighboring ones and record the collapse in the correspondence table.
- Tiphareth is almost always present as the central synthesis / scoring / judgment point.
- The Chesed–Geburah polarity is especially useful for generative + adversarial pipelines.
- Four Worlds give a clean vertical stratification even when the full Tree is reduced.

Load this file when Tree of Life is selected as primary or secondary framework.

## Four Worlds (stacking)

Use when a single Sephira set is not enough for multi-layer systems.

| World | Focus | Typical software layer |
|-------|-------|------------------------|
| Atziluth | Archetypal will | Intent contracts, policy roots |
| Briah | Creation / form | Schemas, types, interfaces |
| Yetzirah | Formation | Services, pipelines, agents |
| Assiah | Action | Runtime, I/O, side effects |

Stacking rule: do not put Assiah concerns in Atziluth modules. Paths between worlds are explicit package boundaries.

## CLI default loci (mechanical → symbolic)

| Mechanical | Symbolic |
|------------|----------|
| intent | kether |
| intake | chokmah |
| constraint | binah |
| expand | chesed |
| adversarial | geburah |
| synthesis | tiphareth |
| persist | netzach |
| analyze | hod |
| store | yesod |
| output | malkuth |

Core collapse for `do project`: **intent, synthesis, output**.

## Dual-naming pattern

```text
# mechanical: synthesis
# symbolic:   tiphareth
# locus:      Central judgment / scoring
```

## Related

- Pipeline overlay: `references/alchemical-stages.md`
- Projection: `references/pragmatic-projections.md`
