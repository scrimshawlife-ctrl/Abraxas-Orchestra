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

    def test_frameworks_json_matches_cli(self) -> None:
        data = json.loads((ROOT / "schemas" / "frameworks.v1.json").read_text())
        self.assertEqual(data.get("schema"), "frameworks.v1")
        self.assertEqual(len(data["frameworks"]), 11)
        r = run_cli("do", "list-frameworks")
        self.assertEqual(r.returncode, 0)
        for key in data["frameworks"]:
            self.assertIn(key, r.stdout)

    def test_framework_refs_exist(self) -> None:
        data = json.loads((ROOT / "schemas" / "frameworks.v1.json").read_text())
        for key, meta in data["frameworks"].items():
            ref = ROOT / meta["reference"]
            self.assertTrue(ref.exists(), f"missing ref for {key}: {meta['reference']}")
        self.assertTrue((ROOT / "references" / "enochian-cli-loci.md").exists())


class TestExamples(unittest.TestCase):
    def test_signal_forager_files(self) -> None:
        root = ROOT / "examples" / "signal-forager-skeleton"
        self.assertTrue((root / "pipeline.py").exists())
        self.assertTrue((root / "run_demo.py").exists())
        self.assertTrue((root / "correspondence-table.json").exists())
        for mod in (
            "intent",
            "intake",
            "constraint",
            "adversarial",
            "synthesis",
            "store",
            "output",
        ):
            self.assertTrue((root / mod / "__init__.py").exists(), mod)

    def test_enochian_chaos_stubs(self) -> None:
        root = ROOT / "examples" / "enochian-chaos-skeleton"
        self.assertTrue((root / "correspondence-table.json").exists())
        self.assertTrue((root / "pipeline.py").exists())
        self.assertTrue((root / "models.py").exists())
        self.assertTrue((root / "run_demo.py").exists())
        for mod in (
            "edge_intake",
            "domain_entry",
            "root_truth_seal",
            "cross_domain_bus",
            "inverse_capability",
            "sovereign_intent",
        ):
            body = (root / mod / "__init__.py").read_text()
            self.assertTrue((root / mod / "__init__.py").exists(), mod)
            self.assertNotIn("def placeholder(", body)
            self.assertNotIn('status": "STUB"', body)
        data = json.loads((root / "correspondence-table.json").read_text())
        self.assertEqual(data.get("framework"), "enochian")
        self.assertEqual(data.get("secondary_overlay"), "chaos-magic")

    def test_enochian_chaos_demo_report(self) -> None:
        demo = ROOT / "examples" / "enochian-chaos-skeleton" / "run_demo.py"
        r = subprocess.run(
            [PYTHON, str(demo)],
            cwd=str(demo.parent),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        report = demo.parent / "_demo_out" / "report.json"
        self.assertTrue(report.exists())
        data = json.loads(report.read_text())
        self.assertTrue(data.get("seal_valid"))
        self.assertIn("kept", data)
        self.assertIn("provenance", data)

    def test_demo_report_shape(self) -> None:
        demo = ROOT / "examples" / "signal-forager-skeleton" / "run_demo.py"
        r = subprocess.run(
            [PYTHON, str(demo)],
            cwd=str(demo.parent),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        report = demo.parent / "_demo_out" / "report.json"
        self.assertTrue(report.exists())
        data = json.loads(report.read_text())
        for key in ("summary", "provenance"):
            self.assertIn(key, data)

    def test_enochian_validation_error(self) -> None:
        import sys as _sys

        root = ROOT / "examples" / "enochian-chaos-skeleton"
        _sys.path.insert(0, str(root))
        try:
            from models import ValidationError  # type: ignore
            from pipeline import run_session  # type: ignore

            with self.assertRaises(ValidationError) as ctx:
                run_session(
                    session_id="",
                    operator="op",
                    intent_id="i1",
                    statement="x",
                    edge_items=[],
                )
            self.assertEqual(ctx.exception.stage, "input")
        finally:
            _sys.path.remove(str(root))
            for name in list(_sys.modules):
                if name in ("models", "pipeline") or name.startswith(
                    (
                        "root_truth",
                        "domain_entry",
                        "edge_intake",
                        "cross_domain",
                        "inverse",
                        "sovereign",
                    )
                ):
                    _sys.modules.pop(name, None)

    def test_forager_validation_error(self) -> None:
        import sys as _sys

        root = ROOT / "examples" / "signal-forager-skeleton"
        _sys.path.insert(0, str(root))
        try:
            from models import ValidationError  # type: ignore
            from pipeline import run_forage  # type: ignore

            with self.assertRaises(ValidationError) as ctx:
                run_forage("", [])
            self.assertEqual(ctx.exception.stage, "intent")
        finally:
            _sys.path.remove(str(root))
            for name in list(_sys.modules):
                if name in (
                    "models",
                    "pipeline",
                    "intent",
                    "intake",
                    "constraint",
                    "adversarial",
                    "synthesis",
                    "store",
                    "output",
                ):
                    _sys.modules.pop(name, None)


class TestInstaller(unittest.TestCase):
    def test_install_refuses_system_path(self) -> None:
        r = subprocess.run(
            ["bash", str(ROOT / "install.sh"), "--dry-run", "--target", "/etc/orchestra"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(r.returncode, 0)
        blob = (r.stderr + r.stdout).lower()
        self.assertTrue("refus" in blob or "outside" in blob or "error" in blob)

    def test_install_refuses_outside_home(self) -> None:
        r = subprocess.run(
            [
                "bash",
                str(ROOT / "install.sh"),
                "--dry-run",
                "--target",
                "/tmp/orchestra-should-fail",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
