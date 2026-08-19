"""Domain models shared by the game, persistence, and interfaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final


class GameMode(StrEnum):
    CLASSIC = "classic"
    TIMED = "timed"
    STREAK = "streak"
    REVERSE = "reverse"
    DAILY = "daily"


class GuessOutcome(StrEnum):
    TOO_LOW = "too_low"
    TOO_HIGH = "too_high"
    CORRECT = "correct"
    OUT_OF_RANGE = "out_of_range"
    EXHAUSTED = "exhausted"
    TIMEOUT = "timeout"


@dataclass(frozen=True, slots=True)
class Difficulty:
    name: str
    minimum: int
    maximum: int
    max_attempts: int
    timed_seconds: int

    @property
    def span(self) -> int:
        return self.maximum - self.minimum + 1


DIFFICULTIES: Final[dict[str, Difficulty]] = {
    "easy": Difficulty("easy", 1, 50, 10, 60),
    "normal": Difficulty("normal", 1, 100, 9, 45),
    "hard": Difficulty("hard", 1, 500, 10, 40),
    "expert": Difficulty("expert", 1, 1000, 10, 35),
}


@dataclass(frozen=True, slots=True)
class GuessFeedback:
    guess: int
    outcome: GuessOutcome
    attempts_used: int
    attempts_left: int
    hint: str | None = None


@dataclass(frozen=True, slots=True)
class GameSummary:
    mode: GameMode
    difficulty: str
    target: int
    won: bool
    attempts: int
    elapsed_seconds: float
    guesses: tuple[int, ...] = ()
    seed: int | None = None


@dataclass(slots=True)
class PlayerStats:
    games_played: int = 0
    games_won: int = 0
    current_streak: int = 0
    best_streak: int = 0
    total_guesses: int = 0
    xp: int = 0
    achievements: set[str] = field(default_factory=set)

    @property
    def win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.games_won / self.games_played

    @property
    def average_guesses(self) -> float:
        if self.games_won == 0:
            return 0.0
        return self.total_guesses / self.games_won
