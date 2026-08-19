"""Small input and file-safety helpers."""

from __future__ import annotations

import re
from pathlib import Path

from .constants import MAX_PROFILE_NAME_LENGTH

_PROFILE_RE = re.compile(r"[^A-Za-z0-9 _.-]+")


def sanitize_profile_name(value: str) -> str:
    cleaned = _PROFILE_RE.sub("", value.strip())[:MAX_PROFILE_NAME_LENGTH].strip()
    return cleaned or "Player"


def bounded_int(value: str | int, minimum: int, maximum: int) -> int:
    result = int(value)
    if result < minimum or result > maximum:
        raise ValueError(f"value must be between {minimum} and {maximum}")
    return result


def ensure_within(base: Path, candidate: Path) -> Path:
    base_resolved = base.resolve()
    candidate_resolved = candidate.resolve()
    if candidate_resolved != base_resolved and base_resolved not in candidate_resolved.parents:
        raise ValueError("path escapes the permitted directory")
    return candidate_resolved
