---
name: orchestra
description: "Structure code, modules, pipelines, and agent systems using traditional esoteric correspondence maps (Tree of Life, alchemy, runes, planetary spheres, I Ching, Solomonic ranks, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic). Use when the user wants dual-named architecture skeletons, symbolic hierarchy for software, fail-closed mapping, automatic Mermaid/HTML/JSON diagrams, repo analyze→map→optimize plans, or Hermes/OpenClaw skill-style packaging for Abraxas Orchestra."
version: 0.4.1
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
python3 scripts/orchestra.py analyze   --path DIR [-f FRAMEWORK] [-o OVERLAY] [--out DIR]
python3 scripts/orchestra.py optimize  --from analysis.json [--out DIR] [--min-strength ADEQUATE]
python3 scripts/orchestra.py optimize  --from analysis.json --apply
python3 scripts/orchestra.py optimize  --from analysis.json --apply --confirm [--backup-dir DIR] [--refresh] [--steps IDS] [--actions NAMES]
```

## Analyze → map → optimize

1. **`analyze --path DIR`** — read-only OBSERVED import graph (Python). Writes `analysis.json` + diagram bundle when `--out` is set.
2. **`-f FRAMEWORK`** — propose fail-closed mappings (`STRONG`/`ADEQUATE`/`WEAK`/`FORCED`). Exit `1` if WEAK/FORCED present; `2` on NOT_COMPUTABLE.
3. **`optimize --from analysis.json`** — plan only by default (no tree writes).
4. **`--apply`** — dry-run of `safe_apply` mechanical moves (rename / package promote / single-file flatten); **`--apply --confirm`** writes after backup. FORCED blocks apply.
5. **`--steps` / `--actions`** — apply only listed step ids or action names.
6. **`--refresh`** — after confirmed apply, re-analyze and write refreshed `analysis.json` beside the backup.

Do not invent symbolic loci. Do not silently “improve” FORCED/WEAK maps.

## Automatic diagrammatic emission

Whenever this skill emits architecture structure **or** the operator/agent needs a diagram (Mermaid, module graph, pipeline map):

1. Prefer `structure` / `project` with `--out DIR` — diagrams write **automatically** beside the skeleton:
   - `architecture.html` — interactive
   - `architecture.json` — agent graph (`orchestra-diagram.v1`)
   - `architecture.mmd` — Mermaid flowchart (paste into docs/PRs)
2. Or call `diagram` / `diagrammit` explicitly for graph-only emission.
3. `analyze --out` also emits the same diagram trio from the observed import graph.
4. Do **not** invent a separate ad-hoc Mermaid sketch when Orchestra can emit from loci or analysis.

Agents: if you would write a Mermaid block for Orchestra-mapped code, run diagram emission first and use `architecture.mmd` (or embed its content).

## Mandatory sequence

1. Identify functional concerns (modules, stages, domains) — or `analyze` an existing tree.
2. Choose primary framework (and optional overlay).
3. Prefer `structure` / `project` with `--out` (auto-diagram), `diagram`, or `analyze`/`optimize`.
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

Local stdlib CLI. No network I/O in structure/analyze/optimize paths. Analyze writes only under `--out`. Optimize apply requires `--confirm` and backs up before rename/promote/flatten.
