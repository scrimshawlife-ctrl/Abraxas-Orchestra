#!/usr/bin/env python3
"""Pure unit tests for diagram_emit + diagram_mermaid (stdlib only)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from diagram_emit import (  # noqa: E402
    _graph_from_loci,
    _html_diagram,
    set_context,
)
from diagram_mermaid import (  # noqa: E402
    _mermaid_id,
    mermaid_from_graph,
    write_diagram_files,
)


class TestDiagramMermaid(unittest.TestCase):
    def test_mermaid_id_sanitizes(self) -> None:
        self.assertEqual(_mermaid_id("pkg.mod-name/x"), "pkg_mod_name_x")
        self.assertEqual(_mermaid_id("a b"), "a_b")

    def test_mermaid_from_graph_structure(self) -> None:
        graph = {
            "framework": "tree-of-life",
            "secondary_overlay": None,
            "nodes": [
                {"id": "intake", "mechanical": "intake", "symbolic": "chokmah"},
                {"id": "output", "mechanical": "output", "symbolic": "malkuth"},
            ],
            "edges": [{"from": "intake", "to": "output", "kind": "sequence"}],
            "flows": [
                {"id": "primary", "name": "main", "steps": ["intake", "output"]}
            ],
        }
        mmd = mermaid_from_graph(graph)
        self.assertIn("flowchart LR", mmd)
        self.assertIn("intake", mmd)
        self.assertIn("output", mmd)
        self.assertIn("-->", mmd)
        self.assertIn("orchestra-diagram.v1", mmd)
        self.assertIn("primary", mmd)

    def test_write_diagram_files(self) -> None:
        graph = {
            "framework": "test",
            "nodes": [{"id": "a", "mechanical": "a", "symbolic": "A"}],
            "edges": [],
            "flows": [],
        }
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            write_diagram_files(out, graph, html="<html>ok</html>", quiet=True)
            self.assertTrue((out / "architecture.json").is_file())
            self.assertTrue((out / "architecture.html").is_file())
            self.assertTrue((out / "architecture.mmd").is_file())
            data = json.loads((out / "architecture.json").read_text(encoding="utf-8"))
            self.assertEqual(data["framework"], "test")
            self.assertIn("flowchart", (out / "architecture.mmd").read_text(encoding="utf-8"))


class TestDiagramEmit(unittest.TestCase):
    def test_graph_from_loci_sequence(self) -> None:
        set_context("0.6.0", {"tree-of-life": {"core_collapse": ["intake", "output"]}})
        loci = [
            ("intake", "chokmah", "in"),
            ("analyze", "hod", "mid"),
            ("output", "malkuth", "out"),
        ]
        graph = _graph_from_loci("tree-of-life", None, loci, [])
        self.assertEqual(len(graph["nodes"]), 3)
        self.assertEqual(len(graph["edges"]), 2)
        self.assertEqual(graph["edges"][0]["from"], "intake")
        self.assertEqual(graph["edges"][0]["to"], "analyze")
        flow_ids = {f["id"] for f in graph["flows"]}
        self.assertIn("primary", flow_ids)
        self.assertIn("core", flow_ids)

    def test_html_diagram_contains_nodes(self) -> None:
        set_context("0.6.0", {})
        loci = [("intent", "kether", "entry"), ("output", "malkuth", "end")]
        graph = _graph_from_loci("tree-of-life", None, loci, [])
        html = _html_diagram(graph)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("intent", html)
        self.assertIn("output", html)


if __name__ == "__main__":
    unittest.main()
