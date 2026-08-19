import base64
import hashlib
import json

import pytest

from guessnova.domain import GameMode, GameSummary
from guessnova.replay import MAX_REPLAY_CODE_LENGTH, decode_replay, encode_replay


def _code_for_payload(payload: object) -> str:
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:16].encode("ascii")
    return base64.urlsafe_b64encode(digest + b"." + raw).decode("ascii").rstrip("=")


def _valid_payload() -> dict[str, object]:
    return {
        "version": 1,
        "mode": "classic",
        "difficulty": "normal",
        "target": 42,
        "won": True,
        "attempts": 4,
        "elapsed_seconds": 2.3,
        "guesses": [10, 20, 30, 42],
        "seed": 7,
        "hints_used": 1,
        "hint_penalty": 10,
    }


def test_replay_round_trip() -> None:
    summary = GameSummary(
        GameMode.CLASSIC,
        "normal",
        42,
        True,
        4,
        2.3,
        (10, 20, 30, 42),
        7,
        hints_used=1,
        hint_penalty=10,
    )
    code = encode_replay(summary)
    assert decode_replay(code) == summary


def test_negative_seed_round_trip() -> None:
    summary = GameSummary(GameMode.CLASSIC, "normal", 42, True, 1, 1.0, (42,), -7)
    assert decode_replay(encode_replay(summary)) == summary


def test_replay_detects_tamper() -> None:
    summary = GameSummary(GameMode.CLASSIC, "normal", 42, True, 1, 1.0, (42,))
    code = encode_replay(summary)
    middle = len(code) // 2
    replacement = "A" if code[middle] != "A" else "B"
    with pytest.raises(ValueError):
        decode_replay(code[:middle] + replacement + code[middle + 1 :])


def test_legacy_v1_replay_without_hint_metadata_still_loads() -> None:
    payload = _valid_payload()
    payload.pop("hints_used")
    payload.pop("hint_penalty")
    restored = decode_replay(_code_for_payload(payload))
    assert restored.hints_used == 0
    assert restored.hint_penalty == 0


@pytest.mark.parametrize(
    "code",
    [
        "",
        "!",
        "not-a-replay",
        "A",
        "====",
        "A" * (MAX_REPLAY_CODE_LENGTH + 1),
    ],
)
def test_malformed_replay_text_is_rejected_cleanly(code: str) -> None:
    with pytest.raises(ValueError):
        decode_replay(code)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("version", 2),
        ("mode", "unknown"),
        ("difficulty", "impossible"),
        ("target", 1000),
        ("won", "yes"),
        ("attempts", -1),
        ("elapsed_seconds", -1.0),
        ("guesses", "42"),
        ("seed", True),
        ("hints_used", -1),
        ("hint_penalty", 2_000_000),
    ],
)
def test_semantically_invalid_signed_payloads_are_rejected(field: str, value: object) -> None:
    payload = _valid_payload()
    payload[field] = value
    with pytest.raises(ValueError):
        decode_replay(_code_for_payload(payload))


def test_unknown_replay_fields_are_rejected() -> None:
    payload = _valid_payload()
    payload["future_secret"] = "unexpected"
    with pytest.raises(ValueError, match="fields"):
        decode_replay(_code_for_payload(payload))


def test_replay_attempt_count_must_match_guess_count() -> None:
    payload = _valid_payload()
    payload["attempts"] = 3
    with pytest.raises(ValueError, match="attempts"):
        decode_replay(_code_for_payload(payload))
