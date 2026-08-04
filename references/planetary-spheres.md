# Planetary & Elemental Spheres Correspondence

Fourth framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide domain separation, layer ownership, and provenance annotation. They are not runtime rules.

Classical Western tradition assigns distinct forces to the seven planetary spheres and the four (or five) elements. In software architecture these become clean domain boundaries and ownership rules.

## Seven Planetary Spheres → Domain Ownership

| Sphere     | Traditional force                          | Architectural domain role                                      | Typical modules / packages                          |
|------------|--------------------------------------------|----------------------------------------------------------------|-----------------------------------------------------|
| Saturn     | Boundary, time, limitation, structure, weight | Hard boundaries, persistence, schema rigidity, long-term constraint | `boundary/`, `persist/`, `schema/`, `constraint/`   |
| Jupiter    | Expansion, law, abundance, higher order    | Expansion policy, governance law, growth rules, higher contracts | `expand/`, `governance/`, `policy/`, `law/`         |
| Mars       | Force, conflict, separation, defense       | Adversarial layers, severity, stress testing, reactive defense  | `adversarial/`, `severity/`, `stress/`, `defense/`  |
| Sun        | Center, vitality, clarity, sovereignty     | Central synthesis, core judgment, vital scoring, sovereign will | `core/`, `synthesis/`, `judgment/`, `brier/`        |
| Venus      | Attraction, harmony, value, relation       | Relation modeling, value exchange, harmony states, affinity     | `relation/`, `value/`, `harmony/`, `affinity/`      |
| Mercury    | Communication, translation, speed, intellect | Signal transport, translation layers, messaging, intellect      | `comms/`, `translate/`, `signal/`, `message/`       |
| Moon       | Reflection, cycle, memory, flux            | Memory substrate, cyclical state, reflection, flux handling     | `memory/`, `cycle/`, `reflect/`, `flux/`            |

## Four (Five) Elements → Layer Character

| Element   | Traditional quality                        | Architectural character                                      | Typical use                                           |
|-----------|--------------------------------------------|--------------------------------------------------------------|-------------------------------------------------------|
| Fire      | Active, transformative, ascending          | Transformation pipelines, generative force, ignition         | Generative modules, transformation stages, ignition   |
| Air       | Mobile, intellectual, communicative        | Communication, analysis, translation, intellect              | Messaging, analysis, translation layers               |
| Water     | Flowing, receptive, emotional / memory     | Flow, memory, intuition streams, adaptive state              | Memory, flow control, adaptive / reflective layers    |
| Earth     | Dense, stable, material, containing        | Persistence, storage, material outputs, containment          | Stores, databases, final outputs, containment         |
| (Aether / Spirit) | Unifying, subtle, bridging         | Cross-domain coordination, higher synthesis, bridging        | Cross-cutting concerns, orchestration, pure contracts |

## Dual-Naming Pattern

```
# mechanical: hard_boundary
# symbolic:   saturn_boundary  (Planetary — Saturn)
```

## Practical Projection Notes

- Planetary spheres excel at domain separation in multi-concern systems.
- Saturn modules should own long-lived constraints and persistence; they fail closed by nature.
- The Sun domain is the natural home for Brier scoring and central judgment.

Load this file when Planetary or Elemental spheres are selected as primary or secondary framework.

## CLI default loci (mechanical → symbolic)

| Mechanical | Symbolic | Domain emphasis |
|------------|----------|-----------------|
| boundary | saturn | Limits, retention, timeboxes |
| governance | jupiter | Policy, expansion rules |
| adversarial | mars | Conflict, severity, stress |
| core | sun | Sovereignty, synthesis center |
| relation | venus | Value, preference, affinity |
| comms | mercury | Translation, messaging, APIs |
| memory | moon | Flux, cache, short-term state |

Core collapse: **boundary, core, comms**.

## Related

- Authority ranks: `references/solomonic.md`
- Projection: `references/pragmatic-projections.md`

Canonical machine table: `schemas/frameworks.v1.json`.
