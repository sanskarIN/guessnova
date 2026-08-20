"""Portable replay-code encoding with integrity protection and strict validation."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import math
from dataclasses import asdict

from .constants import REPLAY_VERSION
from .domain import DIFFICULTIES, GameMode, GameSummary

MAX_REPLAY_CODE_LENGTH = 16_384
MAX_HINT_METADATA = 1_000_000
MIN_PORTABLE_SEED = -(2**63)
MAX_PORTABLE_SEED = 2**63 - 1


def encode_replay(summary: GameSummary) -> str:
    if summary.mode == GameMode.REVERSE:
        raise ValueError("reverse mode is not supported by the replay format")
    body = asdict(summary)
    body["mode"] = summary.mode.value
    body["version"] = REPLAY_VERSION
    raw = json.dumps(body, separators=(",", ":"), sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:16].encode("ascii")
    return base64.urlsafe_b64encode(digest + b"." + raw).decode("ascii").rstrip("=")


def _integer(value: object, field: str, *, minimum: int = 0, maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"invalid replay {field}")
    if value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"invalid replay {field}")
    return value


def _number(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"invalid replay {field}")
    result = float(value)
    if result < 0 or not math.isfinite(result):
        raise ValueError(f"invalid replay {field}")
    return result


def decode_replay(code: str) -> GameSummary:
    if not isinstance(code, str):
        raise ValueError("replay code must be text")
    code = code.strip()
    if not code or len(code) > MAX_REPLAY_CODE_LENGTH:
        raise ValueError("invalid replay code length")

    padded = code + "=" * (-len(code) % 4)
    try:
        decoded = base64.b64decode(padded.encode("ascii"), altchars=b"-_", validate=True)
    except (UnicodeEncodeError, binascii.Error, ValueError) as exc:
        raise ValueError("invalid replay encoding") from exc

    try:
        digest, raw = decoded.split(b".", 1)
    except ValueError as exc:
        raise ValueError("invalid replay envelope") from exc
    if len(digest) != 16 or not raw:
        raise ValueError("invalid replay envelope")

    expected = hashlib.sha256(raw).hexdigest()[:16].encode("ascii")
    if not hmac.compare_digest(digest, expected):
        raise ValueError("replay checksum mismatch")

    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("invalid replay payload") from exc
    if not isinstance(payload, dict):
        raise ValueError("replay payload must be an object")

    version = payload.pop("version", None)
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError("invalid replay version")
    if version != REPLAY_VERSION:
        raise ValueError("unsupported replay version")

    required = {
        "mode",
        "difficulty",
        "target",
        "won",
        "attempts",
        "elapsed_seconds",
        "guesses",
        "seed",
    }
    optional = {"hints_used", "hint_penalty"}
    keys = set(payload)
    if not required <= keys or keys - required - optional:
        raise ValueError("invalid replay fields")

    mode_raw = payload["mode"]
    difficulty = payload["difficulty"]
    won = payload["won"]
    guesses_raw = payload["guesses"]
    seed_raw = payload["seed"]
    if not isinstance(mode_raw, str):
        raise ValueError("invalid replay mode")
    try:
        mode = GameMode(mode_raw)
    except ValueError as exc:
        raise ValueError("invalid replay mode") from exc
    if mode == GameMode.REVERSE:
        raise ValueError("invalid replay mode")
    if not isinstance(difficulty, str) or difficulty not in DIFFICULTIES:
        raise ValueError("invalid replay difficulty")
    if not isinstance(won, bool):
        raise ValueError("invalid replay result")
    if not isinstance(guesses_raw, list):
        raise ValueError("invalid replay guesses")

    rules = DIFFICULTIES[difficulty]
    target = _integer(
        payload["target"],
        "target",
        minimum=rules.minimum,
        maximum=rules.maximum,
    )
    attempts = _integer(
        payload["attempts"],
        "attempts",
        maximum=rules.max_attempts,
    )
    elapsed_seconds = _number(payload["elapsed_seconds"], "elapsed_seconds")
    if len(guesses_raw) != attempts:
        raise ValueError("replay attempts do not match guesses")
    guesses = tuple(
        _integer(item, "guess", minimum=rules.minimum, maximum=rules.maximum)
        for item in guesses_raw
    )
    if won and (not guesses or guesses[-1] != target):
        raise ValueError("winning replay does not end at target")
    if not won and target in guesses:
        raise ValueError("losing replay contains the target")

    if seed_raw is None:
        seed = None
    else:
        seed = _integer(
            seed_raw,
            "seed",
            minimum=MIN_PORTABLE_SEED,
            maximum=MAX_PORTABLE_SEED,
        )

    hints_used = _integer(
        payload.get("hints_used", 0),
        "hints_used",
        maximum=MAX_HINT_METADATA,
    )
    hint_penalty = _integer(
        payload.get("hint_penalty", 0),
        "hint_penalty",
        maximum=MAX_HINT_METADATA,
    )

    return GameSummary(
        mode=mode,
        difficulty=difficulty,
        target=target,
        won=won,
        attempts=attempts,
        elapsed_seconds=elapsed_seconds,
        guesses=guesses,
        seed=seed,
        hints_used=hints_used,
        hint_penalty=hint_penalty,
    )
