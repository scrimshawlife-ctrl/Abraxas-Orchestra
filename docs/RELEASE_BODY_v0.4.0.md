# Orchestra 0.4.0

Broader gated `safe_apply` beyond mechanical rename.

## Highlights

- **Package promote** — `suggest_boundary` may move `module.py` → `module/__init__.py` when the stem matches the mechanical name
- **Package flatten** — `suggest_flatten` collapses single-file packages (`leaf/__init__.py` → `leaf.py`)
- **Selective apply** — `--steps step-1,step-3` and `--actions suggest_rename,suggest_boundary,suggest_flatten`
- Schema: `schemas/optimize-apply.v1.schema.json`
- `suggest_extract` remains advisory (no content invention)

## Install

```bash
git clone --branch v0.4.0 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh
bash install.sh --dry-run && bash install.sh
```

## Notes

See `CHANGELOG.md` and `docs/RELEASE_NOTES.md`.
