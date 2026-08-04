---
name: orchestra
description: "Structure code, modules, pipelines, and agent systems using traditional esoteric correspondence maps (Tree of Life, alchemy, runes, planetary spheres, I Ching, Solomonic ranks, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic). Use when the user wants dual-named architecture skeletons, symbolic hierarchy for software, fail-closed mapping, automatic Mermaid/HTML/JSON diagrams, or Hermes/OpenClaw skill-style packaging for Abraxas Orchestra."
version: 0.1.6
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

## Commands

```text
python3 scripts/orchestra.py check
python3 scripts/orchestra.py list
python3 scripts/orchestra.py structure -f <framework> [-c concerns] [-o overlay] [--out DIR]
python3 scripts/orchestra.py project   -f <framework> [-c concerns] [-o overlay] [--out DIR]
python3 scripts/orchestra.py diagram   -f <framework> [-c concerns] [-o overlay] [--out DIR]
```

## Automatic diagrammatic emission

Whenever this skill emits architecture structure **or** the operator/agent needs a diagram (Mermaid, module graph, pipeline map):

1. Prefer `structure` / `project` with `--out DIR` — diagrams write **automatically** beside the skeleton:
   - `architecture.html` — interactive
   - `architecture.json` — agent graph (`orchestra-diagram.v1`)
   - `architecture.mmd` — Mermaid flowchart (paste into docs/PRs)
2. Or call `diagram` / `diagrammit` explicitly for graph-only emission.
3. Do **not** invent a separate ad-hoc Mermaid sketch when Orchestra can emit from loci.

Agents: if you would write a Mermaid block for Orchestra-mapped code, run diagram emission first and use `architecture.mmd` (or embed its content).

## Mandatory sequence

1. Identify functional concerns (modules, stages, domains).
2. Choose primary framework (and optional overlay).
3. Prefer `scripts/orchestra.py structure` / `project` with `--out` (auto-diagram) or `diagram`.
4. Emit correspondence table JSON matching schema; diagrams auto-write on `--out`.
5. Stop on `NOT_COMPUTABLE` or label `FORCED` — do not invent loci.

## Frameworks

Canonical loci: `schemas/frameworks.v1.json`

Eleven maps: tree-of-life, alchemical-stages, elder-futhark, planetary-spheres, iching-hexagrams, solomonic, peircean-signs, numogram, sacred-geometry, enochian, chaos-magic.

## Install

```bash
bash install.sh --dry-run && bash install.sh
```

## Security

Local stdlib CLI. No network I/O in structure paths.
