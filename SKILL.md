---
name: orchestra
description: "Structure code, modules, pipelines, and agent systems using traditional esoteric correspondence maps (Tree of Life, alchemy, runes, planetary spheres, I Ching, Solomonic ranks, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic). Use when the user wants dual-named architecture skeletons, symbolic hierarchy for software, fail-closed mapping, automatic Mermaid/HTML/JSON diagrams, repo analyze→map→optimize plans, guided wizard plans, or Hermes/OpenClaw skill-style packaging for Abraxas Orchestra. Route work through meta (check/list/wizard), emit (structure/project/diagram), or repo (analyze/optimize) — same groups as the CLI CommandRouter. Prefer wizard when unsure or collecting fields in Desktop chat."
version: 0.8.0
license: Apache-2.0
metadata:
  openclaw:
    requires:
      bins: [python3]
    os: [darwin, linux]
    emoji: "🎼"
  hermes:
    command_router: true
    groups: [meta, emit, repo]
---

# Abraxas Orchestra

Hermes + OpenClaw **coding-agent skill** for symbolic code architecture.

Hosts: **Hermes**, **OpenClaw**. Same contract, different install roots.

CLI routing: `scripts/orchestra_router.py` — **meta** · **emit** · **repo**.  
Hermes agents must pick a group first, then a command inside it (do not invent freehand Mermaid or loci).

Entry (after install):

```bash
python3 ~/.hermes/skills/orchestra/scripts/orchestra.py <command> ...
# or from skill root:
python3 scripts/orchestra.py <command> ...
```

---

## Hermes routing (required)

When this skill activates, **route the user request** into exactly one primary group:

| Group | When to use | Commands |
|-------|-------------|----------|
| **meta** | Integrity, discovery, “what maps exist?”, guided path | `check`, `list`, `wizard` |
| **emit** | Greenfield / skeleton / diagrams from a framework | `structure`, `project`, `diagram` |
| **repo** | Existing codebase observe → map → plan → gated moves | `analyze`, `optimize` |
| Guided path / unsure / Desktop chat collect | **meta** | `wizard` |

Rules:

1. Prefer **one group per turn** unless the user clearly needs a sequence (e.g. emit then repo).
2. Inside a group, pick the smallest command that satisfies the ask.
3. Never invent symbolic loci — only `schemas/frameworks.v1.json`.
4. Prefer CLI emission over freehand architecture diagrams.
5. When unsure which flags/command, prefer **meta** `wizard` over freestyle argv.

### Decision tree

```text
Need to verify install / list maps?
  → meta: check | list

Unsure of path / collecting fields in Desktop chat?
  → meta: wizard  (chat → --answers; print-only default)

Building new dual-named layout or diagram from a framework?
  → emit:
      structure  — full skeleton + auto-diagrams on --out
      project    — same, with pragmatic collapse of oversized maps
      diagram    — graph only (HTML/JSON/Mermaid)

Reading or reshaping an existing tree?
  → repo:
      analyze   — OBSERVED graph; optional -f map (fail-closed)
      optimize  — plan from analysis.json; --apply --confirm to write
```

---

## Wizard (Hermes + Desktop)

When the operator is unsure or you would otherwise freestyle flags:

1. Collect missing fields **in chat** (one at a time). Do **not** use interactive stdin.
2. Write `orchestra-wizard-answers.v1` JSON to a temp file.
3. `python3 scripts/orchestra.py wizard --answers FILE --print-only` (or `--json`).
4. On approval: `wizard --answers FILE --run` or run the printed argv.
5. Never set `confirm_apply: true` unless the user explicitly approved gated renames.

```bash
python3 scripts/orchestra.py wizard --preset greenfield --answers answers.json --print-only
python3 scripts/orchestra.py wizard --answers answers.json --run
```

---

## Commands by group

### meta

```text
python3 scripts/orchestra.py check
python3 scripts/orchestra.py list
python3 scripts/orchestra.py wizard [--answers FILE] [--preset NAME] [--print-only|--run] [--json]
```

- **check** — skill integrity (schemas, version parity surface).
- **list** — frameworks available (alias: `list-frameworks`).
- **wizard** — guided plan from answers/preset; print-only by default; `--run` dispatches in-process. Desktop: chat collect → `--answers` (no interactive stdin).

### emit

```text
python3 scripts/orchestra.py structure -f <framework> [-c concerns] [-o overlay] [--out DIR]
python3 scripts/orchestra.py project   -f <framework> [-c concerns] [-o overlay] [--out DIR]
python3 scripts/orchestra.py diagram   -f <framework> [-c concerns] [-o overlay] [--out DIR] [--project]
```

