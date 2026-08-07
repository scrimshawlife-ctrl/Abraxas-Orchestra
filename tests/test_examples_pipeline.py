#!/usr/bin/env python3
"""Test Tree-of-Life optimized pipeline example — stdlib only."""

from __future__ import annotations

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
        sys.path.insert(0, str(EXAMPLE))
        from intent import accept  # type: ignore

        with self.assertRaises(ValueError):
            accept("")

    def test_stage_modules_exist(self) -> None:
        for name in ("intent", "intake", "analyze", "store", "output"):
            self.assertTrue((EXAMPLE / name / "__init__.py").is_file())


if __name__ == "__main__":
    unittest.main()
