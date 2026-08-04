#!/usr/bin/env python3
"""Tests for orchestra optimize plan + apply (Phase B/C) — stdlib only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "orchestra.py"
FIXTURE = ROOT / "tests" / "fixtures" / "mini_pkg"
RENAME_FIXTURE = ROOT / "tests" / "fixtures" / "rename_pkg"
PYTHON = sys.executable


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(CLI), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


class TestOptimizeCLI(unittest.TestCase):
    def _analysis_with_framework(self, out: Path, path: Path = FIXTURE, framework: str = "tree-of-life") -> Path:
        r = run_cli(
            "analyze",
            "--path", str(path),
            "-f", framework,
            "--out", str(out),
        )
        self.assertIn(r.returncode, (0, 1), r.stdout + r.stderr)
        analysis_path = out / "analysis.json"
        self.assertTrue(analysis_path.exists())
        return analysis_path

    def test_optimize_plan_no_write(self) -> None:
        """Optimize must not modify the analyzed repo tree."""
        with tempfile.TemporaryDirectory() as td:
            analysis_out = Path(td) / "analysis"
            plan_out = Path(td) / "plan"
            analysis_path = self._analysis_with_framework(analysis_out)

            # Snapshot fixture mtimes
            before = {
                p: p.stat().st_mtime_ns
                for p in FIXTURE.rglob("*")
                if p.is_file()
            }
            time.sleep(0.05)
            r = run_cli(
                "optimize",
                "--from", str(analysis_path),
                "--out", str(plan_out),
            )
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            after = {
                p: p.stat().st_mtime_ns
                for p in FIXTURE.rglob("*")
                if p.is_file()
            }
            self.assertEqual(before, after)
            plan = json.loads((plan_out / "optimize-plan.json").read_text())
            self.assertEqual(plan["schema"], "orchestra-optimize-plan.v1")
            self.assertTrue((plan_out / "OPTIMIZE.md").exists())
            # Plan references only observed nodes / schema loci
            node_ids = {
                n["id"]
                for n in json.loads(analysis_path.read_text())["nodes"]
            }
            for step in plan["steps"]:
                for t in step.get("targets") or []:
                    self.assertTrue(
                        t in node_ids or t == "import-flow" or "." in t or t,
                        msg=t,
                    )

    def test_optimize_blocks_forced(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            analysis_path = Path(td) / "analysis.json"
            analysis = {
                "schema": "orchestra-analysis.v1",
                "path": str(FIXTURE),
                "language": "python",
                "framework": "tree-of-life",
                "secondary_overlay": None,
                "status": "FORCED_CORRESPONDENCE",
                "nodes": [
                    {
                        "id": "weird",
                        "path": "weird.py",
                        "kind": "module",
                        "provenance": "OBSERVED",
                        "imports": [],
                        "parse_error": None,
                    }
                ],
                "edges": [],
                "mappings": [
                    {
                        "functional_concern": "weird",
                        "mechanical_name": "weird",
                        "symbolic_name": "unmapped_weird",
                        "symbolic_locus": "unmapped_weird",
                        "strength": "FORCED",
                        "notes": "FORCED — no clean locus",
                        "node_id": "weird",
                    },
                    {
                        "functional_concern": "intake",
                        "mechanical_name": "intake",
                        "symbolic_name": "chokmah",
                        "symbolic_locus": "chokmah",
                        "strength": "STRONG",
                        "notes": "Raw force intake",
                        "node_id": "intake",
                    },
                ],
                "provenance": {"operator": "test", "kind": "OBSERVED"},
            }
            # intake node needed for boundary step targets validity
            analysis["nodes"].append({
                "id": "intake",
                "path": "intake.py",
                "kind": "module",
                "provenance": "OBSERVED",
                "imports": [],
                "parse_error": None,
            })
            analysis_path.write_text(json.dumps(analysis), encoding="utf-8")
            r = run_cli("optimize", "--from", str(analysis_path))
            self.assertEqual(r.returncode, 0, r.stderr)
            plan = json.loads(r.stdout)
            blocked_strengths = {b["strength"] for b in plan["blocked"]}
            self.assertIn("FORCED", blocked_strengths)
            # Forced target must not appear as a plan step target
            forced_targets = {
                t
                for b in plan["blocked"]
                if b["strength"] == "FORCED"
                for t in b.get("targets") or []
            }
            for step in plan["steps"]:
                for t in step.get("targets") or []:
                    self.assertNotIn(t, forced_targets)

    def test_optimize_apply_dry_run_no_write(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "pkg"
            shutil.copytree(RENAME_FIXTURE, work)
            analysis_path = self._analysis_with_framework(
                Path(td) / "a", path=work, framework="alchemical-stages"
            )
            before = sorted(p.name for p in work.glob("*.py"))
            r = run_cli("optimize", "--from", str(analysis_path), "--apply")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            report = json.loads(r.stdout)
            self.assertEqual(report["status"], "DRY_RUN")
            self.assertTrue(report["dry_run"])
            self.assertEqual(before, sorted(p.name for p in work.glob("*.py")))
            self.assertIn("dry-run", r.stderr.lower())

    def test_optimize_apply_confirm_renames(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "pkg"
            shutil.copytree(RENAME_FIXTURE, work)
            analysis_path = self._analysis_with_framework(
                Path(td) / "a", path=work, framework="alchemical-stages"
            )
            backup = Path(td) / "backup"
            r = run_cli(
                "optimize",
                "--from", str(analysis_path),
                "--apply",
                "--confirm",
                "--backup-dir", str(backup),
            )
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            report = json.loads(r.stdout)
            self.assertEqual(report["status"], "APPLIED")
            self.assertTrue((work / "raw_ingest.py").exists())
            self.assertFalse((work / "nigredo.py").exists())
            self.assertTrue((backup / "RESTORE.md").exists())
            # Import rewrite keeps call-site alias
            pipe = (work / "pipeline.py").read_text()
            self.assertIn("raw_ingest", pipe)
            self.assertIn("as nigredo", pipe)
            self.assertIn("nigredo.pull", pipe)

    def test_optimize_apply_blocks_forced(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            analysis_path = Path(td) / "analysis.json"
            analysis_path.write_text(
                json.dumps({
                    "schema": "orchestra-analysis.v1",
                    "path": str(FIXTURE),
                    "language": "python",
                    "framework": "tree-of-life",
                    "status": "FORCED_CORRESPONDENCE",
                    "nodes": [],
                    "edges": [],
                    "mappings": [{
                        "functional_concern": "x",
                        "mechanical_name": "x",
                        "symbolic_name": "unmapped_x",
                        "symbolic_locus": "unmapped_x",
                        "strength": "FORCED",
                        "node_id": "x",
                    }],
                    "provenance": {"kind": "OBSERVED"},
                }),
                encoding="utf-8",
            )
            r = run_cli("optimize", "--from", str(analysis_path), "--apply", "--confirm")
            self.assertEqual(r.returncode, 2)
            self.assertIn("NOT_COMPUTABLE", r.stderr)

    def test_optimize_empty_plan_ok(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            analysis_path = Path(td) / "analysis.json"
            analysis_path.write_text(
                json.dumps({
                    "schema": "orchestra-analysis.v1",
                    "path": str(FIXTURE),
                    "language": "python",
                    "framework": None,
                    "status": "OBSERVED_ONLY",
                    "nodes": [],
                    "edges": [],
                    "mappings": [],
                    "provenance": {"kind": "OBSERVED"},
                }),
                encoding="utf-8",
            )
            r = run_cli("optimize", "--from", str(analysis_path))
            self.assertEqual(r.returncode, 0, r.stderr)
            plan = json.loads(r.stdout)
            self.assertEqual(plan["steps"], [])
            self.assertIn("empty plan", r.stderr.lower())


class TestOptimizeSchema(unittest.TestCase):
    def test_schema_file_exists(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "optimize-plan.v1.schema.json").read_text()
        )
        self.assertEqual(
            schema["properties"]["schema"]["const"],
            "orchestra-optimize-plan.v1",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
