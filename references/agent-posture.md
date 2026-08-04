# Agent Posture (coding-agent build rules)

Operational guidance for **how Orchestra-backed agents implement and evolve code**.

This is **not** an esoteric framework. It is not loaded by `do structure` / `do project`. It does not appear in the correspondence-table schema enum.

Source signal: high-engagement AGENTS.md patterns used in long-running coding-agent sessions (side-project scope). Assimilated only where they reinforce existing Orchestra invariants.

## Scope gates

| Mode | Applies |
|------|---------|
| **Emitted project / app tree** | Full posture below (operator may tighten further) |
| **Orchestra skill surface itself** | Only rules that do **not** break versioned contracts (schema, CLI intents, install paths, dual-name provenance) |
| **Production systems with live users/data** | Operator must override “no compatibility” — fail closed on destructive defaults |

Author of the external signal explicitly limited aggressive rules to side projects. Orchestra inherits that boundary.

## Assimilated rules

### 1. Layered growth (core)

Start from the smallest version that works end to end. Add each capability on a product that already runs. Never trade a working skeleton for unfinished complexity.

Maps to: pragmatic projection, core collapse, minimal dual-named stubs before deep logic.

### 2. Current requirements only

Choose the simplest implementation that fully meets **current** requirements. Avoid speculative abstractions, configuration surfaces, and indirection.

Maps to: no 30-Aethyr directory trees; no speculative Sephirot; mark WEAK/FORCED instead of inventing depth.

### 3. Separation of concerns

Keep modules modular and concerns clearly separated. Mechanical public names stay conventional; symbolic names stay in correspondence tables and internal docs.

Maps to: dual-naming rule; Watchtower / domain boundary discipline.

### 4. Prefer existing, proven material

- Prefer established, well-maintained libraries when they reduce complexity or improve reliability.
- Lean on dependencies already in the **target** project before adding packages or writing parallel implementations.
- Check documentation and types before assuming a library cannot do the job.
- Study how established products solve the problem; adopt proven patterns rather than inventing a private approach from scratch.

Maps to: stdlib-only Orchestra CLI (skill); for emitted apps, reuse the host stack.

### 5. Long-term decisions inside the chosen scope

Do not accept a stopgap that is *meant* to be replaced later **within the same design horizon**. Temporary probes are allowed when labeled SPECULATIVE and time-boxed in provenance.

Maps to: no silent pragmatic projection; no auto-canon promotion of SPECULATIVE maps.

### 6. Compatibility (gated)

**Side-project / disposable tree:** Prefer removing obsolete paths over adding compatibility layers, fallbacks, or migrations.

**Orchestra skill and any versioned public contract:** Preserve backward compatibility for schema, CLI, and install targets across the declared minor line unless a major version explicitly breaks them.

Never apply “delete the old path” to skill contracts, correspondence schema, or host install layout without an explicit version bump and operator approval.

## Anti-assimilation (do not import)

| External impulse | Why rejected |
|------------------|--------------|
| Universal “no backward compatibility” | Breaks Hermes/OpenClaw skill install and schema stability |
| Implicit production defaults that destroy data | Violates fail-closed and human sovereignty |
| Replacing dual-name / SEED provenance with style slogans | Different layer; provenance is non-negotiable |

## Operator checklist

Before accepting agent output:

1. Does an end-to-end path already run for the current requirement?
2. Is every new abstraction justified by a present requirement (not a future maybe)?
3. Are concerns separated and dual-named where structure was emitted?
4. Were existing project dependencies checked before new code or packages?
5. Is any compatibility break scoped to a disposable tree or an explicit major bump?

## Provenance note

When these rules influence a structural decision, record in the correspondence table or design note:

```text
agent_posture: layered-growth | simple-current | no-stopgap | deps-first
```

Do not invent a symbolic locus in Tree of Life / Enochian / etc. for these rules.
