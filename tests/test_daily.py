from datetime import date

from guessnova.daily import daily_game
from guessnova.rng import daily_seed


def test_daily_seed_is_stable() -> None:
    day = date(2026, 8, 19)
    assert daily_seed(day) == daily_seed(day)
    assert daily_seed(day) != daily_seed(date(2026, 8, 20))


def test_daily_game_same_day_same_target() -> None:
    day = date(2026, 8, 19)
    assert daily_game(day).target == daily_game(day).target
