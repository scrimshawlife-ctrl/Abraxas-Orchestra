# Abraxas Orchestra — Hermes Wizard Design

**Status:** Approved  
**Date:** 2026-08-08  
**Version target:** 0.8.0 (minor — new public CLI surface)  
**Hosts:** Hermes (CLI, gateway, Desktop), OpenClaw  
**Repository:** Abraxas Orchestra (`orchestra` skill)

## Intent

Add a guided **wizard** that collapses Orchestra’s meta / emit / repo decision tree into a single, testable path so Hermes agents (and humans) do not freestyle Mermaid, invent loci, or assemble flags by memory.

The wizard is **Approach C**:

1. A thin **CLI command** (`wizard`) registered on the existing `CommandRouter` — interactive for real TTYs, fully non-interactive for agents.
2. A **Hermes routing protocol** in `SKILL.md` / agent posture: chat-driven Q&A → answers JSON → `wizard --print-only` / `--run`.

## Non-goals (YAGNI)

- Native Electron multi-step form inside Hermes Desktop UI
- Silent `optimize --apply --confirm` without explicit operator intent
- Network install / remote repo fetch
- Inventing symbolic loci outside `schemas/frameworks.v1.json`
- Reimplementing structure / analyze / optimize logic inside the wizard

## Context

Orchestra 0.7.0 already ships:

| Group | Commands |
|-------|----------|
| **meta** | `check`, `list` |
| **emit** | `structure`, `project`, `diagram` |
| **repo** | `analyze`, `optimize` |

Hermes Desktop uses the **same agent, skills, and tools** as CLI/gateway. Skill work runs via tool/terminal invocation — **not** a dedicated Orchestra Desktop panel. Interactive stdin wizards are unreliable on the agent tool path; chat + non-interactive CLI is the Desktop-safe contract.

## Purpose & CLI surface

```text
python3 scripts/orchestra.py wizard [options]
```

| Mode | Flags | Behavior |
|------|--------|----------|
| Interactive | default when TTY and no complete answers | Numbered prompts; safe defaults |
| Non-interactive | `--answers PATH\|-` and/or `--preset NAME` | Fully determined; exit non-zero on invalid |
| Plan only | `--print-only` (**default**) | Print resolved plan + exact argv; no mutation beyond printing |
| Execute | `--run` | Dispatch resolved command via the same router handlers |
| Machine out | `--json` | Emit `orchestra-wizard-plan.v1` JSON on stdout |
| Presets | `--preset greenfield\|observe\|map\|optimize-plan` | Seed answers; overridable by `--answers` |

**Safety defaults:**

- Prefer `--print-only`. `--run` is explicit.
- Never set optimize `--confirm` unless answers include `confirm_apply: true`.
- FORCED / WEAK maps still fail closed via existing analyze/optimize handlers.
- Non-TTY without enough answers to resolve → exit `2` with guidance to use `--answers` / chat (Desktop-safe).

## Step flow

Wizard resolves to **one primary Orchestra command** per invocation (sequence plans may be printed as ordered argv lists in a later revision; v1 is single-shot).

```text
1. Intent
   greenfield | observe | map | optimize-plan
   | optimize-apply-dry | optimize-apply-confirm | check | list

2. greenfield (emit)
   → framework (required)
   → concerns (optional; default = framework core_collapse, else default_loci mechanical names)
   → overlay (optional)
   → emit_mode: structure | project | diagram
   → out (required for --run; warn if missing on --print-only)

3. observe | map (repo analyze)
   → path (required)
   → framework (optional for observe; required for map)
   → overlay (optional)
   → lang: python | auto | javascript | typescript | go | rust | ruby (default python)
   → out (recommended)

4. optimize-*
   → from: analysis.json path (required)
   → out (optional for plan)
   → min_strength (default ADEQUATE)
   → apply / confirm_apply
   → refresh / steps / actions (optional)

5. Resolve → plan (argv + rationale + safety notes)

6. If --run → in-process CommandRouter.dispatch(resolved argv)
```

### Presets

| Preset | Intent | Seed defaults |
|--------|--------|----------------|
| `greenfield` | greenfield | `emit_mode=structure`, `framework=tree-of-life`, concerns = that framework’s `core_collapse` |
| `observe` | observe | analyze without `-f`; requires path |
| `map` | map | analyze with framework; requires path + framework |
| `optimize-plan` | optimize-plan | plan-only optimize; requires `from` |

## Answers schema (`orchestra-wizard-answers.v1`)

```json
{
  "schema": "orchestra-wizard-answers.v1",
  "intent": "greenfield",
  "framework": "tree-of-life",
  "concerns": ["intent", "intake", "analyze", "store", "output"],
  "overlay": null,
  "emit_mode": "structure",
  "path": null,
  "from": null,
  "out": "/tmp/orch-skel",
  "lang": "python",
  "min_strength": "ADEQUATE",
  "apply": false,
  "confirm_apply": false,
  "refresh": false,
  "steps": null,
  "actions": null
}
```

### Validation rules

| Rule | Exit |
|------|------|
| Missing `schema` or wrong value | 2 |
| Unknown `intent` / `framework` / `emit_mode` / `lang` | 2 |
| Missing required field for intent | 2 (list missing keys) |
| `confirm_apply: true` without `apply: true` | 2 |
| Interactive requested on non-TTY without complete answers | 2 |
| Unknown keys | 2 — **reject** (strict; agent determinism) |

Concerns are free strings at the wizard layer; emission/mapping remains fail-closed in existing commands (do not invent loci in framework tables).

