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

The Sun sits at the center as the natural Tiphareth / synthesis locus. Saturn and Jupiter form the outer structural polarities (limitation ↔ expansion). Mars and Venus form the dynamic polarities (separation ↔ attraction). Mercury and Moon handle movement and reflection.

## Four (Five) Elements → Layer Character

| Element   | Traditional quality                        | Architectural character                                      | Typical use                                           |
|-----------|--------------------------------------------|--------------------------------------------------------------|-------------------------------------------------------|
| Fire      | Active, transformative, ascending          | Transformation pipelines, generative force, ignition         | Generative modules, transformation stages, ignition   |
| Air       | Mobile, intellectual, communicative        | Communication, analysis, translation, intellect              | Messaging, analysis, translation layers               |
| Water     | Flowing, receptive, emotional / memory     | Flow, memory, intuition streams, adaptive state              | Memory, flow control, adaptive / reflective layers    |
| Earth     | Dense, stable, material, containing        | Persistence, storage, material outputs, containment          | Stores, databases, final outputs, containment         |
| (Aether / Spirit) | Unifying, subtle, bridging         | Cross-domain coordination, higher synthesis, bridging        | Cross-cutting concerns, orchestration, pure contracts |

Elemental character can be applied as a secondary overlay on planetary domains or on Tree-of-Life / aettir structures.

## Dual-Naming Pattern

```
# mechanical: hard_boundary
# symbolic:   saturn_boundary  (Planetary — Saturn)
```

```
# mechanical: signal_transport
# symbolic:   mercury_comms  (Planetary — Mercury)
```

```
# mechanical: central_synthesis
# symbolic:   sun_core  (Planetary — Sun)
```

```
# mechanical: adversarial_filter
# symbolic:   mars_severity  (Planetary — Mars)
```

## Practical Projection Notes

- Planetary spheres excel at domain separation in multi-concern systems. Assigning ownership by sphere reduces cross-domain leakage.
- Saturn modules should own long-lived constraints and persistence; they fail closed by nature.
- Mercury modules own all translation and message movement; they should remain thin and fast.
- The Sun domain is the natural home for Brier scoring, central judgment, and sovereign decision surfaces.
- Mars domains pair cleanly with Hagal’s Aett and Geburah for adversarial work.
- Elemental overlays are lightweight: a module can be “Martial Fire” or “Mercurial Air” without requiring a full second table.
- When combining with Tree of Life, planetary spheres often map onto specific Sephirot or Paths (Saturn near Binah / Geburah, Sun at Tiphareth, Moon near Yesod, etc.). Record the dual mapping in the correspondence table.

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
