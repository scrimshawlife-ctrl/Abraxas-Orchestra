"""Diagram graph + HTML emitters for Abraxas Orchestra."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "0.3.2"
FRAMEWORKS: dict[str, dict[str, Any]] = {}


def set_context(version: str, frameworks: dict[str, dict[str, Any]]) -> None:
    global VERSION, FRAMEWORKS
    VERSION = version
    FRAMEWORKS = frameworks


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _graph_from_loci(
    framework: str,
    overlay: str | None,
    loci: list[tuple[str, str, str]],
    overlay_notes: list[str],
) -> dict[str, Any]:
    """Build agent-facing {nodes, edges, flows} from dual-named loci."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    for i, (mech, sym, note) in enumerate(loci):
        node: dict[str, Any] = {
            "id": mech,
            "mechanical": mech,
            "symbolic": sym,
            "label": f"{mech} · {sym}",
            "note": note,
            "order": i,
        }
        if overlay_notes and i < len(overlay_notes):
            node["overlay"] = overlay_notes[i]
        nodes.append(node)
        if i > 0:
            prev = loci[i - 1][0]
            edges.append(
                {
                    "id": f"e-{prev}-{mech}",
                    "from": prev,
                    "to": mech,
                    "kind": "sequence",
                }
            )

    flows = [
        {
            "id": "primary",
            "name": f"{framework} primary path",
            "steps": [m for m, _, _ in loci],
        }
    ]
    core = list(FRAMEWORKS.get(framework, {}).get("core_collapse") or [])
    core_steps = [m for m, _, _ in loci if m in core]
    if core_steps and core_steps != [m for m, _, _ in loci]:
        flows.append(
            {
                "id": "core",
                "name": f"{framework} core collapse",
                "steps": core_steps,
            }
        )
    if overlay and overlay in FRAMEWORKS:
        flows.append(
            {
                "id": f"overlay-{overlay}",
                "name": f"overlay · {overlay}",
                "steps": [m for m, _, _ in loci],
            }
        )

    return {
        "schema": "orchestra-diagram.v1",
        "framework": framework,
        "secondary_overlay": overlay,
        "nodes": nodes,
        "edges": edges,
        "flows": flows,
        "provenance": {
            "operator": "orchestra-cli",
            "timestamp": _utc_now(),
            "skill_version": VERSION,
        },
    }


def _html_diagram(graph: dict[str, Any]) -> str:
    """Self-contained interactive architecture HTML."""
    title = graph.get("framework", "orchestra")
    data = json.dumps(graph, indent=2)
    data_js = data.replace("</", "<\\/")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Orchestra diagram — {title}</title>
<style>
  :root {{
    --bg: #0f1115; --panel: #171a21; --line: #2a3140; --text: #e8eaed;
    --muted: #9aa3b2; --accent: #7c9cff; --hot: #f0c14a; --node: #1e2430;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: ui-sans-serif, system-ui, sans-serif;
    background: var(--bg); color: var(--text); display: flex; height: 100vh;
  }}
  #canvas-wrap {{ flex: 1; position: relative; overflow: hidden; }}
  svg {{ width: 100%; height: 100%; }}
  .edge {{ stroke: #3d4660; stroke-width: 2; fill: none; }}
  .edge.hot {{ stroke: var(--hot); stroke-width: 3; }}
  .node rect {{
    fill: var(--node); stroke: #3d4660; stroke-width: 1.5; rx: 10;
  }}
  .node.hot rect {{ stroke: var(--hot); stroke-width: 2.5; }}
  .node text {{ fill: var(--text); font-size: 12px; }}
  .node .sym {{ fill: var(--muted); font-size: 10px; }}
  #side {{
    width: 320px; max-width: 40vw; background: var(--panel);
    border-left: 1px solid var(--line); padding: 16px; overflow: auto;
  }}
  h1 {{ font-size: 15px; margin: 0 0 4px; }}
  .meta {{ color: var(--muted); font-size: 12px; margin-bottom: 16px; }}
  .flow {{
    display: block; width: 100%; text-align: left; margin: 0 0 8px;
    padding: 10px 12px; border-radius: 8px; border: 1px solid var(--line);
    background: transparent; color: var(--text); cursor: pointer;
  }}
  .flow:hover, .flow.active {{ border-color: var(--accent); background: #1c2230; }}
  .flow strong {{ display: block; font-size: 13px; }}
  .flow span {{ color: var(--muted); font-size: 11px; }}
  #tip {{
    position: absolute; pointer-events: none; display: none;
    background: #12151c; border: 1px solid var(--line); border-radius: 8px;
    padding: 8px 10px; font-size: 12px; max-width: 260px; z-index: 5;
  }}
  #tip .k {{ color: var(--muted); }}
