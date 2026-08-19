from argparse import Namespace
from pathlib import Path

from guessnova.cli import _show_onboarding, build_parser, main
from guessnova.settings import Settings
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
                "--locale",
                "en",
                "--reduced-motion",
                "--no-smart-hints",
            ]
        )
        == 0
    )
    profile = Storage().load_profile("Tester")
    assert profile.settings.theme == "mono"
    assert profile.settings.locale == "en"
    assert profile.settings.reduced_motion is True
    assert profile.settings.show_smart_hints is False


def test_empty_history_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))
    assert main(["--compact", "history", "--profile", "Tester"]) == 0


def test_onboarding_is_persisted_once_for_saved_play(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    args = Namespace(locale="en", compact=True, no_save=False)
    _show_onboarding(args, storage, Settings(), profile_name="Tester")
    assert storage.load_profile("Tester").settings.onboarding_complete is True


def test_no_save_onboarding_does_not_write_profile_state(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    args = Namespace(locale="en", compact=True, no_save=True)
    _show_onboarding(args, storage, Settings(), profile_name="Tester")
    assert not storage.path.exists()
