from guessnova.domain import GameMode, GuessOutcome
from guessnova.engine import GuessGame


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


def test_timed_timeout() -> None:
    now = [0.0]
    game = GuessGame(mode=GameMode.TIMED, target=42, clock=lambda: now[0])
    now[0] = 999.0
    feedback = game.guess(42)
    assert feedback.outcome == GuessOutcome.TIMEOUT
    assert not game.won
