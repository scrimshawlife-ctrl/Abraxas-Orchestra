# I Ching Hexagrams — Curated Set for State Machines

Fifth framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide discrete state naming, transition rules, and provenance annotation. They are not runtime rules.

The full I Ching contains 64 hexagrams. For architectural use a curated high-signal subset is more practical. The selection below prioritizes states that commonly appear in forecasting, agent, and pipeline systems: beginning, accumulation, obstruction, breakthrough, equilibrium, decline, completion, and return.

## Design Principles for the Curated Set

- Prefer hexagrams that describe clear system states or transitions rather than purely personal or divinatory meanings.
- Keep the set small enough to be memorable (12–16) while covering the major regime types.
- Dual-name every state so mechanical names remain primary.
- Transitions between hexagrams can later become explicit Path-like adapters if needed.

## Curated Hexagram Set (16)

| Hex # | Name (English)          | Traditional image / force                     | Architectural state role                                      | Suggested mechanical / symbolic pairing                  |
|-------|-------------------------|-----------------------------------------------|---------------------------------------------------------------|----------------------------------------------------------|
| 1     | The Creative            | Heaven, pure initiating force, strength       | Pure initiation, unbounded generative start                   | `init_creative` / `qian_creative`                        |
| 2     | The Receptive           | Earth, pure yielding, containment             | Pure reception, containment, yielding ground                  | `receptive_ground` / `kun_receptive`                     |
| 3     | Difficulty at Beginning | Sprouting through obstruction, birth struggle | Early-stage friction, birth of a process under resistance     | `birth_friction` / `zhun_difficulty`                     |
| 5     | Waiting                 | Clouds rising, nourishment while waiting      | Deliberate wait, accumulation while conditions mature         | `deliberate_wait` / `xu_waiting`                         |
| 6     | Conflict                | Heaven & water moving apart, contention       | Open conflict, opposing forces, unresolved polarity           | `open_conflict` / `song_conflict`                        |
| 11     | Peace                   | Heaven & earth in harmony, prosperity         | Balanced flow, harmonious regime, productive equilibrium      | `harmonious_flow` / `tai_peace`                          |
| 12     | Standstill              | Heaven & earth blocked, stagnation            | Blocked regime, stagnation, no productive exchange            | `blocked_standstill` / `pi_standstill`                   |
| 18     | Work on the Decayed    | Wind under mountain, repair of corruption     | Decay repair, debt / corruption remediation                   | `decay_repair` / `gu_decay`                              |
| 23     | Splitting Apart         | Mountain over earth, erosion, collapse        | Controlled or uncontrolled dissolution, stripping away        | `splitting_apart` / `bo_splitting`                       |
| 24     | Return                  | Thunder under earth, turning point            | Return after decline, cyclic renewal, turning point           | `cyclic_return` / `fu_return`                            |
| 29     | The Abysmal             | Water doubled, repeated danger                | Repeated danger, deep risk, necessary passage through peril   | `repeated_danger` / `kan_abysmal`                        |
| 30     | The Clinging            | Fire doubled, clarity, dependence             | Clarity under dependence, illuminated but attached state      | `clinging_clarity` / `li_clinging`                       |
| 32     | Duration                | Thunder & wind, enduring movement             | Enduring process, long-running stable motion                  | `enduring_motion` / `heng_duration`                      |
| 49     | Revolution              | Fire under lake, radical change               | Radical regime change, shedding of old form                   | `radical_revolution` / `ge_revolution`                   |
| 50     | The Cauldron            | Fire under wood, transformation vessel        | Transformation vessel, cooking of new form from old           | `transformation_vessel` / `ding_cauldron`                |
| 63     | After Completion        | Water over fire, ordered completion           | Ordered completion, all lines in place, finished cycle        | `after_completion` / `jiji_completion`                   |
| 64     | Before Completion       | Fire over water, almost finished              | Near-completion, remaining disorder, final push required      | `before_completion` / `weiji_before`                     |

(Hexagram 63 and 64 form a classic completion polarity and are both retained.)

## Dual-Naming Pattern

```
# mechanical: deliberate_wait
# symbolic:   xu_waiting  (I Ching — 5 Waiting)
```

```
# mechanical: radical_revolution
# symbolic:   ge_revolution  (I Ching — 49 Revolution)
```

```
# mechanical: after_completion
# symbolic:   jiji_completion  (I Ching — 63 After Completion)
```

## Practical Projection Notes

- Use the curated set as named states in a state machine or regime tracker. Mechanical names remain the primary identifiers.
- Transitions can be recorded as ordinary directed edges; if a transition itself needs symbolic weight it can later be annotated with a Path-like or hexagram-change rationale.
- The set is deliberately incomplete. Additional hexagrams may be added when a real system surfaces a state that is not well covered.
- “After Completion” (63) and “Before Completion” (64) are especially useful for pipeline end-states and for Brier-scored forecasting regimes.
- “Return” (24) pairs cleanly with cyclical memory and Moon-domain modules.
- “Revolution” (49) and “The Cauldron” (50) are natural homes for radical transformation and alchemical-style refinement stages.
- When combining with other frameworks, a hexagram can sit inside a planetary domain or a Sephira without conflict; record the dual mapping in the correspondence table.

Load this file when I Ching hexagrams are selected as primary or secondary framework for discrete state work.
