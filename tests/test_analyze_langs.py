#!/usr/bin/env python3
"""Unit tests for multi-language analyze extractors and analyze_path."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
CLI = ROOT / "scripts" / "orchestra.py"
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_langs import (  # noqa: E402
    extract_go_imports,
    extract_js_ts_imports,
    extract_ruby_imports,
    extract_rust_imports,
    normalize_lang,
    extensions_for_lang,
    parse_go_imports,
    parse_js_imports,
    parse_ruby_imports,
    parse_rust_imports,
    tokenize_js,
    tokenize_go,
    tokenize_rust,
)
from analyze_repo import analyze_path  # noqa: E402


def _frameworks() -> dict:
    raw = json.loads((ROOT / "schemas" / "frameworks.v1.json").read_text(encoding="utf-8"))
    out = {}
    for k, meta in raw["frameworks"].items():
        loci = [
            (r["mechanical"], r["symbolic"], r.get("note") or "")
            for r in meta.get("default_loci") or []
        ]
        out[k] = {**meta, "default_loci": loci}
    return out


FW = _frameworks()


class TestLangExtractors(unittest.TestCase):
    def test_normalize_aliases(self) -> None:
        self.assertEqual(normalize_lang("js"), "javascript")
        self.assertEqual(normalize_lang("ts"), "typescript")
        self.assertEqual(normalize_lang("auto"), "auto")
        self.assertEqual(normalize_lang("py"), "python")

    def test_js_imports(self) -> None:
        text = """
        import React from 'react';
        import { score } from './analyze.js';
        const x = require('../lib/util');
        export { y } from "./emit.ts";
        """
        specs = extract_js_ts_imports(text)
        self.assertIn("react", specs)
        self.assertIn("./analyze.js", specs)
        self.assertIn("../lib/util", specs)
        self.assertIn("./emit.ts", specs)

    def test_js_ast_nodes_and_tokenizer(self) -> None:
        text = "import {x} from './analyze.js';\n// comment\nrequire(\"pkg\");\n"
        toks = tokenize_js(text)
        self.assertTrue(any(t.kind == "KEYWORD" and t.value == "import" for t in toks))
        self.assertTrue(any(t.kind == "STRING" and t.value == "./analyze.js" for t in toks))
        nodes = parse_js_imports(text)
        kinds = {n.kind for n in nodes}
        self.assertIn("import", kinds)
        self.assertIn("require", kinds)
        self.assertTrue(any(n.is_relative for n in nodes if n.module.startswith(".")))

    def test_go_imports(self) -> None:
        text = """
        package main
        import "fmt"
        import (
            "os"
            foo "github.com/x/y"
        )
        """
        specs = extract_go_imports(text)
        self.assertIn("fmt", specs)
        self.assertIn("os", specs)
        self.assertIn("github.com/x/y", specs)
        nodes = parse_go_imports(text)
        self.assertTrue(all(n.kind == "go_import" for n in nodes))
        self.assertGreaterEqual(len(tokenize_go(text)), 5)

    def test_rust_imports(self) -> None:
        text = """
        use std::collections::HashMap;
        use crate::intake::pull;
        mod store;
        """
        specs = extract_rust_imports(text)
        self.assertTrue(any("collections" in s or "std" in s for s in specs))
        self.assertTrue(any("intake" in s for s in specs))
        self.assertIn("store", specs)
        nodes = parse_rust_imports(text)
        kinds = {n.kind for n in nodes}
        self.assertIn("use", kinds)
        self.assertIn("mod", kinds)
        self.assertTrue(any(t.kind == "OP" and t.value == "::" for t in tokenize_rust(text)))

    def test_ruby_imports(self) -> None:
        text = """
        require 'json'
        require_relative './intake'
        """
        specs = extract_ruby_imports(text)
        self.assertIn("json", specs)
        self.assertIn("./intake", specs)

    def test_auto_extensions_include_multi(self) -> None:
        exts = extensions_for_lang("auto")
        self.assertIn(".py", exts)
        self.assertIn(".js", exts)
        self.assertIn(".go", exts)
        self.assertIn(".rs", exts)
        self.assertIn(".rb", exts)


class TestAnalyzeMultiLang(unittest.TestCase):
    def test_javascript_graph(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "intake.js").write_text(
                "import { score } from './analyze.js';\nexport const a = 1;\n",
                encoding="utf-8",
            )
            (root / "analyze.js").write_text(
                "export function score() { return 1; }\n",
                encoding="utf-8",
            )
            an, code = analyze_path(
                root, frameworks=FW, version="0.5.0", lang="javascript"
            )
            self.assertEqual(code, 0, an)
            self.assertEqual(an["status"], "OBSERVED_ONLY")
            ids = {n["id"] for n in an["nodes"]}
            self.assertIn("intake", ids)
            self.assertIn("analyze", ids)
            edges = {(e["from"], e["to"]) for e in an["edges"] if not e.get("external")}
            self.assertIn(("intake", "analyze"), edges)

    def test_auto_multi_language(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.py").write_text("import b\n", encoding="utf-8")
            (root / "b.py").write_text("x = 1\n", encoding="utf-8")
            (root / "c.js").write_text("import './d.js';\n", encoding="utf-8")
            (root / "d.js").write_text("export default 1;\n", encoding="utf-8")
            an, code = analyze_path(root, frameworks=FW, version="0.5.0", lang="auto")
            self.assertEqual(code, 0)
            langs = set(an.get("languages") or [])
            self.assertIn("python", langs)
            self.assertIn("javascript", langs)
            self.assertGreaterEqual(len(an["nodes"]), 4)

    def test_unsupported_lang_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.py").write_text("x=1\n", encoding="utf-8")
            an, code = analyze_path(
                root, frameworks=FW, version="0.5.0", lang="cobol"
            )
            self.assertEqual(code, 2)
            self.assertEqual(an["status"], "NOT_COMPUTABLE")

    def test_cli_lang_js(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "pkg"
            root.mkdir()
            (root / "intake.js").write_text(
                "import {x} from './store.js';\n", encoding="utf-8"
            )
            (root / "store.js").write_text("export const x=1;\n", encoding="utf-8")
            out = Path(td) / "out"
            r = subprocess.run(
                [
                    PYTHON,
                    str(CLI),
                    "analyze",
                    "--path",
                    str(root),
                    "--lang",
                    "javascript",
                    "--out",
                    str(out),
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            data = json.loads((out / "analysis.json").read_text(encoding="utf-8"))
            self.assertIn("javascript", data.get("languages") or [data.get("language")])


class TestIntegrityInProcess(unittest.TestCase):
    """Drive integrity_check in-process so coverage floors can measure it."""

    def test_check_integrity_real_repo(self) -> None:
        from integrity_check import check_integrity, main, skill_root, LINE_FLOORS

        errs = check_integrity(ROOT)
        self.assertEqual(errs, [])
        self.assertEqual(skill_root(), ROOT)
        self.assertGreater(len(LINE_FLOORS), 5)
        self.assertEqual(main([]), 0)
        # truncated tree fails
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "VERSION").write_text("0.0.0\n", encoding="utf-8")
            (d / "scripts").mkdir()
            (d / "scripts" / "orchestra.py").write_text("# tiny\n", encoding="utf-8")
            errs2 = check_integrity(d)
            self.assertTrue(errs2)


if __name__ == "__main__":
    unittest.main()
