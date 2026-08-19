from pathlib import Path

from guessnova.cli import build_parser, main
from guessnova.domain import GameMode, GameSummary
from guessnova.service import GameService
from guessnova.storage import Storage


def test_history_parser_accepts_advanced_filters() -> None:
    args = build_parser().parse_args(
        [
            "history",
            "--result",
            "win",
            "--search",
            "daily",
            "--since",
            "2026-08-01",
            "--until",
            "2026-08-31",
            "--group-by",
            "mode",
            "--limit",
            "50",
        ]
    )
    assert args.result == "win"
    assert args.search == "daily"
    assert args.since.isoformat() == "2026-08-01"
    assert args.until.isoformat() == "2026-08-31"
    assert args.group_by == "mode"
    assert args.limit == 50


def test_profile_commands_create_rename_delete_and_restore(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))
    assert main(["--compact", "profiles", "create", "Alpha"]) == 0
    assert main(["--compact", "profiles", "rename", "Alpha", "Nova"]) == 0
    assert Storage().active_profile_name() == "Nova"
    assert main(["--compact", "profiles", "delete", "Nova", "--yes"]) == 0
    assert Storage().list_deleted_profile_names() == ["Nova"]
    assert main(["--compact", "profiles", "restore", "Nova"]) == 0
    assert Storage().list_profile_names() == ["Nova"]


def test_history_command_filters_saved_sessions(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))
    storage = Storage()
    service = GameService(storage)
    service.record(
        GameSummary(GameMode.CLASSIC, "normal", 42, True, 2, 1.0, (20, 42), 1),
        "Tester",
    )
    service.record(
        GameSummary(GameMode.DAILY, "hard", 80, False, 10, 3.0, tuple(range(10)), 2),
        "Tester",
    )
    assert (
        main(
            [
                "--compact",
                "history",
                "--profile",
                "Tester",
                "--result",
                "win",
                "--group-by",
                "result",
            ]
        )
        == 0
    )


def test_non_positive_history_limit_is_rejected_by_parser() -> None:
    parser = build_parser()
    try:
        parser.parse_args(["history", "--limit", "0"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("expected argparse to reject a zero limit")
