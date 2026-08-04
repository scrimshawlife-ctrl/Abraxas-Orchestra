# Enochian Correspondence

Tenth framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide hierarchical depth, elemental domain separation, invocation interfaces, jurisdiction maps, and provenance annotation. They are not runtime rules and do not implement operative magical practice.

## Two streams (read first)

What modern literature calls “Enochian” is not a single fixed doctrine from 1584.

| Stream | Source character | Orchestra default |
|--------|------------------|-------------------|
| **Dee-purist** | Diaries of John Dee & Edward Kelley (c. 1582–1587): Heptarchia, Loagaeth/Gebofal, Aires & 91 Parts of the Earth, Great Table as letter-squares | Use for historical fidelity and non-elemental tablet work |
| **Neo-Enochian** | Golden Dawn *Book H*, elemental Watchtowers, Tablet of Union, Crowley (*Liber Chanokh*, *Vision and the Voice*) | **Default for Orchestra domain separation** |

Dee did **not** assign the four tablets to Air/Fire/Water/Earth in the modern elemental way. That attribution is a later Golden Dawn elaboration. Orchestra still defaults to neo-Enochian elemental Watchtowers because they produce a clean, maintainable four-way domain partition. When Dee-purist fidelity is required, drop elemental labels and treat tablets as directional/letter-square domains only. Record which stream is active in the correspondence table.

Primary historical phases in the Dee material:

1. **Heptarchia** — sevenfold planetary angelic royalty  
2. **Loagaeth / Gebofal + 48 Angelical Keys** — language, tables, Calls  
3. **Aires (Aethyrs) + 91 Parts of the Earth** — depth bands and jurisdiction  
4. **Great Table (Watchtowers)** — four letter-tablets joined by the Black Cross  

---

## Four Watchtowers → Elemental Domain Separation (neo-Enochian default)

Each Watchtower is treated as a complete elemental kingdom with hierarchy of names, seniors, and kerubic forces. In architecture they become four primary domain partitions with strict boundary discipline.

| Watchtower | Element | Traditional force                    | Architectural domain role                                      | Typical modules / packages                    |
|------------|---------|--------------------------------------|----------------------------------------------------------------|-----------------------------------------------|
| East       | Air     | Intellect, communication, mobility   | Analysis, messaging, translation, intellect surfaces           | `air/`, `comms/`, `analyze/`, `translate/`    |
| South      | Fire    | Will, transformation, intensity      | Generative force, transformation pipelines, ignition           | `fire/`, `transform/`, `generate/`, `ignite/` |
| West       | Water   | Emotion, flux, memory, depth         | Flow, memory substrate, adaptive state, reflection             | `water/`, `memory/`, `flow/`, `reflect/`      |
| North      | Earth   | Stability, material, containment     | Persistence, storage, material outputs, hard constraints       | `earth/`, `persist/`, `store/`, `contain/`    |

Cross-Watchtower traffic should pass through explicit gates (Calls or named interfaces). Silent leakage between elemental domains is treated as architectural pollution.

### Authority ladder inside a Watchtower (neo-Enochian)

| Rank | Traditional extract                         | Architectural role                                      |
|------|---------------------------------------------|---------------------------------------------------------|
| Names of God (3) | Horizontal arm of the Great Cross     | Domain-wide root seals                                  |
| Elemental King   | Spiral from tablet center               | Sovereign controller of the domain                      |
| Six Seniors      | Arms of the Great Cross (planetary)     | Mid-tier governance officers                            |
| Kerubic angels   | Sub-angle tops                          | Bounded functional command                              |
| Servient angels  | Remaining squares                       | Task-scoped workers                                     |
| Cacodemons       | Inverse / lower constructions           | Fail modes, adversarial mirrors, inverse capabilities   |

Cacodemons are the Enochian contribution to **explicit inverse surfaces**: where a servient capability heals, its inverse can harm; where one allocates, the inverse denies. Map them to adversarial modules, chaos injection, or documented anti-features — never as silent side effects.

