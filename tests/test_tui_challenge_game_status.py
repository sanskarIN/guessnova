from guessnova.domain import GameMode
from guessnova.engine import GuessGame
from guessnova.tui_challenge import game_status


def test_game_status_describes_seeded_classic_without_target() -> None:
    game = GuessGame(
        difficulty_name="hard",
        mode=GameMode.CLASSIC,
        seed=731,
        target=42,
    )

    status = game_status(game, locale="en")

    assert status == "Active: classic · hard · seed 731"
    assert "42" not in status


def test_game_status_describes_existing_daily_by_seed_when_date_is_unknown() -> None:
    game = GuessGame(
        difficulty_name="easy",
        mode=GameMode.DAILY,
        seed=20260819,
        target=42,
    )

    status = game_status(game, locale="en")

    assert status == "Active: daily · easy · seed 20260819"
    assert "42" not in status
