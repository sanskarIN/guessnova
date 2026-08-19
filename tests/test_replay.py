import pytest

from guessnova.domain import GameMode, GameSummary
from guessnova.replay import decode_replay, encode_replay


def test_replay_round_trip() -> None:
    summary = GameSummary(GameMode.CLASSIC, "normal", 42, True, 4, 2.3, (10, 20, 30, 42), 7)
    code = encode_replay(summary)
    assert decode_replay(code) == summary


def test_replay_detects_tamper() -> None:
    summary = GameSummary(GameMode.CLASSIC, "normal", 42, True, 1, 1.0)
    code = encode_replay(summary)
    last = "A" if code[-1] != "A" else "B"
    with pytest.raises((ValueError, Exception)):
        decode_replay(code[:-1] + last)
