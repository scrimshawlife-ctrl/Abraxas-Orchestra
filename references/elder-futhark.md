# Elder Futhark Correspondence

Third framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide sequential pipeline stages, aettir partitions, and provenance annotation. They are not runtime rules.

## Three Aettir → Pipeline Partitions

| Aett | Traditional force | Architectural partition | Typical stages |
|------|-------------------|-------------------------|----------------|
| Freyr’s Aett | Beginnings, wealth, force | Intake and resource establishment | resource, signal intake |
| Hagal’s Aett | Disruption, constraint, protection | Constraint, crisis, protection | hard constraint, protection |
| Tyr’s Aett | Order, judgment, human surface | Judgment, community, inheritance | judgment, human surface, store |

## Selected Runes → Architectural Loci

| Rune | Force | Architectural role | Mechanical |
|------|-------|-------------------|------------|
| Fehu | Wealth / cattle | Resource pool | `resource` |
| Ansuz | Signal / breath of gods | Inspired intake | `signal_intake` |
| Nauthiz | Need / constraint | Hard constraint | `hard_constraint` |
| Algiz | Elk / protection | Guardian layer | `protection` |
| Tiwaz | Tyr / justice | Ordered judgment | `just_judgment` |
| Mannaz | Human | Human surface | `human_surface` |
| Othala | Heritage | Inherited store | `inherited_store` |

## Dual-Naming Pattern

```
# mechanical: signal_intake
# symbolic:   ansuz
```

## Practical Projection Notes

- Aettir give a natural three-phase pipeline partition.
- Prefer selected high-signal runes over the full 24 for v0.1 defaults.

Load this file when Elder Futhark is selected as primary or secondary framework.

## CLI default loci (mechanical → symbolic)

| Mechanical | Symbolic | Note |
|------------|----------|------|
| `resource` | `fehu` | Resource / wealth pool |
| `signal_intake` | `ansuz` | Inspired signal intake |
| `hard_constraint` | `nauthiz` | Need-driven constraint |
| `protection` | `algiz` | Guardian / protection layer |
| `just_judgment` | `tiwaz` | Ordered judgment |
| `human_surface` | `mannaz` | Human / community surface |
| `inherited_store` | `othala` | Ancestral / inherited store |

Core collapse for `do project`: **`signal_intake`, `just_judgment`, `human_surface`**.

Canonical machine table: `schemas/frameworks.v1.json`.
