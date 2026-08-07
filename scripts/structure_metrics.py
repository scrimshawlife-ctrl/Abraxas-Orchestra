#!/usr/bin/env python3
"""Structure metrics for Orchestra analysis (stdlib only).

Computes measurable graph/map quality signals used by the before/after
benchmark and embedded under ``analysis["metrics"]``:

- mapping strength histogram + weighted map quality
- import-graph size, edges, nodes in cycles (Tarjan SCC)
- responsibility mix (identifier/call tokens ≥2 concern categories)

Does **not** claim domain CPU speedups.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path
from typing import Any

STRENGTH_WEIGHT: dict[str, int] = {
    "STRONG": 3,
    "ADEQUATE": 2,
    "WEAK": 1,
    "FORCED": 0,
}

CONCERN_TOKENS: dict[str, frozenset[str]] = {
    "intake": frozenset({"load", "pull", "open", "read", "intake", "raw"}),
    "score": frozenset({"score", "reweight", "filter", "analyze", "weight"}),
    "store": frozenset({"persist", "store", "dump", "save", "stamp", "stamp_partial"}),
    "emit": frozenset({"emit", "manifest", "build_report"}),
}


def map_quality_score(mappings: list[dict[str, Any]] | None) -> float:
    """Weighted mapping quality (STRONG best)."""
    total = 0.0
    for m in mappings or []:
        total += float(STRENGTH_WEIGHT.get(str(m.get("strength") or ""), 0))
    return total


def strength_histogram(mappings: list[dict[str, Any]] | None) -> dict[str, int]:
    hist: dict[str, int] = defaultdict(int)
    for m in mappings or []:
        hist[str(m.get("strength") or "?")] += 1
    return dict(hist)


def graph_from_analysis(analysis: dict[str, Any]) -> dict[str, set[str]]:
    """Directed local import graph: node_id → set of local targets."""
    node_ids = {n["id"] for n in (analysis.get("nodes") or []) if n.get("id")}
    graph: dict[str, set[str]] = {nid: set() for nid in node_ids}
    for e in analysis.get("edges") or []:
        if e.get("external"):
            continue
        src, dst = e.get("from"), e.get("to")
        if src in graph and dst in node_ids and src != dst:
            graph[src].add(dst)
    return graph


def count_cycles(graph: dict[str, set[str]]) -> tuple[int, int]:
    """Return (nodes_in_cycles, cyclic_scc_count) via Tarjan SCC + self-loops."""
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

    self_loops = sum(1 for v, outs in graph.items() if v in outs)
    multi = [c for c in sccs if len(c) > 1]
    cyclic_nodes = sum(len(c) for c in multi) + self_loops
    return cyclic_nodes, len(multi) + self_loops


def _identifiers(tree_ast: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree_ast):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
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


def mix_score_for_tree(root: Path) -> dict[str, Any]:
    """Responsibility mix over Python sources under root (skip __init__)."""
    mixed: list[dict[str, Any]] = []
    pure = 0
    if not root.is_dir():
        return {"mixed_files": 0, "pure_files": 0, "mixed_detail": []}
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts or path.name == "__init__.py":
            continue
        try:
            tree_ast = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError, UnicodeError):
            continue
        idents = _identifiers(tree_ast)
        concerns = [c for c, tokens in CONCERN_TOKENS.items() if idents & tokens]
        if len(concerns) >= 2:
            try:
                rel = path.relative_to(root).as_posix()
            except ValueError:
                rel = path.name
            mixed.append({"file": rel, "concerns": concerns})
        elif len(concerns) == 1:
            pure += 1
    return {
        "mixed_files": len(mixed),
        "pure_files": pure,
        "mixed_detail": mixed,
    }


def compute_structure_metrics(
    analysis: dict[str, Any],
    *,
    tree: Path | None = None,
) -> dict[str, Any]:
    """
    Build the metrics block for analysis.json.

    ``tree`` enables responsibility-mix scoring (optional).
    """
    mappings = list(analysis.get("mappings") or [])
    hist = strength_histogram(mappings)
    graph = graph_from_analysis(analysis)
    edge_count = sum(len(v) for v in graph.values())
    cyclic_nodes, cyclic_sccs = count_cycles(graph)

    metrics: dict[str, Any] = {
        "schema": "orchestra-structure-metrics.v1",
        "map": {
            "quality": map_quality_score(mappings),
            "strength_histogram": hist,
            "strong": hist.get("STRONG", 0),
            "adequate": hist.get("ADEQUATE", 0),
            "weak": hist.get("WEAK", 0),
            "forced": hist.get("FORCED", 0),
            "mapping_count": len(mappings),
        },
        "graph": {
            "nodes": len(graph),
            "local_edges": edge_count,
            "nodes_in_cycles": cyclic_nodes,
            "cyclic_sccs": cyclic_sccs,
        },
    }
    if tree is not None:
        mix = mix_score_for_tree(tree)
        metrics["mix"] = {
            "mixed_files": mix["mixed_files"],
            "pure_files": mix["pure_files"],
            "mixed_detail": mix["mixed_detail"],
        }
    return metrics


def format_metrics_summary(metrics: dict[str, Any]) -> str:
    """One-line human summary for stderr."""
    m = metrics.get("map") or {}
    g = metrics.get("graph") or {}
    mix = metrics.get("mix") or {}
    parts = [
        f"map_quality={m.get('quality', 0)}",
        f"strong={m.get('strong', 0)}",
        f"weak={m.get('weak', 0)}",
        f"forced={m.get('forced', 0)}",
        f"cycles={g.get('nodes_in_cycles', 0)}",
        f"edges={g.get('local_edges', 0)}",
    ]
    if mix:
        parts.append(f"mixed_files={mix.get('mixed_files', 0)}")
    return "# metrics: " + " ".join(parts)
