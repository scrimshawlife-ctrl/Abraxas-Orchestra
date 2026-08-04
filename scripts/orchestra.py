#!/usr/bin/env python3
"""
Abraxas Orchestra — CLI entrypoint (v0.1 executable surface)

Minimal, fail-closed, dual-naming skeleton emitter.
Stdlib only. No external dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "0.1.0"
SKILL_ROOT = Path(__file__).resolve().parent.parent

FRAMEWORKS: dict[str, dict[str, Any]] = {
    "tree-of-life": {
        "title": "Tree of Life",
        "reference": "references/tree-of-life-mappings.md",
        "default_loci": [
            ("intent", "kether", "System intent / entry contract"),
            ("intake", "chokmah", "Raw force intake"),
            ("constraint", "binah", "Schema / form constraint"),
            ("expand", "chesed", "Generative expansion"),
            ("adversarial", "geburah", "Severity / filtering"),
            ("synthesis", "tiphareth", "Central judgment / scoring"),
            ("persist", "netzach", "Enduring pattern"),
            ("analyze", "hod", "Analytical decomposition"),
            ("store", "yesod", "Foundation / substrate"),
            ("output", "malkuth", "Concrete manifestation"),
        ],
        "core_collapse": ["intent", "synthesis", "output"],
    },
    "alchemical-stages": {
        "title": "Alchemical Stages",
        "reference": "references/alchemical-stages.md",
        "default_loci": [
            ("raw_ingest", "nigredo", "Chaos / putrefaction intake"),
            ("purify", "albedo", "Separation / schema wash"),
            ("illuminate", "citrinitas", "Insight / scoring"),
            ("coagulate", "rubedo", "Final stable emission"),
        ],
        "core_collapse": ["raw_ingest", "illuminate", "coagulate"],
    },
    "elder-futhark": {
        "title": "Elder Futhark",
        "reference": "references/elder-futhark.md",
        "default_loci": [
            ("resource", "fehu", "Resource / wealth pool"),
            ("signal_intake", "ansuz", "Inspired signal intake"),
            ("hard_constraint", "nauthiz", "Need-driven constraint"),
            ("protection", "algiz", "Guardian / protection layer"),
            ("just_judgment", "tiwaz", "Ordered judgment"),
            ("human_surface", "mannaz", "Human / community surface"),
            ("inherited_store", "othala", "Ancestral / inherited store"),
        ],
        "core_collapse": ["signal_intake", "just_judgment", "human_surface"],
    },
    "planetary-spheres": {
        "title": "Planetary Spheres",
        "reference": "references/planetary-spheres.md",
        "default_loci": [
            ("boundary", "saturn", "Hard boundary / persistence"),
            ("governance", "jupiter", "Expansion policy / law"),
            ("adversarial", "mars", "Severity / conflict"),
            ("core", "sun", "Central synthesis / sovereignty"),
            ("relation", "venus", "Relation / value"),
            ("comms", "mercury", "Translation / messaging"),
            ("memory", "moon", "Memory / flux"),
        ],
        "core_collapse": ["boundary", "core", "comms"],
    },
    "iching-hexagrams": {
        "title": "I Ching (curated)",
        "reference": "references/iching-hexagrams.md",
        "default_loci": [
            ("init", "qian_creative", "Pure initiation"),
            ("wait", "xu_waiting", "Deliberate accumulation"),
            ("conflict", "song_conflict", "Open polarity"),
            ("harmony", "tai_peace", "Balanced flow"),
            ("return", "fu_return", "Cyclic renewal"),
            ("revolution", "ge_revolution", "Radical change"),
            ("completion", "jiji_completion", "Ordered completion"),
        ],
        "core_collapse": ["init", "harmony", "completion"],
    },
    "solomonic": {
        "title": "Solomonic Hierarchy",
        "reference": "references/solomonic.md",
        "default_loci": [
            ("sovereign", "king_contract", "Root authority"),
            ("domain_owner", "duke_service", "Major domain ownership"),
            ("executive", "president_admin", "Operational control"),
            ("task_agent", "knight_worker", "Task-scoped worker"),
            ("knowledge", "solomonic_knowledge", "Revelation / research"),
            ("binding", "solomonic_bind", "Constraint / containment"),
            ("judgment", "solomonic_justice", "Truth / judgment"),
        ],
        "core_collapse": ["sovereign", "executive", "task_agent"],
    },
    "peircean-signs": {
        "title": "Peircean Signs",
        "reference": "references/peircean-signs.md",
        "default_loci": [
            ("likeness", "icon", "Similarity representation"),
            ("trace", "index", "Causal / contiguity link"),
            ("convention", "symbol", "Conventional code"),
            ("type_schema", "legisign", "General type / law"),
            ("instance", "sinsign", "Concrete token / event"),
            ("inference", "argument", "Necessary consequence"),
        ],
        "core_collapse": ["trace", "convention", "inference"],
    },
    "numogram": {
        "title": "Numogram",
        "reference": "references/numogram.md",
        "default_loci": [
            ("potential", "zone_0", "Void / pure potential"),
            ("init", "zone_1", "First differentiation"),
            ("structure", "zone_4", "Stable order"),
            ("threshold", "zone_5", "Tipping / intensive peak"),
            ("feedback", "zone_6", "Resonance / amplify"),
            ("completion", "zone_9", "Return / final intensity"),
        ],
        "core_collapse": ["init", "threshold", "completion"],
    },
    "sacred-geometry": {
        "title": "Sacred Geometry",
        "reference": "references/sacred-geometry.md",
        "default_loci": [
            ("nested_core", "golden_depth", "φ-bounded nesting"),
            ("coord_graph", "tetrahedral_core", "Minimal coordination"),
            ("shared_zone", "vesica_interface", "Shared contract overlap"),
            ("fractal_layer", "self_similar", "Recursive repetition"),
        ],
        "core_collapse": ["nested_core", "shared_zone"],
    },
    "enochian": {
        "title": "Enochian",
        "reference": "references/enochian.md",
        "default_loci": [
            ("edge_intake", "aethyr_tex", "Material gateway / edge intake"),
            ("air_comms", "watchtower_east", "Air domain — analysis / messaging"),
            ("fire_transform", "watchtower_south", "Fire domain — transformation"),
            ("water_memory", "watchtower_west", "Water domain — memory / flux"),
            ("earth_persist", "watchtower_north", "Earth domain — persistence"),
            ("domain_entry", "enochian_call", "Invocation / domain-entry token"),
            ("sovereign_intent", "aethyr_lil", "Apex intent / pure contract"),
        ],
        "core_collapse": ["edge_intake", "domain_entry", "sovereign_intent"],
    },
    "chaos-magic": {
        "title": "Chaos Magic",
        "reference": "references/chaos-magic.md",
        "default_loci": [
            ("paradigm_switch", "chaos_shift", "Paradigm engine / framework select"),
            ("intent_token", "sigil_glyph", "Compressed intent token"),
            ("context_reset", "banishing_clear", "Session / context banishing"),
            ("outcome_gate", "results_metric", "Results eval gate"),
            ("custom_alphabet", "alphabet_desire", "Project-local symbolic encoding"),
        ],
        "core_collapse": ["paradigm_switch", "intent_token", "outcome_gate"],
    },
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cmd_list_frameworks(_: argparse.Namespace) -> int:
    print(f"Abraxas Orchestra {VERSION} — available frameworks\n")
    for key, meta in FRAMEWORKS.items():
        ref = meta["reference"]
        exists = (SKILL_ROOT / ref).exists()
        status = "OK" if exists else "MISSING_REF"
        print(f"  {key:22}  {meta['title']:28}  [{status}]")
    print()
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    errors: list[str] = []
    required = [
        "SKILL.md",
        "orchestra.manifest.yaml",
        "VERSION",
        "schemas/correspondence-table.v1.schema.json",
    ]
    for rel in required:
        if not (SKILL_ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    for key, meta in FRAMEWORKS.items():
        ref = SKILL_ROOT / meta["reference"]
        if not ref.exists():
            errors.append(f"missing reference for {key}: {meta['reference']}")

    if errors:
        print("CHECK FAILED")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"CHECK OK — Orchestra {VERSION}")
    print(f"  skill root : {SKILL_ROOT}")
    print(f"  frameworks : {len(FRAMEWORKS)}")
    return 0


def _select_loci(
    framework: str, concerns: list[str] | None
) -> list[tuple[str, str, str]]:
    meta = FRAMEWORKS[framework]
    defaults = meta["default_loci"]
    if not concerns:
        return list(defaults)

    selected: list[tuple[str, str, str]] = []
    for concern in concerns:
        c = concern.strip().lower()
        matched = False
        for mech, sym, note in defaults:
            if c in mech.lower() or c in sym.lower() or c in note.lower():
                selected.append((mech, sym, note))
                matched = True
        if not matched:
            selected.append((concern, f"unmapped_{concern}", "FORCED — no clean locus"))
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for item in selected:
        if item[0] not in seen:
            seen.add(item[0])
            out.append(item)
    return out


def _apply_pragmatic_projection(
    framework: str, loci: list[tuple[str, str, str]]
) -> tuple[list[tuple[str, str, str]], str | None]:
    forced = [x for x in loci if x[2].startswith("FORCED")]
    clean = [x for x in loci if not x[2].startswith("FORCED")]

    meta = FRAMEWORKS[framework]
    core_names = set(meta.get("core_collapse") or [])

    projection_note: str | None = None

    if forced:
        loci = clean
        projection_note = (
            f"Dropped {len(forced)} FORCED locus/loci; retained clean mappings only."
        )

    if len(loci) > 6 and core_names:
        collapsed = [x for x in loci if x[0] in core_names]
        if not collapsed:
            collapsed = [loci[0], loci[len(loci) // 2], loci[-1]]
        dropped = len(loci) - len(collapsed)
        loci = collapsed
        extra = f" Collapsed {dropped} non-core loci to framework core set."
        projection_note = (projection_note or "") + extra

    return loci, projection_note


def _overlay_annotation(
    primary_loci: list[tuple[str, str, str]], overlay: str
) -> list[str]:
    if overlay not in FRAMEWORKS:
        return []
    o_loci = FRAMEWORKS[overlay]["default_loci"]
    notes: list[str] = []
    for i, _ in enumerate(primary_loci):
        if i < len(o_loci):
            _, o_sym, o_note = o_loci[i]
            notes.append(f"overlay:{overlay}/{o_sym} ({o_note})")
        else:
            notes.append(f"overlay:{overlay}/—")
    return notes


def _module_stub_py(mech: str, sym: str, note: str, overlay_line: str | None) -> str:
    overlay_doc = f"\n    Overlay: {overlay_line}" if overlay_line else ""
    return f'''"""
{mech} — dual-named module stub

