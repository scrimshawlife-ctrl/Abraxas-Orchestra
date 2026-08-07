#!/usr/bin/env python3
"""
Measurable before/after for Tree-of-Life structure (stdlib only).

Demonstrates improvement *beyond* rename semantics:
  1. Behavioral parity (happy path) — same payload shape
  2. Orchestra analyze scorecard — mapping status + strength histogram
  3. Import-graph hygiene — edges, cycles, SCCs
  4. Responsibility mix — files touching ≥2 concern categories
  5. Early-exit control-flow — invalid intent cost (timeit)

Usage (from repo root or this directory):
  python3 examples/benchmark-tree-of-life/harness.py
  python3 examples/benchmark-tree-of-life/harness.py --json
"""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import subprocess
import sys
import tempfile
import timeit
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CLI = REPO / "scripts" / "orchestra.py"
BEFORE_ROOT = ROOT / "before"
AFTER_ROOT = ROOT / "after"
PYTHON = sys.executable

# Concern tokens on *identifiers/calls* (not docstrings) for mix scoring.
CONCERN_TOKENS: dict[str, frozenset[str]] = {
    "intake": frozenset({"load", "pull", "open", "read", "intake", "raw"}),
    "score": frozenset({"score", "reweight", "filter", "analyze", "weight"}),
    "store": frozenset({"persist", "store", "dump", "save", "stamp", "stamp_partial"}),
    "emit": frozenset({"emit", "manifest", "build_report"}),
}


def _py_files(tree: Path) -> list[Path]:
    return sorted(
        p for p in tree.rglob("*.py")
        if "__pycache__" not in p.parts and p.name != "__init__.py"
    )


def _node_id(tree: Path, path: Path) -> str:
    rel = path.relative_to(tree).as_posix()
    if rel.endswith("/__init__.py"):
        return rel[: -len("/__init__.py")] or path.parent.name
    if rel.endswith(".py"):
        return rel[: -len(".py")]
    return rel


def _module_graph(tree: Path) -> tuple[dict[str, set[str]], list[str]]:
    """
    Build a simplified import graph among local modules under `tree`.
    Nodes are posix relative paths without .py (e.g. myapp/utils).
    """
    files = [p for p in tree.rglob("*.py") if "__pycache__" not in p.parts]
    rel_ids: dict[Path, str] = {p: _node_id(tree, p) for p in files}
    # dotted name → node id (prefer longest match later)
    name_to_node: dict[str, str] = {}
    for node in rel_ids.values():
        name_to_node[node.replace("/", ".")] = node

    def resolve_name(dotted: str) -> str | None:
        if dotted in name_to_node:
            return name_to_node[dotted]
        # prefix: myapp.helpers.foo → myapp.helpers
        parts = dotted.split(".")
        while parts:
            key = ".".join(parts)
            if key in name_to_node:
                return name_to_node[key]
            parts.pop()
        return None

    graph: dict[str, set[str]] = {n: set() for n in rel_ids.values()}

    for p, node in rel_ids.items():
        try:
            tree_ast = ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        except SyntaxError:
            continue
        pkg_parts = node.split("/")
        # file module: package is parent; package __init__: package is node itself
        is_init = p.name == "__init__.py"
        for stmt in ast.walk(tree_ast):
            candidates: list[str] = []
            if isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    candidates.append(alias.name)
            elif isinstance(stmt, ast.ImportFrom):
                level = stmt.level or 0
                mod = stmt.module or ""
                if level:
                    # PEP 328: level is dots; module file `.` = parent package
                    base_parts = list(pkg_parts if is_init else pkg_parts[:-1])
                    for _ in range(level - 1):
                        if base_parts:
                            base_parts.pop()
                    if mod:
                        base_parts = base_parts + mod.split(".")
                    base = ".".join(base_parts)
                    if mod or level:
                        candidates.append(base)
                    for alias in stmt.names:
                        if alias.name == "*":
                            continue
                        candidates.append(f"{base}.{alias.name}" if base else alias.name)
                else:
                    if mod:
                        candidates.append(mod)
                        for alias in stmt.names:
                            if alias.name != "*":
                                candidates.append(f"{mod}.{alias.name}")
            for t in candidates:
                hit = resolve_name(t)
                if hit and hit != node:
                    graph[node].add(hit)
    return graph, sorted(graph.keys())


