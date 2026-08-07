#!/usr/bin/env python3
"""Tests for critical-file integrity floors — stdlib only."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
SCRIPT = ROOT / "scripts" / "integrity_check.py"


class TestIntegrityCheck(unittest.TestCase):
    def test_real_repo_passes(self) -> None:
        r = subprocess.run(
            [PYTHON, str(SCRIPT)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("INTEGRITY OK", r.stdout)

    def test_truncated_orchestra_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td)
            # Minimal skill tree with truncated CLI
            (dest / "scripts").mkdir()
            (dest / "VERSION").write_text("0.4.0\n", encoding="utf-8")
            (dest / "SKILL.md").write_text(
                "---\nname: orchestra\nversion: 0.4.0\n---\n"
                "name: orchestra\nanalyze\noptimize\n" + ("x\n" * 50),
                encoding="utf-8",
            )
            (dest / "install.sh").write_text(
                "#!/bin/bash\nvalidate_target\nallow-outside-home\ndry-run\n"
                + ("# pad\n" * 160),
                encoding="utf-8",
            )
            # Copy real modules that must exist for floors, then truncate orchestra
            for rel in (
                "scripts/optimize_apply.py",
                "scripts/optimize_enrich.py",
                "scripts/optimize_rewrite.py",
                "scripts/analyze_repo.py",
                "scripts/optimize_plan.py",
            ):
                shutil.copy2(ROOT / rel, dest / rel)
            (dest / "scripts" / "orchestra.py").write_text(
                "# truncated\nVERSION = '0.4.0'\n",
                encoding="utf-8",
            )
            r = subprocess.run(
                [PYTHON, str(SCRIPT), "--root", str(dest)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn("INTEGRITY FAIL", r.stderr)
            self.assertIn("orchestra.py", r.stderr)


class TestMappingNormalize(unittest.TestCase):
    def test_hyphen_underscore_adequate(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        from analyze_repo import _map_node_to_locus  # type: ignore

        node = {"id": "pkg.edge_intake", "path": "edge_intake.py", "kind": "module"}
        loci = [("edge-intake", "Edge", "edge intake")]
        m = _map_node_to_locus(node, loci, source_text="")
        self.assertIsNotNone(m)
        assert m is not None
        self.assertIn(m["strength"], {"STRONG", "ADEQUATE"})
        self.assertEqual(m["mechanical_name"], "edge-intake")


if __name__ == "__main__":
    unittest.main()
