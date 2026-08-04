# OpenClaw Edition — Abraxas Orchestra

This document describes the OpenClaw-specific packaging and install path for the Orchestra skill.

## Relationship to Hermes Edition

The core contract (`SKILL.md`), reference mappings, dual-naming rules, fail-closed posture, and CLI behavior are shared.

Differences are limited to:
- Install location
- Mutable runtime state location
- Installer tooling / discovery mechanism
- Optional branch packaging

## Target install

```bash
openclaw skills install git:scrimshawlife-ctrl/Abraxas-Orchestra-Hermes@openclaw --global
```

Default install path:
```
~/.openclaw/skills/orchestra
```

## Manual install (until openclaw branch is cut)

From a clone of `main`:

```bash
./install.sh --target ~/.openclaw/skills/orchestra
python3 ~/.openclaw/skills/orchestra/scripts/orchestra.py check
python3 ~/.openclaw/skills/orchestra/scripts/orchestra.py do list-frameworks
```

The installer is host-agnostic; only the target directory differs.

## State isolation

Mutable runtime state (ledgers, temporary correspondence caches, operator preferences) must live outside the skill package directory. The skill package itself remains read-only after installation.

Recommended state root:
```
~/.openclaw/state/orchestra/
```

## Validation before activation

The installer (and `check`) verify:
- Presence of `SKILL.md`
- Presence of `orchestra.manifest.yaml`
- Presence of primary reference files under `references/`
- Version consistency between `VERSION` and the manifest
- CLI syntax / basic integrity

## Branch status

A permanent `openclaw` branch is planned. Until it is cut, the `main` surface is usable via `--target` as shown above. When the branch exists it will carry any OpenClaw-specific path defaults and discovery metadata while keeping the creative corpus aligned with Hermes.

## CLI surface (identical to Hermes)

```bash
python3 scripts/orchestra.py do list-frameworks
python3 scripts/orchestra.py do structure -f tree-of-life -c "intake,synthesis,output" --out ./out
python3 scripts/orchestra.py do project -f numogram --out ./out-projected
python3 scripts/orchestra.py check
```
