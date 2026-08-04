# Tree of Life Correspondence Tables

Primary hierarchical framework for Abraxas Orchestra v0.1.

These mappings are design references. They guide skeleton generation and provenance annotation. They are not runtime rules.

## Four Worlds → Abstraction Strata

| World       | Traditional role                  | Software mapping                                      |
|-------------|-----------------------------------|-------------------------------------------------------|
| Atziluth    | Emanation / pure archetypes       | Intent & domain language                              |
| Briah       | Creation / intellectual form      | Architecture & schemas                                |
| Yetzirah    | Formation / subtle structure      | Concrete modules & algorithms                         |
| Assiah      | Action / material manifestation   | Runtime, side-effects, persistence, deployment        |

Direction of emanation is downward (Atziluth → Assiah). Upward leakage is restricted and must be explicit.

## Sephirot → Architectural Roles

| Sephira     | Number | Architectural role                                      | Typical modules |
|-------------|--------|---------------------------------------------------------|-----------------|
| Kether      | 1      | System intent, entry contract                           | `intent/` |
| Chokmah     | 2      | Raw intake, generative force                            | `intake/` |
| Binah       | 3      | Constraint, schema enforcement                          | `constraint/` |
| Chesed      | 4      | Generative expansion                                    | `expand/` |
| Geburah     | 5      | Adversarial filtering, severity                         | `adversarial/` |
| Tiphareth   | 6      | Central synthesis, scoring                              | `synthesis/` |
| Netzach     | 7      | Pattern persistence                                     | `persist/` |
| Hod         | 8      | Analytical decomposition                                | `analyze/` |
| Yesod       | 9      | Data substrate                                          | `store/` |
| Malkuth     | 10     | Concrete outputs, human surface                         | `output/` |

## Practical Projection Notes

- Not every system needs all ten Sephirot. Collapse unused loci and record the collapse.
- Tiphareth is almost always present as the central synthesis / scoring point.
- The Chesed–Geburah polarity is especially useful for generative + adversarial pipelines.

Load this file when Tree of Life is selected as primary or secondary framework.

## Four Worlds (stacking)

| World | Focus | Typical software layer |
|-------|-------|------------------------|
| Atziluth | Archetypal will | Intent contracts, policy roots |
| Briah | Creation / form | Schemas, types, interfaces |
| Yetzirah | Formation | Services, pipelines, agents |
| Assiah | Action | Runtime, I/O, side effects |

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

## Related

- Pipeline overlay: `references/alchemical-stages.md`
- Projection: `references/pragmatic-projections.md`

Canonical machine table: `schemas/frameworks.v1.json`.
