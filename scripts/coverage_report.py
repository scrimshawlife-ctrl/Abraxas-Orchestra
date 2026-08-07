#!/usr/bin/env python3
"""Soft quality / coverage report for Orchestra (stdlib only).

Most CLI tests drive the product via *subprocess*, so a naive line tracer on
unittest discovery under-reports real coverage. This report therefore has three
layers:

1. **Import check** — every ``scripts/*.py`` imports cleanly
2. **Test linkage** — which scripts are named/imported from ``tests/``
3. **In-process line coverage** — modules exercised by pure unit tests
   (``test_mapping``, ``test_integrity``, ``test_semver``, …) under ``trace``

Exit codes:
  0 — report produced and import check passed
  2 — import failure or unit tests failed under the tracer

With ``--gate``, also enforces hard floors on core modules (CI gate).
"""

from __future__ import annotations

import argparse
import importlib
import os
import re
import sys
import trace
import unittest
from pathlib import Path

# In-process line-coverage floors for core modules (percent).
# Tuned to pure unit tests (not CLI subprocess suite). Raise deliberately.
COVERAGE_FLOORS: dict[str, float] = {
    "analyze_repo.py": 15.0,
    "analyze_langs.py": 35.0,
    "bump_version.py": 40.0,
    "integrity_check.py": 25.0,
}

# Scripts that must be mentioned from tests/ (subprocess CLI coverage counts).
REQUIRED_LINKAGE: tuple[str, ...] = (
    "analyze_repo.py",
    "analyze_langs.py",
    "orchestra.py",
    "optimize_apply.py",
    "optimize_plan.py",
    "optimize_enrich.py",
    "bump_version.py",
    "integrity_check.py",
    "coverage_report.py",
)


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _script_files(root: Path) -> list[Path]:
    return sorted(
        p
        for p in (root / "scripts").glob("*.py")
        if p.is_file() and p.name != "__init__.py"
    )


def _import_check(root: Path, scripts: list[Path]) -> list[str]:
    """Import each script as a module; return error strings."""
    scripts_dir = str((root / "scripts").resolve())
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    errors: list[str] = []
    for path in scripts:
        mod_name = path.stem
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        try:
            importlib.import_module(mod_name)
        except Exception as exc:  # noqa: BLE001 — report any import failure
            errors.append(f"{path.name}: import failed: {exc}")
    return errors


def _test_linkage(root: Path, scripts: list[Path]) -> dict[str, list[str]]:
    """Map script basename → test files that mention it."""
    tests_dir = root / "tests"
    test_files = sorted(tests_dir.glob("test_*.py"))
    texts = {t.name: t.read_text(encoding="utf-8") for t in test_files}
    linked: dict[str, list[str]] = {}
    for path in scripts:
        hits: list[str] = []
        stem = path.stem
        name = path.name
        for tname, text in texts.items():
            if (
                name in text
                or stem in text
                or f"import {stem}" in text
                or f"from {stem}" in text
            ):
                hits.append(tname)
        linked[path.name] = hits
    return linked


def _inprocess_coverage(root: Path) -> tuple[bool, dict[str, tuple[int, int, float]], str]:
    """
    Run pure (non-CLI-subprocess-heavy) unit modules under trace.

    Returns (ok, {script_name: (hit, exec, pct)}, note).
    """
    scripts_dir = (root / "scripts").resolve()
    tests_dir = (root / "tests").resolve()
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    if str(tests_dir) not in sys.path:
        sys.path.insert(0, str(tests_dir))
    os.chdir(root)

    # Prefer unit modules that import scripts in-process (not CLI subprocess)
    preferred = [
        "test_mapping",
        "test_integrity",
        "test_semver",
        "test_analyze_langs",
        # do not include test_coverage_report — it re-enters this script
    ]
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for name in preferred:
        f = tests_dir / f"{name}.py"
        if not f.is_file():
            continue
        # Load by path so discovery does not depend on package layout
        suite.addTests(loader.discover(str(tests_dir), pattern=f"{name}.py"))

    if suite.countTestCases() == 0:
        return False, {}, "no in-process unit tests found"

    # Hide unittest noise
    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, "w"))
    tracer = trace.Trace(
        count=True,
        trace=False,
        ignoredirs=[sys.prefix, sys.exec_prefix],
    )
    holder: dict[str, object] = {"result": None}

    def _run() -> None:
        holder["result"] = runner.run(suite)

    tracer.runfunc(_run)
    result = holder["result"]
    ok = bool(result and getattr(result, "wasSuccessful", lambda: False)())

    counts: dict[str, dict[int, int]] = {}
    for (fname, lineno), n in tracer.results().counts.items():
        path = Path(fname).resolve()
        try:
            path.relative_to(scripts_dir)
        except ValueError:
            continue
        if path.suffix != ".py":
            continue
        key = str(path)
        bucket = counts.setdefault(key, {})
        bucket[lineno] = bucket.get(lineno, 0) + n

    per_file: dict[str, tuple[int, int, float]] = {}
    for path in _script_files(root):
        key = str(path.resolve())
        exec_lines: set[int] = set()
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            exec_lines.add(i)
        hit_map = counts.get(key, {})
        hit = {ln for ln in exec_lines if hit_map.get(ln, 0) > 0}
        n_exec = len(exec_lines)
        n_hit = len(hit)
        pct = (100.0 * n_hit / n_exec) if n_exec else 0.0
        # Always record gate modules; others only if touched
        if n_hit > 0 or path.name in COVERAGE_FLOORS:
            per_file[path.name] = (n_hit, n_exec, pct)

    note = (
        "in-process coverage from pure unit tests only "
        f"({', '.join(preferred)}); CLI subprocess tests are not line-traced"
    )
    return ok, per_file, note


