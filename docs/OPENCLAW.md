# OpenClaw Edition — Abraxas Orchestra

This document describes the OpenClaw-specific packaging and install path for the Orchestra skill.

## Relationship to Hermes Edition

The core contract (SKILL.md), reference mappings, dual-naming rules, and fail-closed posture are shared.

Differences are limited to:
- Install location
- Mutable runtime state location
- Installer tooling
- Host discovery mechanism

## Branch

The OpenClaw edition lives on the permanent branch `openclaw`.

```
https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes/tree/openclaw
```

## Install Command (target)

```bash
openclaw skills install git:scrimshawlife-ctrl/Abraxas-Orchestra-Hermes@openclaw --global
```

Default install path:
```
~/.openclaw/skills/orchestra
```

## State Isolation

Mutable runtime state (ledgers, temporary correspondence caches, operator preferences) must live outside the skill package directory. The skill package itself remains read-only after installation.

## Validation

Before activation the installer must verify:
- Presence of SKILL.md
- Presence of orchestra.manifest.yaml
- Presence of primary reference files under references/
- Version consistency between VERSION and the manifest

## Status

This document is a design contract for v0.1. Actual OpenClaw branch and installer wiring will be created after the Hermes surface is accepted and the first executable scaffolding is authorized.
