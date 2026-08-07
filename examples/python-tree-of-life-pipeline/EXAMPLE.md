# Python best case — optimized by Tree of Life

This is **not** a rename-only skeleton. The map optimizes the code:

| Stage | Symbolic | Allowed work | Forbidden here |
|-------|----------|--------------|----------------|
| `intent` | kether | Validate goals / limits | I/O, scoring |
| `intake` | chokmah | Pull raw records | Scoring, persist |
| `analyze` | hod | Score / filter | File I/O, emission |
| `store` | yesod | Persist | New scoring rules |
| `output` | malkuth | Final payload shape | Intake, analysis |

## Run

```bash
cd examples/python-tree-of-life-pipeline
python3 pipeline.py
```

## Hermes route

1. **emit** `structure -f tree-of-life -c "intent,intake,analyze,store,output"` (scaffold)  
2. Implement domain logic **inside** each stage’s contract (this example)  
3. Optional **repo** `analyze` to re-check import graph stays clean  

See site: [Python best case before/after](https://scrimshawlife-ctrl.github.io/Abraxas-Orchestra/#before-after).
