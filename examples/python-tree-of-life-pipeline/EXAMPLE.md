# Python best case — optimized by Tree of Life

This is **not** a rename-only skeleton. The map optimizes the code:

| Stage | Symbolic | Allowed work | Forbidden here |
|-------|----------|--------------|----------------|
| `tol.intent` | kether | Validate goals / limits | I/O, scoring |
| `tol.intake` | chokmah | Pull raw records | Scoring, persist |
| `tol.analyze` | hod | Score / filter | File I/O, emission |
| `tol.store` | yesod | Persist | New scoring rules |
| `tol.output` | malkuth | Final payload shape | Intake, analysis |

Package name is `tol` (not bare `intent`/`analyze`) so imports never shadow other examples.

## Run

```bash
cd examples/python-tree-of-life-pipeline
python3 pipeline.py
```

## Hermes route

1. **emit** `structure -f tree-of-life -c "intent,intake,analyze,store,output"` (scaffold)  
2. Implement domain logic **inside** each stage’s contract (this example under `tol/`)  
3. Optional **repo** `analyze` to re-check import graph  

Site: [before & after](https://scrimshawlife-ctrl.github.io/Abraxas-Orchestra/#before-after).
