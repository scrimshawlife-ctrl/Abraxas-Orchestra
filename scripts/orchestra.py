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

# ---------------------------------------------------------------------------
# Framework registry (v0.1 — mirrors references/ and manifest)
# ---------------------------------------------------------------------------

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

    # Match concerns against mechanical names (case-insensitive substring)
    selected: list[tuple[str, str, str]] = []
    for concern in concerns:
        c = concern.strip().lower()
        matched = False
        for mech, sym, note in defaults:
            if c in mech.lower() or c in sym.lower() or c in note.lower():
                selected.append((mech, sym, note))
                matched = True
        if not matched:
            # Unknown concern — still emit a forced locus so operator sees it
            selected.append((concern, f"unmapped_{concern}", "FORCED — no clean locus"))
    # Deduplicate while preserving order
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for item in selected:
        if item[0] not in seen:
            seen.add(item[0])
            out.append(item)
    return out


def cmd_structure(args: argparse.Namespace) -> int:
    framework = args.framework
    if framework not in FRAMEWORKS:
        print(f"NOT_COMPUTABLE — unknown framework: {framework}", file=sys.stderr)
        print(f"Known: {', '.join(FRAMEWORKS)}", file=sys.stderr)
        return 2

    concerns = None
    if args.concerns:
        concerns = [c.strip() for c in args.concerns.split(",") if c.strip()]

    loci = _select_loci(framework, concerns)
    meta = FRAMEWORKS[framework]

    # Build correspondence table
    mappings = []
    forced = 0
    for mech, sym, note in loci:
        strength = "FORCED" if note.startswith("FORCED") else "ADEQUATE"
        if strength == "FORCED":
            forced += 1
        mappings.append(
            {
                "functional_concern": note if not note.startswith("FORCED") else mech,
                "mechanical_name": mech,
                "symbolic_name": sym,
                "symbolic_locus": sym,
                "strength": strength,
                "notes": note,
            }
        )

    status = "FORCED_CORRESPONDENCE" if forced else "CLEAN"
    table = {
        "framework": framework,
        "secondary_overlay": None,
        "status": status,
        "mappings": mappings,
        "pragmatic_projection": None,
        "provenance": {
            "operator": "orchestra-cli",
            "timestamp": _utc_now(),
            "skill_version": VERSION,
        },
    }

    # Emit dual-named skeleton (directory-style)
    print(f"# Abraxas Orchestra — structure skeleton")
    print(f"# framework : {framework} ({meta['title']})")
    print(f"# status    : {status}")
    print(f"# generated : {table['provenance']['timestamp']}")
    print()
    print("## Dual-named skeleton")
    print()
    for mech, sym, note in loci:
        print(f"{mech}/")
        print(f"  # mechanical : {mech}")
        print(f"  # symbolic   : {sym}")
        print(f"  # locus note : {note}")
        print()

    print("## Correspondence table (JSON)")
    print()
    print(json.dumps(table, indent=2))
    print()

    if status == "FORCED_CORRESPONDENCE":
        print(
            "# WARNING: one or more concerns had no clean locus. "
            "Review FORCED mappings before accepting.",
            file=sys.stderr,
        )
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="orchestra",
        description="Abraxas Orchestra — symbolic code architecture CLI",
    )
    p.add_argument("--version", action="version", version=f"Orchestra {VERSION}")
    sub = p.add_subparsers(dest="command", required=True)

    # do <intent>
    do_p = sub.add_parser("do", help="Execute an intent")
    do_sub = do_p.add_subparsers(dest="intent", required=True)

    struct_p = do_sub.add_parser(
        "structure", help="Emit dual-named skeleton + correspondence table"
    )
    struct_p.add_argument(
        "--framework",
        "-f",
        required=True,
        help="Framework key (see: do list-frameworks)",
    )
    struct_p.add_argument(
        "--concerns",
        "-c",
        default=None,
        help="Comma-separated functional concerns to map (optional)",
    )
    struct_p.set_defaults(func=cmd_structure)

    list_p = do_sub.add_parser("list-frameworks", help="List available frameworks")
    list_p.set_defaults(func=cmd_list_frameworks)

    # check
    check_p = sub.add_parser("check", help="Validate skill integrity")
    check_p.set_defaults(func=cmd_check)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
