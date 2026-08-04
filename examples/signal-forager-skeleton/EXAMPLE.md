# Example — Signal Forager Skeleton

End-to-end demonstration of Abraxas Orchestra applied to a signal-foraging subsystem.

## Intent

Structure a minimal signal-forager with:

- Clear entry contract (intent)
- Raw signal intake
- Schema / constraint enforcement
- Adversarial filtering
- Central synthesis / scoring
- Persistent store
- Concrete output surface

## Command used

```bash
python3 scripts/orchestra.py do structure \
  -f tree-of-life \
  -o alchemical-stages \
  -c "intent,intake,constraint,adversarial,synthesis,store,output" \
  --out examples/signal-forager-skeleton
```

## Mapping summary

| Mechanical   | Symbolic (Tree of Life) | Overlay (Alchemical)      |
|--------------|-------------------------|---------------------------|
| intent       | kether                  | nigredo                   |
| intake       | chokmah                 | albedo                    |
| constraint   | binah                   | citrinitas                |
| adversarial  | geburah                 | rubedo                    |
| synthesis    | tiphareth               | (paired by index)         |
| store        | yesod                   | (paired by index)         |
| output       | malkuth                 | (paired by index)         |

Primary framework supplies hierarchy and polarity. Alchemical overlay annotates process stage character. Overlay pairing is index-based in v0.1 (best-effort); operators may refine dual mappings in the correspondence table.

## Generated artifacts

- `SKELETON.md` — human-readable map
- `correspondence-table.json` — machine-readable provenance
- Per-module `__init__.py` — dual-named typed stubs ready for implementation

## How to extend

1. Replace each `placeholder()` with real logic.
2. Add Path / gate modules between polar pairs (e.g. intake ↔ constraint, adversarial ↔ synthesis).
3. Run `do project` if the map grows beyond six modules and a reduced core is preferred.
4. Record any pragmatic collapse in the correspondence table before promoting structure.

## Status

CLEAN — all selected concerns mapped to strong or adequate loci. No FORCED entries.
