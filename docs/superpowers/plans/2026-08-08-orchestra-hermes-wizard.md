# Orchestra Hermes Wizard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `orchestra wizard` (meta group) — non-interactive `--answers`/`--preset` plan+run for Hermes Desktop/agents, optional TTY interactive mode — targeting Orchestra **0.8.0**.

**Architecture:** Pure stdlib module `scripts/orchestra_wizard.py` validates answers, merges presets, and builds argv plans (`orchestra-wizard-plan.v1`). Thin `cmd_wizard` in `scripts/orchestra.py` registers on `CommandRouter` (meta). `--run` re-enters `build_router().dispatch(plan.argv)` in-process. Hermes chat protocol lives in `SKILL.md` / `agent-posture.md` only (no Desktop Electron form).

**Tech Stack:** Python ≥ 3.11, stdlib only (`argparse`, `json`, `unittest`, `pathlib`). Existing `CommandRouter` / `orchestra.py` handlers. Spec: `docs/superpowers/specs/2026-08-08-orchestra-hermes-wizard-design.md`.

## Global Constraints

- Stdlib only — no new third-party dependencies.
- Do not invent loci; frameworks only from `schemas/frameworks.v1.json` via existing `_load_frameworks` / `FRAMEWORKS`.
- Default is **print-only**; `--run` is explicit.
- Never emit optimize `--confirm` unless answers have `confirm_apply: true` (and `apply: true`).
- Non-TTY without complete answers → exit `2` (no hang on `input()`).
- Unknown answer keys rejected (strict).
- Version bump to **0.8.0** only in the final docs/version task (after feature works at 0.7.0 code path, or bump early if version-parity requires — prefer implement under current VERSION then `bump_version.py minor` last).
- Preserve fail-closed analyze/optimize behavior; wizard only builds argv.
- Tests: `python3 -m unittest` (no pytest required).

## File map

| File | Responsibility |
|------|----------------|
| `scripts/orchestra_wizard.py` | Answers merge/validate, plan resolve, interactive prompts, format human/json plan |
| `scripts/orchestra.py` | `cmd_wizard`, `_add_wizard_args`, register `wizard` in `build_router()`; docstring/group comment |
| `schemas/wizard-answers.v1.schema.json` | JSON Schema for answers contract |
| `tests/test_wizard.py` | Unit + CLI subprocess tests |
| `scripts/smoke.sh` | One non-interactive wizard print-only line |
| `SKILL.md`, `references/agent-posture.md` | Hermes routing: prefer wizard when unsure; Desktop chat protocol |
| `README.md`, `docs/DESIGN.md`, `CHANGELOG.md` | Discoverability |
| `VERSION`, `orchestra.manifest.yaml`, `install.sh`, `SKILL.md` version | 0.8.0 parity via `bump_version.py minor` |

---

### Task 1: Core resolve library (TDD)

**Files:**
- Create: `scripts/orchestra_wizard.py`
- Create: `tests/test_wizard.py`
- Modify: none yet (import frameworks by loading schema path the same way orchestra does, or accept `frameworks` dict injection for tests)

**Interfaces:**
- Consumes: framework dict shaped like `orchestra.FRAMEWORKS` (`default_loci` list of tuples, `core_collapse` list)
- Produces:
  - `ANSWERS_SCHEMA = "orchestra-wizard-answers.v1"`
  - `PLAN_SCHEMA = "orchestra-wizard-plan.v1"`
  - `INTENTS`, `PRESETS`, `EMIT_MODES`, `LANGS` constants
  - `class WizardError(Exception)` with `.message` and optional `.missing: list[str]`
  - `def load_answers(path_or_dash: str) -> dict`  # path or `-` for stdin
  - `def merge_preset(preset: str | None, answers: dict | None) -> dict`
  - `def validate_answers(answers: dict, frameworks: dict) -> dict`  # returns normalized copy
  - `def resolve_plan(answers: dict, frameworks: dict, *, run: bool = False) -> dict`  # plan dict
  - `def format_plan_human(plan: dict, skill_root_hint: str = "scripts/orchestra.py") -> str`
  - `def format_plan_json(plan: dict) -> str`

- [ ] **Step 1: Write failing unit tests for resolve/validate**

Create `tests/test_wizard.py`:

