# OpenClaw packaging

Abraxas Orchestra is a **hermes-openclaw-skill**.

## Install

```bash
bash install.sh --target ~/.openclaw/skills/orchestra
```

Default without `--target` installs to Hermes (`~/.hermes/skills/orchestra`).

## Discovery

- Entry: `SKILL.md` (name `orchestra`)
- Manifest: `orchestra.manifest.yaml`
- CLI: `scripts/orchestra.py`
- Runtime gate: Python 3.11+ on PATH (`metadata.openclaw.requires.bins`)

## State isolation

Keep mutable runtime state outside the skill install directory. The skill package is treated as read-mostly after install.

## Validation

```bash
python3 ~/.openclaw/skills/orchestra/scripts/orchestra.py check
```

## Community registries

See `docs/COMMUNITY.md` for Agent Skills spec alignment, license gaps, and pre-publish checklist.
