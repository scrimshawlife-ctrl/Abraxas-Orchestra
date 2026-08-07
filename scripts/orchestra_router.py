"""CLI command router for Abraxas Orchestra.

Central registry maps command names/aliases → handlers and argparse config.
Keeps the public CLI surface stable while simplifying registration and dispatch.
Stdlib only.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Callable, Sequence

Handler = Callable[[argparse.Namespace], int]
ArgBuilder = Callable[[argparse.ArgumentParser], None]


@dataclass(frozen=True)
class CommandSpec:
    """One routable CLI command."""

    name: str
    handler: Handler
    help: str
    aliases: tuple[str, ...] = ()
    group: str = "general"
    configure: ArgBuilder | None = None


# Display order for groups in --help epilog
GROUP_ORDER: tuple[str, ...] = ("meta", "emit", "repo", "general")
GROUP_LABELS: dict[str, str] = {
    "meta": "Meta",
    "emit": "Emit (structure / diagrams)",
    "repo": "Repo (analyze / optimize)",
    "general": "Other",
}


class CommandRouter:
    """Register commands once; build argparse and dispatch argv."""

    def __init__(
        self,
        *,
        prog: str = "orchestra",
        description: str = "Abraxas Orchestra — symbolic code architecture CLI",
        version: str = "0.0.0",
    ) -> None:
        self.prog = prog
        self.description = description
        self.version = version
        self._specs: dict[str, CommandSpec] = {}
        self._order: list[str] = []

    def add(self, spec: CommandSpec) -> None:
        if spec.name in self._specs:
            raise ValueError(f"duplicate command: {spec.name}")
        self._specs[spec.name] = spec
        self._order.append(spec.name)
        for alias in spec.aliases:
            if alias in self._specs or alias in self._order:
                # aliases live only in argparse; still guard primary names
                if alias in self._specs:
                    raise ValueError(f"alias collides with command: {alias}")

    def get(self, name: str) -> CommandSpec | None:
        if name in self._specs:
            return self._specs[name]
        for spec in self._specs.values():
            if name in spec.aliases:
                return spec
        return None

    def names(self) -> list[str]:
        return list(self._order)

    def _epilog(self) -> str:
        by_group: dict[str, list[str]] = {}
        for name in self._order:
            spec = self._specs[name]
            by_group.setdefault(spec.group, []).append(name)
        lines = ["Command groups:"]
        for g in GROUP_ORDER:
            names = by_group.get(g) or []
            if not names:
                continue
            label = GROUP_LABELS.get(g, g)
            lines.append(f"  {label}: {', '.join(names)}")
        lines.append("")
        lines.append("Legacy: `do <command>` is still accepted.")
        return "\n".join(lines)

    def build_parser(self) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(
            prog=self.prog,
            description=self.description,
            epilog=self._epilog(),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        p.add_argument(
            "--version",
            action="version",
            version=f"Orchestra {self.version}",
        )
        sub = p.add_subparsers(dest="command", required=True, metavar="COMMAND")

        for name in self._order:
            spec = self._specs[name]
            sp = sub.add_parser(
                spec.name,
                help=spec.help,
                aliases=list(spec.aliases),
            )
            if spec.configure is not None:
                spec.configure(sp)
            sp.set_defaults(func=spec.handler, _router_command=spec.name)

        return p

    def normalize_argv(self, argv: Sequence[str] | None) -> list[str]:
        """Strip legacy `do` prefix; return a mutable argv list."""
        if argv is None:
            raw = sys.argv[1:]
        else:
            raw = list(argv)
        if len(raw) >= 1 and raw[0] == "do":
            if len(raw) >= 2:
                print(
                    "note: `do` is optional — use `orchestra <command>` directly",
                    file=sys.stderr,
                )
                return raw[1:]
            return raw
        return raw

    def dispatch(self, argv: Sequence[str] | None = None) -> int:
        """Parse argv and run the matched command handler."""
        args_list = self.normalize_argv(argv)
        parser = self.build_parser()
        ns = parser.parse_args(args_list)
        func = getattr(ns, "func", None)
        if func is None:
            parser.print_help()
            return 2
        return int(func(ns))
