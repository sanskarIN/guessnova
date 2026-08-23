import pytest

from guessnova.engine import ReverseGuesser


def test_reverse_guess_requires_feedback_before_next_guess() -> None:
    reverse = ReverseGuesser(1, 100)
    assert reverse.next_guess() == 50

    with pytest.raises(RuntimeError, match="respond before"):
        reverse.next_guess()

    assert reverse.attempts == 1
    assert reverse.current == 50


def test_valid_reverse_feedback_consumes_pending_guess() -> None:
    reverse = ReverseGuesser(1, 100)
    assert reverse.next_guess() == 50
    reverse.respond("higher")

    assert reverse.current is None
    assert reverse.low == 51
    assert reverse.next_guess() == 75


def test_invalid_reverse_feedback_keeps_pending_guess_recoverable() -> None:
    reverse = ReverseGuesser(1, 2)
    assert reverse.next_guess() == 1

    with pytest.raises(ValueError, match="inconsistent"):
        reverse.respond("lower")

    assert reverse.current == 1
    assert reverse.low == 1
    assert reverse.high == 2
    reverse.respond("higher")
    assert reverse.current is None
    assert reverse.next_guess() == 2
