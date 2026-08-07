#!/usr/bin/env python3
"""Unit tests for CommandRouter — stdlib only."""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from orchestra import build_parser, build_router, main  # noqa: E402
from orchestra_router import CommandRouter, CommandSpec  # noqa: E402


class TestCommandRouter(unittest.TestCase):
    def test_register_and_dispatch(self) -> None:
        hits: list[str] = []

        def h_a(_: argparse.Namespace) -> int:
            hits.append("a")
            return 0

        def h_b(_: argparse.Namespace) -> int:
            hits.append("b")
            return 7

        r = CommandRouter(prog="t", description="test", version="0.0.1")
        r.add(CommandSpec(name="alpha", handler=h_a, help="a", group="meta"))
        r.add(CommandSpec(name="beta", handler=h_b, help="b", aliases=("b",), group="repo"))
        self.assertEqual(r.names(), ["alpha", "beta"])
        self.assertEqual(r.dispatch(["alpha"]), 0)
        self.assertEqual(r.dispatch(["b"]), 7)
        self.assertEqual(hits, ["a", "b"])
        self.assertIsNotNone(r.get("beta"))
        self.assertEqual(r.get("b").name, "beta")  # type: ignore[union-attr]

    def test_legacy_do_prefix(self) -> None:
        seen: list[str] = []

        def h(_: argparse.Namespace) -> int:
            seen.append("ok")
            return 0

        r = CommandRouter(prog="t", description="t", version="0")
        r.add(CommandSpec(name="ping", handler=h, help="p"))
        code = r.dispatch(["do", "ping"])
        self.assertEqual(code, 0)
        self.assertEqual(seen, ["ok"])

    def test_duplicate_raises(self) -> None:
        r = CommandRouter(prog="t", description="t", version="0")

        def h(_: argparse.Namespace) -> int:
            return 0

        r.add(CommandSpec(name="x", handler=h, help="x"))
        with self.assertRaises(ValueError):
            r.add(CommandSpec(name="x", handler=h, help="x"))

    def test_epilog_groups(self) -> None:
        r = build_router()
        text = r.build_parser().format_help()
        self.assertIn("Meta", text)
        self.assertIn("Emit", text)
        self.assertIn("Repo", text)
        self.assertIn("check", text)
        self.assertIn("analyze", text)

    def test_orchestra_router_commands(self) -> None:
        r = build_router()
        expected = {
            "check", "list", "structure", "project", "diagram", "analyze", "optimize",
        }
        self.assertEqual(set(r.names()), expected)
        # aliases resolve
        self.assertEqual(r.get("list-frameworks").name, "list")  # type: ignore[union-attr]
        self.assertEqual(r.get("diagrammit").name, "diagram")  # type: ignore[union-attr]

    def test_build_parser_backcompat(self) -> None:
        p = build_parser()
        ns = p.parse_args(["check"])
        self.assertTrue(callable(ns.func))

    def test_main_check(self) -> None:
        code = main(["check"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
