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

VERSION = "0.1.2"
SKILL_ROOT = Path(__file__).resolve().parent.parent

def _load_frameworks() -> dict[str, dict[str, Any]]:
    """Load canonical framework tables from schemas/frameworks.v1.json."""
    path = SKILL_ROOT / "schemas" / "frameworks.v1.json"
    if not path.exists():
        raise SystemExit(f"MISSING frameworks schema: {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    frameworks: dict[str, dict[str, Any]] = {}
    for key, meta in raw.get("frameworks", {}).items():
        loci = []
        for row in meta.get("default_loci", []):
            loci.append(
                (
                    row["mechanical"],
                    row["symbolic"],
                    row.get("note") or "",
                )
            )
        frameworks[key] = {
            "title": meta["title"],
            "reference": meta["reference"],
            "default_loci": loci,
            "core_collapse": list(meta.get("core_collapse") or []),
        }
    return frameworks


FRAMEWORKS: dict[str, dict[str, Any]] = _load_frameworks()


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


def _validate_table_against_schema(table: dict[str, Any]) -> list[str]:
    """Lightweight schema check (stdlib only — no jsonschema dependency)."""
    errors: list[str] = []
    allowed_fw = {
        "tree-of-life", "alchemical-stages", "elder-futhark", "planetary-spheres",
        "iching-hexagrams", "solomonic", "peircean-signs", "numogram",
        "sacred-geometry", "enochian", "chaos-magic", "composite",
    }
    allowed_status = {"CLEAN", "WEAK_MAPPINGS", "FORCED_CORRESPONDENCE", "NOT_COMPUTABLE"}
    allowed_strength = {"STRONG", "ADEQUATE", "WEAK", "FORCED"}
    allowed_map_keys = {
        "functional_concern", "mechanical_name", "symbolic_name", "symbolic_locus",
        "strength", "notes", "overlay_note",
    }
    allowed_top = {
        "framework", "secondary_overlay", "status", "mappings",
        "pragmatic_projection", "provenance",
    }

    for k in table:
        if k not in allowed_top:
            errors.append(f"unknown top-level key: {k}")

    if "framework" not in table:
        errors.append("missing required: framework")
    elif table["framework"] not in allowed_fw:
        errors.append(f"framework not in schema enum: {table['framework']}")

    if "status" not in table:
        errors.append("missing required: status")
    elif table["status"] not in allowed_status:
        errors.append(f"status not in schema enum: {table['status']}")

    if "mappings" not in table:
        errors.append("missing required: mappings")
    elif not isinstance(table["mappings"], list):
        errors.append("mappings must be an array")
    else:
        for i, m in enumerate(table["mappings"]):
            if not isinstance(m, dict):
                errors.append(f"mappings[{i}] not an object")
                continue
            for k in m:
                if k not in allowed_map_keys:
                    errors.append(f"mappings[{i}] unknown key: {k}")
            for req in ("functional_concern", "symbolic_locus", "strength"):
                if req not in m:
                    errors.append(f"mappings[{i}] missing required: {req}")
            if "strength" in m and m["strength"] not in allowed_strength:
                errors.append(f"mappings[{i}] bad strength: {m['strength']}")

    return errors


def cmd_check(_: argparse.Namespace) -> int:
    errors: list[str] = []
    required = [
        "SKILL.md", "orchestra.manifest.yaml", "VERSION",
        "schemas/correspondence-table.v1.schema.json",
        "schemas/frameworks.v1.json",
    ]
    for rel in required:
        if not (SKILL_ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    for key, meta in FRAMEWORKS.items():
        ref = SKILL_ROOT / meta["reference"]
        if not ref.exists():
            errors.append(f"missing reference for {key}: {meta['reference']}")

    for key in FRAMEWORKS:
        loci = _select_loci(key, None)[:3]
        table = _build_table(key, None, loci, [], None)
        for e in _validate_table_against_schema(table):
            errors.append(f"{key}: {e}")

    if "tree-of-life" in FRAMEWORKS and "chaos-magic" in FRAMEWORKS:
        loci = _select_loci("tree-of-life", ["intent", "output"])
        ov_notes = _overlay_annotation(loci, "chaos-magic")
        table = _build_table("tree-of-life", "chaos-magic", loci, ov_notes, None)
        for e in _validate_table_against_schema(table):
            errors.append(f"overlay-sample: {e}")

    if errors:
        print("CHECK FAILED")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"CHECK OK — Orchestra {VERSION}")
    print(f"  skill root : {SKILL_ROOT}")
    print(f"  frameworks : {len(FRAMEWORKS)}")
    print(f"  schema     : correspondence-table.v1 validated for all frameworks")
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
            stub_body = [f"# {mech}", "", f"mechanical: `{mech}`", f"symbolic: `{sym}`", f"locus: {note}", ""]
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
        print("NOT_COMPUTABLE — overlay must differ from primary framework", file=sys.stderr)
        return 2

    loci = _select_loci(framework, concerns)
    projection: str | None = None
    if project:
        loci, projection = _apply_pragmatic_projection(framework, loci)
        if not loci:
            print("NOT_COMPUTABLE — pragmatic projection removed all loci", file=sys.stderr)
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
        _write_skeleton(out_dir, framework, meta, loci, table, overlay_notes, python_stubs=True)
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
    return _emit_structure(args.framework, args.overlay, concerns, args.out, project=False)


def cmd_project(args: argparse.Namespace) -> int:
    concerns = None
    if args.concerns:
        concerns = [c.strip() for c in args.concerns.split(",") if c.strip()]
    return _emit_structure(args.framework, args.overlay, concerns, args.out, project=True)


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
        sp.add_argument("--framework", "-f", required=True, help="Primary framework key")
        sp.add_argument("--overlay", "-o", default=None, help="Secondary overlay")
        sp.add_argument("--concerns", "-c", default=None, help="Comma-separated concerns")
        sp.add_argument("--out", default=None, help="Write skeleton + JSON to DIR")

    struct_p = do_sub.add_parser("structure", help="Emit dual-named skeleton + correspondence table")
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
