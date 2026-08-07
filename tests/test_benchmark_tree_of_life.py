#!/usr/bin/env python3
"""Structure benchmark before/after — stdlib only."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "examples" / "benchmark-tree-of-life" / "harness.py"
PYTHON = sys.executable


class TestStructureBenchmark(unittest.TestCase):
    def test_harness_passes(self) -> None:
        r = subprocess.run(
            [PYTHON, str(HARNESS)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("parity: PASS", r.stdout)
        self.assertIn("better_map_quality", r.stdout)
        self.assertIn("PASS", r.stdout)

    def test_harness_json_verdict(self) -> None:
        r = subprocess.run(
            [PYTHON, str(HARNESS), "--json"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual(data["schema"], "orchestra-structure-benchmark.v1")
        self.assertTrue(data["verdict"]["parity"])
        self.assertTrue(data["verdict"]["better_map_quality"])
        self.assertTrue(data["verdict"]["fewer_cycles"])
        self.assertTrue(data["verdict"]["fewer_mixed_files"])
        self.assertTrue(data["verdict"]["after_rejects_empty"])
        self.assertGreater(data["map_quality"]["after"], data["map_quality"]["before"])
        self.assertGreater(
            data["before"]["graph"]["nodes_in_cycles"],
            data["after"]["graph"]["nodes_in_cycles"],
        )
        # Early-exit: after should be cheaper when rejecting empty source
        self.assertLess(
            data["after"]["early_exit"]["per_call_us"],
            data["before"]["early_exit"]["per_call_us"],
        )


if __name__ == "__main__":
    unittest.main()
