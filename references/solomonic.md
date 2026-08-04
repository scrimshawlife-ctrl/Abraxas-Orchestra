# Solomonic Hierarchy & Functional Correspondence

Sixth framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide authority tiers, functional domain ownership, sealed contracts, and provenance annotation. They are not runtime rules and do not implement any operative magical practice.

The Solomonic tradition (primarily the *Lemegeton* / Lesser Key and related grimoires) supplies a highly structured hierarchy of ranks, offices, and sealed instruments. For software architecture the useful extract is the rank ladder, the functional specializations, and the notion of the sealed contract (pentacle).

## Rank Hierarchy → Authority & Privilege Tiers

The traditional ranks form a clear descending ladder of authority and scope. In architecture they map onto privilege levels, capability breadth, and decision scope.

| Rank          | Traditional scope                          | Architectural authority role                                      | Typical modules / packages                          |
|---------------|--------------------------------------------|-------------------------------------------------------------------|-----------------------------------------------------|
| King          | Broadest command, multiple legions         | Top-level sovereign contract, system-wide policy, root authority  | `sovereign/`, `root_policy/`, `king_contract/`      |
| Duke          | High command, substantial forces           | Major domain ownership, high-privilege services                   | `domain_owner/`, `duke_service/`                    |
| Prince        | Elevated office, often specialized         | Elevated specialized authority, cross-cutting privileged ops      | `elevated_ops/`, `prince_authority/`                |
| Marquis       | Regional or functional command             | Mid-high functional command, bounded but strong privilege         | `functional_command/`, `marquis_scope/`             |
| President     | Administrative / executive office          | Executive administration, operational control surfaces            | `executive/`, `admin_control/`                      |
| Earl / Count  | Mid-level command                         | Mid-tier services, limited but clear authority                    | `mid_service/`, `earl_scope/`                       |
| Knight        | Mobile, task-oriented force                | Task-scoped agents, mobile workers, limited privilege             | `task_agent/`, `knight_worker/`                     |

Direction of authority is downward. Higher ranks may constrain or authorize lower ranks; lower ranks do not spontaneously escalate.

## Functional Categories → Domain Specialization

Traditional spirit offices cluster into recurring functional types. These become clean domain ownership labels.

| Functional type          | Traditional office emphasis                     | Architectural domain role                                      | Suggested mechanical / symbolic pairing                  |
|--------------------------|-------------------------------------------------|----------------------------------------------------------------|----------------------------------------------------------|
| Knowledge / Revelation   | Liberal sciences, hidden things, teaching       | Knowledge retrieval, research, revelation interfaces           | `knowledge_reveal` / `solomonic_knowledge`               |
| Treasure / Resource      | Location or bestowal of wealth, materials       | Resource discovery, allocation, value surfaces                 | `resource_discovery` / `solomonic_treasure`              |
| Warfare / Conflict       | Battle, destruction of enemies, fortification   | Adversarial, defensive, conflict resolution modules            | `conflict_ops` / `solomonic_warfare`                     |
| Love / Relation          | Affections, alliances, reconciliation           | Relation modeling, alliance, reconciliation surfaces           | `relation_alliance` / `solomonic_love`                   |
| Travel / Movement        | Transportation, speed, bridges, roads           | Transport, routing, movement, bridging layers                  | `transport_bridge` / `solomonic_travel`                  |
| Transformation           | Shape-changing, alteration of form or state     | State transformation, form alteration, metamorphosis           | `form_transform` / `solomonic_change`                    |
| Binding / Constraint     | Binding, restriction, containment of force      | Constraint enforcement, binding contracts, containment         | `binding_constraint` / `solomonic_bind`                  |
| Judgment / Truth         | Detection of truth, exposure of lies, justice   | Truth verification, judgment, exposure of falsehood            | `truth_judgment` / `solomonic_justice`                   |

A single module may carry both a rank (authority tier) and a functional type (domain specialization).

## Sealed Contracts (Pentacles) → Capability Tokens

In the tradition a pentacle is a sealed instrument that authorizes and constrains a specific operation. In architecture this maps cleanly onto:

- Capability tokens
- Sealed interface contracts
- Authorization packets that both enable and limit an action

| Sealed contract concept | Architectural expression                                      |
|-------------------------|---------------------------------------------------------------|
| Pentacle of authority   | Capability token or authorization packet                      |
| Seal of a specific office | Typed interface that grants only the offices of that function |
| Time-bounded seal       | Expiring capability or lease                                  |
| Directional / elemental seal | Scoped capability limited to a planetary or elemental domain |

Sealed contracts are the natural home for fail-closed authorization surfaces. A module that requires a higher rank or a specific functional office must present a valid seal; absence of the seal is a hard denial.

## Dual-Naming Pattern

```
# mechanical: root_policy
# symbolic:   king_contract  (Solomonic — King rank)
```

```
# mechanical: knowledge_reveal
# symbolic:   solomonic_knowledge  (Solomonic — Knowledge office)
```

```
# mechanical: binding_constraint
# symbolic:   solomonic_bind  (Solomonic — Binding office)
```

```
# mechanical: capability_token
# symbolic:   pentacle_seal  (Solomonic — sealed contract)
```

## Practical Projection Notes

- The rank ladder is especially useful for privilege and authorization design. It pairs cleanly with Saturn (boundary) and Sun (sovereign) planetary domains.
- Functional categories can overlay planetary spheres or Tree-of-Life Sephirot without conflict; record dual mappings in the correspondence table.
- Sealed contracts (pentacles) are the strongest architectural contribution of the Solomonic material: they give a traditional language for capability-based security and fail-closed authorization.
- Do not attempt to map all 72 Goetic spirits individually. The rank + functional type abstraction is the practical projection.
- When a system requires only light hierarchical structure, collapse the seven ranks into three tiers (Sovereign / Officer / Worker) and record the collapse.

Load this file when Solomonic hierarchy, ranks, functional offices, or sealed contracts are selected as primary or secondary framework.
