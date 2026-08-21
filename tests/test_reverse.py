import pytest

from guessnova.engine import ReverseGuesser


def test_reverse_guesser_binary_searches() -> None:
    target = 73
    engine = ReverseGuesser(1, 100)
    while not engine.finished:
        guess = engine.next_guess()
        engine.respond("correct" if guess == target else "higher" if guess < target else "lower")
    assert engine.current == target
    assert engine.attempts <= 7


def test_reverse_rejects_invalid_response() -> None:
    engine = ReverseGuesser()
    engine.next_guess()
    with pytest.raises(ValueError):
        engine.respond("maybe")


def test_reverse_requires_guess_before_response() -> None:
    with pytest.raises(RuntimeError):
        ReverseGuesser().respond("correct")


def test_reverse_contradiction_does_not_corrupt_search_bounds() -> None:
    engine = ReverseGuesser(1, 2)
    assert engine.next_guess() == 1

    with pytest.raises(ValueError, match="inconsistent"):
        engine.respond("lower")

    assert (engine.low, engine.high, engine.current, engine.attempts) == (1, 2, 1, 1)
    engine.respond("higher")
    assert engine.next_guess() == 2


def test_reverse_rejects_feedback_after_completion() -> None:
    engine = ReverseGuesser(1, 2)
    assert engine.next_guess() == 1
    engine.respond("correct")
    snapshot = (engine.low, engine.high, engine.current, engine.attempts)

    with pytest.raises(RuntimeError, match="already finished"):
        engine.respond("higher")

    assert (engine.low, engine.high, engine.current, engine.attempts) == snapshot
