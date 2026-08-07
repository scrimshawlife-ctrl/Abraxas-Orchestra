# Orchestra 0.6.0

AST-grade multi-language import parsing + higher, subprocess-aware coverage floors.

## Highlights

- Tokenizers + structured `ImportNode` trees for JS/TS, Go, Rust, Ruby (stdlib only)
- Coverage measurement runs pure unit tests **and** in-process CLI exercises under one tracer
- Raised hard floors on core modules (`coverage_report.py --gate` / CI `coverage-gate`)

## Install

```bash
git clone --branch v0.6.0 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh && bash install.sh
python3 scripts/coverage_report.py --gate
python3 scripts/orchestra.py analyze --path . --lang auto --out /tmp/orch-an
```