On-disk JSON Schema: `schemas/wizard-answers.v1.schema.json` (document + unit-test contract; required for 0.8.0).

## Plan schema (`orchestra-wizard-plan.v1`)

Printed with `--json` (and used in tests):

```json
{
  "schema": "orchestra-wizard-plan.v1",
  "group": "emit",
  "command": "structure",
  "argv": ["structure", "-f", "tree-of-life", "-c", "intent,intake,analyze,store,output", "--out", "/tmp/orch-skel"],
  "rationale": "Greenfield dual-named skeleton from tree-of-life with core pipeline concerns.",
  "safety": [
    "print-only unless --run",
    "writes only under --out when run",
    "no optimize confirm"
  ],
  "run": false
}
```

Human (default) stdout: short prose + exact invocation:

```text
python3 scripts/orchestra.py structure -f tree-of-life -c "..." --out /tmp/orch-skel
```

## Components

| Piece | Location | Role |
|-------|----------|------|
| Wizard implementation | `scripts/orchestra_wizard.py` | Validate answers, merge presets, build argv, interactive prompts, plan emit |
| CLI entry | `cmd_wizard` in `scripts/orchestra.py` (thin) | Argparse config + call wizard module |
| Router | `build_router()` | Register `wizard` in **meta** group |
| Answers schema | `schemas/wizard-answers.v1.schema.json` | Contract |
| Hermes protocol | `SKILL.md`, `references/agent-posture.md` | Chat → answers → wizard |
| Tests | `tests/test_wizard.py` | Presets, validation, argv resolve, non-TTY, safety |
| Docs | `README.md`, `docs/DESIGN.md`, `CHANGELOG.md` | Discoverability |
| Version | `VERSION`, `SKILL.md`, bump tooling | 0.8.0 when shipping |

**Implementation constraints:**

- Stdlib only (match Orchestra).
- Reuse `_load_frameworks()` and existing handlers; do not duplicate structure/analyze/optimize.
- Prefer in-process `CommandRouter.dispatch(argv)` for `--run`.
- Interactive TTY only when `sys.stdin.isatty()` and answers incomplete.
- Interactive optimize confirm: require typing `CONFIRM` (not a bare yes).

## Hermes + Desktop routing protocol

When the skill activates and the user is unsure, wants guidance, or has not named a concrete command:

1. Prefer **meta → wizard** over freehand architecture or ad-hoc Mermaid.
2. Collect missing fields **in chat, one question at a time** (or accept a full dump if the user already provided everything). Desktop chat is the UX surface; do not open an interactive stdin wizard from the agent tool path.
3. Write answers JSON (temp file under `/tmp` or under a user-chosen `--out` parent).
4. Run `wizard --answers … --print-only` (optionally `--json`).
5. Show the plan; on approval, `wizard --answers … --run` **or** execute the printed argv with the same skill root.
6. Never set `confirm_apply: true` unless the user explicitly requested gated filesystem renames after reviewing an optimize plan.
7. After emit, continue existing agent posture: implement domain logic inside locus contracts; do not stop at empty scaffolds.

Update the Hermes routing table:

| User wants… | Group | Commands |
|-------------|-------|----------|
| Guided path / unsure | **meta** | `wizard` |
| Health / list maps | **meta** | `check`, `list` |
| New skeleton / diagram | **emit** | `structure`, `project`, `diagram` |
| Observe / map / refactor | **repo** | `analyze`, `optimize` |

## Errors & security

| Case | Behavior |
|------|----------|
| Validation failure | stderr message + exit 2 |
| Downstream command failure on `--run` | propagate that command’s exit code |
| Path / write surfaces | unchanged from analyze / optimize / structure (no new network I/O; skill tree not mutated by wizard itself) |
| Optimize apply | dry-run when `apply` true and `confirm_apply` false; writes only when both true (matches CLI) |

## Testing

`tests/test_wizard.py` (stdlib unittest, same style as existing suite):

1. Each preset resolves to expected command name + critical argv tokens.
2. Default plan never includes `--confirm`.
3. `confirm_apply` without `apply` rejected.
4. Unknown framework / intent rejected.
5. Non-TTY interactive path exits 2 without hanging.
6. Greenfield `--run` without `out` fails; print-only may warn but still emit plan with missing-out note (implementation: **fail resolve if out missing for greenfield when `--run`; on print-only include warning in plan.safety**).
7. Smoke: write a temp answers file for observe + `tests/fixtures/mini_pkg`, then `orchestra.py wizard --answers <file> --print-only` succeeds (argv contains `analyze` and `--path`).

Extend `scripts/smoke.sh` with one non-interactive wizard print-only invocation if smoke stays under existing time budget.

## Versioning & release

- Ship as **0.8.0** (new command + skill contract).
- Follow `docs/SEMVER.md` and `scripts/bump_version.py`.
- Merge via PR with green `ci-ok`.

## Implementation order (for writing-plans)

1. `orchestra_wizard.py` — pure resolve/validate + plan structs (unit-testable).
2. Wire `wizard` command + argparse; register meta group.
3. Interactive prompts (TTY only).
4. `--run` via router dispatch.
5. Schema file + tests + smoke line.
6. SKILL.md / agent-posture / README / DESIGN / CHANGELOG / VERSION.

## Success criteria

- Hermes Desktop chat can complete a greenfield or observe flow without any stdin interactive prompts.
- Agents produce the same argv a careful human would for structure/analyze/optimize-plan.
- No optimize confirm without explicit answers.
- Existing commands and fail-closed mapping behavior unchanged.
- `python3 scripts/orchestra.py check` and suite remain green.
