"""Multi-language source graph helpers for Orchestra analyze (stdlib only).

Python remains AST-accurate (handled in analyze_repo). Other languages use
best-effort regex OBSERVED import edges — fail-closed on unsupported langs.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable

# Language key → file extensions
LANG_EXTENSIONS: dict[str, frozenset[str]] = {
    "python": frozenset({".py"}),
    "javascript": frozenset({".js", ".jsx", ".mjs", ".cjs"}),
    "typescript": frozenset({".ts", ".tsx", ".mts", ".cts"}),
    "go": frozenset({".go"}),
    "rust": frozenset({".rs"}),
    "ruby": frozenset({".rb"}),
}

# Alias map for CLI convenience
LANG_ALIASES: dict[str, str] = {
    "py": "python",
    "js": "javascript",
    "jsx": "javascript",
    "ts": "typescript",
    "tsx": "typescript",
    "rs": "rust",
    "rb": "ruby",
    "golang": "go",
    "auto": "auto",
    "multi": "auto",
    "all": "auto",
}

SUPPORTED_LANGS = frozenset(LANG_EXTENSIONS) | {"auto"}


def normalize_lang(lang: str) -> str:
    key = (lang or "python").strip().lower()
    return LANG_ALIASES.get(key, key)


def extensions_for_lang(lang: str) -> frozenset[str]:
    """Return file extensions to collect for a language key (not auto)."""
    n = normalize_lang(lang)
    if n == "auto":
        out: set[str] = set()
        for exts in LANG_EXTENSIONS.values():
            out |= exts
        return frozenset(out)
    if n not in LANG_EXTENSIONS:
        return frozenset()
    return LANG_EXTENSIONS[n]


def language_for_path(path: Path) -> str | None:
    suf = path.suffix.lower()
    for lang, exts in LANG_EXTENSIONS.items():
        if suf in exts:
            return lang
    return None


def module_id_for_file(root: Path, path: Path, lang: str) -> str:
    """Stable module id: path-based, language-aware separators."""
    rel = path.relative_to(root)
    parts = list(rel.parts)
    if lang == "python":
        if parts[-1] == "__init__.py":
            parts = parts[:-1]
        else:
            parts[-1] = Path(parts[-1]).stem
        if not parts:
            return root.name or "root"
        return ".".join(parts)

    if lang == "go":
        # package dir + file stem; prefer directory as package unit for non-test
        stem = Path(parts[-1]).stem
        if stem.endswith("_test"):
            stem = stem[: -len("_test")]
        dir_parts = parts[:-1]
        if dir_parts:
            return "/".join(dir_parts + [stem])
        return stem

    if lang == "rust":
        stem = Path(parts[-1]).stem
        if stem == "mod":
            parts = parts[:-1]
            return "::".join(parts) if parts else "crate"
        if stem == "lib":
            return "crate"
        if stem == "main":
            return "main"
        return "::".join(parts[:-1] + [stem]) if parts else stem

    # JS/TS/Ruby: path with / and no extension
    stem = Path(parts[-1]).stem
    # drop index/mod conventions lightly
    if stem in {"index", "mod"} and len(parts) > 1:
        parts = parts[:-1]
        return "/".join(parts) if parts else stem
    return "/".join(parts[:-1] + [stem])


def _strip_js_comments(text: str) -> str:
    """Strip // and /* */ comments only (keep string literals for import paths)."""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"//.*?$", " ", text, flags=re.M)
    return text


