"""Daily challenge helpers."""

from __future__ import annotations

from datetime import date

from .domain import DIFFICULTIES, GameMode
from .engine import GuessGame
from .rng import portable_daily_seed, portable_daily_target


def daily_game(day: date | None = None, difficulty: str = "normal") -> GuessGame:
    """Create the same daily target in Python and browser clients."""
    selected_day = day or date.today()
    try:
        difficulty_config = DIFFICULTIES[difficulty]
    except KeyError as exc:
        raise ValueError(f"unknown difficulty: {difficulty}") from exc
    seed = portable_daily_seed(selected_day, difficulty)
    target = portable_daily_target(
        selected_day,
        difficulty_config.minimum,
        difficulty_config.maximum,
        difficulty,
    )
    return GuessGame(
        difficulty_name=difficulty,
        mode=GameMode.DAILY,
        seed=seed,
        target=target,
    )
