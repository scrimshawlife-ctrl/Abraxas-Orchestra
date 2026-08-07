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
            self.assertTrue((out / "architecture.json").exists())
            self.assertTrue((out / "architecture.html").exists())
            self.assertTrue((out / "architecture.mmd").exists())
            mmd = (out / "architecture.mmd").read_text()
            self.assertIn("```mermaid", mmd)
            self.assertIn("flowchart", mmd)

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
            self.assertTrue((out / "architecture.mmd").exists())

    def test_diagram_writes_mmd(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "arch"
            r = run_cli("diagram", "-f", "tree-of-life", "-c", "intent,output", "--out", str(out))
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("mermaid", (out / "architecture.mmd").read_text())

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
        self.assertTrue((ROOT / "examples" / "signal-forager-skeleton" / "pipeline.py").exists())

    def test_enochian_chaos_stubs(self) -> None:
        root = ROOT / "examples" / "enochian-chaos-skeleton"
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

class TestPackageIdentity(unittest.TestCase):
    """Guard live packaging surfaces against wrong repo name drift."""

    CANON = "https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra"
    STALE = "Abraxas-Orchestra-Hermes"

    def _read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_readme_clone_urls_use_real_repo(self) -> None:
        text = self._read("README.md")
        self.assertNotIn(self.STALE, text)
        self.assertIn(f"{self.CANON}.git", text)
        self.assertIn(f"- Repo: {self.CANON}", text)

    def test_manifest_and_notice_repository(self) -> None:
        manifest = self._read("orchestra.manifest.yaml")
        notice = self._read("NOTICE")
        for text in (manifest, notice):
            self.assertNotIn(self.STALE, text)
            self.assertIn(self.CANON, text)

    def test_schema_ids_use_real_repo(self) -> None:
        schemas = list((ROOT / "schemas").glob("*.json"))
        self.assertGreaterEqual(len(schemas), 4)
        for path in schemas:
            text = path.read_text(encoding="utf-8")
            if '"$id"' not in text:
                continue
            self.assertNotIn(self.STALE, text, msg=path.name)
            self.assertIn(self.CANON, text, msg=path.name)

    def test_design_documents_040_surface(self) -> None:
        design = self._read("docs/DESIGN.md")
        self.assertRegex(design, r"0\.\d+\.\d+")
        for cmd in ("analyze", "optimize", "structure", "diagram", "check", "list"):
            self.assertIn(cmd, design)
        self.assertNotIn("Version target**: 0.1.2", design)

    def test_hermes_skill_routes_like_cli_router(self) -> None:
        """Hermes SKILL.md must document the same meta/emit/repo groups as CLI."""
        skill = self._read("SKILL.md")
        self.assertIn("Hermes routing", skill)
        for group in ("meta", "emit", "repo"):
            self.assertIn(group, skill)
        for cmd in (
            "check", "list", "structure", "project", "diagram", "analyze", "optimize",
        ):
            self.assertIn(cmd, skill)
        manifest = self._read("orchestra.manifest.yaml")
        self.assertIn("command_groups:", manifest)
        posture = self._read("references/agent-posture.md")
        self.assertIn("meta", posture)
        self.assertIn("emit", posture)
        self.assertIn("repo", posture)
