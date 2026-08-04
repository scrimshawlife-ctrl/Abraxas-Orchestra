# Contributing

Private skill package. External PRs are not solicited by default.

## Local checks before any change

```bash
bash scripts/smoke.sh
```

Must exit 0.

## Adding a framework

Update **together** (single commit preferred):

1. `references/<key>.md` — dual-naming table + architectural intent  
2. `scripts/orchestra.py` — `FRAMEWORKS` entry  
3. `schemas/correspondence-table.v1.schema.json` — framework enum  
4. `orchestra.manifest.yaml` — frameworks list  
5. `install.sh` — required refs list  
6. `SKILL.md` — supported frameworks section  
7. `CHANGELOG.md`

Then: `python3 scripts/orchestra.py check` and `bash scripts/smoke.sh`.

## Agent posture

When filling skeletons, follow `references/agent-posture.md`.

## Binary assets

GitHub connector text pushes cannot carry JPEG/WebP. Commit `assets/hero.jpg` from a local git client. Specs: `assets/README.md`.

## License

Proprietary evaluation terms (`LICENSE`). Do not assume OSI redistribution rights.
