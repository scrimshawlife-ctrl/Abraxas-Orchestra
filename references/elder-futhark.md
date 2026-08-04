# Elder Futhark Correspondence Tables

Third framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide subsystem boundaries, intent-bearing names, and provenance annotation. They are not runtime rules.

The Elder Futhark consists of 24 runes arranged in three aettir (families) of eight. The aettir provide natural major subsystem boundaries. Individual runes supply precise intent labels for modules, interfaces, or comment sigils.

## Three Aettir → Major Subsystem Boundaries

| Aett              | Traditional force                          | Architectural boundary role                                      | Typical contents                                      |
|-------------------|--------------------------------------------|------------------------------------------------------------------|-------------------------------------------------------|
| Freyr’s Aett      | Fertility, beginnings, material force, wealth, travel | Intake, generation, expansion, raw material, movement           | Ingest, generative, expand, travel/transport, resource |
| Hagal’s Aett      | Disruption, constraint, necessity, trial, transformation | Constraint, severity, testing, boundary, forced change          | Schema, adversarial, filter, trial, transform          |
| Tyr’s Aett        | Order, justice, human & divine law, completion, community | Synthesis, judgment, order, output, human surface, completion   | Core/synthesis, judgment, output, report, governance   |

The three aettir form a natural progression: generative force → trial/constraint → ordered completion. This maps cleanly onto many Abraxas pipelines (ingest → adversarial/filter → synthesis/output).

## Individual Runes → Architectural Intent

### Freyr’s Aett (1–8)

| Rune     | Name     | Traditional force                          | Architectural role                                      | Suggested mechanical / symbolic pairing                  |
|----------|----------|--------------------------------------------|---------------------------------------------------------|----------------------------------------------------------|
| ᚠ        | Fehu     | Cattle, mobile wealth, liquid resource     | Resource pool, credit, fungible value, energy budget    | `resource_pool` / `fehu_wealth`                          |
| ᚢ        | Uruz     | Aurochs, vital strength, untamed force     | Raw capacity, vitality, untamed generative power        | `raw_capacity` / `uruz_strength`                         |
| ᚦ        | Thurisaz | Thorn, giant, reactive force, defense      | Reactive barrier, defensive spike, threat response      | `reactive_barrier` / `thurisaz_thorn`                    |
| ᚨ        | Ansuz    | God, mouth, inspired speech, signal        | Signal intake, inspired communication, oracle voice     | `signal_intake` / `ansuz_voice`                          |
| ᚱ        | Raidho   | Ride, ordered journey, rhythm              | Ordered movement, transport, rhythmic process           | `ordered_transport` / `raidho_journey`                   |
| ᚲ        | Kenaz    | Torch, controlled fire, illumination       | Controlled illumination, technical knowledge, craft     | `controlled_light` / `kenaz_torch`                       |
| ᚷ        | Gebo     | Gift, exchange, partnership                | Exchange interface, gift/reciprocity, balanced transfer | `exchange_interface` / `gebo_gift`                       |
| ᚹ        | Wunjo    | Joy, harmony, fellowship                   | Harmony state, successful integration, fellowship       | `harmony_state` / `wunjo_joy`                            |

### Hagal’s Aett (9–16)

| Rune     | Name     | Traditional force                          | Architectural role                                      | Suggested mechanical / symbolic pairing                  |
|----------|----------|--------------------------------------------|---------------------------------------------------------|----------------------------------------------------------|
| ᚺ        | Hagalaz  | Hail, disruption, sudden necessity         | Disruption event, forced reset, hailstorm of change     | `disruption_event` / `hagalaz_hail`                      |
| ᚾ        | Nauthiz  | Need, constraint, friction, necessity      | Hard constraint, friction, need-driven limitation       | `hard_constraint` / `nauthiz_need`                       |
| ᛁ        | Isa      | Ice, stasis, concentration, stillness      | Stasis, freeze, concentration point, pause              | `stasis_point` / `isa_ice`                               |
| ᛃ        | Jera     | Year, harvest, cyclical reward             | Cyclical completion, harvest, seasonal reward           | `cyclical_harvest` / `jera_year`                         |
| ᛇ        | Eihwaz   | Yew, endurance, axis, defense              | Enduring axis, defensive core, vertical resilience      | `enduring_axis` / `eihwaz_yew`                           |
| ᛈ        | Perthro  | Lot-cup, chance, hidden process, mystery   | Hidden process, probabilistic core, lot/chance          | `hidden_process` / `perthro_lot`                         |
| ᛉ        | Algiz    | Elk, protection, higher connection         | Protection layer, higher connection, guardian           | `protection_layer` / `algiz_elk`                         |
| ᛊ        | Sowilo   | Sun, success, clarity, vital force         | Clarity, success signal, vital illumination             | `clarity_signal` / `sowilo_sun`                          |

### Tyr’s Aett (17–24)

| Rune     | Name     | Traditional force                          | Architectural role                                      | Suggested mechanical / symbolic pairing                  |
|----------|----------|--------------------------------------------|---------------------------------------------------------|----------------------------------------------------------|
| ᛏ        | Tiwaz    | Tyr, justice, ordered conflict, polarity   | Just judgment, ordered conflict, polarity axis          | `just_judgment` / `tiwaz_justice`                        |
| ᛒ        | Berkano  | Birch, growth, enclosure, becoming         | Contained growth, enclosure, becoming process           | `contained_growth` / `berkano_birch`                     |
| ᛖ        | Ehwaz    | Horse, trust, cooperative movement         | Trusted partnership, cooperative movement, vehicle      | `trusted_partnership` / `ehwaz_horse`                    |
| ᛗ        | Mannaz   | Human, self, community, intelligence       | Human surface, self-model, community intelligence       | `human_surface` / `mannaz_human`                         |
| ᛚ        | Laguz    | Water, flow, life current, intuition       | Flow, life current, intuitive stream                    | `life_flow` / `laguz_water`                              |
| ᛜ        | Ingwaz   | Ing, gestation, internal potential         | Gestation, internal potential, stored seed              | `gestation_seed` / `ingwaz_potential`                    |
| ᛞ        | Dagaz    | Day, breakthrough, polar transformation    | Breakthrough, polar flip, day-break transformation      | `breakthrough` / `dagaz_day`                             |
| ᛟ        | Othala   | Ancestral property, inheritance, homeland  | Inherited store, ancestral continuity, homeland base    | `inherited_store` / `othala_homeland`                    |

## Dual-Naming Pattern

```
# mechanical: signal_intake
# symbolic:   ansuz_voice  (Elder Futhark — Ansuz)
```

```
# mechanical: hard_constraint
# symbolic:   nauthiz_need  (Elder Futhark — Nauthiz)
```

```
# mechanical: just_judgment
# symbolic:   tiwaz_justice  (Elder Futhark — Tiwaz)
```

## Practical Projection Notes

- The three aettir give clean major directory or package boundaries for medium-to-large systems.
- Not every system needs all 24 runes. Select a focused subset that matches the actual functional concerns and record the selection in the correspondence table.
- Hagal’s Aett is especially useful for adversarial, constraint, and transformation layers.
- Tyr’s Aett maps naturally onto synthesis, judgment, human surface, and completion modules.
- Individual runes work well as intent-bearing names for small, focused modules or as comment sigils that recover the original design force.
- When combining with Tree of Life, the aettir can overlay the vertical Worlds or the horizontal polarities (Chesed–Geburah, Netzach–Hod).

Load this file when Elder Futhark is selected as primary or secondary framework.
