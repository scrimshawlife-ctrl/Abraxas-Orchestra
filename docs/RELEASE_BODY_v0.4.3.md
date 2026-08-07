# Orchestra 0.4.3

Soft quality / coverage reporting (no hard floor).

## Highlights

- `python3 scripts/coverage_report.py` — import check, test linkage, in-process line coverage
- CI job `coverage-soft` uploads the report; **`ci-ok` does not require it**
- Hard coverage gates remain deferred (see ROADMAP)

## Install

```bash
git clone --branch v0.4.3 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh && bash install.sh
```