</style>
</head>
<body>
  <div id="canvas-wrap">
    <svg id="svg"></svg>
    <div id="tip"></div>
  </div>
  <aside id="side">
    <h1>Orchestra diagram</h1>
    <div class="meta" id="meta"></div>
    <div id="flows"></div>
  </aside>
<script>
const GRAPH = {data_js};
const svg = document.getElementById('svg');
const tip = document.getElementById('tip');
const meta = document.getElementById('meta');
const flowsEl = document.getElementById('flows');

meta.textContent = [
  GRAPH.framework,
  GRAPH.secondary_overlay ? 'overlay · ' + GRAPH.secondary_overlay : null,
  (GRAPH.nodes || []).length + ' nodes',
].filter(Boolean).join(' · ');

const W = 900, H = 640;
svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

function layout(nodes) {{
  const n = nodes.length || 1;
  const padX = 80, padY = 80;
  if (n <= 8) {{
    const pos = {{}};
    nodes.forEach((node, i) => {{
      pos[node.id] = {{
        x: padX + i * ((W - padX * 2) / Math.max(n - 1, 1)),
        y: H / 2,
      }};
    }});
    return pos;
  }}
  const cols = Math.ceil(Math.sqrt(n));
  const rows = Math.ceil(n / cols);
  const dx = (W - padX * 2) / Math.max(cols - 1, 1);
  const dy = (H - padY * 2) / Math.max(rows - 1, 1);
  const pos = {{}};
  nodes.forEach((node, i) => {{
    const c = i % cols, r = Math.floor(i / cols);
    pos[node.id] = {{ x: padX + c * dx, y: padY + r * dy }};
  }});
  return pos;
}}

let POS = layout(GRAPH.nodes || []);
let activeFlow = null;

function clearHot() {{
  svg.querySelectorAll('.hot').forEach(el => el.classList.remove('hot'));
}}

function highlight(flow) {{
  clearHot();
  if (!flow) return;
  const steps = flow.steps || [];
  const set = new Set(steps);
  svg.querySelectorAll('.node').forEach(el => {{
    if (set.has(el.dataset.id)) el.classList.add('hot');
  }});
  for (let i = 0; i < steps.length - 1; i++) {{
    svg.querySelectorAll('.edge').forEach(el => {{
      if (el.dataset.from === steps[i] && el.dataset.to === steps[i+1]) {{
        el.classList.add('hot');
      }}
    }});
  }}
}}

