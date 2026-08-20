"""Top-level GuessNova command dispatcher with compatibility-preserving routes."""

from __future__ import annotations

import sys

from .cli import main as game_main
from .doctor_cli import main as doctor_main
from .web_server import main as web_main

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


def _web_args(argv: list[str]) -> list[str] | None:
    """Return web-server arguments when argv addresses the web command."""
    if not argv or argv[0] != "web":
        return None
    return argv[1:]


def _print_command_hints() -> None:
    print("\nRecovery and backup diagnostics: guessnova doctor --help")
    print("Cross-platform browser/PWA interface: guessnova web --help")


def main(argv: list[str] | None = None) -> int:
    """Dispatch gameplay, diagnostics, or the bundled cross-platform web interface."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    routed_doctor = _doctor_args(arguments)
    if routed_doctor is not None:
        return doctor_main(routed_doctor)

    routed_web = _web_args(arguments)
    if routed_web is not None:
        return web_main(routed_web)

    if arguments in (["--help"], ["-h"]):
        try:
            return game_main(arguments)
        finally:
            _print_command_hints()

    result = game_main(arguments)
    if not arguments:
        _print_command_hints()
    return result
