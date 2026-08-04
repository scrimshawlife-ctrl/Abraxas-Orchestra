"""Mermaid + write helpers for Orchestra diagrams."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def mermaid_from_graph(graph: dict[str, Any]) -> str:
    lines = ["```mermaid", "flowchart LR"]
    for n in graph.get("nodes") or []:
        nid = str(n["id"]).replace("-", "_")
        label = f'{n.get("mechanical", n["id"])}<br/>{n.get("symbolic", "")}'.replace('"', "'")
        lines.append(f'  {nid}["{label}"]')
    for e in graph.get("edges") or []:
        a = str(e["from"]).replace("-", "_")
        b = str(e["to"]).replace("-", "_")
        lines.append(f"  {a} --> {b}")
    lines.append("```")
    flows = graph.get("flows") or []
    if flows:
        lines.append("")
        lines.append("<!-- flows")
        for f in flows:
            steps = " → ".join(f.get("steps") or [])
            lines.append(f"  {f.get('id')}: {f.get('name')} :: {steps}")
        lines.append("-->")
    meta = [
        f"<!-- orchestra-diagram.v1 framework={graph.get('framework')} -->",
        f"<!-- overlay={graph.get('secondary_overlay')} -->",
        "",
    ]
    return "\n".join(meta + lines) + "\n"


def write_diagram_files(
    out_dir: Path,
    graph: dict[str, Any],
    *,
    html: str,
    quiet: bool = False,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "architecture.json").write_text(
        json.dumps(graph, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "architecture.html").write_text(html, encoding="utf-8")
    (out_dir / "architecture.mmd").write_text(
        mermaid_from_graph(graph), encoding="utf-8"
    )
    if not quiet:
        print(f"# wrote diagram → {out_dir}")
        print(
            f"#   architecture.json  ({len(graph.get('nodes') or [])} nodes, "
            f"{len(graph.get('edges') or [])} edges, {len(graph.get('flows') or [])} flows)"
        )
        print("#   architecture.html")
        print("#   architecture.mmd")
