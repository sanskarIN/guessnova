from datetime import date

from guessnova.domain import GameMode
from guessnova.tui_challenge import challenge_detail, challenge_status
from guessnova.tui_workspace import ChallengeConfiguration


def test_seeded_challenge_status_identifies_mode_difficulty_and_seed() -> None:
    configuration = ChallengeConfiguration(
        mode=GameMode.TIMED,
        difficulty="hard",
        seed=20260819,
    )

    status = challenge_status(configuration, locale="en")

    assert status == "Active: timed · hard · seed 20260819"


def test_daily_challenge_status_identifies_date_in_hindi() -> None:
    configuration = ChallengeConfiguration(
        mode=GameMode.DAILY,
        difficulty="normal",
        day=date(2026, 8, 19),
    )

    detail = challenge_detail(configuration, locale="hi")
    status = challenge_status(configuration, locale="hi")

    assert detail == "तारीख 2026-08-19"
    assert "daily" in status
    assert "normal" in status
    assert "2026-08-19" in status


def test_unseeded_challenge_status_never_contains_hidden_target() -> None:
    configuration = ChallengeConfiguration(
        mode=GameMode.CLASSIC,
        difficulty="easy",
    )

    status = challenge_status(configuration, locale="en")

    assert status == "Active: classic · easy · random seed"
    assert "target" not in status.casefold()
