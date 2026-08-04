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

| Functional type          | Traditional office emphasis                     | Architectural domain role                                      |
|--------------------------|-------------------------------------------------|----------------------------------------------------------------|
| Knowledge / revelation   | Teaching, secrets, liberal sciences             | Research, knowledge retrieval, revelation surfaces             |
| Binding / constraint     | Binding, containment, restriction               | Constraint engines, sandboxing, capability reduction           |
| Treasure / resource      | Hidden wealth, discovery                        | Resource discovery, inventory, allocation                      |
| War / adversarial        | Conflict, courage, opposition                   | Adversarial filters, stress, defense                           |
| Love / relation          | Affection, alliance, reconciliation             | Relation modeling, affinity, partnership contracts             |
| Justice / truth          | Judgment, honesty, exposure of deceit           | Audit, truth-scoring, integrity checks                         |
| Travel / transport       | Movement, messengers, swiftness                 | Messaging, transport, routing                                  |

## Sealed Contracts (Pentacles) → Capability Tokens

Pentacles become capability tokens / sealed contracts: explicit authorization objects that grant bounded powers and fail closed when absent or invalid.

## Dual-Naming Pattern

```
# mechanical: root_policy
# symbolic:   king_contract  (Solomonic — King)
```

```
# mechanical: task_worker
# symbolic:   knight_agent  (Solomonic — Knight)
```

## Practical Projection Notes

- The rank ladder is especially useful for privilege and authorization design.
- Sealed contracts are the strongest architectural contribution: capability-based security language.
- Do not map all 72 Goetic spirits individually; use rank + functional type.
- Collapse seven ranks to three tiers (Sovereign / Officer / Worker) when light hierarchy is enough.

Load this file when Solomonic hierarchy is selected as primary or secondary framework.

## CLI default loci (mechanical → symbolic)

| Mechanical | Symbolic | Note |
|------------|----------|------|
| `sovereign` | `king_contract` | Root authority |
| `domain_owner` | `duke_service` | Major domain ownership |
| `executive` | `president_admin` | Operational control |
| `task_agent` | `knight_worker` | Task-scoped worker |
| `knowledge` | `solomonic_knowledge` | Revelation / research |
| `binding` | `solomonic_bind` | Constraint / containment |
| `judgment` | `solomonic_justice` | Truth / judgment |

Core collapse for `do project`: **`sovereign`, `executive`, `task_agent`**.

Canonical machine table: `schemas/frameworks.v1.json`.
