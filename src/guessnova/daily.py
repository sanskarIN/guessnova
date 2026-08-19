"""Daily challenge helpers."""

from __future__ import annotations

from datetime import date

from .domain import GameMode
from .engine import GuessGame
from .rng import daily_seed


def daily_game(day: date | None = None, difficulty: str = "normal") -> GuessGame:
    selected_day = day or date.today()
    return GuessGame(difficulty_name=difficulty, mode=GameMode.DAILY, seed=daily_seed(selected_day))
