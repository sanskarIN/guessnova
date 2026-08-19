"""Portable replay-code encoding with integrity protection."""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import asdict

from .constants import REPLAY_VERSION
from .domain import GameMode, GameSummary


def encode_replay(summary: GameSummary) -> str:
    body = asdict(summary)
    body["mode"] = summary.mode.value
    body["version"] = REPLAY_VERSION
    raw = json.dumps(body, separators=(",", ":"), sort_keys=True).encode()
    digest = hashlib.sha256(raw).hexdigest()[:16].encode()
    return base64.urlsafe_b64encode(digest + b"." + raw).decode().rstrip("=")


def decode_replay(code: str) -> GameSummary:
    padded = code + "=" * (-len(code) % 4)
    decoded = base64.urlsafe_b64decode(padded.encode())
    digest, raw = decoded.split(b".", 1)
    expected = hashlib.sha256(raw).hexdigest()[:16].encode()
    if digest != expected:
        raise ValueError("replay checksum mismatch")
    payload = json.loads(raw)
    if int(payload.pop("version")) != REPLAY_VERSION:
        raise ValueError("unsupported replay version")
    payload["mode"] = GameMode(payload["mode"])
    payload["guesses"] = tuple(payload.get("guesses", []))
    return GameSummary(**payload)
