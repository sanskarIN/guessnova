"""Validation for completed GuessGame summaries crossing persistence/replay boundaries."""

from __future__ import annotations

import math

from .domain import DIFFICULTIES, GameMode, GameSummary


def _integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_game_summary(summary: GameSummary) -> None:
    """Reject summaries that cannot be produced by the supported GuessGame engine."""
    if not isinstance(summary.mode, GameMode) or summary.mode == GameMode.REVERSE:
        raise ValueError("summary mode is invalid")
    if summary.difficulty not in DIFFICULTIES:
        raise ValueError("summary difficulty is invalid")

    rules = DIFFICULTIES[summary.difficulty]
    if not _integer(summary.target) or not rules.minimum <= summary.target <= rules.maximum:
        raise ValueError("summary target is invalid")
    if not isinstance(summary.won, bool):
        raise ValueError("summary result is invalid")
    if not _integer(summary.attempts) or not 0 <= summary.attempts <= rules.max_attempts:
        raise ValueError("summary attempts are invalid")
    if summary.won and summary.attempts < 1:
        raise ValueError("winning summary must use at least one attempt")
    if not summary.won and summary.mode != GameMode.TIMED and summary.attempts != rules.max_attempts:
        raise ValueError("non-timed losing summary must exhaust its attempts")

    if isinstance(summary.elapsed_seconds, bool) or not isinstance(
        summary.elapsed_seconds, (int, float)
    ):
        raise ValueError("summary elapsed time is invalid")
    if summary.elapsed_seconds < 0 or not math.isfinite(float(summary.elapsed_seconds)):
        raise ValueError("summary elapsed time is invalid")

    if not isinstance(summary.guesses, tuple) or len(summary.guesses) != summary.attempts:
        raise ValueError("summary guesses do not match attempts")
    for guess in summary.guesses:
        if not _integer(guess) or not rules.minimum <= guess <= rules.maximum:
            raise ValueError("summary guess is invalid")

    if summary.won and summary.guesses[-1] != summary.target:
        raise ValueError("winning summary must end at the target")
    if not summary.won and summary.target in summary.guesses:
        raise ValueError("losing summary cannot contain the target")

    if summary.seed is not None and not _integer(summary.seed):
        raise ValueError("summary seed is invalid")
    if not _integer(summary.hints_used) or summary.hints_used < 0:
        raise ValueError("summary hints_used is invalid")
    if not _integer(summary.hint_penalty) or summary.hint_penalty < 0:
        raise ValueError("summary hint_penalty is invalid")