```python
#!/usr/bin/env python3
"""Tests for orchestra wizard — stdlib only."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from orchestra_wizard import (  # noqa: E402
    ANSWERS_SCHEMA,
    WizardError,
    merge_preset,
    resolve_plan,
    validate_answers,
)

# Minimal frameworks fixture (tree-of-life shaped)
FW = {
    "tree-of-life": {
        "title": "Tree of Life",
        "reference": "references/tree-of-life-mappings.md",
        "default_loci": [
            ("intent", "kether", "entry"),
            ("intake", "chokmah", "in"),
            ("analyze", "hod", "score"),
            ("store", "yesod", "store"),
            ("output", "malkuth", "out"),
            ("synthesis", "tiphareth", "mid"),
        ],
        "core_collapse": ["intent", "synthesis", "output"],
    },
    "alchemical-stages": {
        "title": "Alchemical Stages",
        "reference": "references/alchemical-stages.md",
        "default_loci": [
            ("raw_ingest", "nigredo", ""),
            ("illuminate", "citrinitas", ""),
            ("coagulate", "rubedo", ""),
        ],
        "core_collapse": ["raw_ingest", "illuminate", "coagulate"],
    },
}


class TestWizardResolve(unittest.TestCase):
    def test_preset_greenfield_argv(self) -> None:
        raw = merge_preset("greenfield", None)
        ans = validate_answers({**raw, "out": "/tmp/skel"}, FW)
        plan = resolve_plan(ans, FW, run=False)
        self.assertEqual(plan["schema"], "orchestra-wizard-plan.v1")
        self.assertEqual(plan["group"], "emit")
        self.assertEqual(plan["command"], "structure")
        self.assertEqual(plan["argv"][0], "structure")
        self.assertIn("-f", plan["argv"])
        self.assertIn("tree-of-life", plan["argv"])
        self.assertIn("--out", plan["argv"])
        self.assertNotIn("--confirm", plan["argv"])
        self.assertFalse(plan["run"])

    def test_preset_observe_argv(self) -> None:
        raw = merge_preset("observe", {"path": "tests/fixtures/mini_pkg"})
        ans = validate_answers(raw, FW)
        plan = resolve_plan(ans, FW)
        self.assertEqual(plan["command"], "analyze")
        self.assertIn("--path", plan["argv"])
        self.assertNotIn("-f", plan["argv"])

    def test_preset_map_requires_framework(self) -> None:
        raw = merge_preset("map", {"path": "pkg"})
        # map preset should set intent map but still need framework
        with self.assertRaises(WizardError):
            validate_answers(raw, FW)

    def test_map_with_framework(self) -> None:
        raw = merge_preset(
            "map",
            {"path": "pkg", "framework": "tree-of-life", "out": "/tmp/an"},
        )
        ans = validate_answers(raw, FW)
        plan = resolve_plan(ans, FW)
        self.assertEqual(plan["command"], "analyze")
        self.assertIn("-f", plan["argv"])
        self.assertIn("tree-of-life", plan["argv"])

    def test_optimize_plan_no_confirm(self) -> None:
        raw = merge_preset(
            "optimize-plan",
            {"from": "/tmp/analysis.json", "out": "/tmp/plan"},
        )
        ans = validate_answers(raw, FW)
        plan = resolve_plan(ans, FW)
        self.assertEqual(plan["command"], "optimize")
        self.assertIn("--from", plan["argv"])
        self.assertNotIn("--apply", plan["argv"])
        self.assertNotIn("--confirm", plan["argv"])

    def test_confirm_apply_without_apply_rejected(self) -> None:
        with self.assertRaises(WizardError):
            validate_answers(
                {
                    "schema": ANSWERS_SCHEMA,
                    "intent": "optimize-apply-confirm",
                    "from": "/tmp/a.json",
                    "apply": False,
                    "confirm_apply": True,
                },
                FW,
            )

    def test_unknown_framework_rejected(self) -> None:
        with self.assertRaises(WizardError):
            validate_answers(
                {
                    "schema": ANSWERS_SCHEMA,
                    "intent": "greenfield",
                    "framework": "not-real",
                    "out": "/tmp/x",
                },
                FW,
            )

    def test_unknown_key_rejected(self) -> None:
        with self.assertRaises(WizardError):
            validate_answers(
                {
                    "schema": ANSWERS_SCHEMA,
                    "intent": "list",
                    "extra_junk": True,
                },
                FW,
            )

    def test_greenfield_run_requires_out(self) -> None:
        ans = validate_answers(
            {
                "schema": ANSWERS_SCHEMA,
                "intent": "greenfield",
                "framework": "tree-of-life",
                "emit_mode": "structure",
            },
            FW,
        )
        with self.assertRaises(WizardError):
            resolve_plan(ans, FW, run=True)
        plan = resolve_plan(ans, FW, run=False)
        self.assertTrue(any("out" in s.lower() for s in plan["safety"]))

    def test_optimize_apply_confirm_argv(self) -> None:
        ans = validate_answers(
            {
                "schema": ANSWERS_SCHEMA,
                "intent": "optimize-apply-confirm",
                "from": "/tmp/a.json",
                "apply": True,
                "confirm_apply": True,
            },
            FW,
        )
        plan = resolve_plan(ans, FW)
        self.assertIn("--apply", plan["argv"])
        self.assertIn("--confirm", plan["argv"])

    def test_check_and_list(self) -> None:
        for intent, cmd in (("check", "check"), ("list", "list")):
            ans = validate_answers(
                {"schema": ANSWERS_SCHEMA, "intent": intent}, FW
            )
            plan = resolve_plan(ans, FW)
            self.assertEqual(plan["command"], cmd)
            self.assertEqual(plan["argv"], [cmd])
            self.assertEqual(plan["group"], "meta")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests — expect fail (module missing)**

```bash
cd /home/scrimshawlife/Abraxas-Orchestra
python3 -m unittest tests.test_wizard -v
```

Expected: `ModuleNotFoundError: No module named 'orchestra_wizard'` (or import error).

- [ ] **Step 3: Implement `scripts/orchestra_wizard.py`**

Implement full module (stdlib only). Critical logic:

```python
#!/usr/bin/env python3
"""Abraxas Orchestra wizard — guided plan/resolve for Hermes + CLI.

Stdlib only. Does not reimplement structure/analyze/optimize.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ANSWERS_SCHEMA = "orchestra-wizard-answers.v1"
PLAN_SCHEMA = "orchestra-wizard-plan.v1"

INTENTS = frozenset({
    "greenfield",
    "observe",
    "map",
    "optimize-plan",
    "optimize-apply-dry",
    "optimize-apply-confirm",
    "check",
    "list",
})
EMIT_MODES = frozenset({"structure", "project", "diagram"})
LANGS = frozenset({
    "python", "auto", "javascript", "typescript", "go", "rust", "ruby",
})
ALLOWED_KEYS = frozenset({
    "schema", "intent", "framework", "concerns", "overlay", "emit_mode",
    "path", "from", "out", "lang", "min_strength", "apply", "confirm_apply",
    "refresh", "steps", "actions",
})
MIN_STRENGTHS = frozenset({"STRONG", "ADEQUATE", "WEAK", "FORCED"})

PRESETS: dict[str, dict[str, Any]] = {
    "greenfield": {
        "schema": ANSWERS_SCHEMA,
        "intent": "greenfield",
        "framework": "tree-of-life",
        "emit_mode": "structure",
    },
    "observe": {
        "schema": ANSWERS_SCHEMA,
        "intent": "observe",
    },
    "map": {
        "schema": ANSWERS_SCHEMA,
        "intent": "map",
    },
    "optimize-plan": {
        "schema": ANSWERS_SCHEMA,
        "intent": "optimize-plan",
        "apply": False,
        "confirm_apply": False,
    },
}


class WizardError(Exception):
    def __init__(self, message: str, missing: list[str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.missing = missing or []


def load_answers(path_or_dash: str) -> dict[str, Any]:
    if path_or_dash == "-":
        text = sys.stdin.read()
    else:
        text = Path(path_or_dash).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise WizardError("answers must be a JSON object")
    return data


def merge_preset(preset: str | None, answers: dict[str, Any] | None) -> dict[str, Any]:
    base: dict[str, Any] = {}
    if preset:
        if preset not in PRESETS:
            raise WizardError(f"unknown preset: {preset}")
        base = dict(PRESETS[preset])
    if answers:
        base.update(answers)
    if "schema" not in base:
        base["schema"] = ANSWERS_SCHEMA
    return base


def validate_answers(answers: dict[str, Any], frameworks: dict[str, Any]) -> dict[str, Any]:
    unknown = set(answers) - ALLOWED_KEYS
    if unknown:
        raise WizardError(f"unknown keys: {sorted(unknown)}")
    if answers.get("schema") != ANSWERS_SCHEMA:
        raise WizardError(f"schema must be {ANSWERS_SCHEMA}")
    intent = answers.get("intent")
    if intent not in INTENTS:
        raise WizardError(f"unknown intent: {intent}")

    out = dict(answers)
    # Defaults
    out.setdefault("apply", False)
    out.setdefault("confirm_apply", False)
    out.setdefault("refresh", False)
    out.setdefault("lang", "python")
    out.setdefault("min_strength", "ADEQUATE")
    out.setdefault("emit_mode", "structure")

    if out["confirm_apply"] and not out["apply"]:
        raise WizardError("confirm_apply requires apply: true")

    if out["lang"] not in LANGS:
        raise WizardError(f"unknown lang: {out['lang']}")
    if out["min_strength"] not in MIN_STRENGTHS:
        raise WizardError(f"unknown min_strength: {out['min_strength']}")
    if out["emit_mode"] not in EMIT_MODES:
        raise WizardError(f"unknown emit_mode: {out['emit_mode']}")

    fw = out.get("framework")
    if fw is not None and fw not in frameworks:
        raise WizardError(f"unknown framework: {fw}")

    # Normalize concerns: list[str] or comma string → list[str] | None
    concerns = out.get("concerns")
    if isinstance(concerns, str):
        out["concerns"] = [c.strip() for c in concerns.split(",") if c.strip()]
    elif concerns is not None and not isinstance(concerns, list):
        raise WizardError("concerns must be list or comma-separated string")

    missing: list[str] = []
    if intent == "greenfield":
        if not fw:
            missing.append("framework")
    elif intent == "observe":
        if not out.get("path"):
            missing.append("path")
    elif intent == "map":
        if not out.get("path"):
            missing.append("path")
        if not fw:
            missing.append("framework")
    elif intent in (
        "optimize-plan",
        "optimize-apply-dry",
        "optimize-apply-confirm",
    ):
        if not out.get("from"):
            missing.append("from")
    # check/list: no extra required

    if intent == "optimize-apply-dry":
        out["apply"] = True
        out["confirm_apply"] = False
    elif intent == "optimize-apply-confirm":
        out["apply"] = True
        out["confirm_apply"] = True

    if missing:
        raise WizardError(f"missing required fields: {missing}", missing=missing)

    # Default concerns for greenfield from core_collapse
    if intent == "greenfield" and not out.get("concerns") and fw:
        collapse = list(frameworks[fw].get("core_collapse") or [])
        if collapse:
            out["concerns"] = collapse
        else:
            out["concerns"] = [m for m, _, _ in frameworks[fw]["default_loci"]]

    return out


def resolve_plan(
    answers: dict[str, Any],
    frameworks: dict[str, Any],
    *,
    run: bool = False,
) -> dict[str, Any]:
    a = answers
    intent = a["intent"]
    safety: list[str] = ["print-only unless --run"]
    argv: list[str]
    group: str
    command: str
    rationale: str

    if intent == "check":
        group, command, argv = "meta", "check", ["check"]
        rationale = "Skill integrity check."
    elif intent == "list":
        group, command, argv = "meta", "list", ["list"]
        rationale = "List available frameworks."
    elif intent == "greenfield":
        mode = a["emit_mode"]
        group, command = "emit", mode
        argv = [mode, "-f", a["framework"]]
        if a.get("overlay"):
            argv.extend(["-o", a["overlay"]])
        concerns = a.get("concerns") or []
        if concerns:
            argv.extend(["-c", ",".join(concerns)])
        if a.get("out"):
            argv.extend(["--out", a["out"]])
        else:
            safety.append("warning: out missing — required for --run")
            if run:
                raise WizardError("greenfield --run requires out")
        rationale = f"Greenfield {mode} from {a['framework']}."
        safety.append("writes only under --out when run")
    elif intent in ("observe", "map"):
        group, command = "repo", "analyze"
        argv = ["analyze", "--path", a["path"]]
        if intent == "map" or a.get("framework"):
            argv.extend(["-f", a["framework"]])
        if a.get("overlay"):
            argv.extend(["-o", a["overlay"]])
        lang = a.get("lang") or "python"
        if lang != "python":
            argv.extend(["--lang", lang])
        if a.get("out"):
            argv.extend(["--out", a["out"]])
        rationale = "Observe import graph" + (
            f" and map onto {a.get('framework')}" if a.get("framework") else " (no framework map)"
        ) + "."
        safety.append("analyze is read-only for source tree; writes only under --out")
    elif intent in (
        "optimize-plan",
        "optimize-apply-dry",
        "optimize-apply-confirm",
    ):
        group, command = "repo", "optimize"
        argv = ["optimize", "--from", a["from"]]
        if a.get("out"):
            argv.extend(["--out", a["out"]])
        ms = a.get("min_strength") or "ADEQUATE"
        if ms != "ADEQUATE":
            argv.extend(["--min-strength", ms])
        if a.get("apply"):
            argv.append("--apply")
            safety.append("apply dry-run unless --confirm")
        if a.get("confirm_apply"):
            argv.append("--confirm")
            safety.append("CONFIRM apply will write after backup")
        else:
            safety.append("no optimize confirm")
        if a.get("refresh"):
            argv.append("--refresh")
        if a.get("steps"):
            steps = a["steps"]
            if isinstance(steps, list):
                steps = ",".join(steps)
            argv.extend(["--steps", steps])
        if a.get("actions"):
            actions = a["actions"]
            if isinstance(actions, list):
                actions = ",".join(actions)
            argv.extend(["--actions", actions])
        rationale = f"Optimize path for intent {intent}."
    else:
        raise WizardError(f"unhandled intent: {intent}")

    if "--confirm" not in argv:
        if "no optimize confirm" not in safety and intent.startswith("optimize"):
            safety.append("no optimize confirm")

    return {
        "schema": PLAN_SCHEMA,
        "group": group,
        "command": command,
        "argv": argv,
        "rationale": rationale,
        "safety": safety,
        "run": run,
    }


def format_plan_json(plan: dict[str, Any]) -> str:
    return json.dumps(plan, indent=2, sort_keys=True) + "\n"


def format_plan_human(plan: dict[str, Any], skill_root_hint: str = "scripts/orchestra.py") -> str:
    parts = [
        f"Orchestra wizard plan — group={plan['group']} command={plan['command']}",
        plan["rationale"],
        "Safety: " + "; ".join(plan["safety"]),
        "",
        f"python3 {skill_root_hint} " + " ".join(_shell_quote(a) for a in plan["argv"]),
        "",
    ]
    if plan.get("run"):
        parts.append("(will execute via --run)")
    else:
        parts.append("Print-only. Re-run with --run to execute.")
    return "\n".join(parts) + "\n"


def _shell_quote(s: str) -> str:
    if not s or any(c in s for c in ' \t\n"\'$&|;<>'):
        return json.dumps(s)
    return s


# Interactive helpers used in Task 3
def interactive_collect(frameworks: dict[str, Any]) -> dict[str, Any]:
    """TTY prompts → answers dict. Caller must ensure stdin is a TTY."""
    print("Abraxas Orchestra wizard")
    intents = sorted(INTENTS)
    for i, name in enumerate(intents, 1):
        print(f"  {i}. {name}")
    choice = input("Intent number (or name): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(intents):
        intent = intents[int(choice) - 1]
    elif choice in INTENTS:
        intent = choice
    else:
        raise WizardError(f"invalid intent choice: {choice}")

    answers: dict[str, Any] = {"schema": ANSWERS_SCHEMA, "intent": intent}
    fw_keys = sorted(frameworks.keys())

    def pick_framework(required: bool) -> str | None:
        print("Frameworks:")
        for i, k in enumerate(fw_keys, 1):
            print(f"  {i}. {k}")
        raw = input("Framework number/name" + ("" if required else " [empty=skip]") + ": ").strip()
        if not raw:
            if required:
                raise WizardError("framework required")
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(fw_keys):
            return fw_keys[int(raw) - 1]
        if raw in frameworks:
            return raw
        raise WizardError(f"unknown framework: {raw}")

    if intent == "greenfield":
        answers["framework"] = pick_framework(True)
        answers["emit_mode"] = input("emit_mode [structure]: ").strip() or "structure"
        c = input("concerns comma-separated [core_collapse default]: ").strip()
        if c:
            answers["concerns"] = c
        o = input("overlay [empty]: ").strip()
        if o:
            answers["overlay"] = o
        answers["out"] = input("out directory: ").strip() or None
    elif intent in ("observe", "map"):
        answers["path"] = input("path to analyze: ").strip()
        if intent == "map":
            answers["framework"] = pick_framework(True)
        else:
            fw = pick_framework(False)
            if fw:
                answers["framework"] = fw
        answers["out"] = input("out directory [empty]: ").strip() or None
        lang = input("lang [python]: ").strip()
        if lang:
            answers["lang"] = lang
    elif intent.startswith("optimize"):
        answers["from"] = input("path to analysis.json: ").strip()
        answers["out"] = input("out directory [empty]: ").strip() or None
        if intent == "optimize-apply-confirm":
            conf = input("Type CONFIRM to allow apply writes: ").strip()
            if conf != "CONFIRM":
                raise WizardError("apply confirm aborted (did not type CONFIRM)")
            answers["apply"] = True
            answers["confirm_apply"] = True
        elif intent == "optimize-apply-dry":
            answers["apply"] = True
            answers["confirm_apply"] = False
    return answers
```

- [ ] **Step 4: Run unit tests — expect pass**

```bash
python3 -m unittest tests.test_wizard -v
```

Expected: all `TestWizardResolve` tests OK.

- [ ] **Step 5: Commit**

```bash
git add scripts/orchestra_wizard.py tests/test_wizard.py
git commit -m "feat(wizard): add resolve/validate library and unit tests"
```

---

### Task 2: Wire `wizard` CLI command (print-only)

**Files:**
- Modify: `scripts/orchestra.py` (module docstring groups, `cmd_wizard`, `_add_wizard_args`, `build_router`)
- Modify: `tests/test_wizard.py` (add CLI integration class)

**Interfaces:**
- Consumes: `orchestra_wizard.merge_preset`, `validate_answers`, `resolve_plan`, `format_plan_*`, `load_answers`, `WizardError`; `FRAMEWORKS` from orchestra
- Produces: `cmd_wizard(args) -> int` registered as meta command `wizard`

- [ ] **Step 1: Add failing CLI tests** to `tests/test_wizard.py`:

```python
CLI = ROOT / "scripts" / "orchestra.py"
PYTHON = sys.executable


def run_cli(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(CLI), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        input=input_text,
    )


class TestWizardCLI(unittest.TestCase):
    def test_wizard_help(self) -> None:
        r = run_cli("wizard", "--help")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("answers", r.stdout)

    def test_wizard_print_only_observe_json(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ans_path = Path(td) / "answers.json"
            ans_path.write_text(
                json.dumps({
                    "schema": "orchestra-wizard-answers.v1",
                    "intent": "observe",
                    "path": "tests/fixtures/mini_pkg",
                    "out": str(Path(td) / "out"),
                }),
                encoding="utf-8",
            )
            r = run_cli("wizard", "--answers", str(ans_path), "--json")
            self.assertEqual(r.returncode, 0, r.stderr)
            plan = json.loads(r.stdout)
            self.assertEqual(plan["command"], "analyze")
            self.assertIn("analyze", plan["argv"][0])
            self.assertFalse(plan["run"])

    def test_wizard_non_tty_without_answers_exits_2(self) -> None:
        # Subprocess has no TTY for stdin
        r = run_cli("wizard")
        self.assertEqual(r.returncode, 2)
```

- [ ] **Step 2: Run CLI tests — expect fail**

```bash
python3 -m unittest tests.TestWizardCLI -v 2>&1 || python3 -m unittest tests.test_wizard.TestWizardCLI -v
```

Expected: fail — `invalid choice: 'wizard'` or similar.

- [ ] **Step 3: Wire command in `scripts/orchestra.py`**

1. Update module docstring groups to include `wizard` under meta.
2. Add imports:

```python
from orchestra_wizard import (
    WizardError,
    format_plan_human,
    format_plan_json,
    interactive_collect,
    load_answers,
    merge_preset,
    resolve_plan,
    validate_answers,
)
```

3. Add handlers:

```python
def cmd_wizard(args: argparse.Namespace) -> int:
    """Guided plan (default) or execute resolved Orchestra command."""
    try:
        answers_in: dict | None = None
        if getattr(args, "answers", None):
            answers_in = load_answers(args.answers)
        preset = getattr(args, "preset", None)
        if preset or answers_in is not None:
            raw = merge_preset(preset, answers_in)
        else:
            if not sys.stdin.isatty():
                print(
                    "wizard: non-interactive use requires --answers and/or --preset "
                    "(Hermes Desktop: collect fields in chat, then pass --answers)",
                    file=sys.stderr,
                )
                return 2
            raw = interactive_collect(FRAMEWORKS)
        answers = validate_answers(raw, FRAMEWORKS)
        run = bool(getattr(args, "run", False))
        # --print-only is default; --run overrides
        if getattr(args, "print_only", False) and run:
            print("wizard: both --print-only and --run set; using --run", file=sys.stderr)
        plan = resolve_plan(answers, FRAMEWORKS, run=run)
        if getattr(args, "json", False):
            sys.stdout.write(format_plan_json(plan))
        else:
            sys.stdout.write(format_plan_human(plan, skill_root_hint=str(Path(sys.argv[0]))))
        if not run:
            return 0
        # Task 4 implements dispatch; for now return 0 after print if not run
        return _wizard_run(plan)
    except WizardError as e:
        print(f"wizard error: {e.message}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"wizard error: invalid JSON: {e}", file=sys.stderr)
        return 2


def _wizard_run(plan: dict) -> int:
    """Dispatch resolved argv in-process. Implemented fully in Task 4."""
    return build_router().dispatch(list(plan["argv"]))


def _add_wizard_args(sp: argparse.ArgumentParser) -> None:
    sp.add_argument(
        "--answers",
        default=None,
        help="Path to answers JSON, or '-' for stdin",
    )
    sp.add_argument(
        "--preset",
        choices=["greenfield", "observe", "map", "optimize-plan"],
        default=None,
        help="Seed answers from a named preset",
    )
    sp.add_argument(
        "--print-only",
        action="store_true",
        default=True,
        help="Print plan only (default)",
    )
    sp.add_argument(
        "--run",
        action="store_true",
        help="Execute resolved command after printing plan",
    )
    sp.add_argument(
        "--json",
        action="store_true",
        help="Emit orchestra-wizard-plan.v1 JSON",
    )
```

**Note on `--print-only` default:** `store_true` with `default=True` is awkward if we also need to turn it off. Prefer: no `--print-only` flag that defaults true; **absence of `--run` means print-only**. Still accept `--print-only` as no-op for agent clarity:

```python
sp.add_argument("--print-only", action="store_true", help="Print plan only (default if --run omitted)")
sp.add_argument("--run", action="store_true", help="Execute resolved command")
```

`run = bool(args.run)`.

4. Register in `build_router()`:

```python
router.add(CommandSpec(
    name="wizard",
    handler=cmd_wizard,
    help="Guided plan/execute for Hermes (answers JSON or interactive TTY)",
    group="meta",
    configure=_add_wizard_args,
))
```

- [ ] **Step 4: Run tests**

```bash
python3 -m unittest tests.test_wizard -v
python3 scripts/orchestra.py wizard --help
```

Expected: all pass; help lists wizard.

- [ ] **Step 5: Commit**

```bash
git add scripts/orchestra.py tests/test_wizard.py
git commit -m "feat(wizard): register meta wizard CLI (print-only + answers)"
```

---

### Task 3: Interactive TTY path

**Files:**
- Modify: `scripts/orchestra_wizard.py` (`interactive_collect` already sketched — polish)
- Modify: `tests/test_wizard.py` (mock stdin)

**Interfaces:**
- Consumes: `interactive_collect(frameworks) -> dict`
- Produces: same answers shape as JSON path

- [ ] **Step 1: Add test with mocked stdin**

```python
class TestWizardInteractive(unittest.TestCase):
    def test_interactive_list(self) -> None:
        from orchestra_wizard import interactive_collect
        # pick list intent by name
        fake = "list\n"
        with mock.patch("builtins.input", side_effect=fake.strip().split("\n")):
            # intent by name "list"
            pass
        with mock.patch("builtins.input", side_effect=["list"]):
            ans = interactive_collect(FW)
        self.assertEqual(ans["intent"], "list")
        validated = validate_answers(ans, FW)
        plan = resolve_plan(validated, FW)
        self.assertEqual(plan["argv"], ["list"])
```

- [ ] **Step 2: Run — fix interactive_collect if needed until pass**

```bash
python3 -m unittest tests.test_wizard.TestWizardInteractive -v
```

- [ ] **Step 3: Commit**

```bash
git add scripts/orchestra_wizard.py tests/test_wizard.py
git commit -m "feat(wizard): interactive TTY collect path"
```

---

### Task 4: `--run` in-process dispatch + integration

**Files:**
- Modify: `scripts/orchestra.py` (`_wizard_run` already calls `dispatch`)
- Modify: `tests/test_wizard.py`

- [ ] **Step 1: Failing test — wizard --run structure into temp dir**

```python
def test_wizard_run_structure(self) -> None:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "skel"
        ans_path = Path(td) / "a.json"
        ans_path.write_text(json.dumps({
            "schema": "orchestra-wizard-answers.v1",
            "intent": "greenfield",
            "framework": "tree-of-life",
            "emit_mode": "structure",
            "concerns": ["intent", "output"],
            "out": str(out),
        }), encoding="utf-8")
        r = run_cli("wizard", "--answers", str(ans_path), "--run")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((out / "correspondence-table.json").exists())
```

- [ ] **Step 2: Run test — should pass if Task 2 wired `_wizard_run`; else fix recursion**

**Recursion guard:** `cmd_wizard` must not re-enter wizard. `dispatch(plan["argv"])` only runs non-wizard commands. Add assert:

```python
def _wizard_run(plan: dict[str, Any]) -> int:
    argv = list(plan["argv"])
    if not argv or argv[0] == "wizard":
        print("wizard error: refusing to dispatch wizard", file=sys.stderr)
        return 2
    return build_router().dispatch(argv)
```

- [ ] **Step 3: Run full wizard tests + existing suite sample**

```bash
python3 -m unittest tests.test_wizard -v
python3 -m unittest tests.test_orchestra -v
```

Expected: pass.

- [ ] **Step 4: Commit**

```bash
git add scripts/orchestra.py tests/test_wizard.py
git commit -m "feat(wizard): in-process --run dispatch with integration test"
```

---

### Task 5: JSON Schema + smoke

**Files:**
- Create: `schemas/wizard-answers.v1.schema.json`
- Modify: `scripts/smoke.sh`
- Modify: `scripts/orchestra.py` `cmd_check` if integrity should mention wizard schema (optional — only if `integrity_check.py` enumerates schemas)

- [ ] **Step 1: Write schema file**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://abraxas.local/orchestra/wizard-answers.v1.schema.json",
  "title": "orchestra-wizard-answers.v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema", "intent"],
  "properties": {
    "schema": { "const": "orchestra-wizard-answers.v1" },
    "intent": {
      "type": "string",
      "enum": [
        "greenfield", "observe", "map", "optimize-plan",
        "optimize-apply-dry", "optimize-apply-confirm", "check", "list"
      ]
    },
    "framework": { "type": ["string", "null"] },
    "concerns": {
      "oneOf": [
        { "type": "array", "items": { "type": "string" } },
        { "type": "string" },
        { "type": "null" }
      ]
    },
    "overlay": { "type": ["string", "null"] },
    "emit_mode": {
      "type": "string",
      "enum": ["structure", "project", "diagram"]
    },
    "path": { "type": ["string", "null"] },
    "from": { "type": ["string", "null"] },
    "out": { "type": ["string", "null"] },
    "lang": {
      "type": "string",
      "enum": ["python", "auto", "javascript", "typescript", "go", "rust", "ruby"]
    },
    "min_strength": {
      "type": "string",
      "enum": ["STRONG", "ADEQUATE", "WEAK", "FORCED"]
    },
    "apply": { "type": "boolean" },
    "confirm_apply": { "type": "boolean" },
    "refresh": { "type": "boolean" },
    "steps": {
      "oneOf": [
        { "type": "array", "items": { "type": "string" } },
        { "type": "string" },
        { "type": "null" }
      ]
    },
    "actions": {
      "oneOf": [
        { "type": "array", "items": { "type": "string" } },
        { "type": "string" },
        { "type": "null" }
      ]
    }
  }
}
```

- [ ] **Step 2: Extend smoke.sh** after `orchestra check`:

```bash
echo "==> wizard print-only observe"
WIZ_DIR="$(mktemp -d "${TMPDIR:-/tmp}/orchestra-wizard.XXXXXX")"
cat > "$WIZ_DIR/answers.json" <<EOF
{
  "schema": "orchestra-wizard-answers.v1",
  "intent": "observe",
  "path": "tests/fixtures/mini_pkg",
  "out": "$WIZ_DIR/out"
}
EOF
python3 scripts/orchestra.py wizard --answers "$WIZ_DIR/answers.json" --json | grep -q '"command": "analyze"'
rm -rf "$WIZ_DIR"
```

- [ ] **Step 3: Run smoke (or at least wizard line + unittest)**

```bash
bash scripts/smoke.sh
```

Expected: `SMOKE OK`.

- [ ] **Step 4: Commit**

```bash
git add schemas/wizard-answers.v1.schema.json scripts/smoke.sh
git commit -m "feat(wizard): answers JSON schema and smoke coverage"
```

---

### Task 6: Hermes docs + version 0.8.0

**Files:**
- Modify: `SKILL.md` (meta table + Hermes algorithm + frontmatter groups)
- Modify: `references/agent-posture.md` (wizard-first when unsure)
- Modify: `README.md` (command table + wizard examples)
- Modify: `docs/DESIGN.md` (executable surface)
- Modify: `CHANGELOG.md` (0.8.0 section)
- Version parity: run `python3 scripts/bump_version.py minor` (0.7.0 → 0.8.0) so `VERSION`, `orchestra.py`, `SKILL.md`, `orchestra.manifest.yaml`, `install.sh` match

- [ ] **Step 1: Update SKILL.md routing**

Add under Hermes routing table:

| Guided path / unsure / Desktop chat collect | **meta** | `wizard` |

Add section **Wizard (Hermes + Desktop)**:

```markdown
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
```

Update frontmatter `groups: [meta, emit, repo]` (unchanged) and description to mention wizard.

- [ ] **Step 2: agent-posture.md** — add row: unsure → **meta** `wizard`.

- [ ] **Step 3: README + DESIGN** — document `wizard` under meta; note Desktop uses chat + `--answers`.

- [ ] **Step 4: Bump version + CHANGELOG**

```bash
python3 scripts/bump_version.py minor
# Edit CHANGELOG.md for 0.8.0: wizard command, Hermes protocol, schema
python3 scripts/bump_version.py check
python3 scripts/orchestra.py check
python3 -m unittest discover -s tests -v
bash scripts/smoke.sh
```

- [ ] **Step 5: Commit**

```bash
git add SKILL.md references/agent-posture.md README.md docs/DESIGN.md CHANGELOG.md VERSION \
  scripts/orchestra.py orchestra.manifest.yaml install.sh
git commit -m "docs+release: Orchestra 0.8.0 Hermes wizard"
```

- [ ] **Step 6: Reinstall into Hermes skill tree (operator)**

```bash
bash install.sh --dry-run && bash install.sh
python3 ~/.hermes/skills/orchestra/scripts/orchestra.py wizard --help
```

---

## Spec coverage checklist

| Spec requirement | Task |
|------------------|------|
| `wizard` meta command | 2 |
| Interactive TTY | 3 |
| `--answers` / `--preset` | 1–2 |
| `--print-only` default / `--run` | 2, 4 |
| `--json` plan schema | 1–2 |
| Strict unknown keys | 1 |
| No confirm by default | 1 |
| Non-TTY exit 2 | 2 |
| Desktop chat protocol in SKILL | 6 |
| `wizard-answers.v1.schema.json` | 5 |
| smoke | 5 |
| 0.8.0 version | 6 |
| In-process dispatch | 4 |
| Reuse existing handlers | 4 |

## Self-review notes

- No TBD placeholders in task steps.
- `merge_preset` then `validate_answers` order is consistent across tests and CLI.
- Argv flags match real CLI: `-f`/`-o`/`-c` for emit; `--path`/`-f`/`--lang`/`--out` for analyze; `--from`/`--apply`/`--confirm` for optimize.
- Avoid `store_true default=True` trap for print-only (document: no `--run` ⇒ print-only).

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-08-orchestra-hermes-wizard.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — this session, executing-plans with checkpoints  

Which approach?
