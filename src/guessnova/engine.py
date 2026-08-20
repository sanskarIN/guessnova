"""Core game engines with no terminal/UI dependencies."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field

from .domain import DIFFICULTIES, Difficulty, GameMode, GameSummary, GuessFeedback, GuessOutcome
from .hints import smart_hint
from .rng import RandomSource

Clock = Callable[[], float]
HINT_PENALTY_XP = 10


@dataclass(slots=True)
class GuessGame:
    difficulty_name: str = "normal"
    mode: GameMode = GameMode.CLASSIC
    seed: int | None = None
    target: int | None = None
    clock: Clock = time.monotonic
    _started_at: float = field(init=False)
    _finished_at: float | None = field(default=None, init=False)
    _guesses: list[int] = field(default_factory=list, init=False)
    _finished: bool = field(default=False, init=False)
    _won: bool = field(default=False, init=False)
    _hints_used: int = field(default=0, init=False)
    _hint_penalty: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        try:
            self.mode = GameMode(self.mode)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"unknown game mode: {self.mode}") from exc
        if self.mode == GameMode.REVERSE:
            raise ValueError("reverse mode requires ReverseGuesser")
        if self.difficulty_name not in DIFFICULTIES:
            raise ValueError(f"unknown difficulty: {self.difficulty_name}")
        difficulty = self.difficulty
        if self.target is None:
            self.target = RandomSource(self.seed).randint(difficulty.minimum, difficulty.maximum)
        elif not difficulty.minimum <= self.target <= difficulty.maximum:
            raise ValueError("target is outside the difficulty range")
        self._started_at = self.clock()

    @property
    def difficulty(self) -> Difficulty:
        return DIFFICULTIES[self.difficulty_name]

    @property
    def target_value(self) -> int:
        if self.target is None:
            raise RuntimeError("game target has not been initialized")
        return self.target

    @property
    def attempts_used(self) -> int:
        return len(self._guesses)

    @property
    def attempts_left(self) -> int:
        return max(0, self.difficulty.max_attempts - self.attempts_used)

    def _elapsed_at(self, timestamp: float) -> float:
        return max(0.0, timestamp - self._started_at)

    @property
    def elapsed_seconds(self) -> float:
        endpoint = self._finished_at if self._finished_at is not None else self.clock()
        return self._elapsed_at(endpoint)

    @property
    def is_finished(self) -> bool:
        return self._finished

    @property
    def won(self) -> bool:
        return self._won

    @property
    def hints_used(self) -> int:
        return self._hints_used

    @property
    def hint_penalty(self) -> int:
        return self._hint_penalty

    def _is_timed_out_at(self, timestamp: float) -> bool:
        return (
            self.mode == GameMode.TIMED
            and self._elapsed_at(timestamp) >= self.difficulty.timed_seconds
        )

    def _finish(self, timestamp: float, *, won: bool = False) -> None:
        self._finished = True
        self._won = won
        self._finished_at = timestamp

    def request_hint(self, *, penalize: bool = True) -> str:
        """Return a deterministic narrowed-range clue without consuming an attempt."""
        if self._finished:
            raise RuntimeError("game is already finished")
        now = self.clock()
        if self._is_timed_out_at(now):
            self._finish(now)
            raise RuntimeError("time expired")
        target = self.target_value
        radius = max(2, self.difficulty.span // 10)
        lower = max(self.difficulty.minimum, target - radius)
        upper = min(self.difficulty.maximum, target + radius)
        if lower == upper:
            lower = max(self.difficulty.minimum, lower - 1)
            upper = min(self.difficulty.maximum, upper + 1)
        self._hints_used += 1
        if penalize:
            self._hint_penalty += HINT_PENALTY_XP
        suffix = (
            f" Using it costs {HINT_PENALTY_XP} XP from a winning reward." if penalize else ""
        )
        return f"Range hint: the target is between {lower} and {upper}.{suffix}"

    def guess(self, value: int) -> GuessFeedback:
        if self._finished:
            raise RuntimeError("game is already finished")
        now = self.clock()
        if self._is_timed_out_at(now):
            self._finish(now)
            return GuessFeedback(
                value, GuessOutcome.TIMEOUT, self.attempts_used, self.attempts_left
            )
        if not self.difficulty.minimum <= value <= self.difficulty.maximum:
            return GuessFeedback(
                value, GuessOutcome.OUT_OF_RANGE, self.attempts_used, self.attempts_left
            )

        self._guesses.append(value)
        target = self.target_value
        if value == target:
            self._finish(now, won=True)
            return GuessFeedback(
                value, GuessOutcome.CORRECT, self.attempts_used, self.attempts_left
            )

        if self.attempts_left == 0:
            self._finish(now)
            return GuessFeedback(value, GuessOutcome.EXHAUSTED, self.attempts_used, 0)

        outcome = GuessOutcome.TOO_LOW if value < target else GuessOutcome.TOO_HIGH
        return GuessFeedback(
            value,
            outcome,
            self.attempts_used,
            self.attempts_left,
            smart_hint(target, value, self.difficulty),
        )

    def summary(self) -> GameSummary:
        return GameSummary(
            mode=self.mode,
            difficulty=self.difficulty_name,
            target=self.target_value,
            won=self._won,
            attempts=self.attempts_used,
            elapsed_seconds=self.elapsed_seconds,
            guesses=tuple(self._guesses),
            seed=self.seed,
            hints_used=self._hints_used,
            hint_penalty=self._hint_penalty,
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
