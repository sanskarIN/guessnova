"""Versioned portable challenge identity for future cross-interface parity.

This module is additive preparation for the next GuessNova compatibility line. It
does not change the current CLI or Textual challenge setup semantics. Callers
must opt in to the descriptor contract explicitly.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from typing import Final

from .daily import daily_game
from .domain import DIFFICULTIES, GameMode
from .engine import GuessGame
from .rng import fnv1a32, portable_daily_target

PORTABLE_CHALLENGE_DESCRIPTOR_VERSION: Final = 1
PORTABLE_CHALLENGE_NAMESPACE: Final = "guessnova-challenge-v1"
MAX_PORTABLE_SEED: Final = (1 << 53) - 1
PORTABLE_CHALLENGE_MODES: Final = frozenset(
    {GameMode.CLASSIC, GameMode.TIMED, GameMode.STREAK, GameMode.DAILY}
)


@dataclass(frozen=True, slots=True)
class PortableChallengeDescriptor:
    """Canonical deterministic challenge identity shared by Python and browsers."""

    mode: GameMode
    difficulty: str
    seed: int | None = None
    day: date | None = None
    version: int = PORTABLE_CHALLENGE_DESCRIPTOR_VERSION

    def __post_init__(self) -> None:
        if (
            not isinstance(self.version, int)
            or isinstance(self.version, bool)
            or self.version != PORTABLE_CHALLENGE_DESCRIPTOR_VERSION
        ):
            raise ValueError(
                f"unsupported portable challenge descriptor version: {self.version}"
            )

        try:
            selected_mode = GameMode(self.mode)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"unknown game mode: {self.mode}") from exc
        object.__setattr__(self, "mode", selected_mode)

        if selected_mode not in PORTABLE_CHALLENGE_MODES:
            raise ValueError(f"game mode is not portable: {selected_mode.value}")
        if not isinstance(self.difficulty, str) or self.difficulty not in DIFFICULTIES:
            raise ValueError(f"unknown difficulty: {self.difficulty}")

        if selected_mode == GameMode.DAILY:
            if self.seed is not None:
                raise ValueError("daily portable challenges cannot carry a seed")
            if not isinstance(self.day, date):
                raise ValueError("daily portable challenges require a challenge date")
            return

        if self.day is not None:
            raise ValueError(
                "only daily portable challenges can carry a challenge date"
            )
        if (
            not isinstance(self.seed, int)
            or isinstance(self.seed, bool)
            or abs(self.seed) > MAX_PORTABLE_SEED
        ):
            raise ValueError(
                f"portable challenge seed must be a safe integer between "
                f"{-MAX_PORTABLE_SEED} and {MAX_PORTABLE_SEED}"
            )

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> PortableChallengeDescriptor:
        """Parse a strict canonical descriptor mapping and reject unknown fields."""
        if not isinstance(payload, Mapping):
            raise ValueError("portable challenge descriptor must be an object")

        version = payload.get("version")
        if (
            not isinstance(version, int)
            or isinstance(version, bool)
            or version != PORTABLE_CHALLENGE_DESCRIPTOR_VERSION
        ):
            raise ValueError(
                f"unsupported portable challenge descriptor version: {version}"
            )

        raw_mode = payload.get("mode")
        if not isinstance(raw_mode, str):
            raise ValueError(f"unknown game mode: {raw_mode}")
        try:
            mode = GameMode(raw_mode)
        except ValueError as exc:
            raise ValueError(f"unknown game mode: {raw_mode}") from exc
        if mode not in PORTABLE_CHALLENGE_MODES:
            raise ValueError(f"game mode is not portable: {mode.value}")

        expected_keys = {"version", "mode", "difficulty", "day"}
        if mode != GameMode.DAILY:
            expected_keys = {"version", "mode", "difficulty", "seed"}
        actual_keys = set(payload)
        if actual_keys != expected_keys:
            missing = sorted(expected_keys - actual_keys)
            unknown = sorted(str(key) for key in actual_keys - expected_keys)
            details: list[str] = []
            if missing:
                details.append(f"missing fields: {', '.join(missing)}")
            if unknown:
                details.append(f"unknown fields: {', '.join(unknown)}")
            raise ValueError(
                "invalid portable challenge descriptor fields ("
                + "; ".join(details)
                + ")"
            )

        difficulty = payload["difficulty"]
        if not isinstance(difficulty, str):
            raise ValueError(f"unknown difficulty: {difficulty}")

        if mode == GameMode.DAILY:
            raw_day = payload["day"]
            if not isinstance(raw_day, str):
                raise ValueError("portable challenge date must use YYYY-MM-DD")
            try:
                selected_day = date.fromisoformat(raw_day)
            except ValueError as exc:
                raise ValueError("portable challenge date must use YYYY-MM-DD") from exc
            if selected_day.isoformat() != raw_day:
                raise ValueError(
                    "portable challenge date must use canonical YYYY-MM-DD"
                )
            return cls(
                mode=mode,
                difficulty=difficulty,
                day=selected_day,
                version=version,
            )

        seed = payload["seed"]
        if not isinstance(seed, int) or isinstance(seed, bool):
            raise ValueError("portable challenge seed must be a safe integer")
        return cls(mode=mode, difficulty=difficulty, seed=seed, version=version)

    def to_dict(self) -> dict[str, object]:
        """Return the canonical JSON-compatible representation."""
        payload: dict[str, object] = {
            "version": self.version,
            "mode": self.mode.value,
            "difficulty": self.difficulty,
        }
        if self.mode == GameMode.DAILY:
            if self.day is None:  # pragma: no cover - guarded by __post_init__
                raise RuntimeError("daily portable challenge date is unavailable")
            payload["day"] = self.day.isoformat()
        else:
            if self.seed is None:  # pragma: no cover - guarded by __post_init__
                raise RuntimeError("portable challenge seed is unavailable")
            payload["seed"] = self.seed
        return payload

    def target(self) -> int:
        """Resolve the portable hidden target for this deterministic descriptor."""
        difficulty = DIFFICULTIES[self.difficulty]
        if self.mode == GameMode.DAILY:
            if self.day is None:  # pragma: no cover - guarded by __post_init__
                raise RuntimeError("daily portable challenge date is unavailable")
            return portable_daily_target(
                self.day,
                difficulty.minimum,
                difficulty.maximum,
                self.difficulty,
            )

        if self.seed is None:  # pragma: no cover - guarded by __post_init__
            raise RuntimeError("portable challenge seed is unavailable")
        fingerprint = (
            f"{PORTABLE_CHALLENGE_NAMESPACE}:{self.mode.value}:"
            f"{self.difficulty}:{self.seed}"
        )
        return difficulty.minimum + fnv1a32(fingerprint) % difficulty.span

    def build_game(self) -> GuessGame:
        """Build an opt-in game using the portable target without changing legacy setup."""
        if self.mode == GameMode.DAILY:
            if self.day is None:  # pragma: no cover - guarded by __post_init__
                raise RuntimeError("daily portable challenge date is unavailable")
            return daily_game(self.day, difficulty=self.difficulty)
        return GuessGame(
            difficulty_name=self.difficulty,
            mode=self.mode,
            seed=self.seed,
            target=self.target(),
        )
