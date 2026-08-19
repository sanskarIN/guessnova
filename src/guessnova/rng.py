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
        return random.Random(self.seed).randint(minimum, maximum) if self.seed is not None else random.randint(minimum, maximum)


def daily_seed(day: date, namespace: str = "guessnova-daily-v1") -> int:
    digest = hashlib.sha256(f"{namespace}:{day.isoformat()}".encode()).digest()
    return int.from_bytes(digest[:8], "big", signed=False)