### Black Cross and Tablet of Union → Cross-domain bus

| Construct | Role in neo-Enochian | Architectural expression |
|-----------|----------------------|--------------------------|
| **Black Cross** | Joins the four tablets into the Great Table | Shared cross-cutting concerns; bus between domains |
| **Tablet of Union** | Spirit / fifth element (GD) | Orchestration layer, pure contracts, cross-domain coordination |

Treat Union / Black Cross modules as the only legitimate place for multi-Watchtower policy. Pair with Chaos Magic banishing for session isolation and with Solomonic seals for capability tokens.

---

## Thirty Aethyrs → Progressive Depth Layers

The Aethyrs (Aires) form a sequential depth structure from the densest (TEX, 30th) to the most subtle (LIL, 1st). In architecture they map to progressive refinement layers, nested abstraction, or staged initiation of a process. Crowley fixed the modern initiatory reading (outer → inner); Dee’s framing is more geographic/cosmic (Parts distributed through Aires).

| Band        | Aethyrs (approx.) | Character                              | Architectural use                                      |
|-------------|-------------------|----------------------------------------|--------------------------------------------------------|
| Dense       | 30–25             | Material, chaotic, early differentiation | Raw intake, unrefined state, edge collection           |
| Formative   | 24–19             | Structure emerging, polar tension      | Schema formation, constraint hardening                 |
| Operative   | 18–13             | Active work, conflict, governance      | Core processing, adversarial, policy enforcement       |
| Illuminated | 12–7              | Clarity, higher synthesis              | Scoring, judgment, cross-domain synthesis              |
| Subtle      | 6–1               | Abstract, sovereign, continuum         | Meta-contracts, system-wide policy, pure intent        |

Full 30-layer nesting is almost never appropriate. Prefer banded collapse (5 bands above) or a curated subset of Aethyrs that match actual pipeline stages. Record any collapse as a pragmatic projection.

### Curated high-signal Aethyrs

| Aethyr | Traditional character              | Architectural locus                                      |
|--------|------------------------------------|----------------------------------------------------------|
| TEX    | Lowest, material gateway           | Edge intake / external boundary                          |
| RII    | Early differentiation              | First schema split                                       |
| POP    | Division, polarity                 | Polar module separation                                  |
| ZIM    | Watery flux, transition            | State transition / flow control                          |
| LOE    | Justice, balance                   | Fairness / equilibrium constraints                       |
| OXO    | Wheel, cyclic motion               | Cyclic process / time-circuit analogue                   |
| ZAA    | Solitude, singular focus           | Isolated worker / single-responsibility unit             |
| DES    | Acceptable sacrifice / exchange    | Costed operation / explicit tradeoff surface             |
| BAG    | Doubt, interrogation               | Validation / challenge gate                              |
| ZID    | Holy table / foundation of work    | Core workbench / primary processing surface              |
| ZIP    | Threshold of higher orders         | Elevation gate to meta-layers                            |
| UT     | Compassion / higher mercy          | Soft policy / graceful degradation                       |
| LIL    | First, purest                      | Sovereign intent / system apex                           |

---

## 91 Parts of the Earth → Jurisdiction Map

Dee’s *Liber Scientiae* lists ninety-one (sometimes ninety-two with one hidden) **Parts of the Earth** — regions of geopolitical and cultural influence under zodiacal kings and governors, distributed across the thirty Aethyrs.

| Traditional idea | Architectural expression |
|------------------|--------------------------|
| Part of the Earth | Tenant, region, market, or legal jurisdiction |
| Zodiacal King | Policy authority for a cluster of Parts |
| Governors / ministers | Operational controllers under that authority |
| Geographic placement | Routing, residency, or compliance boundaries |

Use Parts when the system needs multi-region or multi-tenant authority maps. Do not invent a full 91-node tree by default; collapse to the jurisdictions the product actually serves and record the projection.