function draw() {{
  svg.innerHTML = '';
  const gEdges = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  const gNodes = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  (GRAPH.edges || []).forEach(e => {{
    const a = POS[e.from], b = POS[e.to];
    if (!a || !b) return;
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const midX = (a.x + b.x) / 2;
    path.setAttribute('d', 'M ' + a.x + ' ' + a.y + ' C ' + midX + ' ' + a.y + ', ' + midX + ' ' + b.y + ', ' + b.x + ' ' + b.y);
    path.setAttribute('class', 'edge');
    path.dataset.id = e.id;
    path.dataset.from = e.from;
    path.dataset.to = e.to;
    gEdges.appendChild(path);
  }});
  (GRAPH.nodes || []).forEach(n => {{
    const p = POS[n.id];
    if (!p) return;
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'node');
    g.dataset.id = n.id;
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', p.x - 70);
    rect.setAttribute('y', p.y - 28);
    rect.setAttribute('width', 140);
    rect.setAttribute('height', 56);
    const t1 = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    t1.setAttribute('x', p.x);
    t1.setAttribute('y', p.y - 4);
    t1.setAttribute('text-anchor', 'middle');
    t1.textContent = n.mechanical;
    const t2 = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    t2.setAttribute('x', p.x);
    t2.setAttribute('y', p.y + 14);
    t2.setAttribute('text-anchor', 'middle');
    t2.setAttribute('class', 'sym');
    t2.textContent = n.symbolic;
    g.appendChild(rect); g.appendChild(t1); g.appendChild(t2);
    g.addEventListener('mousemove', (ev) => {{
      tip.style.display = 'block';
      tip.style.left = (ev.clientX + 12) + 'px';
      tip.style.top = (ev.clientY + 12) + 'px';
      tip.innerHTML = '<div><strong>' + n.mechanical + '</strong></div>'
        + '<div class="k">symbolic</div><div>' + n.symbolic + '</div>'
        + (n.note ? '<div class="k">note</div><div>' + n.note + '</div>' : '')
        + (n.overlay ? '<div class="k">overlay</div><div>' + n.overlay + '</div>' : '');
    }});
    g.addEventListener('mouseleave', () => {{ tip.style.display = 'none'; }});
    gNodes.appendChild(g);
  }});
  svg.appendChild(gEdges);
  svg.appendChild(gNodes);
  if (activeFlow) highlight(activeFlow);
}}

(GRAPH.flows || []).forEach(f => {{
  const btn = document.createElement('button');
  btn.className = 'flow';
  btn.innerHTML = '<strong>' + f.name + '</strong><span>' + (f.steps || []).join(' → ') + '</span>';
  btn.addEventListener('click', () => {{
    activeFlow = f;
    flowsEl.querySelectorAll('.flow').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    highlight(f);
  }});
  flowsEl.appendChild(btn);
}});

draw();
</script>
</body>
</html>
"""


def run_diagram(
    *,
    framework: str,
    overlay: str | None,
    loci: list[tuple[str, str, str]],
    overlay_notes: list[str],
    out: str | None,
    quiet: bool = False,
) -> dict:
    """Emit JSON (+ HTML/Mermaid when out set). Returns graph dict."""
    from diagram_mermaid import write_diagram_files

    graph = _graph_from_loci(framework, overlay, loci, overlay_notes)
    if not out:
        print(json.dumps(graph, indent=2))
        return graph
    out_dir = Path(out).expanduser().resolve()
    write_diagram_files(
        out_dir,
        graph,
        html=_html_diagram(graph),
        quiet=quiet,
    )
    return graph


def emit_diagram_bundle(
    *,
    version: str,
    frameworks: dict[str, dict[str, Any]],
    framework: str,
    overlay: str | None,
    loci: list[tuple[str, str, str]],
    overlay_notes: list[str],
    out_dir: Path,
    quiet: bool = True,
) -> dict:
    """Always-on diagram emission for structure/project --out paths."""
    set_context(version, frameworks)
    return run_diagram(
        framework=framework,
        overlay=overlay,
        loci=loci,
        overlay_notes=overlay_notes,
        out=str(out_dir),
        quiet=quiet,
    )


def emit_observed_diagram(
    graph: dict[str, Any],
    out_dir: Path,
    *,
    quiet: bool = True,
) -> dict:
    """Write diagram bundle from a pre-built observed/import graph."""
    from diagram_mermaid import write_diagram_files

    write_diagram_files(
        out_dir,
        graph,
        html=_html_diagram(graph),
        quiet=quiet,
    )
    return graph
