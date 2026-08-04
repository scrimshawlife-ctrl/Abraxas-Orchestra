---
name: orchestra
description: "Structure code, modules, pipelines, and agent systems using traditional esoteric correspondence maps (Tree of Life, alchemy, runes, planetary spheres, I Ching, Solomonic ranks, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic). Use when the user wants dual-named architecture skeletons, symbolic hierarchy for software, fail-closed mapping, or Hermes/OpenClaw skill-style packaging for Abraxas Orchestra."
version: 0.1.3
license: Apache-2.0
metadata:
  openclaw:
    requires:
      bins: [python3]
    os: [darwin, linux]
    emoji: "🎼"
---

# Abraxas Orchestra

Hermes + OpenClaw **coding-agent skill** for symbolic code architecture.

Hosts: **Hermes**, **OpenClaw**. Same contract, different install roots.

Production freeze checklist: `docs/COMPLETION.md`. Public debut: `docs/PUBLIC_RELEASE.md`. Security audit: `docs/SECURITY_AUDIT.md`.

## When to use

- Map software structure onto a traditional correspondence system
- Emit dual-named module skeletons (mechanical primary, symbolic secondary)
- Overlay Chaos Magic or a second framework on a primary map
- Fail closed when a mapping is forced or non-computable

## When not to use

- Runtime ritual / operative magic systems
- Network services, secret brokers, or remote code installers
- Inventing symbolic loci to force a map to fit

## Mandatory sequence

1. Identify functional concerns (modules, stages, domains).
2. Choose primary framework (and optional overlay).
3. Prefer `scripts/orchestra.py do structure` / `do project`.
4. Emit correspondence table JSON matching schema.
5. Stop on `NOT_COMPUTABLE` or label `FORCED` — do not invent loci.

## Frameworks

Canonical loci: `schemas/frameworks.v1.json`

Eleven maps: tree-of-life, alchemical-stages, elder-futhark, planetary-spheres, iching-hexagrams, solomonic, peircean-signs, numogram, sacred-geometry, enochian, chaos-magic.

Detailed tables live in `references/`. Loci for CLI emission live in `schemas/frameworks.v1.json`. Load markdown references when the chosen framework requires detail. Keep active context lean.

## Agent posture

See `references/agent-posture.md` when implementing code under this skill.

## Install

```bash
bash install.sh --dry-run
bash install.sh
# OpenClaw:
bash install.sh --target ~/.openclaw/skills/orchestra
```

Installer refuses system paths and targets outside `$HOME` unless `--allow-outside-home`.

## Security

Local stdlib CLI. No network I/O in structure paths. See `docs/SECURITY.md` and `.github/SECURITY.md`.
