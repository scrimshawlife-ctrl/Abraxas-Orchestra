# Sacred Geometry & Recursive Proportion

Ninth framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide nesting depth, modular proportion, symmetry constraints, and provenance annotation. They are not runtime rules.

Sacred geometry supplies ratio, symmetry, and recursive self-similarity as structural disciplines. For software architecture the useful extract is controlled nesting, golden-ratio depth limits, Platonic adjacency, and fractal self-similarity between high-level and low-level forms.

## Core Ratios → Structural Discipline

| Ratio / constant      | Traditional force                          | Architectural application                                      |
|-----------------------|--------------------------------------------|----------------------------------------------------------------|
| Golden ratio (φ ≈ 1.618) | Organic growth, balanced proportion     | Nesting depth limits, module size ratios, split proportions    |
| Square root of 2      | Diagonal, expansion from unity             | Orthogonal expansion, dual-axis growth                         |
| Square root of 3      | Vesica height, generative interval         | Triadic interval, generative spacing                           |
| Square root of 5      | Related to φ, pentagonal                   | Pentagonal / five-fold structures                              |
| Pi (π)                | Circle, continuum, return                  | Cyclic boundaries, continuous regimes                          |

Golden-ratio nesting is the highest-leverage rule: a module should not contain more than φ-related levels of subordinate structure without an explicit pragmatic projection.

## Platonic Solids → Adjacency & Coordination Graphs

| Solid          | Faces / vertices / edges | Traditional element          | Architectural graph role                                      |
|----------------|--------------------------|------------------------------|---------------------------------------------------------------|
| Tetrahedron    | 4 / 4 / 6                | Fire                         | Minimal complete graph, tight coordination, four-node core    |
| Cube           | 6 / 8 / 12               | Earth                        | Orthogonal stability, six-face domain separation              |
| Octahedron     | 8 / 6 / 12               | Air                          | Dual to cube, flexible coordination, dual polarity            |
| Dodecahedron   | 12 / 20 / 30             | Aether / cosmos              | High-connectivity, twelve-fold domain or month-like cycles    |
| Icosahedron    | 20 / 12 / 30             | Water                        | Dense local connectivity, fluid / adaptive service mesh       |

Use Platonic adjacency when service or module graphs need explicit symmetry and bounded degree. Prefer tetrahedron or cube for small systems; reserve dodecahedron / icosahedron for high-connectivity meshes.

## Recursive Self-Similarity → Fractal Module Discipline

A structure is recursively self-similar when the organization of a high-level package is mirrored (at reduced scale) in its sub-packages.

| Pattern                    | Architectural expression                                      |
|----------------------------|---------------------------------------------------------------|
| Same layering at every depth | Every major package repeats the same internal stage or Sephirotic pattern |
| Same polarity at every depth | Every level carries a Chesed–Geburah or syzygetic pair         |
| Same interface style at every depth | Adapters / gates / Paths appear at consistent relative positions |
| Bounded depth by φ         | Nesting beyond a golden-ratio-derived limit requires explicit justification |

Recursive self-similarity is especially powerful when combined with Tree of Life (Four Worlds repeated inside modules) or Numogram (syzygies repeated at multiple scales).

## Vesica Piscis & Generative Intervals

The vesica (intersection of two circles) is the traditional generative interval. In architecture it maps to:

- The shared interface zone between two domains
- The “overlap” package that both sides may depend on without ownership leakage
- The minimal common contract between polar modules

## Dual-Naming Pattern

```
# mechanical: nested_core
# symbolic:   golden_depth_limit  (Sacred Geometry — φ nesting)
```

```
# mechanical: coordination_graph
# symbolic:   tetrahedral_core  (Sacred Geometry — Tetrahedron)
```

```
# mechanical: shared_contract_zone
# symbolic:   vesica_interface  (Sacred Geometry — Vesica Piscis)
```

```
# mechanical: fractal_layer
# symbolic:   self_similar_repeat  (Sacred Geometry — recursive proportion)
```

## Practical Projection Notes

- Golden-ratio depth limits are the simplest and highest-value rule. A module that nests more than three or four levels should be examined for pragmatic collapse.
- Platonic solids are useful for service-graph design, not for directory trees. Prefer them when modeling inter-service adjacency and degree constraints.
- Recursive self-similarity pairs cleanly with Tree of Life (repeat the Four Worlds or a reduced Sephirotic pattern at every major package) and with Numogram (repeat syzygies at multiple scales).
- Vesica-style shared contracts prevent ownership leakage between polar domains (e.g., between a Mars adversarial module and a Venus relation module).
- Sacred geometry is a constraint language more than a primary hierarchy. It is usually applied as an overlay on Tree of Life, Numogram, or planetary domains.
- When pure geometric discipline would produce awkward module counts or forced symmetries, record a pragmatic projection and collapse to the nearest practical structure.

Load this file when sacred geometry, recursive proportion, golden-ratio limits, Platonic adjacency, or fractal self-similarity are selected as primary or secondary framework.
