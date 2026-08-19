"""Core game engines with no terminal/UI dependencies."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field

from .domain import DIFFICULTIES, GameMode, GameSummary, GuessFeedback, GuessOutcome
from .hints import smart_hint
from .rng import RandomSource

Clock = Callable[[], float]


@dataclass(slots=True)
class GuessGame:
    difficulty_name: str = "normal"
    mode: GameMode = GameMode.CLASSIC
    seed: int | None = None
    target: int | None = None
    clock: Clock = time.monotonic
    _started_at: float = field(init=False)
    _guesses: list[int] = field(default_factory=list, init=False)
    _finished: bool = field(default=False, init=False)
    _won: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if self.difficulty_name not in DIFFICULTIES:
            raise ValueError(f"unknown difficulty: {self.difficulty_name}")
        difficulty = self.difficulty
        if self.target is None:
            self.target = RandomSource(self.seed).randint(difficulty.minimum, difficulty.maximum)
        elif not difficulty.minimum <= self.target <= difficulty.maximum:
            raise ValueError("target is outside the difficulty range")
        self._started_at = self.clock()

    @property
    def difficulty(self):  # type: ignore[no-untyped-def]
        return DIFFICULTIES[self.difficulty_name]

    @property
    def attempts_used(self) -> int:
        return len(self._guesses)

    @property
    def attempts_left(self) -> int:
        return max(0, self.difficulty.max_attempts - self.attempts_used)

    @property
    def elapsed_seconds(self) -> float:
        return max(0.0, self.clock() - self._started_at)

    @property
    def is_finished(self) -> bool:
        return self._finished

    @property
    def won(self) -> bool:
        return self._won

    def _is_timed_out(self) -> bool:
        return self.mode == GameMode.TIMED and self.elapsed_seconds >= self.difficulty.timed_seconds

    def guess(self, value: int) -> GuessFeedback:
        if self._finished:
            raise RuntimeError("game is already finished")
        if self._is_timed_out():
            self._finished = True
            return GuessFeedback(value, GuessOutcome.TIMEOUT, self.attempts_used, self.attempts_left)
        if not self.difficulty.minimum <= value <= self.difficulty.maximum:
            return GuessFeedback(value, GuessOutcome.OUT_OF_RANGE, self.attempts_used, self.attempts_left)

        self._guesses.append(value)
        if value == self.target:
            self._finished = True
            self._won = True
            return GuessFeedback(value, GuessOutcome.CORRECT, self.attempts_used, self.attempts_left)

        if self.attempts_left == 0:
            self._finished = True
            return GuessFeedback(value, GuessOutcome.EXHAUSTED, self.attempts_used, 0)

        outcome = GuessOutcome.TOO_LOW if value < self.target else GuessOutcome.TOO_HIGH
        return GuessFeedback(
            value,
            outcome,
            self.attempts_used,
            self.attempts_left,
            smart_hint(self.target, value, self.difficulty),
        )

    def summary(self) -> GameSummary:
        return GameSummary(
            mode=self.mode,
            difficulty=self.difficulty_name,
            target=int(self.target),
            won=self._won,
            attempts=self.attempts_used,
            elapsed_seconds=self.elapsed_seconds,
            guesses=tuple(self._guesses),
            seed=self.seed,
        )


@dataclass(slots=True)
class ReverseGuesser:
    minimum: int = 1
    maximum: int = 100
    low: int = field(init=False)
    high: int = field(init=False)
    current: int | None = field(default=None, init=False)
    attempts: int = field(default=0, init=False)
    finished: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if self.minimum >= self.maximum:
            raise ValueError("minimum must be less than maximum")
        self.low = self.minimum
        self.high = self.maximum

    def next_guess(self) -> int:
        if self.finished:
            raise RuntimeError("reverse game is already finished")
        if self.low > self.high:
            raise ValueError("responses are inconsistent")
        self.current = (self.low + self.high) // 2
        self.attempts += 1
        return self.current

    def respond(self, response: str) -> None:
        if self.current is None:
            raise RuntimeError("call next_guess before respond")
        response = response.strip().lower()
        if response == "correct":
            self.finished = True
            return
        if response == "higher":
            self.low = self.current + 1
        elif response == "lower":
            self.high = self.current - 1
        else:
            raise ValueError("response must be higher, lower, or correct")
        if self.low > self.high:
            raise ValueError("responses are inconsistent")
