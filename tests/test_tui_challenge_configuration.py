from datetime import date

import pytest

from guessnova.domain import GameMode
from guessnova.tui_workspace import ChallengeConfiguration, parse_workspace_challenge


def test_parse_workspace_challenge_resolves_seeded_numeric_mode() -> None:
    configuration = parse_workspace_challenge(
        mode="timed",
        difficulty="hard",
        seed_text=" 20260819 ",
        day_text="ignored-for-non-daily",
    )

    assert configuration == ChallengeConfiguration(
        mode=GameMode.TIMED,
        difficulty="hard",
        seed=20260819,
    )
    assert configuration.mode_value == "timed"
    assert configuration.seed_text == "20260819"
    assert configuration.day_text == ""


def test_parse_workspace_challenge_resolves_blank_daily_date_from_injected_today() -> None:
    configuration = parse_workspace_challenge(
        mode="daily",
        difficulty="expert",
        seed_text="ignored-for-daily",
        today=date(2026, 8, 19),
    )

    assert configuration.mode == GameMode.DAILY
    assert configuration.difficulty == "expert"
    assert configuration.seed is None
    assert configuration.seed_text == ""
    assert configuration.day == date(2026, 8, 19)
    assert configuration.day_text == "2026-08-19"


def test_challenge_configuration_builds_reproducible_seeded_game() -> None:
    configuration = ChallengeConfiguration(
        mode=GameMode.STREAK,
        difficulty="normal",
        seed=431,
    )

    first = configuration.build_game()
    second = configuration.build_game()

    assert first.mode == GameMode.STREAK
    assert first.difficulty_name == "normal"
    assert first.seed == 431
    assert first.target_value == second.target_value


def test_challenge_configuration_builds_reproducible_daily_game() -> None:
    configuration = ChallengeConfiguration(
        mode=GameMode.DAILY,
        difficulty="easy",
        day=date(2026, 8, 19),
    )

    first = configuration.build_game()
    second = configuration.build_game()

    assert first.mode == GameMode.DAILY
    assert first.difficulty_name == "easy"
    assert first.seed is not None
    assert first.seed == second.seed
    assert first.target_value == second.target_value


def test_parse_workspace_challenge_rejects_reverse_unknown_and_malformed_fields() -> None:
    with pytest.raises(ValueError, match="dedicated reverse"):
        parse_workspace_challenge(mode="reverse", difficulty="normal")
    with pytest.raises(ValueError, match="unknown game mode"):
        parse_workspace_challenge(mode="future", difficulty="normal")
    with pytest.raises(ValueError, match="unknown difficulty"):
        parse_workspace_challenge(mode="classic", difficulty="future")
    with pytest.raises(ValueError, match="whole number"):
        parse_workspace_challenge(mode="classic", difficulty="normal", seed_text="nova")
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        parse_workspace_challenge(mode="daily", difficulty="normal", day_text="19-08-2026")


def test_challenge_configuration_rejects_inconsistent_manual_construction() -> None:
    with pytest.raises(ValueError, match="resolved date"):
        ChallengeConfiguration(mode=GameMode.DAILY, difficulty="normal")
    with pytest.raises(ValueError, match="derive their seed"):
        ChallengeConfiguration(
            mode=GameMode.DAILY,
            difficulty="normal",
            seed=1,
            day=date(2026, 8, 19),
        )
    with pytest.raises(ValueError, match="only daily"):
        ChallengeConfiguration(
            mode=GameMode.CLASSIC,
            difficulty="normal",
            day=date(2026, 8, 19),
        )
