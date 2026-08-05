"""Tests for scripts/bump_version.py"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


def _load():
    root = Path(__file__).resolve().parent.parent
    path = root / "scripts" / "bump_version.py"
    spec = importlib.util.spec_from_file_location("bump_version", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestSemver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bv = _load()

    def test_parse_and_bump(self):
        self.assertEqual(self.bv.parse_semver("0.3.1"), (0, 3, 1))
        self.assertEqual(self.bv.bump((0, 3, 1), "patch"), (0, 3, 2))
        self.assertEqual(self.bv.bump((0, 3, 1), "minor"), (0, 4, 0))
        self.assertEqual(self.bv.bump((0, 3, 1), "major"), (1, 0, 0))

    def test_reject_v_prefix_in_file_value(self):
        with self.assertRaises(ValueError):
            self.bv.parse_semver("v0.3.1")

    def test_check_real_repo(self):
        root = Path(__file__).resolve().parent.parent
        errs = self.bv.check_parity(root)
        self.assertEqual(errs, [], errs)

    def test_apply_roundtrip_tmpdir(self):
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            (t / "scripts").mkdir()
            (t / "VERSION").write_text("0.3.1\n")
            (t / "scripts" / "orchestra.py").write_text('VERSION = "0.3.1"\n')
            (t / "SKILL.md").write_text("---\nversion: 0.3.1\n---\n")
            (t / "orchestra.manifest.yaml").write_text("version: 0.3.1\n")
            (t / "install.sh").write_text(
                '# Abraxas Orchestra — atomic installer (v0.3.1)\nVERSION="0.3.1"\n'
            )
            self.bv.apply_version(t, "0.3.2", dry=False)
            self.assertEqual((t / "VERSION").read_text().strip(), "0.3.2")
            self.assertEqual(self.bv.check_parity(t), [])


if __name__ == "__main__":
    unittest.main()
