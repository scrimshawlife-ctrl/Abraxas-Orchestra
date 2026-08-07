"""Multi-language source graph helpers for Orchestra analyze (stdlib only).

Python remains full AST (handled in analyze_repo). Other languages use
**structured tokenizers + import-surface parsers** (AST-grade for dependency
edges — not full language compilers). No third-party parsers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator

# Language key → file extensions
LANG_EXTENSIONS: dict[str, frozenset[str]] = {
    "python": frozenset({".py"}),
    "javascript": frozenset({".js", ".jsx", ".mjs", ".cjs"}),
    "typescript": frozenset({".ts", ".tsx", ".mts", ".cts"}),
    "go": frozenset({".go"}),
    "rust": frozenset({".rs"}),
    "ruby": frozenset({".rb"}),
}

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


@dataclass(frozen=True)
class Token:
    kind: str  # IDENT, STRING, KEYWORD, OP, PUNCT, EOF
    value: str
    line: int
    col: int


@dataclass(frozen=True)
class ImportNode:
    """AST-grade import node (dependency surface only)."""

    kind: str  # import | export_from | require | use | mod | go_import | ruby_require
    module: str
    is_relative: bool
    line: int
    raw: str = ""


def normalize_lang(lang: str) -> str:
    key = (lang or "python").strip().lower()
    return LANG_ALIASES.get(key, key)


def extensions_for_lang(lang: str) -> frozenset[str]:
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

    stem = Path(parts[-1]).stem
    if stem in {"index", "mod"} and len(parts) > 1:
        parts = parts[:-1]
        return "/".join(parts) if parts else stem
    return "/".join(parts[:-1] + [stem])


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------


def _line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_nl = text.rfind("\n", 0, index)
    col = index - last_nl
    return line, col


# ---------------------------------------------------------------------------
# JS / TS tokenizer + import parser
# ---------------------------------------------------------------------------

_JS_KEYWORDS = frozenset({
    "import", "export", "from", "require", "as", "type", "default",
    "const", "let", "var", "function", "class", "return", "async", "await",
})


def tokenize_js(text: str) -> list[Token]:
    """Tokenizer for JS/TS dependency surface (handles strings, comments, templates)."""
    tokens: list[Token] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in " \t\r\n":
            i += 1
            continue
        # line comment
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            i += 2
            while i < n and text[i] != "\n":
                i += 1
            continue
        # block comment
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i = min(n, i + 2)
            continue
        line, col = _line_col(text, i)
        # string '
        if ch in "'\"":
            quote = ch
            j = i + 1
            buf: list[str] = []
            while j < n:
                c = text[j]
                if c == "\\":
                    if j + 1 < n:
                        buf.append(text[j + 1])
                        j += 2
                        continue
                if c == quote:
                    j += 1
                    break
                buf.append(c)
                j += 1
            tokens.append(Token("STRING", "".join(buf), line, col))
            i = j
            continue
        # template literal — capture as STRING of first static part only for import()
        if ch == "`":
            j = i + 1
            buf = []
            while j < n:
                c = text[j]
                if c == "\\":
                    j += 2
                    continue
                if c == "`":
                    j += 1
                    break
                if c == "$" and j + 1 < n and text[j + 1] == "{":
                    # skip interpolation
                    depth = 1
                    j += 2
                    while j < n and depth:
                        if text[j] == "{":
                            depth += 1
                        elif text[j] == "}":
                            depth -= 1
                        j += 1
                    buf.append("${…}")
                    continue
                buf.append(c)
                j += 1
            tokens.append(Token("STRING", "".join(buf), line, col))
            i = j
            continue
        # number (skip)
        if ch.isdigit():
            j = i + 1
            while j < n and (text[j].isalnum() or text[j] in "._"):
                j += 1
            tokens.append(Token("NUMBER", text[i:j], line, col))
            i = j
            continue
        # ident / keyword
        if ch.isalpha() or ch in "_$":
            j = i + 1
            while j < n and (text[j].isalnum() or text[j] in "_$"):
                j += 1
            word = text[i:j]
            kind = "KEYWORD" if word in _JS_KEYWORDS else "IDENT"
            tokens.append(Token(kind, word, line, col))
            i = j
            continue
        # multi-char ops
        if text.startswith("=>", i) or text.startswith("...", i):
            tokens.append(Token("OP", text[i : i + (3 if text.startswith("...", i) else 2)], line, col))
            i += 3 if text.startswith("...", i) else 2
            continue
        # single punct
        tokens.append(Token("PUNCT", ch, line, col))
        i += 1
    tokens.append(Token("EOF", "", text.count("\n") + 1, 0))
    return tokens


class _TokStream:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0

    def peek(self) -> Token:
        return self.tokens[self.i]

    def advance(self) -> Token:
        t = self.tokens[self.i]
        if t.kind != "EOF":
            self.i += 1
        return t

    def match(self, kind: str, value: str | None = None) -> Token | None:
        t = self.peek()
        if t.kind == kind and (value is None or t.value == value):
            return self.advance()
        return None

    def match_kw(self, *words: str) -> Token | None:
        t = self.peek()
        if t.kind == "KEYWORD" and t.value in words:
            return self.advance()
        return None


def parse_js_imports(text: str) -> list[ImportNode]:
    """Parse JS/TS import/export/require into ImportNode AST list."""
    ts = _TokStream(tokenize_js(text))
    nodes: list[ImportNode] = []

    def skip_balanced(open_ch: str, close_ch: str) -> None:
        depth = 1
        ts.advance()  # consume open
        while ts.peek().kind != "EOF" and depth:
            t = ts.advance()
            if t.value == open_ch:
                depth += 1
            elif t.value == close_ch:
                depth -= 1

    def skip_until_semi_or_nl() -> None:
        while ts.peek().kind != "EOF":
            t = ts.peek()
            if t.value == ";":
                ts.advance()
                return
            if t.value in "{([":
                pairs = {"{": "}", "[": "]", "(": ")"}
                skip_balanced(t.value, pairs[t.value])
                continue
            ts.advance()

    while ts.peek().kind != "EOF":
        t = ts.peek()
        # import ... from 'mod'  |  import 'mod'
        if t.kind == "KEYWORD" and t.value == "import":
            start = ts.advance()
            # import type ...
            ts.match_kw("type")
            # side-effect import 'x'
            if ts.peek().kind == "STRING":
                s = ts.advance()
                nodes.append(ImportNode(
                    "import", s.value, s.value.startswith("."), s.line, s.value
                ))
                ts.match("PUNCT", ";")
                continue
            # dynamic import( 'x' )
            if ts.peek().value == "(":
                ts.advance()
                if ts.peek().kind == "STRING":
                    s = ts.advance()
                    nodes.append(ImportNode(
                        "import", s.value, s.value.startswith("."), s.line, s.value
                    ))
                # drain )
                while ts.peek().kind != "EOF" and ts.peek().value != ")":
                    ts.advance()
                ts.match("PUNCT", ")")
                ts.match("PUNCT", ";")
                continue
            # skip binding until from or ;
            while ts.peek().kind != "EOF":
                if ts.match_kw("from"):
                    if ts.peek().kind == "STRING":
                        s = ts.advance()
                        nodes.append(ImportNode(
                            "import", s.value, s.value.startswith("."), s.line, s.value
                        ))
                    ts.match("PUNCT", ";")
                    break
                if ts.peek().value == "{":
                    skip_balanced("{", "}")
                    continue
                if ts.peek().value == ";":
                    ts.advance()
                    break
                ts.advance()
            continue

        # export ... from 'mod'
        if t.kind == "KEYWORD" and t.value == "export":
            ts.advance()
            ts.match_kw("type")
            # export { } from 'x' | export * from 'x'
            saw_from = False
            while ts.peek().kind != "EOF":
                if ts.match_kw("from"):
                    saw_from = True
                    if ts.peek().kind == "STRING":
                        s = ts.advance()
                        nodes.append(ImportNode(
                            "export_from", s.value, s.value.startswith("."), s.line, s.value
                        ))
                    ts.match("PUNCT", ";")
                    break
                if ts.peek().value == "{":
                    skip_balanced("{", "}")
                    continue
                if ts.peek().value == "*":
                    ts.advance()
                    continue
                if ts.peek().value == ";":
                    ts.advance()
                    break
                # export default / export function — not a re-export
                if ts.peek().kind in {"KEYWORD", "IDENT"} and not saw_from:
                    # might still be export default function — stop if no from soon
                    if ts.peek().value in {"default", "async", "function", "class", "const", "let", "var"}:
                        skip_until_semi_or_nl()
                        break
                ts.advance()
            continue

        # require('x')
        if t.kind == "KEYWORD" and t.value == "require":
            ts.advance()
            if ts.match("PUNCT", "(") and ts.peek().kind == "STRING":
                s = ts.advance()
                nodes.append(ImportNode(
                    "require", s.value, s.value.startswith("."), s.line, s.value
                ))
                ts.match("PUNCT", ")")
            continue

        # bare IDENT require when keyword map missed (minifiers)
        if t.kind == "IDENT" and t.value == "require":
            ts.advance()
            if ts.match("PUNCT", "(") and ts.peek().kind == "STRING":
                s = ts.advance()
                nodes.append(ImportNode(
                    "require", s.value, s.value.startswith("."), s.line, s.value
                ))
                ts.match("PUNCT", ")")
            continue

        ts.advance()

    return nodes


def extract_js_ts_imports(text: str) -> list[str]:
    """Public API: module specifiers from JS/TS (AST-grade parser)."""
    return _unique([n.module for n in parse_js_imports(text)])


# ---------------------------------------------------------------------------
# Go tokenizer + import parser
# ---------------------------------------------------------------------------


def tokenize_go(text: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in " \t\r\n":
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            i += 2
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i = min(n, i + 2)
            continue
        line, col = _line_col(text, i)
        if ch == '"':
            j = i + 1
            buf: list[str] = []
            while j < n:
                c = text[j]
                if c == "\\":
                    if j + 1 < n:
                        buf.append(text[j + 1])
                        j += 2
                        continue
                if c == '"':
                    j += 1
                    break
                buf.append(c)
                j += 1
            tokens.append(Token("STRING", "".join(buf), line, col))
            i = j
            continue
        if ch == "`":  # raw string
            j = i + 1
            while j < n and text[j] != "`":
                j += 1
            tokens.append(Token("STRING", text[i + 1 : j], line, col))
            i = min(n, j + 1)
            continue
        if ch.isalpha() or ch == "_":
            j = i + 1
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            word = text[i:j]
            kind = "KEYWORD" if word in {"import", "package", "type", "func", "var", "const"} else "IDENT"
            tokens.append(Token(kind, word, line, col))
            i = j
            continue
        tokens.append(Token("PUNCT", ch, line, col))
        i += 1
    tokens.append(Token("EOF", "", text.count("\n") + 1, 0))
    return tokens


def parse_go_imports(text: str) -> list[ImportNode]:
    ts = _TokStream(tokenize_go(text))
    nodes: list[ImportNode] = []
    while ts.peek().kind != "EOF":
        if ts.match_kw("import"):
            # import "x"
            if ts.peek().kind == "STRING":
                s = ts.advance()
                nodes.append(ImportNode("go_import", s.value, False, s.line, s.value))
                continue
            # import alias "x"
            if ts.peek().kind == "IDENT":
                ts.advance()
                if ts.peek().kind == "STRING":
                    s = ts.advance()
                    nodes.append(ImportNode("go_import", s.value, False, s.line, s.value))
                continue
            # import ( ... )
            if ts.match("PUNCT", "("):
                while ts.peek().kind != "EOF" and ts.peek().value != ")":
                    if ts.peek().kind == "IDENT":
                        ts.advance()  # alias optional
                    if ts.peek().kind == "STRING":
                        s = ts.advance()
                        nodes.append(ImportNode("go_import", s.value, False, s.line, s.value))
                    else:
                        ts.advance()
                ts.match("PUNCT", ")")
                continue
        ts.advance()
    return nodes


def extract_go_imports(text: str) -> list[str]:
    return _unique([n.module for n in parse_go_imports(text)])


# ---------------------------------------------------------------------------
# Rust tokenizer + use/mod parser
# ---------------------------------------------------------------------------


def tokenize_rust(text: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in " \t\r\n":
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            i += 2
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i = min(n, i + 2)
            continue
        line, col = _line_col(text, i)
        if ch == '"':
            j = i + 1
            buf: list[str] = []
            while j < n:
                c = text[j]
                if c == "\\":
                    j += 2
                    continue
                if c == '"':
                    j += 1
                    break
                buf.append(c)
                j += 1
            tokens.append(Token("STRING", "".join(buf), line, col))
            i = j
            continue
        if text.startswith("::", i):
            tokens.append(Token("OP", "::", line, col))
            i += 2
            continue
        if ch.isalpha() or ch == "_":
            j = i + 1
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            word = text[i:j]
            kind = "KEYWORD" if word in {
                "use", "mod", "crate", "super", "self", "as", "pub", "extern",
            } else "IDENT"
            tokens.append(Token(kind, word, line, col))
            i = j
            continue
        tokens.append(Token("PUNCT", ch, line, col))
        i += 1
    tokens.append(Token("EOF", "", text.count("\n") + 1, 0))
    return tokens


def parse_rust_imports(text: str) -> list[ImportNode]:
    ts = _TokStream(tokenize_rust(text))
    nodes: list[ImportNode] = []

    def parse_path() -> tuple[str, int]:
        parts: list[str] = []
        line = ts.peek().line
        while True:
            t = ts.peek()
            if t.kind in {"IDENT", "KEYWORD"} and t.value not in {"as", "pub"}:
                parts.append(ts.advance().value)
                if ts.match("OP", "::"):
                    continue
                break
            if t.kind == "OP" and t.value == "::":
                ts.advance()
                continue
            break
        return "::".join(parts), line

    while ts.peek().kind != "EOF":
        if ts.match_kw("use"):
            # use path::{...}; or use path;
            path, line = parse_path()
            if ts.peek().value == "{":
                # braced — keep root path as module unit
                depth = 0
                while ts.peek().kind != "EOF":
                    t = ts.advance()
                    if t.value == "{":
                        depth += 1
                    elif t.value == "}":
                        depth -= 1
                        if depth == 0:
                            break
            ts.match_kw("as")
            if ts.peek().kind == "IDENT":
                ts.advance()
            ts.match("PUNCT", ";")
            if path:
                nodes.append(ImportNode("use", path, path.startswith(("crate", "super", "self")), line, path))
            continue
        if ts.match_kw("mod"):
            if ts.peek().kind == "IDENT":
                name = ts.advance()
                # mod foo;  (not inline mod foo { })
                if ts.peek().value == ";":
                    ts.advance()
                    nodes.append(ImportNode("mod", name.value, True, name.line, name.value))
                else:
                    # skip inline module body
                    if ts.peek().value == "{":
                        depth = 0
                        while ts.peek().kind != "EOF":
                            t = ts.advance()
                            if t.value == "{":
                                depth += 1
                            elif t.value == "}":
                                depth -= 1
                                if depth == 0:
                                    break
            continue
        ts.advance()
    return nodes


def extract_rust_imports(text: str) -> list[str]:
    return _unique([n.module for n in parse_rust_imports(text)])


# ---------------------------------------------------------------------------
# Ruby tokenizer + require parser
# ---------------------------------------------------------------------------


def tokenize_ruby(text: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in " \t\r\n":
            i += 1
            continue
        if ch == "#":
            while i < n and text[i] != "\n":
                i += 1
            continue
        line, col = _line_col(text, i)
        if ch in "'\"":
            quote = ch
            j = i + 1
            buf: list[str] = []
            while j < n:
                c = text[j]
                if c == "\\" and j + 1 < n:
                    buf.append(text[j + 1])
                    j += 2
                    continue
                if c == quote:
                    j += 1
                    break
                buf.append(c)
                j += 1
            tokens.append(Token("STRING", "".join(buf), line, col))
            i = j
            continue
        if ch.isalpha() or ch == "_":
            j = i + 1
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            word = text[i:j]
            kind = "KEYWORD" if word in {
                "require", "require_relative", "load", "autoload",
            } else "IDENT"
            tokens.append(Token(kind, word, line, col))
            i = j
            continue
        tokens.append(Token("PUNCT", ch, line, col))
        i += 1
    tokens.append(Token("EOF", "", text.count("\n") + 1, 0))
    return tokens


def parse_ruby_imports(text: str) -> list[ImportNode]:
    ts = _TokStream(tokenize_ruby(text))
    nodes: list[ImportNode] = []
    while ts.peek().kind != "EOF":
        if ts.match_kw("require", "require_relative", "load"):
            # optional (
            ts.match("PUNCT", "(")
            if ts.peek().kind == "STRING":
                s = ts.advance()
                rel = s.value.startswith(".") or s.value.startswith("/")
                nodes.append(ImportNode("ruby_require", s.value, rel, s.line, s.value))
            ts.match("PUNCT", ")")
            continue
        ts.advance()
    return nodes


def extract_ruby_imports(text: str) -> list[str]:
    return _unique([n.module for n in parse_ruby_imports(text)])


# ---------------------------------------------------------------------------
# Public extractors map + edge resolution
# ---------------------------------------------------------------------------


def _unique(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for x in items:
        if x and x not in seen:
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

PARSERS: dict[str, Callable[[str], list[ImportNode]]] = {
    "javascript": parse_js_imports,
    "typescript": parse_js_imports,
    "go": parse_go_imports,
    "rust": parse_rust_imports,
    "ruby": parse_ruby_imports,
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
    """Return list of (target_id, external) using AST-grade import nodes."""
    if lang == "python":
        return []
    parser = PARSERS.get(lang)
    if not parser:
        return []
    nodes = parser(text)
    out: list[tuple[str, bool]] = []
    seen: set[str] = set()
    for node in nodes:
        spec = node.module
        if lang in {"javascript", "typescript"}:
            target = (
                _resolve_rel_path_id(root, current, spec, known, lang)
                if node.is_relative or spec.startswith(".")
                else spec
            )
        elif lang == "ruby" and node.is_relative:
            target = _resolve_rel_path_id(root, current, spec, known, lang)
        elif lang == "go":
            target = spec
            for kid in known:
                if kid.endswith(spec.split("/")[-1]) or kid == spec:
                    target = kid
                    break
        elif lang == "rust":
            target = spec
            if spec in known:
                target = spec
            else:
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
    try:
        resolved = (base / spec).resolve()
        rel = resolved.relative_to(root.resolve())
    except Exception:
        return spec
    candidates: list[str] = []
    parts = list(rel.parts)
    joined = "/".join(parts)
    candidates.append(joined)
    if parts:
        candidates.append(
            "/".join(
                p if i < len(parts) - 1 else Path(p).stem
                for i, p in enumerate(parts)
            )
        )
    for c in candidates:
        if c in known:
            return c
        c2 = re.sub(r"\.(js|ts|tsx|jsx|mjs|cjs)$", "", c)
        if c2 in known:
            return c2
    try:
        synth = root / rel
        if not synth.suffix:
            for ext in LANG_EXTENSIONS.get(lang, ()):
                candidate = root / f"{rel}{ext}"
                if candidate.exists():
                    return module_id_for_file(root, candidate, lang)
        return module_id_for_file(
            root,
            synth if synth.suffix else synth.with_suffix(".js"),
            lang,
        )
    except Exception:
        return "/".join(str(p) for p in parts)