def _count_cycles(graph: dict[str, set[str]]) -> tuple[int, int]:
    """Return (nodes_in_cycles, scc_count_with_size_gt_1) via Tarjan SCC."""
    index = 0
    stack: list[str] = []
    onstack: set[str] = set()
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    sccs: list[list[str]] = []

    def strongconnect(v: str) -> None:
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        onstack.add(v)
        for w in graph.get(v, ()):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in onstack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            comp: list[str] = []
            while True:
                w = stack.pop()
                onstack.discard(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    for v in graph:
        if v not in indices:
            strongconnect(v)

    cyclic_nodes = sum(len(c) for c in sccs if len(c) > 1)
    # Also count self-loops as cycles
    self_loops = sum(1 for v, outs in graph.items() if v in outs)
    multi = sum(1 for c in sccs if len(c) > 1)
    return cyclic_nodes + self_loops, multi + self_loops


def _identifiers(tree_ast: ast.AST) -> set[str]:
    """Collect function/call/name identifiers; ignore string/docstring content."""
    names: set[str] = set()
    for node in ast.walk(tree_ast):
        if isinstance(node, ast.FunctionDef):
            names.add(node.name)
        elif isinstance(node, ast.AsyncFunctionDef):
            names.add(node.name)
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                names.add(f.id)
            elif isinstance(f, ast.Attribute):
                names.add(f.attr)
        elif isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
    return {n.lower() for n in names}


def _mix_score(tree: Path) -> dict[str, Any]:
    mixed: list[dict[str, Any]] = []
    pure = 0
    for path in _py_files(tree):
        try:
            tree_ast = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            continue
        idents = _identifiers(tree_ast)
        seen: list[str] = []
        for concern, tokens in CONCERN_TOKENS.items():
            if idents & tokens:
                seen.append(concern)
        if len(seen) >= 2:
            mixed.append({
                "file": path.relative_to(tree).as_posix(),
                "concerns": seen,
            })
        elif len(seen) == 1:
            pure += 1
    return {
        "mixed_files": len(mixed),
        "pure_files": pure,
        "mixed_detail": mixed,
    }


def _analyze(tree: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="orch-bench-") as td:
        out = Path(td)
        r = subprocess.run(
            [
                PYTHON,
                str(CLI),
                "analyze",
                "--path",
                str(tree),
                "-f",
                "tree-of-life",
                "--out",
                str(out),
            ],
            cwd=str(REPO),
            capture_output=True,
            text=True,
        )
        analysis_path = out / "analysis.json"
        if not analysis_path.exists():
            return {
                "ok": False,
                "exit_code": r.returncode,
                "stderr": (r.stderr or r.stdout)[:500],
            }
        data = json.loads(analysis_path.read_text(encoding="utf-8"))
        hist: dict[str, int] = defaultdict(int)
        for m in data.get("mappings") or []:
            hist[str(m.get("strength") or "?")] += 1
        return {
            "ok": True,
            "exit_code": r.returncode,
            "status": data.get("status"),
            "node_count": len(data.get("nodes") or []),
            "edge_count": len(data.get("edges") or []),
            "strength_histogram": dict(hist),
            "strong": hist.get("STRONG", 0),
            "adequate": hist.get("ADEQUATE", 0),
            "weak": hist.get("WEAK", 0),
            "forced": hist.get("FORCED", 0),
        }


def _load_runner(tree: Path, module: str, attr: str = "run"):
    """Import run() from before/after without polluting permanent path forever."""
    if str(tree) not in sys.path:
        sys.path.insert(0, str(tree))
    # Drop cached package modules under this tree's top name
    top = module.split(".")[0]
    for name in list(sys.modules):
        if name == top or name.startswith(top + "."):
            del sys.modules[name]
    mod = importlib.import_module(module)
    return getattr(mod, attr)


def _canonical(result: dict[str, Any]) -> dict[str, Any]:
    """Stable subset for parity (ignore ordering-only noise)."""
    items = result.get("items") or []
    slim = [
        {
            "id": it.get("id"),
            "text": it.get("text"),
            "weight": it.get("weight"),
            "score": it.get("score"),
            "stored": it.get("stored"),
        }
        for it in items
    ]
    return {
        "count": result.get("count"),
        "status": result.get("status"),
        "stage": result.get("stage"),
        "symbolic": result.get("symbolic"),
        "items": slim,
    }


def _time_invalid_intent(fn, repeats: int = 800) -> dict[str, Any]:
    """
    Time the invalid-source path.
    After: raises at intent (cheap).
    Before: still does full load/score/dump (expensive).
    """

    def call_before_style() -> None:
        fn("")  # before accepts empty

    def call_after_style() -> None:
        try:
            fn("")
        except ValueError:
            return

    # Detect which style
    raised = False
    try:
        fn("")
    except ValueError:
        raised = True

    timer = call_after_style if raised else call_before_style
    total = timeit.timeit(timer, number=repeats)
    return {
        "rejects_empty": raised,
        "repeats": repeats,
        "total_seconds": round(total, 6),
        "per_call_us": round(total / repeats * 1_000_000, 3),
    }


def measure_tree(label: str, tree: Path, module: str) -> dict[str, Any]:
    graph, nodes = _module_graph(tree)
    edge_count = sum(len(v) for v in graph.values())
    cyclic_nodes, cyclic_sccs = _count_cycles(graph)
    mix = _mix_score(tree)
    analysis = _analyze(tree)
    run = _load_runner(tree, module)
    happy = run("demo-source", max_items=8)
    early = _time_invalid_intent(run)
    return {
        "label": label,
        "path": str(tree.relative_to(REPO)) if tree.is_relative_to(REPO) else str(tree),
        "module": module,
        "happy_path": _canonical(happy),
        "analyze": analysis,
        "graph": {
            "nodes": len(nodes),
            "edges": edge_count,
            "nodes_in_cycles": cyclic_nodes,
            "cyclic_sccs": cyclic_sccs,
        },
        "mix": {
            "mixed_files": mix["mixed_files"],
            "pure_files": mix["pure_files"],
            "mixed_detail": mix["mixed_detail"],
        },
        "early_exit": early,
    }


def _map_quality(analysis: dict[str, Any]) -> float:
    """Weighted mapping quality (STRONG best). Missing analysis → 0."""
    if not analysis.get("ok"):
        return 0.0
    return float(
        analysis.get("strong", 0) * 3
        + analysis.get("adequate", 0) * 2
        + analysis.get("weak", 0) * 1
        + analysis.get("forced", 0) * 0
    )


def _score_better(before: dict[str, Any], after: dict[str, Any]) -> dict[str, bool]:
    ba = before["analyze"]
    aa = after["analyze"]
    b_bad = ba.get("weak", 0) + ba.get("forced", 0)
    a_bad = aa.get("weak", 0) + aa.get("forced", 0)
    return {
        "parity": before["happy_path"] == after["happy_path"],
        "better_map_quality": (
            _map_quality(aa) > _map_quality(ba)
            or a_bad < b_bad
            or (aa.get("status") == "CLEAN" and ba.get("status") not in (None, "CLEAN", "OBSERVED_ONLY"))
            or aa.get("strong", 0) > ba.get("strong", 0)
        ),
        "fewer_cycles": after["graph"]["nodes_in_cycles"] < before["graph"]["nodes_in_cycles"],
        "fewer_mixed_files": after["mix"]["mixed_files"] < before["mix"]["mixed_files"],
        "after_rejects_empty": after["early_exit"]["rejects_empty"]
        and not before["early_exit"]["rejects_empty"],
        "early_exit_faster": (
            after["early_exit"]["rejects_empty"]
            and after["early_exit"]["per_call_us"] < before["early_exit"]["per_call_us"]
        ),
    }


def _print_report(before: dict[str, Any], after: dict[str, Any], verdict: dict[str, bool]) -> None:
    def line(metric: str, b: Any, a: Any, ok: bool | None = None) -> None:
        flag = ""
        if ok is True:
            flag = "  ✓"
        elif ok is False:
            flag = "  ✗"
        print(f"  {metric:<28}  before={b!s:<18}  after={a!s:<18}{flag}")

    print("Abraxas Orchestra — structure benchmark (tree-of-life)")
    print("=" * 72)
    print("\n1) Behavioral parity (happy path, max_items=8)")
    print(f"  parity: {'PASS' if verdict['parity'] else 'FAIL'}")

    print("\n2) Analyze scorecard (-f tree-of-life)")
    bq, aq = _map_quality(before["analyze"]), _map_quality(after["analyze"])
    line("status", before["analyze"].get("status"), after["analyze"].get("status"), verdict["better_map_quality"])
    line("map quality (weighted)", round(bq, 1), round(aq, 1), verdict["better_map_quality"])
    line("STRONG", before["analyze"].get("strong"), after["analyze"].get("strong"))
    line("ADEQUATE", before["analyze"].get("adequate"), after["analyze"].get("adequate"))
    line("WEAK", before["analyze"].get("weak"), after["analyze"].get("weak"))
    line("FORCED", before["analyze"].get("forced"), after["analyze"].get("forced"))
    line("nodes", before["analyze"].get("node_count"), after["analyze"].get("node_count"))
    line("edges", before["analyze"].get("edge_count"), after["analyze"].get("edge_count"))

    print("\n3) Import-graph hygiene (local modules)")
    line("graph nodes", before["graph"]["nodes"], after["graph"]["nodes"])
    line("graph edges", before["graph"]["edges"], after["graph"]["edges"])
    line("nodes in cycles", before["graph"]["nodes_in_cycles"], after["graph"]["nodes_in_cycles"], verdict["fewer_cycles"])
    line("cyclic SCCs", before["graph"]["cyclic_sccs"], after["graph"]["cyclic_sccs"])

    print("\n4) Responsibility mix (≥2 concern categories / file)")
    line("mixed files", before["mix"]["mixed_files"], after["mix"]["mixed_files"], verdict["fewer_mixed_files"])
    line("pure files", before["mix"]["pure_files"], after["mix"]["pure_files"])
    if before["mix"]["mixed_detail"]:
        print("  before mixed detail:")
        for row in before["mix"]["mixed_detail"]:
            print(f"    - {row['file']}: {', '.join(row['concerns'])}")

    print("\n5) Early-exit control flow (empty source × N)")
    line("rejects empty", before["early_exit"]["rejects_empty"], after["early_exit"]["rejects_empty"], verdict["after_rejects_empty"])
    line(
        "per call (µs)",
        before["early_exit"]["per_call_us"],
        after["early_exit"]["per_call_us"],
        verdict["early_exit_faster"],
    )
    line("repeats", before["early_exit"]["repeats"], after["early_exit"]["repeats"])

    keys = [
        "parity",
        "better_map_quality",
        "fewer_cycles",
        "fewer_mixed_files",
        "after_rejects_empty",
        "early_exit_faster",
    ]
    passed = sum(1 for k in keys if verdict[k])
    print("\n" + "=" * 72)
    print(f"Verdict: {passed}/{len(keys)} improvement checks passed")
    for k in keys:
        print(f"  [{'PASS' if verdict[k] else 'FAIL'}] {k}")
    print()
    print("Note: we do not claim domain scoring is CPU-faster — structure")
    print("improves map quality, graph hygiene, mix, and fail-closed control flow.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable report")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write full JSON report to this path",
    )
    args = parser.parse_args()

    if not CLI.is_file():
        print(f"ERROR: CLI not found at {CLI}", file=sys.stderr)
        return 2

    before = measure_tree("before", BEFORE_ROOT, "myapp.main")
    after = measure_tree("after", AFTER_ROOT, "tol.pipeline")
    verdict = _score_better(before, after)
    report = {
        "schema": "orchestra-structure-benchmark.v1",
        "framework": "tree-of-life",
        "before": before,
        "after": after,
        "verdict": verdict,
        "map_quality": {
            "before": _map_quality(before["analyze"]),
            "after": _map_quality(after["analyze"]),
        },
        "passed": all(
            verdict[k]
            for k in (
                "parity",
                "better_map_quality",
                "fewer_cycles",
                "fewer_mixed_files",
                "after_rejects_empty",
            )
        ),
    }

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        _print_report(before, after, verdict)

    # Hard requirements for CI: parity + structure wins (not flaky µs alone)
    hard = (
        verdict["parity"]
        and verdict["better_map_quality"]
        and verdict["fewer_cycles"]
        and verdict["fewer_mixed_files"]
        and verdict["after_rejects_empty"]
    )
    # early_exit_faster is soft (timing noise) but reported
    return 0 if hard else 1


if __name__ == "__main__":
    raise SystemExit(main())