def evaluate_gates(
    *,
    import_errors: list[str],
    linked: dict[str, list[str]],
    per_file: dict[str, tuple[int, int, float]],
    unit_ok: bool,
) -> list[str]:
    """Return human-readable gate failures (empty = pass)."""
    fails: list[str] = []
    if import_errors:
        fails.append(f"import check failed ({len(import_errors)} module(s))")
    if not unit_ok:
        fails.append("pure unit tests failed under tracer")
    for name in REQUIRED_LINKAGE:
        if name not in linked or not linked[name]:
            # allow missing file (optional future modules)
            fails.append(f"linkage required: {name} not mentioned in tests/")
    for name, floor in sorted(COVERAGE_FLOORS.items()):
        if name not in per_file:
            fails.append(f"coverage floor: {name} not measured (need >= {floor:.1f}%)")
            continue
        _h, _e, pct = per_file[name]
        if pct + 1e-9 < floor:
            fails.append(
                f"coverage floor: {name} at {pct:.1f}% < required {floor:.1f}%"
            )
    return fails


def run_report(root: Path | None = None, *, gate: bool = False) -> tuple[int, str]:
    root = (root or skill_root()).resolve()
    scripts = _script_files(root)
    lines: list[str] = []
    title = "Orchestra coverage gate report" if gate else "Orchestra soft quality report"
    lines.append(f"{title} (stdlib)")
    lines.append(f"root: {root}")
    lines.append("")

    # 1. Imports
    lines.append("## 1. Import check (scripts/*.py)")
    import_errors = _import_check(root, scripts)
    if import_errors:
        for e in import_errors:
            lines.append(f"  FAIL {e}")
    else:
        lines.append(f"  OK — {len(scripts)} modules import cleanly")
    lines.append("")

    # 2. Linkage
    lines.append("## 2. Test linkage (mentioned from tests/)")
    linked = _test_linkage(root, scripts)
    linked_n = 0
    orphan: list[str] = []
    for name in sorted(linked):
        hits = linked[name]
        if hits:
            linked_n += 1
            lines.append(f"  {name:<28} ← {', '.join(hits)}")
        else:
            orphan.append(name)
    lines.append(f"  linked {linked_n}/{len(scripts)}")
    if orphan:
        lines.append("  not named in tests (may still be hit via smoke/CLI subprocess):")
        for name in orphan:
            lines.append(f"    - {name}")
    lines.append("")

    # 3. In-process coverage
    lines.append("## 3. In-process line coverage (pure unit tests)")
    ok, per_file, note = _inprocess_coverage(root)
    lines.append(f"  {note}")
    if per_file:
        lines.append(f"  {'file':<28} {'hit':>5} {'exec':>5} {'pct':>7} {'floor':>7}")
        lines.append("  " + "-" * 56)
        total_h = total_e = 0
        for name, (h, e, pct) in sorted(per_file.items(), key=lambda x: x[1][2]):
            floor = COVERAGE_FLOORS.get(name)
            floor_s = f"{floor:.1f}%" if floor is not None else "-"
            lines.append(f"  {name:<28} {h:>5} {e:>5} {pct:>6.1f}% {floor_s:>7}")
            total_h += h
            total_e += e
        overall = (100.0 * total_h / total_e) if total_e else 0.0
        lines.append("  " + "-" * 56)
        lines.append(f"  {'SUBTOTAL (listed)':<28} {total_h:>5} {total_e:>5} {overall:>6.1f}%")
    else:
        lines.append("  (no script lines hit by pure unit tests)")
    if not ok:
        lines.append("  note: pure unit tests reported failures under tracer")
    lines.append("")

    gate_fails = evaluate_gates(
        import_errors=import_errors,
        linked=linked,
        per_file=per_file,
        unit_ok=ok,
    )
    if gate:
        lines.append("## 4. Hard gates")
        if gate_fails:
            lines.append("  GATE FAIL")
            for f in gate_fails:
                lines.append(f"  - {f}")
        else:
            lines.append("  GATE OK — imports, linkage, and coverage floors")
        lines.append("")
        lines.append(
            "Floors (in-process %): "
            + ", ".join(f"{k}>={v:.0f}%" for k, v in sorted(COVERAGE_FLOORS.items()))
        )
        lines.append("")
    else:
        lines.append(
            "soft mode — floors not enforced; run with --gate for CI hard gate"
        )
        lines.append(
            "Floors (reference): "
            + ", ".join(f"{k}>={v:.0f}%" for k, v in sorted(COVERAGE_FLOORS.items()))
        )
        lines.append("")

    text = "\n".join(lines)
    if import_errors or not ok:
        return 2, text
    if gate and gate_fails:
        return 2, text
    return 0, text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Soft/hard quality coverage report for Orchestra")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None, help="Write report to this path")
    parser.add_argument(
        "--gate",
        action="store_true",
        help="Enforce hard floors + required test linkage (CI gate)",
    )
    args = parser.parse_args(argv)
    code, text = run_report(args.root, gate=args.gate)
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
