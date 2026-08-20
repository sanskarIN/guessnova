import pytest

from guessnova.domain import GameMode, GuessOutcome
from guessnova.engine import HINT_PENALTY_XP, GuessGame


def test_correct_guess_wins() -> None:
    game = GuessGame(target=42)
    feedback = game.guess(42)
    assert feedback.outcome == GuessOutcome.CORRECT
    assert game.won
    assert game.is_finished
    assert game.summary().guesses == (42,)


def test_wrong_guess_has_hint() -> None:
    game = GuessGame(target=80)
    feedback = game.guess(20)
    assert feedback.outcome == GuessOutcome.TOO_LOW
    assert feedback.hint is not None
    assert feedback.attempts_used == 1


def test_out_of_range_does_not_consume_attempt() -> None:
    game = GuessGame(target=50)
    feedback = game.guess(1000)
    assert feedback.outcome == GuessOutcome.OUT_OF_RANGE
    assert game.attempts_used == 0


def test_attempt_exhaustion() -> None:
    game = GuessGame(difficulty_name="easy", target=50)
    for _ in range(game.difficulty.max_attempts - 1):
        assert game.guess(1).outcome == GuessOutcome.TOO_LOW
    final = game.guess(1)
    assert final.outcome == GuessOutcome.EXHAUSTED
    assert game.is_finished
    assert not game.won


def test_seed_is_reproducible() -> None:
    first = GuessGame(seed=1234)
    second = GuessGame(seed=1234)
    assert first.target == second.target


def test_invalid_difficulty() -> None:
    try:
        GuessGame(difficulty_name="impossible")
    except ValueError as exc:
        assert "unknown difficulty" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_reverse_mode_requires_reverse_guesser() -> None:
    with pytest.raises(ValueError, match="ReverseGuesser"):
        GuessGame(mode=GameMode.REVERSE)


def test_runtime_mode_values_are_normalized_and_validated() -> None:
    timed = GuessGame(mode="timed", target=42)  # type: ignore[arg-type]
    assert timed.mode is GameMode.TIMED

    with pytest.raises(ValueError, match="unknown game mode"):
        GuessGame(mode="unknown", target=42)  # type: ignore[arg-type]


def test_timed_timeout() -> None:
    now = [0.0]
    game = GuessGame(mode=GameMode.TIMED, target=42, clock=lambda: now[0])
    now[0] = 999.0
    feedback = game.guess(42)
    assert feedback.outcome == GuessOutcome.TIMEOUT
    assert not game.won


def test_explicit_range_hint_tracks_penalty_without_consuming_attempt() -> None:
    game = GuessGame(difficulty_name="easy", target=42)
    hint = game.request_hint()
    assert "between" in hint
    assert game.attempts_used == 0
    assert game.hints_used == 1
    assert game.hint_penalty == HINT_PENALTY_XP
    summary = game.summary()
    assert summary.hints_used == 1
    assert summary.hint_penalty == HINT_PENALTY_XP


def test_explicit_hint_penalty_can_be_disabled() -> None:
    game = GuessGame(difficulty_name="easy", target=42)
    game.request_hint(penalize=False)
    assert game.hints_used == 1
    assert game.hint_penalty == 0
