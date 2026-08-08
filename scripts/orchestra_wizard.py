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
        try:
            text = Path(path_or_dash).read_text(encoding="utf-8")
        except OSError as e:
            raise WizardError(f"cannot read answers file: {e}") from e
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

    for flag in ("apply", "confirm_apply", "refresh"):
        if not isinstance(out[flag], bool):
            raise WizardError(f"{flag} must be a boolean (got {type(out[flag]).__name__})")

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

    if intent == "optimize-plan":
        out["apply"] = False
        out["confirm_apply"] = False
    elif intent == "optimize-apply-dry":
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
