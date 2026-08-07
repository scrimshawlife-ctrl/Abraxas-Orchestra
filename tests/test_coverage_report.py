#!/usr/bin/env python3
"""Tests for soft coverage/quality report — stdlib only."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SCRIPT = ROOT / "scripts" / "coverage_report.py"


class TestCoverageReport(unittest.TestCase):
    def test_report_runs_and_imports_ok(self) -> None:
        r = subprocess.run(
            [PYTHON, str(SCRIPT)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Import check", r.stdout)
        self.assertIn("OK —", r.stdout)
        self.assertIn("Test linkage", r.stdout)
        self.assertIn("soft report only", r.stdout)
        # In-process section should mention analyze_repo or mapping-related hits
        self.assertIn("In-process line coverage", r.stdout)

    def test_report_writes_out_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "report.txt"
            r = subprocess.run(
                [PYTHON, str(SCRIPT), "--out", str(out)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(out.is_file())
            text = out.read_text(encoding="utf-8")
            self.assertIn("Orchestra soft quality report", text)
            self.assertGreater(len(text), 200)

    def test_broken_script_import_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td)
            # Minimal tree with one broken script
            (dest / "scripts").mkdir()
            (dest / "tests").mkdir()
            (dest / "tests" / "test_noop.py").write_text(
                "import unittest\nclass T(unittest.TestCase):\n"
                "    def test_ok(self):\n        self.assertTrue(True)\n",
                encoding="utf-8",
            )
            (dest / "scripts" / "broken_mod.py").write_text(
                "raise RuntimeError('boom')\n",
                encoding="utf-8",
            )
            r = subprocess.run(
                [PYTHON, str(SCRIPT), "--root", str(dest)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn("import failed", r.stdout.lower() + r.stderr.lower())


if __name__ == "__main__":
    unittest.main()
