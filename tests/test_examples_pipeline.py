#!/usr/bin/env python3
"""Test Tree-of-Life optimized pipeline example — stdlib only."""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "python-tree-of-life-pipeline"
PYTHON = sys.executable


class TestPythonTreeOfLifePipeline(unittest.TestCase):
    def test_pipeline_runs_and_respects_stages(self) -> None:
        r = subprocess.run(
            [PYTHON, str(EXAMPLE / "pipeline.py")],
            cwd=str(EXAMPLE),
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('"status": "OK"', r.stdout)
        self.assertIn('"count":', r.stdout)
        self.assertIn("malkuth", r.stdout)

    def test_intent_rejects_empty_source(self) -> None:
        # Load as package without polluting bare top-level names
        if str(EXAMPLE) not in sys.path:
            sys.path.insert(0, str(EXAMPLE))
        intent = importlib.import_module("tol.intent")
        with self.assertRaises(ValueError):
            intent.accept("")

    def test_stage_modules_exist(self) -> None:
        for name in ("intent", "intake", "analyze", "store", "output", "pipeline"):
            self.assertTrue((EXAMPLE / "tol" / f"{name}.py").is_file())


if __name__ == "__main__":
    unittest.main()
