"""Import-line rewrite helpers for Orchestra optimize apply.

Stdlib only. Mechanical module-id renames; preserves `as old` aliases.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from optimize_enrich import under_root


def rewrite_import_line(line: str, id_map: dict[str, str]) -> str:
    """Rewrite module names on import lines; keep `as old` aliases so call sites stay valid."""
    stripped = line.lstrip()
    if not (stripped.startswith("import ") or stripped.startswith("from ")):
        return line
    new_line = line
    for old, new in sorted(id_map.items(), key=lambda x: -len(x[0])):
        leaf_old = old.split(".")[-1]
        leaf_new = new.split(".")[-1]
        m = re.match(
            rf"^(\s*from\s+\.+\s+import\s+)({re.escape(leaf_old)})(\s*(?:#.*)?)$",
            new_line,
        )
        if m and leaf_old != leaf_new:
            new_line = f"{m.group(1)}{leaf_new} as {leaf_old}{m.group(3)}"
            continue
        new_line = re.sub(
            rf"(from\s+\.+)({re.escape(leaf_old)})(\s+import\b)",
            rf"\1{leaf_new}\3",
            new_line,
        )
        replaced = re.sub(
            rf"(?<![\w.]){re.escape(old)}(?=[\s.,\\]|$)",
            new,
            new_line,
        )
        if replaced != new_line and " as " not in replaced:
            bare = re.match(
                rf"^(\s*import\s+)({re.escape(new)})(\s*(?:#.*)?)$",
                replaced,
            )
            if bare and leaf_old != leaf_new:
                replaced = f"{bare.group(1)}{new} as {leaf_old}{bare.group(3)}"
        new_line = replaced
    return new_line

def rewrite_imports_in_tree(
    root: Path,
    id_map: dict[str, str],
    *,
    dry_run: bool,
) -> list[str]:
    """Rewrite import module names for renamed modules. Returns touched rel paths."""
    touched: list[str] = []
    if not id_map:
        return touched
    for py in root.rglob("*.py"):
        if any(
            part in {".venv", "venv", "__pycache__", ".git", ".orchestra-backups"}
            for part in py.parts
        ):
            continue
        if not under_root(py, root):
            continue
        try:
            text = py.read_text(encoding="utf-8")
        except OSError:
            continue
        lines = text.splitlines(keepends=True)
        changed = False
        out_lines: list[str] = []
        for line in lines:
            rewritten = rewrite_import_line(line, id_map)
            if rewritten != line:
                changed = True
            out_lines.append(rewritten)
        if not changed:
            continue
        rel = str(py.relative_to(root))
        touched.append(rel)
        if not dry_run:
            py.write_text("".join(out_lines), encoding="utf-8")
    return touched
