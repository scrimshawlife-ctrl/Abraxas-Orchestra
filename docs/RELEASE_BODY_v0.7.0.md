# Orchestra 0.7.0

Structure that optimizes work — contracts, measurable metrics, and a before/after proof.

## Highlights

- **Contract-oriented emission** — `structure` / `project --out` stage stubs ship `run()` + `contract()` with locus **ALLOWED** / **FORBIDDEN**; multi-stage maps also write `pipeline.py`
- **Structure metrics in analyze** — every run embeds map quality, import cycles, and responsibility mix; `--out` writes `structure-metrics.json`; stderr prints `# metrics: …`
- **Measurable before/after** — `examples/benchmark-tree-of-life/harness.py` proves parity + map/cycles/mix/early-exit wins beyond rename semantics
- **Hermes routing** — agents use the same **meta** / **emit** / **repo** groups as the CLI `CommandRouter`
- Site + docs: Python best-case optimized by the map (not rename-only)

## Install

```bash
git clone --branch v0.7.0 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh && bash install.sh
python3 scripts/orchestra.py check
python3 examples/benchmark-tree-of-life/harness.py
python3 scripts/orchestra.py analyze \
  --path examples/benchmark-tree-of-life/after \
  -f tree-of-life --out /tmp/orch-m
# → analysis.json + structure-metrics.json; stderr has # metrics:
```

## Notes

We do **not** claim domain scoring is generally CPU-faster. Structure improves map quality, graph hygiene, responsibility mix, and fail-closed control flow.