def extract_js_ts_imports(text: str) -> list[str]:
    """Extract import/require/export-from module specifiers."""
    cleaned = _strip_js_comments(text)
    found: list[str] = []
    patterns = [
        r"""\bimport\s+(?:type\s+)?[^'"\n]*?\sfrom\s+['"]([^'"]+)['"]""",
        r"""\bimport\s+['"]([^'"]+)['"]""",
        r"""\bexport\s+(?:type\s+)?[^'"\n]*?\sfrom\s+['"]([^'"]+)['"]""",
        r"""\brequire\s*\(\s*['"]([^'"]+)['"]\s*\)""",
        r"""\bimport\s*\(\s*['"]([^'"]+)['"]\s*\)""",
    ]
    for pat in patterns:
        for m in re.finditer(pat, cleaned):
            found.append(m.group(1))
    # preserve order unique
    out: list[str] = []
    seen: set[str] = set()
    for x in found:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def extract_go_imports(text: str) -> list[str]:
    found: list[str] = []
    # single import "x"
    for m in re.finditer(r'^\s*import\s+(?:\w+\s+)?\"([^\"]+)\"', text, re.M):
        found.append(m.group(1))
    # import ( ... )
    block = re.search(r"^\s*import\s*\((.*?)\)", text, re.S | re.M)
    if block:
        for m in re.finditer(r'\"([^\"]+)\"', block.group(1)):
            found.append(m.group(1))
    out: list[str] = []
    seen: set[str] = set()
    for x in found:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def extract_rust_imports(text: str) -> list[str]:
    found: list[str] = []
    # use foo::bar::{a, b};  use foo::bar;
    for m in re.finditer(r"^\s*use\s+([^;]+);", text, re.M):
        body = m.group(1).strip()
        # take root path before::{
        body = re.sub(r"\s+as\s+\w+", "", body)
        body = body.split("{")[0].strip().rstrip(":")
        if body:
            # normalize foo::bar:: to foo::bar
            body = body.strip(":").replace(" ", "")
            found.append(body)
    for m in re.finditer(r"^\s*mod\s+(\w+)\s*;", text, re.M):
        found.append(m.group(1))
    out: list[str] = []
    seen: set[str] = set()
    for x in found:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def extract_ruby_imports(text: str) -> list[str]:
    found: list[str] = []
    for m in re.finditer(
        r"""^\s*(?:require|require_relative|load)\s*\(?\s*['"]([^'"]+)['"]""",
        text,
        re.M,
    ):
        found.append(m.group(1))
    out: list[str] = []
    seen: set[str] = set()
    for x in found:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


EXTRACTORS: dict[str, Callable[[str], list[str]]] = {
    "javascript": extract_js_ts_imports,
    "typescript": extract_js_ts_imports,
    "go": extract_go_imports,
    "rust": extract_rust_imports,
    "ruby": extract_ruby_imports,
}


def extract_edges_for_file(
    *,
    lang: str,
    text: str,
    root: Path,
    current: Path,
    known: set[str],
    self_id: str,
) -> list[tuple[str, bool]]:
    """Return list of (target_id, external)."""
    if lang == "python":
        return []  # handled by AST in analyze_repo
    extractor = EXTRACTORS.get(lang)
    if not extractor:
        return []
    specs = extractor(text)
    out: list[tuple[str, bool]] = []
    seen: set[str] = set()
    for spec in specs:
        if lang in {"javascript", "typescript"}:
            if spec.startswith("."):
                target = _resolve_rel_path_id(root, current, spec, known, lang)
            else:
                target = spec
        elif lang == "ruby" and (spec.startswith(".") or spec.startswith("/")):
            target = _resolve_rel_path_id(root, current, spec, known, lang)
        elif lang == "go":
            # stdlib / module paths are external unless known suffix match
            target = spec
            for kid in known:
                if kid.endswith(spec.split("/")[-1]) or kid == spec:
                    target = kid
                    break
        elif lang == "rust":
            # crate-local use paths
            if spec.startswith("crate") or spec.startswith("super") or spec.startswith("self"):
                target = spec
            elif "::" in spec or spec.isidentifier():
                target = spec
            else:
                target = spec
            if spec in known:
                target = spec
            else:
                # try last segment
                last = spec.split("::")[-1]
                for kid in known:
                    if kid.endswith(last) or kid.split("::")[-1] == last:
                        target = kid
                        break
        else:
            target = spec

        if not target or target == self_id or target in seen:
            continue
        seen.add(target)
        out.append((target, target not in known))
    return out


def _resolve_rel_path_id(
    root: Path,
    current: Path,
    spec: str,
    known: set[str],
    lang: str,
) -> str:
    base = current.parent
    # normalize ./foo/bar
    try:
        resolved = (base / spec).resolve()
        rel = resolved.relative_to(root.resolve())
    except Exception:
        return spec
    # try matching known modules by suffix path
    candidates = []
    parts = list(rel.parts)
    # with and without index
    joined = "/".join(parts)
    candidates.append(joined)
    if parts:
        candidates.append("/".join(parts[:-1] + [Path(parts[-1]).stem]) if Path(parts[-1]).suffix else joined)
        candidates.append("/".join(p if i < len(parts) - 1 else Path(p).stem for i, p in enumerate(parts)))
    for c in candidates:
        if c in known:
            return c
        # try without extension artifacts
        c2 = re.sub(r"\.(js|ts|tsx|jsx|mjs|cjs)$", "", c)
        if c2 in known:
            return c2
    # default id style
    try:
        synth = root / rel
        if not synth.suffix:
            # guess
            for ext in LANG_EXTENSIONS.get(lang, ()):
                if (root / f"{rel}{ext}").exists():
                    return module_id_for_file(root, root / f"{rel}{ext}", lang)
        return module_id_for_file(root, synth if synth.suffix else synth.with_suffix(".js"), lang)
    except Exception:
        return "/".join(str(p) for p in parts)
