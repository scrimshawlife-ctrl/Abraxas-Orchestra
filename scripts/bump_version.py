#!/usr/bin/env python3
"""Bump Orchestra package version (single source of truth: VERSION file).

Usage:
  python3 scripts/bump_version.py patch|minor|major
  python3 scripts/bump_version.py set X.Y.Z
  python3 scripts/bump_version.py show
  python3 scripts/bump_version.py check

Options:
  --dry-run   Print actions; write nothing
  --root DIR  Repo root (default: parent of scripts/)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SEMVER_CORE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def parse_semver(text: str) -> tuple[int, int, int]:
    """Parse VERSION file form: MAJOR.MINOR.PATCH only (no v-prefix)."""
    text = text.strip()
    m = SEMVER_CORE.match(text)
    if not m:
        raise ValueError(
            f"invalid VERSION {text!r}; expected MAJOR.MINOR.PATCH "
            "(no v-prefix, no pre-release in VERSION file)"
        )
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def format_semver(parts: tuple[int, int, int]) -> str:
    return f"{parts[0]}.{parts[1]}.{parts[2]}"


def bump(parts: tuple[int, int, int], kind: str) -> tuple[int, int, int]:
    major, minor, patch = parts
    if kind == "major":
        return major + 1, 0, 0
    if kind == "minor":
        return major, minor + 1, 0
    if kind == "patch":
        return major, minor, patch + 1
    raise ValueError(kind)


def read_version(root: Path) -> str:
    path = root / "VERSION"
    if not path.is_file():
        raise FileNotFoundError(f"missing {path}")
    return path.read_text(encoding="utf-8").strip()


def replace_once(path: Path, pattern: str, repl: str, *, dry: bool) -> None:
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(pattern, repl, text, count=1, flags=re.MULTILINE)
    if n != 1:
        raise RuntimeError(f"{path}: expected 1 match for {pattern!r}, got {n}")
    if dry:
        print(f"[dry-run] update {path}")
        return
    path.write_text(new, encoding="utf-8")
    print(f"updated {path}")


def apply_version(root: Path, new: str, *, dry: bool) -> None:
    if dry:
        print(f"[dry-run] write VERSION -> {new}")
    else:
        (root / "VERSION").write_text(new + "\n", encoding="utf-8")
        print("updated VERSION")

    replace_once(
        root / "scripts" / "orchestra.py",
        r'^VERSION = "[^"]+"$',
        f'VERSION = "{new}"',
        dry=dry,
    )
    replace_once(
        root / "SKILL.md",
        r"^version:\s*\S+$",
        f"version: {new}",
        dry=dry,
    )
    replace_once(
        root / "orchestra.manifest.yaml",
        r"^version:\s*\S+$",
        f"version: {new}",
        dry=dry,
    )
    replace_once(
        root / "install.sh",
        r'^VERSION="[^"]+"$',
        f'VERSION="{new}"',
        dry=dry,
    )
    install = root / "install.sh"
    text = install.read_text(encoding="utf-8")
    text2, n = re.subn(
        r"(# Abraxas Orchestra — atomic installer \(v)[^)]+(\))",
        rf"\g<1>{new}\2",
        text,
        count=1,
    )
    if n == 1 and text2 != text:
        if dry:
            print("[dry-run] update install.sh header comment")
        else:
            install.write_text(text2, encoding="utf-8")
            print("updated install.sh header")


def check_parity(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        v = read_version(root)
        parse_semver(v)
    except (OSError, ValueError) as exc:
        return [str(exc)]

    checks = [
        (root / "scripts" / "orchestra.py", rf'^VERSION = "{re.escape(v)}"\s*$'),
        (root / "SKILL.md", rf"^version:\s*{re.escape(v)}\s*$"),
        (root / "orchestra.manifest.yaml", rf"^version:\s*{re.escape(v)}\s*$"),
        (root / "install.sh", rf'^VERSION="{re.escape(v)}"\s*$'),
    ]
    for path, pat in checks:
        if not path.is_file():
            errors.append(f"missing {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if not re.search(pat, text, flags=re.MULTILINE):
            errors.append(f"parity fail: {path} does not contain version {v}")
    return errors


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Orchestra semantic version bump")
    p.add_argument(
        "action",
        choices=["show", "check", "patch", "minor", "major", "set"],
        help="show | check | bump kind | set",
    )
    p.add_argument("value", nargs="?", help="X.Y.Z when action=set")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--root", type=Path, default=None)
    args = p.parse_args(argv)

    root = args.root or Path(__file__).resolve().parent.parent
    root = root.resolve()

    if args.action == "show":
        v = read_version(root)
        parse_semver(v)
        print(v)
        return 0

    if args.action == "check":
        errs = check_parity(root)
        if errs:
            for e in errs:
                print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print(f"version check OK ({read_version(root)})")
        return 0

    current = parse_semver(read_version(root))
    if args.action == "set":
        if not args.value:
            print("set requires X.Y.Z", file=sys.stderr)
            return 2
        new = format_semver(parse_semver(args.value))
    else:
        new = format_semver(bump(current, args.action))

    old = format_semver(current)
    if new == old:
        print(f"no change ({old})")
        return 0

    print(f"{old} -> {new}")
    apply_version(root, new, dry=args.dry_run)
    if not args.dry_run:
        print("Next: edit CHANGELOG.md + docs/RELEASE_NOTES.md, then:")
        print("  bash scripts/release_preflight.sh")
        print(f'  git tag -a v{new} -m "Orchestra {new}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
