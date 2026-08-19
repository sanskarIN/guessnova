from guessnova.domain import DIFFICULTIES
from guessnova.hints import smart_hint


def test_hint_contains_direction_and_parity() -> None:
    hint = smart_hint(42, 20, DIFFICULTIES["normal"])
    assert "higher" in hint
    assert "even" in hint


def test_hint_can_point_lower() -> None:
    assert "lower" in smart_hint(25, 80, DIFFICULTIES["normal"])
