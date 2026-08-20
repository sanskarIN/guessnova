from datetime import date

from guessnova.daily import daily_game
from guessnova.rng import daily_seed, fnv1a32, portable_daily_seed, portable_daily_target


def test_daily_seed_is_stable() -> None:
    day = date(2026, 8, 19)
    assert daily_seed(day) == daily_seed(day)
    assert daily_seed(day) != daily_seed(date(2026, 8, 20))


def test_portable_hash_matches_browser_vector() -> None:
    text = "guessnova-daily-v2:2026-08-19:normal"
    assert fnv1a32(text) == 230_553_734
    assert portable_daily_seed(date(2026, 8, 19), "normal") == 230_553_734
    assert portable_daily_target(date(2026, 8, 19), 1, 100, "normal") == 35


def test_daily_game_same_day_same_target() -> None:
    day = date(2026, 8, 19)
    first = daily_game(day)
    second = daily_game(day)
    assert first.target == second.target == 35
    assert first.seed == second.seed == 230_553_734


def test_daily_game_difficulty_uses_its_own_portable_range() -> None:
    day = date(2026, 8, 20)
    game = daily_game(day, "expert")
    assert 1 <= game.target_value <= 1000
    assert game.seed == portable_daily_seed(day, "expert")
