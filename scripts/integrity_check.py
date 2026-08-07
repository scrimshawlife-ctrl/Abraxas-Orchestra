#!/usr/bin/env python3
"""Critical-file integrity floors for Abraxas Orchestra.

Guards against accidental truncation of CLI entrypoints (see docs/RESTORE_NOTE.md).
Stdlib only. Exit 0 on pass, 2 on fail.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Minimum line counts (with headroom under current sizes). Floors only grow
# when intentional large deletes land — raise deliberately, never silently.
LINE_FLOORS: dict[str, int] = {
    "scripts/orchestra.py": 500,
    "scripts/optimize_apply.py": 300,
    "scripts/optimize_enrich.py": 200,
    "scripts/optimize_rewrite.py": 50,
    "scripts/analyze_repo.py": 400,
    "scripts/optimize_plan.py": 150,
    "install.sh": 150,
    "SKILL.md": 40,
    "VERSION": 1,
}

# Substrings that must appear in critical files (anti-placeholder / anti-empty).
MUST_CONTAIN: dict[str, list[str]] = {
    "scripts/orchestra.py": ["def main", "analyze", "optimize", "CHECK OK"],
    "scripts/optimize_apply.py": ["def apply_optimize_plan", "safe_apply", "--confirm"],
    "install.sh": ["validate_target", "allow-outside-home", "dry-run"],
    "SKILL.md": ["name: orchestra", "analyze", "optimize"],
}


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def check_integrity(root: Path | None = None) -> list[str]:
    """Return list of error strings; empty means pass."""
    root = root or skill_root()
    errors: list[str] = []

    version_path = root / "VERSION"
    if not version_path.is_file():
        errors.append("missing VERSION file")
        version = ""
    else:
        version = version_path.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            errors.append(f"VERSION not semver X.Y.Z: {version!r}")

    for rel, floor in sorted(LINE_FLOORS.items()):
        path = root / rel
        if not path.is_file():
            errors.append(f"missing critical file: {rel}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"unreadable {rel}: {exc}")
            continue
        n = len(text.splitlines())
        if n < floor:
            errors.append(f"{rel}: {n} lines < floor {floor} (possible truncation)")
        if len(text.strip()) < 20 and rel != "VERSION":
            errors.append(f"{rel}: content too small ({len(text)} bytes)")

    for rel, needles in sorted(MUST_CONTAIN.items()):
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing required marker {needle!r}")

    # orchestra.py VERSION constant should match VERSION file when present
    orch = root / "scripts" / "orchestra.py"
    if orch.is_file() and version:
        orch_text = orch.read_text(encoding="utf-8")
        m = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', orch_text)
        if m and m.group(1) != version:
            errors.append(
                f"scripts/orchestra.py VERSION={m.group(1)!r} != VERSION file {version!r}"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Orchestra critical-file integrity check")
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Skill root (default: parent of scripts/)",
    )
    args = parser.parse_args(argv)
    errors = check_integrity(args.root)
    if errors:
        print("INTEGRITY FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 2
    root = args.root or skill_root()
    print(f"INTEGRITY OK — {len(LINE_FLOORS)} critical files under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
