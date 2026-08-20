"""Deterministic random-number utilities."""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class RandomSource:
    seed: int | None = None

    def randint(self, minimum: int, maximum: int) -> int:
        return (
            random.Random(self.seed).randint(minimum, maximum)
            if self.seed is not None
            else random.randint(minimum, maximum)
        )


def daily_seed(day: date, namespace: str = "guessnova-daily-v1") -> int:
    """Return the legacy Python daily seed retained for replay compatibility."""
    digest = hashlib.sha256(f"{namespace}:{day.isoformat()}".encode()).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def fnv1a32(text: str) -> int:
    """Return a portable unsigned FNV-1a hash shared with the browser client."""
    value = 0x811C9DC5
    for byte in text.encode("utf-8"):
        value ^= byte
        value = (value * 0x01000193) & 0xFFFFFFFF
    return value


def portable_daily_seed(
    day: date,
    difficulty_name: str = "normal",
    namespace: str = "guessnova-daily-v2",
) -> int:
    """Return the cross-language daily seed used by Python and web clients."""
    return fnv1a32(f"{namespace}:{day.isoformat()}:{difficulty_name}")


def portable_daily_target(
    day: date,
    minimum: int,
    maximum: int,
    difficulty_name: str = "normal",
) -> int:
    """Map the portable daily seed into an inclusive difficulty range."""
    if minimum > maximum:
        raise ValueError("minimum must not exceed maximum")
    span = maximum - minimum + 1
    return minimum + portable_daily_seed(day, difficulty_name) % span
