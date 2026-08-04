#!/usr/bin/env python3
"""Tests for orchestra analyze (Phase A) — stdlib only."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "orchestra.py"
FIXTURE = ROOT / "tests" / "fixtures" / "mini_pkg"
PYTHON = sys.executable


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(CLI), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


class TestAnalyzeCLI(unittest.TestCase):
    def test_analyze_fixture_graph(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            r = run_cli("analyze", "--path", str(FIXTURE), "--out", str(out))
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            data = json.loads((out / "analysis.json").read_text())
            self.assertEqual(data["schema"], "orchestra-analysis.v1")
            self.assertEqual(data["provenance"]["kind"], "SPECULATIVE")
            self.assertGreaterEqual(len(data["nodes"]), 4)
            self.assertGreaterEqual(len(data["edges"]), 1)
            self.assertIn(data["status"], {"OBSERVED_ONLY", "CLEAN"})
            self.assertTrue((out / "architecture.json").exists())
            self.assertTrue((out / "architecture.html").exists())
            self.assertTrue((out / "architecture.mmd").exists())
            mmd = (out / "architecture.mmd").read_text()
            self.assertIn("flowchart", mmd)

    def test_analyze_unknown_path(self) -> None:
        r = run_cli("analyze", "--path", "/tmp/orchestra-no-such-dir-xyz")
        self.assertEqual(r.returncode, 2)
        self.assertIn("NOT_COMPUTABLE", r.stderr)

    def test_analyze_system_root_refused(self) -> None:
        r = run_cli("analyze", "--path", "/etc")
        self.assertEqual(r.returncode, 2)
        self.assertIn("NOT_COMPUTABLE", r.stderr)

    def test_analyze_with_framework(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "mapped"
            r = run_cli(
                "analyze",
                "--path", str(FIXTURE),
                "-f", "tree-of-life",
                "--out", str(out),
            )
            self.assertIn(r.returncode, (0, 1), r.stdout + r.stderr)
            data = json.loads((out / "analysis.json").read_text())
            self.assertTrue(data["mappings"])
            symbolic = {m["symbolic_locus"] for m in data["mappings"]}
            # Must come from frameworks schema — never invented
            allowed = {
                "kether", "chokmah", "binah", "chesed", "geburah",
                "tiphareth", "netzach", "hod", "yesod", "malkuth",
            }
            self.assertTrue(symbolic <= allowed)
            self.assertTrue((out / "correspondence-table.json").exists())
            # Strong matches expected for intake/analyze/store/output
            mechs = {m["mechanical_name"] for m in data["mappings"]}
            self.assertTrue({"intake", "analyze", "store", "output"} & mechs)

    def test_analyze_skips_venv(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "pkg"
            root.mkdir()
            (root / "real.py").write_text("x = 1\n", encoding="utf-8")
            venv = root / ".venv" / "lib"
            venv.mkdir(parents=True)
            (venv / "hidden.py").write_text("y = 2\n", encoding="utf-8")
            r = run_cli("analyze", "--path", str(root))
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads(r.stdout)
            paths = {n["path"] for n in data["nodes"]}
            self.assertIn("real.py", paths)
            self.assertFalse(any(".venv" in p for p in paths))

    def test_analyze_parse_error_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "pkg"
            root.mkdir()
            (root / "ok.py").write_text("a = 1\n", encoding="utf-8")
            (root / "bad.py").write_text("def (\n", encoding="utf-8")
            r = run_cli("analyze", "--path", str(root))
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads(r.stdout)
            bad = next(n for n in data["nodes"] if n["id"] == "bad")
            self.assertIsNotNone(bad["parse_error"])

    def test_analyze_unknown_framework(self) -> None:
        r = run_cli("analyze", "--path", str(FIXTURE), "-f", "not-real")
        self.assertEqual(r.returncode, 2)


class TestAnalyzeSchema(unittest.TestCase):
    def test_schema_file_exists(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "analysis.v1.schema.json").read_text()
        )
        self.assertEqual(schema["properties"]["schema"]["const"], "orchestra-analysis.v1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