---

## Heptarchia → Planetary Office Layer

The **Heptarchia Mystica** is Dee’s earlier sevenfold system: planetary “royalty” of angels governing earthly action and knowledge of nature’s bounds.

| Heptarchic idea | Architectural expression |
|-----------------|--------------------------|
| Seven kings / princes | Planetary domain owners (pair with `planetary-spheres`) |
| Day/hour offices | Scheduled authority windows / temporal capability leases |
| Heptarchic hierarchy | Rank ladder orthogonal to Watchtower elemental rank |

When both Enochian and planetary-spheres frameworks are active, Heptarchia is the natural bridge: Watchtowers own elemental partition; Heptarchia owns planetary office and timing.

---

## Calls (Keys) → Invocation Protocols

The Eighteen Calls (plus the Call of the Thirty Aethyrs) are formal invocation texts. Architecturally they become:

- Explicit protocol messages that open a domain or layer  
- Versioned interface contracts that must be presented to enter a Watchtower or Aethyr  
- Audit-logged operations (every Call leaves provenance)  

| Call concept              | Architectural expression                                      |
|---------------------------|---------------------------------------------------------------|
| Opening Call              | Bootstrap / session init message                              |
| Elemental Call            | Domain-entry token for a Watchtower                           |
| Aethyr Call               | Layer-entry token for a depth band                            |
| Closing / banishing form  | Session teardown / context reset                              |

A module that requires Watchtower or Aethyr authority must receive a valid Call-token; absence is hard denial (fail-closed).

Counting note: Dee material yields **48 Angelical Keys**; modern practice often speaks of **19 Calls** (18 + Aethyr Call applied thirty times). For architecture, treat “Call” as the token type; do not encode 48 distinct protocol messages unless the system truly needs them.

---

## Dual-Naming Pattern

```
# mechanical: edge_intake
# symbolic:   aethyr_tex  (Enochian — TEX)
```

```
# mechanical: fire_transform
# symbolic:   watchtower_south  (Enochian — Fire Watchtower, neo)
```

```
# mechanical: domain_entry_token
# symbolic:   enochian_call  (Enochian — Call / Key)
```

```
# mechanical: sovereign_intent
# symbolic:   aethyr_lil  (Enochian — LIL)
```

```
# mechanical: cross_domain_bus
# symbolic:   tablet_of_union  (Enochian — Union / Black Cross)
```

```
# mechanical: inverse_capability
# symbolic:   cacodemon_mirror  (Enochian — inverse square)
```

---

## Practical Projection Notes

- Watchtowers (neo-Enochian elemental) excel at four-way domain separation and pair with planetary elemental overlays and sacred-geometry quaternary structures.
- Prefer the five Aethyr bands over a literal 30-directory tree. Thirty nested levels violate golden-ratio depth discipline.
- Calls are the Enochian contribution to capability-based security: every cross-domain or cross-layer entry requires an explicit, logged invocation.
- Parts of the Earth map to multi-tenant / multi-region authority; collapse aggressively to real jurisdictions.
- Heptarchia bridges Enochian and `planetary-spheres` without forcing a second elemental model.
- Cacodemons belong next to adversarial / Geburah / Mars loci — explicit inverse surfaces, not hidden behavior.
- When combining with Tree of Life, Watchtowers can sit under the Four Worlds or map onto elemental attributions of the Sephirot; record dual mappings and which Enochian stream is in use.
- When combining with Solomonic material, use Enochian for elemental/directional structure and Solomonic for rank/office hierarchy; Seniors ≈ mid-tier officers, Kings ≈ domain sovereigns.
- Chaos Magic (see `chaos-magic.md`) treats Enochian as one paradigm among many; banishing clears residual Watchtower assumptions when switching maps.

Load this file when Enochian Watchtowers, Aethyrs, Calls, Parts of the Earth, Heptarchia, or tablet-names are selected as primary or secondary framework.
