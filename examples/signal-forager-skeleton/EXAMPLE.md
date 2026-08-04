# Example — Signal Forager Skeleton

End-to-end demonstration of Abraxas Orchestra applied to a signal-foraging subsystem
with **working pipeline logic**.

## Intent

Structure and implement a minimal signal-forager with:

- Clear entry contract (intent / Kether)
- Raw signal intake (intake / Chokmah)
- Schema / constraint enforcement (constraint / Binah)
- Adversarial filtering (adversarial / Geburah)
- Central synthesis / scoring (synthesis / Tiphareth)
- Persistent store (store / Yesod)
- Concrete output surface (output / Malkuth)

## Run the demo

```bash
cd examples/signal-forager-skeleton
python3 run_demo.py
```

Artifacts land in `_demo_out/report.json` and `_demo_out/store.json`.

## Pipeline path

```
intent → intake → constraint → adversarial → synthesis → store → output
```

| Mechanical   | Symbolic (Tree of Life) | Role                                      |
|--------------|-------------------------|-------------------------------------------|
| intent       | kether                  | Forage contract (query, limits, tags)     |
| intake       | chokmah                 | Heterogeneous → RawSignal                 |
| constraint   | binah                   | Fail-closed schema validation             |
| adversarial  | geburah                 | Noise / dup / weight / relevance filter   |
| synthesis    | tiphareth               | Score + OBSERVED/INFERRED/SPECULATIVE     |
| store        | yesod                   | In-memory + JSON persistence              |
| output       | malkuth                 | ForageReport emit (text / JSON)           |

## Programmatic use

```python
from pipeline import run_forage
from output import emit_text

report, scored, store = run_forage(
    "energy market stress",
    [{"text": "energy futures widened", "tags": ["market"], "weight": 0.9, "source": "api"}],
    max_signals=10,
)
print(emit_text(report))
```

## Design notes

- Stdlib only. Deterministic given identical inputs.
- Epistemic labels follow Abraxas OBSERVED / INFERRED / SPECULATIVE discipline.
- Fail-closed at constraint: missing text or invalid weight is rejected with reason.
- Adversarial pass drops noise patterns, duplicates, under-weight, and query-irrelevant items.
- Synthesis scores by weight + tag bonus + query-term hits; source type biases label.

## Regenerating structure only

```bash
./regenerate.sh
```

Overwrites dual-name stubs; re-apply logic from this tree or from git history if needed.
