#!/usr/bin/env python3
"""Production smoke tests for Abraxas Orchestra CLI — stdlib only."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "orchestra.py"
PYTHON = sys.executable


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(CLI), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


class TestOrchestraCLI(unittest.TestCase):
    def test_check_ok(self) -> None:
        r = run_cli("check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("CHECK OK", r.stdout)

    def test_list_frameworks(self) -> None:
        r = run_cli("do", "list-frameworks")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("tree-of-life", r.stdout)
        self.assertIn("enochian", r.stdout)
        self.assertIn("chaos-magic", r.stdout)

    def test_structure_clean(self) -> None:
        r = run_cli("do", "structure", "-f", "tree-of-life", "-c", "intent,output")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"status": "CLEAN"', r.stdout)
        self.assertIn("intent", r.stdout)

    def test_structure_unknown_framework(self) -> None:
        r = run_cli("do", "structure", "-f", "not-a-real-map")
        self.assertEqual(r.returncode, 2)
        self.assertIn("NOT_COMPUTABLE", r.stderr)

    def test_structure_overlay_same_as_primary(self) -> None:
        r = run_cli("do", "structure", "-f", "enochian", "-o", "enochian")
        self.assertEqual(r.returncode, 2)
        self.assertIn("NOT_COMPUTABLE", r.stderr)

    def test_structure_writes_out(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "skel"
            r = run_cli(
                "do",
                "structure",
                "-f",
                "chaos-magic",
                "-c",
                "paradigm_switch,intent_token",
                "--out",
                str(out),
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            table = out / "correspondence-table.json"
            self.assertTrue(table.exists())
            data = json.loads(table.read_text())
            self.assertEqual(data["framework"], "chaos-magic")
            self.assertIn("mappings", data)
            self.assertTrue((out / "paradigm_switch" / "__init__.py").exists())

    def test_project_collapses(self) -> None:
        r = run_cli("do", "project", "-f", "tree-of-life")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("tree-of-life", r.stdout)

    def test_enochian_overlay_table(self) -> None:
        r = run_cli(
            "do",
            "structure",
            "-f",
            "enochian",
            "-o",
            "chaos-magic",
            "-c",
            "root_truth_seal,domain_entry",
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("overlay_note", r.stdout)
        self.assertIn("sigillum_dei_aemeth", r.stdout)


class TestSchemaFile(unittest.TestCase):
    def test_schema_exists_and_lists_frameworks(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "correspondence-table.v1.schema.json").read_text()
        )
        enum = schema["properties"]["framework"]["enum"]
        for key in (
            "tree-of-life",
            "enochian",
            "chaos-magic",
            "composite",
        ):
            self.assertIn(key, enum)


if __name__ == "__main__":
    unittest.main(verbosity=2)
