# Orchestra 0.5.0

Multi-language analyze + hard coverage floors.

## Highlights

- **`analyze --lang`**: `python` (AST), `javascript`, `typescript`, `go`, `rust`, `ruby`, `auto`
- **Coverage gate**: `python3 scripts/coverage_report.py --gate` (CI `coverage-gate` required by `ci-ok`)
- Soft report remains available without floors

## Install

```bash
git clone --branch v0.5.0 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh && bash install.sh
python3 scripts/orchestra.py analyze --path . --lang auto --out /tmp/orch-an
```
