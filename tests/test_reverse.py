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
