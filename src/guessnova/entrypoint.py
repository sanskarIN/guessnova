"""Top-level GuessNova command dispatcher with compatibility-preserving doctor routing."""

from __future__ import annotations

import sys

from .cli import main as game_main
from .doctor_cli import main as doctor_main

_GLOBAL_PRESENTATION_FLAGS = {"--plain", "--compact"}


def _doctor_args(argv: list[str]) -> list[str] | None:
    """Return standalone-doctor arguments when argv addresses the doctor command."""
    prefix: list[str] = []
    index = 0
    while index < len(argv) and argv[index] in _GLOBAL_PRESENTATION_FLAGS:
        prefix.append(argv[index])
        index += 1
    if index >= len(argv) or argv[index] != "doctor":
        return None
    return [*prefix, *argv[index + 1 :]]


def _print_doctor_hint() -> None:
    print("\nRecovery and backup diagnostics: guessnova doctor --help")


def main(argv: list[str] | None = None) -> int:
    """Dispatch normal gameplay commands or the compatibility-safe doctor subcommand."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    routed = _doctor_args(arguments)
    if routed is not None:
        return doctor_main(routed)

    result = game_main(arguments)
    if not arguments or arguments in (["--help"], ["-h"]):
        _print_doctor_hint()
    return result
