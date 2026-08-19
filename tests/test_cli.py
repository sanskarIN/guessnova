from pathlib import Path

from guessnova.cli import build_parser, main
from guessnova.storage import Storage


def test_parser_defaults() -> None:
    args = build_parser().parse_args(["play", "--no-save"])
    assert args.difficulty == "normal"
    assert args.mode == "classic"
    assert args.hints is None


def test_parser_supports_plain_and_compact_modes() -> None:
    args = build_parser().parse_args(["--plain", "--compact", "about"])
    assert args.plain is True
    assert args.compact is True
    assert args.command == "about"


def test_help_without_subcommand() -> None:
    assert main([]) == 0


def test_about_command() -> None:
    assert main(["--compact", "about"]) == 0


def test_settings_command_persists_profile_preferences(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))
    assert (
        main(
            [
                "--compact",
                "settings",
                "--profile",
                "Tester",
                "--theme",
                "mono",
                "--reduced-motion",
                "--no-smart-hints",
            ]
        )
        == 0
    )
    profile = Storage().load_profile("Tester")
    assert profile.settings.theme == "mono"
    assert profile.settings.reduced_motion is True
    assert profile.settings.show_smart_hints is False


def test_empty_history_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))
    assert main(["--compact", "history", "--profile", "Tester"]) == 0
