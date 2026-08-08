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


class TestWizardInteractive(unittest.TestCase):
    def test_interactive_list(self) -> None:
        from orchestra_wizard import interactive_collect

        with mock.patch("builtins.input", side_effect=["list"]):
            ans = interactive_collect(FW)
        self.assertEqual(ans["intent"], "list")
        validated = validate_answers(ans, FW)
        plan = resolve_plan(validated, FW)
        self.assertEqual(plan["argv"], ["list"])


if __name__ == "__main__":
    unittest.main()
