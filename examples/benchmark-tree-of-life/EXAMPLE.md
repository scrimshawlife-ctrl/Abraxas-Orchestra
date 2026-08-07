# Structure benchmark — Tree of Life before / after

Measurable proof that **map-aligned structure** improves more than names.

| Tree | Layout | Intent |
|------|--------|--------|
| `before/myapp/` | Flat `utils` / `helpers` / `stuff` / `main` | Mixed loci, import cycles, no early contract |
| `after/tol/` | `intent` → `intake` → `analyze` → `store` → `output` | One locus per module, one-way flow |

Same happy-path behavior (`source="demo-source"`, `max_items=8`). Different structure.

## Run

From repo root:

```bash
python3 examples/benchmark-tree-of-life/harness.py
python3 examples/benchmark-tree-of-life/harness.py --json
python3 examples/benchmark-tree-of-life/harness.py --out /tmp/orch-bench.json
```

Exit `0` when hard checks pass: parity, better map quality, fewer cycles, fewer mixed-responsibility files, after rejects empty source. Early-exit µs is reported (soft; can vary by host).

## What is measured

1. **Behavioral parity** — canonical happy-path payload equal  
2. **Analyze scorecard** — `orchestra analyze -f tree-of-life` STRONG/ADEQUATE/WEAK/FORCED + weighted map quality  
3. **Import-graph hygiene** — local edges, nodes in cycles (Tarjan SCC)  
4. **Responsibility mix** — files whose identifiers/calls hit ≥2 of {intake, score, store, emit}  
5. **Early-exit control flow** — empty `source`: before still runs the pipeline; after fails closed at `intent` (and is cheaper)

We **do not** claim domain scoring is generally CPU-faster. Structure optimizes map quality, graph hygiene, mix, and fail-closed control flow.

## Hermes route

1. **repo** `analyze --path examples/benchmark-tree-of-life/before -f tree-of-life --out /tmp/b`  
2. **repo** `analyze --path examples/benchmark-tree-of-life/after -f tree-of-life --out /tmp/a`  
3. Diff `structure-metrics.json` (or run `harness.py` for parity + early-exit too)  

Analyze always prints `# metrics: map_quality=… strong=… cycles=… mixed_files=…` on stderr.

Site: [before & after + metrics](https://scrimshawlife-ctrl.github.io/Abraxas-Orchestra/#before-after).
