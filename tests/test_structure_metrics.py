#!/usr/bin/env python3
"""Unit + CLI tests for structure metrics (stdlib only)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "orchestra.py"
SCRIPTS = ROOT / "scripts"
BEFORE = ROOT / "examples" / "benchmark-tree-of-life" / "before"
AFTER = ROOT / "examples" / "benchmark-tree-of-life" / "after"
PYTHON = sys.executable

sys.path.insert(0, str(SCRIPTS))
from structure_metrics import (  # noqa: E402
    compute_structure_metrics,
    format_metrics_summary,
    map_quality_score,
)


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(CLI), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


class TestStructureMetricsUnit(unittest.TestCase):
    def test_map_quality_weights(self) -> None:
        score = map_quality_score([
            {"strength": "STRONG"},
            {"strength": "ADEQUATE"},
            {"strength": "WEAK"},
            {"strength": "FORCED"},
        ])
        self.assertEqual(score, 3 + 2 + 1 + 0)

    def test_compute_from_synthetic_cycle(self) -> None:
        analysis = {
            "nodes": [
                {"id": "a", "path": "a.py", "kind": "module", "provenance": "OBSERVED"},
                {"id": "b", "path": "b.py", "kind": "module", "provenance": "OBSERVED"},
            ],
            "edges": [
                {"from": "a", "to": "b", "kind": "import", "provenance": "OBSERVED"},
                {"from": "b", "to": "a", "kind": "import", "provenance": "OBSERVED"},
            ],
            "mappings": [
                {"strength": "STRONG"},
                {"strength": "STRONG"},
            ],
        }
        m = compute_structure_metrics(analysis)
        self.assertEqual(m["schema"], "orchestra-structure-metrics.v1")
        self.assertEqual(m["map"]["quality"], 6.0)
        self.assertEqual(m["map"]["strong"], 2)
        self.assertEqual(m["graph"]["nodes_in_cycles"], 2)
        self.assertGreaterEqual(m["graph"]["cyclic_sccs"], 1)
        self.assertIn("map_quality=", format_metrics_summary(m))


class TestStructureMetricsCLI(unittest.TestCase):
    def test_analyze_embeds_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            r = run_cli(
                "analyze",
                "--path",
                str(AFTER),
                "-f",
                "tree-of-life",
                "--out",
                str(out),
            )
            self.assertIn(r.returncode, (0, 1), r.stdout + r.stderr)
            data = json.loads((out / "analysis.json").read_text())
            self.assertIn("metrics", data)
            self.assertEqual(data["metrics"]["schema"], "orchestra-structure-metrics.v1")
            self.assertIn("map", data["metrics"])
            self.assertIn("graph", data["metrics"])
            self.assertIn("mix", data["metrics"])
            self.assertTrue((out / "structure-metrics.json").is_file())
            self.assertIn("# metrics:", r.stderr)

    def test_before_worse_than_after(self) -> None:
        """Product proof: map quality and cycles improve after staging."""
        with tempfile.TemporaryDirectory() as td:
            b_out = Path(td) / "before"
            a_out = Path(td) / "after"
            rb = run_cli(
                "analyze", "--path", str(BEFORE), "-f", "tree-of-life", "--out", str(b_out),
            )
            ra = run_cli(
                "analyze", "--path", str(AFTER), "-f", "tree-of-life", "--out", str(a_out),
            )
            self.assertIn(rb.returncode, (0, 1), rb.stderr)
            self.assertIn(ra.returncode, (0, 1), ra.stderr)
            before = json.loads((b_out / "analysis.json").read_text())["metrics"]
            after = json.loads((a_out / "analysis.json").read_text())["metrics"]
            self.assertGreater(after["map"]["quality"], before["map"]["quality"])
            self.assertGreater(after["map"]["strong"], before["map"]["strong"])
            self.assertLess(
                after["graph"]["nodes_in_cycles"],
                before["graph"]["nodes_in_cycles"],
            )
            self.assertLess(
                after["mix"]["mixed_files"],
                before["mix"]["mixed_files"],
            )


if __name__ == "__main__":
    unittest.main()
