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
    def test_legacy_do_prefix(self) -> None:
        r = run_cli("do", "list")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("tree-of-life", r.stdout)

    def test_check_ok(self) -> None:
        r = run_cli("check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("CHECK OK", r.stdout)

    def test_list_frameworks(self) -> None:
        r = run_cli("list")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("tree-of-life", r.stdout)

    def test_structure_clean(self) -> None:
        r = run_cli("structure", "-f", "tree-of-life", "-c", "intent,output")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"status": "CLEAN"', r.stdout)

    def test_structure_unknown_framework(self) -> None:
        r = run_cli("structure", "-f", "not-a-real-map")
        self.assertEqual(r.returncode, 2)
        self.assertIn("NOT_COMPUTABLE", r.stderr)

    def test_structure_overlay_same_as_primary(self) -> None:
        r = run_cli("structure", "-f", "enochian", "-o", "enochian")
        self.assertEqual(r.returncode, 2)

    def test_structure_writes_out(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "skel"
            r = run_cli(
                "structure", "-f", "chaos-magic",
                "-c", "paradigm_switch,intent_token", "--out", str(out),
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((out / "correspondence-table.json").exists())

    def test_diagram_writes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "arch"
            r = run_cli(
                "diagram", "-f", "tree-of-life",
                "-c", "intent,synthesis,output", "--out", str(out),
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads((out / "architecture.json").read_text())
            self.assertEqual(data.get("schema"), "orchestra-diagram.v1")
            self.assertTrue(data.get("nodes"))
            self.assertTrue((out / "architecture.html").exists())
            self.assertIn("Orchestra diagram", (out / "architecture.html").read_text())

    def test_diagram_alias(self) -> None:
        r = run_cli("diagrammit", "-f", "chaos-magic", "-c", "intent_token")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("orchestra-diagram.v1", r.stdout)

    def test_project_collapses(self) -> None:
        r = run_cli("project", "-f", "tree-of-life")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_enochian_overlay_table(self) -> None:
        r = run_cli(
            "structure", "-f", "enochian", "-o", "chaos-magic",
            "-c", "root_truth_seal,domain_entry",
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("overlay_note", r.stdout)


class TestSchemaFile(unittest.TestCase):
    def test_schema_exists_and_lists_frameworks(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "correspondence-table.v1.schema.json").read_text()
        )
        for key in ("tree-of-life", "enochian", "chaos-magic", "composite"):
            self.assertIn(key, schema["properties"]["framework"]["enum"])

    def test_frameworks_json_matches_cli(self) -> None:
        data = json.loads((ROOT / "schemas" / "frameworks.v1.json").read_text())
        self.assertEqual(len(data["frameworks"]), 11)
        r = run_cli("list")
        self.assertEqual(r.returncode, 0)
        for key in data["frameworks"]:
            self.assertIn(key, r.stdout)

    def test_framework_refs_exist(self) -> None:
        data = json.loads((ROOT / "schemas" / "frameworks.v1.json").read_text())
        for key, meta in data["frameworks"].items():
            self.assertTrue((ROOT / meta["reference"]).exists(), key)


class TestExamples(unittest.TestCase):
    def test_signal_forager_files(self) -> None:
        root = ROOT / "examples" / "signal-forager-skeleton"
        self.assertTrue((root / "pipeline.py").exists())

    def test_enochian_chaos_stubs(self) -> None:
        root = ROOT / "examples" / "enochian-chaos-skeleton"
        self.assertTrue((root / "pipeline.py").exists())
        body = (root / "root_truth_seal" / "__init__.py").read_text()
        self.assertNotIn("def placeholder(", body)

    def test_enochian_chaos_demo_report(self) -> None:
        demo = ROOT / "examples" / "enochian-chaos-skeleton" / "run_demo.py"
        r = subprocess.run([PYTHON, str(demo)], cwd=str(demo.parent), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_demo_report_shape(self) -> None:
        demo = ROOT / "examples" / "signal-forager-skeleton" / "run_demo.py"
        r = subprocess.run([PYTHON, str(demo)], cwd=str(demo.parent), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_enochian_validation_error(self) -> None:
        import sys as _sys
        root = ROOT / "examples" / "enochian-chaos-skeleton"
        _sys.path.insert(0, str(root))
        try:
            from models import ValidationError  # type: ignore
            from pipeline import run_session  # type: ignore
            with self.assertRaises(ValidationError):
                run_session(session_id="", operator="op", intent_id="i1", statement="x", edge_items=[])
        finally:
            _sys.path.remove(str(root))
            for name in list(_sys.modules):
                if name in ("models", "pipeline"):
                    _sys.modules.pop(name, None)

    def test_forager_validation_error(self) -> None:
        import sys as _sys
        root = ROOT / "examples" / "signal-forager-skeleton"
        _sys.path.insert(0, str(root))
        try:
            from models import ValidationError  # type: ignore
            from pipeline import run_forage  # type: ignore
            with self.assertRaises(ValidationError):
                run_forage("", [])
        finally:
            _sys.path.remove(str(root))
            for name in list(_sys.modules):
                if name in ("models", "pipeline"):
                    _sys.modules.pop(name, None)


class TestInstaller(unittest.TestCase):
    def test_install_refuses_system_path(self) -> None:
        r = subprocess.run(
            ["bash", str(ROOT / "install.sh"), "--dry-run", "--target", "/etc/orchestra"],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertNotEqual(r.returncode, 0)

    def test_install_refuses_outside_home(self) -> None:
        r = subprocess.run(
            ["bash", str(ROOT / "install.sh"), "--dry-run", "--target", "/tmp/orchestra-should-fail"],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