- **structure** — dual-named skeleton + correspondence table; stage stubs carry **ALLOWED** / **FORBIDDEN** locus contracts (`run()` + `contract()`); multi-stage `--out` also writes `pipeline.py`; auto-writes diagrams.
- **project** — like structure, but collapses oversized / forced maps (explicit projection).
- **diagram** — graph only (`diagrammit` alias); optional `--project` projection.

Shared flags: `-f` framework (required), `-c` concerns, `-o` overlay, `--out` directory.

### repo

```text
python3 scripts/orchestra.py analyze  --path DIR [-f FRAMEWORK] [-o OVERLAY] [--lang python|auto|…] [--out DIR]
python3 scripts/orchestra.py optimize --from analysis.json [--out DIR] [--min-strength ADEQUATE]
python3 scripts/orchestra.py optimize --from analysis.json --apply
python3 scripts/orchestra.py optimize --from analysis.json --apply --confirm [--backup-dir DIR] [--refresh] [--steps IDS] [--actions NAMES]
```

#### analyze → map → optimize

1. **`analyze --path DIR`** — read-only OBSERVED import graph.  
   - `--lang python` (default) full AST; `javascript` / `typescript` / `go` / `rust` / `ruby` / `auto` for multi-lang.  
   - Always embeds **`metrics`** (map quality, import cycles, responsibility mix); stderr prints `# metrics: …`.  
   - Writes `analysis.json` + `structure-metrics.json` + diagram trio when `--out` is set.
2. **`-f FRAMEWORK`** — fail-closed mappings (`STRONG` / `ADEQUATE` / `WEAK` / `FORCED`). Exit `1` if WEAK/FORCED; `2` on NOT_COMPUTABLE.
3. **`optimize --from analysis.json`** — plan only by default (no tree writes).
4. **`--apply`** — dry-run of `safe_apply` (rename / promote / flatten); **`--apply --confirm`** writes after backup. FORCED blocks apply.
5. **`--steps` / `--actions`** — selective apply; **`--refresh`** re-analyzes after confirmed apply.

Do not invent symbolic loci. Do not silently “improve” FORCED/WEAK maps.

---

## Automatic diagrammatic emission (emit + repo)

Whenever this skill emits architecture **or** the operator needs a diagram:

1. Prefer **emit** `structure` / `project` with `--out DIR` — diagrams write automatically:
   - `architecture.html` — interactive  
   - `architecture.json` — agent graph (`orchestra-diagram.v1`)  
   - `architecture.mmd` — Mermaid  
2. Or **emit** `diagram` for graph-only.
3. **repo** `analyze --out` emits the same trio from the observed graph.
4. Do **not** invent ad-hoc Mermaid when Orchestra can emit from loci or analysis.

Agents: if you would write a Mermaid block for Orchestra-mapped code, run emission first and use `architecture.mmd`.

---

## Mandatory sequence (Hermes)

1. **Route** to meta / emit / repo (table above). Prefer **meta** `wizard` when flags/path are unclear.
2. Identify functional concerns — or **repo** `analyze` an existing tree.
3. Choose primary framework (and optional overlay); **meta** `list` if unsure.
4. Prefer **emit** with `--out` (auto-diagram) or **repo** analyze/optimize.
5. Emit correspondence table JSON matching schema; diagrams auto-write on `--out`.
6. **Implement domain logic inside each stage’s locus contract** — do not stop at empty scaffolds.
   The map optimizes responsibilities and call direction (see `examples/python-tree-of-life-pipeline/`).
7. Stop on `NOT_COMPUTABLE` or label `FORCED` — do not invent loci.

---

## Frameworks

Canonical loci: `schemas/frameworks.v1.json`

Eleven maps: tree-of-life, alchemical-stages, elder-futhark, planetary-spheres, iching-hexagrams, solomonic, peircean-signs, numogram, sacred-geometry, enochian, chaos-magic.

Fit guide: `docs/FRAMEWORK_FIT.md` · Agent posture: `references/agent-posture.md`

---

## Install (Hermes)

```bash
bash install.sh --dry-run && bash install.sh
# → ~/.hermes/skills/orchestra
```

OpenClaw: `bash install.sh --target ~/.openclaw/skills/orchestra`

---

## Security

Local stdlib CLI. No network I/O in emit/repo structure/analyze/optimize paths. Analyze writes only under `--out`. Optimize apply requires `--confirm` and backs up before rename/promote/flatten.