mechanical: {mech}
symbolic:   {sym}
locus:      {note}{overlay_doc}

Generated by Abraxas Orchestra {VERSION}.
Replace this stub with production implementation.
"""

from __future__ import annotations

from typing import Any


def placeholder() -> dict[str, Any]:
    """Minimal typed placeholder. Operator replaces with real logic."""
    return {{
        "mechanical": "{mech}",
        "symbolic": "{sym}",
        "status": "STUB",
    }}
'''


def _write_skeleton(
    out_dir: Path,
    framework: str,
    meta: dict[str, Any],
    loci: list[tuple[str, str, str]],
    table: dict[str, Any],
    overlay_notes: list[str],
    *,
    python_stubs: bool = True,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    table_path = out_dir / "correspondence-table.json"
    table_path.write_text(json.dumps(table, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Skeleton — {framework} ({meta['title']})",
        "",
        f"Status: {table['status']}",
        f"Generated: {table['provenance']['timestamp']}",
        f"Skill: Orchestra {VERSION}",
    ]
    if table.get("pragmatic_projection"):
        lines.append(f"Projection: {table['pragmatic_projection']}")
    lines += ["", "## Dual-named modules", ""]

    for i, (mech, sym, note) in enumerate(loci):
        lines.append(f"### `{mech}/`")
        lines.append(f"- mechanical: `{mech}`")
        lines.append(f"- symbolic: `{sym}`")
        lines.append(f"- locus: {note}")
        ov = overlay_notes[i] if overlay_notes and i < len(overlay_notes) else None
        if ov:
            lines.append(f"- {ov}")
        lines.append("")

        mod_dir = out_dir / mech
        mod_dir.mkdir(parents=True, exist_ok=True)

        if python_stubs:
            (mod_dir / "__init__.py").write_text(
                _module_stub_py(mech, sym, note, ov), encoding="utf-8"
            )
        else:
            stub_body = [
                f"# {mech}",
                "",
                f"mechanical: `{mech}`",
                f"symbolic: `{sym}`",
                f"locus: {note}",
                "",
            ]
            if ov:
                stub_body.append(ov)
                stub_body.append("")
            (mod_dir / "README.md").write_text("\n".join(stub_body), encoding="utf-8")

    (out_dir / "SKELETON.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _build_table(
    framework: str,
    overlay: str | None,
    loci: list[tuple[str, str, str]],
    overlay_notes: list[str],
    projection: str | None,
) -> dict[str, Any]:
    mappings = []
    forced = 0
    for i, (mech, sym, note) in enumerate(loci):
        strength = "FORCED" if note.startswith("FORCED") else "ADEQUATE"
        if strength == "FORCED":
            forced += 1
        entry: dict[str, Any] = {
            "functional_concern": note if not note.startswith("FORCED") else mech,
            "mechanical_name": mech,
            "symbolic_name": sym,
            "symbolic_locus": sym,
            "strength": strength,
            "notes": note,
        }
        if overlay_notes and i < len(overlay_notes):
            entry["overlay_note"] = overlay_notes[i]
        mappings.append(entry)

    status = "FORCED_CORRESPONDENCE" if forced else "CLEAN"
    return {
        "framework": framework,
        "secondary_overlay": overlay,
        "status": status,
        "mappings": mappings,
        "pragmatic_projection": projection,
        "provenance": {
            "operator": "orchestra-cli",
            "timestamp": _utc_now(),
            "skill_version": VERSION,
        },
    }


def _emit_structure(
    framework: str,
    overlay: str | None,
    concerns: list[str] | None,
    out: str | None,
    *,
    project: bool = False,
) -> int:
    if framework not in FRAMEWORKS:
        print(f"NOT_COMPUTABLE — unknown framework: {framework}", file=sys.stderr)
        print(f"Known: {', '.join(FRAMEWORKS)}", file=sys.stderr)
        return 2

    if overlay and overlay not in FRAMEWORKS:
        print(f"NOT_COMPUTABLE — unknown overlay: {overlay}", file=sys.stderr)
        return 2
    if overlay and overlay == framework:
        print(
            "NOT_COMPUTABLE — overlay must differ from primary framework",
            file=sys.stderr,
        )
        return 2

    loci = _select_loci(framework, concerns)
    projection: str | None = None
    if project:
        loci, projection = _apply_pragmatic_projection(framework, loci)
        if not loci:
            print(
                "NOT_COMPUTABLE — pragmatic projection removed all loci",
                file=sys.stderr,
            )
            return 2

    meta = FRAMEWORKS[framework]
    overlay_notes = _overlay_annotation(loci, overlay) if overlay else []
    table = _build_table(framework, overlay, loci, overlay_notes, projection)

    print("# Abraxas Orchestra — structure skeleton")
    print(f"# framework : {framework} ({meta['title']})")
    if overlay:
        print(f"# overlay   : {overlay} ({FRAMEWORKS[overlay]['title']})")
    if project:
        print("# mode      : project (pragmatic projection applied)")
    print(f"# status    : {table['status']}")
    if projection:
        print(f"# projection: {projection.strip()}")
    print(f"# generated : {table['provenance']['timestamp']}")
    print()
    print("## Dual-named skeleton")
    print()
    for i, (mech, sym, note) in enumerate(loci):
        print(f"{mech}/")
        print(f"  # mechanical : {mech}")
        print(f"  # symbolic   : {sym}")
        print(f"  # locus note : {note}")
        if overlay_notes and i < len(overlay_notes):
            print(f"  # {overlay_notes[i]}")
        print()

    print("## Correspondence table (JSON)")
    print()
    print(json.dumps(table, indent=2))
    print()

    if out:
        out_dir = Path(out).expanduser().resolve()
        _write_skeleton(
            out_dir, framework, meta, loci, table, overlay_notes, python_stubs=True
        )
        print(f"# wrote skeleton → {out_dir}")
        print("#   SKELETON.md")
        print("#   correspondence-table.json")
        for mech, _, _ in loci:
            print(f"#   {mech}/__init__.py")
        print()

    if table["status"] == "FORCED_CORRESPONDENCE":
        print(
            "# WARNING: one or more concerns had no clean locus. "
            "Review FORCED mappings before accepting.",
            file=sys.stderr,
        )
        return 1
    return 0


def cmd_structure(args: argparse.Namespace) -> int:
    concerns = None
    if args.concerns:
        concerns = [c.strip() for c in args.concerns.split(",") if c.strip()]
    return _emit_structure(
        args.framework, args.overlay, concerns, args.out, project=False
    )


def cmd_project(args: argparse.Namespace) -> int:
    concerns = None
    if args.concerns:
        concerns = [c.strip() for c in args.concerns.split(",") if c.strip()]
    return _emit_structure(
        args.framework, args.overlay, concerns, args.out, project=True
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="orchestra",
        description="Abraxas Orchestra — symbolic code architecture CLI",
    )
    p.add_argument("--version", action="version", version=f"Orchestra {VERSION}")
    sub = p.add_subparsers(dest="command", required=True)

    do_p = sub.add_parser("do", help="Execute an intent")
    do_sub = do_p.add_subparsers(dest="intent", required=True)

    def add_structure_args(sp: argparse.ArgumentParser) -> None:
        sp.add_argument(
            "--framework", "-f", required=True, help="Primary framework key"
        )
        sp.add_argument("--overlay", "-o", default=None, help="Secondary overlay")
        sp.add_argument(
            "--concerns", "-c", default=None, help="Comma-separated concerns"
        )
        sp.add_argument(
            "--out", default=None, help="Write skeleton + JSON to DIR"
        )

    struct_p = do_sub.add_parser(
        "structure", help="Emit dual-named skeleton + correspondence table"
    )
    add_structure_args(struct_p)
    struct_p.set_defaults(func=cmd_structure)

    project_p = do_sub.add_parser(
        "project",
        help="Emit skeleton with pragmatic projection (collapse oversized / forced maps)",
    )
    add_structure_args(project_p)
    project_p.set_defaults(func=cmd_project)

    list_p = do_sub.add_parser("list-frameworks", help="List available frameworks")
    list_p.set_defaults(func=cmd_list_frameworks)

    check_p = sub.add_parser("check", help="Validate skill integrity")
    check_p.set_defaults(func=cmd_check)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
