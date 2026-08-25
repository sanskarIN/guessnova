from __future__ import annotations

from datetime import date

import pytest

from guessnova.challenge_descriptor import MAX_PORTABLE_SEED, PortableChallengeDescriptor
from guessnova.domain import GameMode


def test_future_descriptor_versions_are_rejected() -> None:
    with pytest.raises(ValueError, match="unsupported portable challenge descriptor version"):
        PortableChallengeDescriptor.from_dict(
            {"version": 2, "mode": "classic", "difficulty": "normal", "seed": 42}
        )


def test_reverse_is_not_a_portable_target_descriptor() -> None:
    with pytest.raises(ValueError, match="game mode is not portable"):
        PortableChallengeDescriptor.from_dict(
            {"version": 1, "mode": "reverse", "difficulty": "normal", "seed": 42}
        )


def test_seeded_descriptor_requires_exact_fields() -> None:
    with pytest.raises(ValueError, match="missing fields: seed"):
        PortableChallengeDescriptor.from_dict(
            {"version": 1, "mode": "classic", "difficulty": "normal"}
        )


def test_daily_descriptor_rejects_extra_seed_field() -> None:
    with pytest.raises(ValueError, match="unknown fields: seed"):
        PortableChallengeDescriptor.from_dict(
            {
                "version": 1,
                "mode": "daily",
                "difficulty": "normal",
                "day": "2026-08-25",
                "seed": 42,
            }
        )


def test_invalid_dates_are_rejected() -> None:
    with pytest.raises(ValueError, match="portable challenge date"):
        PortableChallengeDescriptor.from_dict(
            {
                "version": 1,
                "mode": "daily",
                "difficulty": "normal",
                "day": "2026-02-30",
            }
        )


def test_seed_must_fit_exactly_in_both_runtimes() -> None:
    with pytest.raises(ValueError, match="safe integer"):
        PortableChallengeDescriptor(
            mode=GameMode.CLASSIC,
            difficulty="normal",
            seed=MAX_PORTABLE_SEED + 1,
        )


def test_direct_daily_descriptor_requires_a_real_date() -> None:
    descriptor = PortableChallengeDescriptor(
        mode=GameMode.DAILY,
        difficulty="normal",
        day=date(2026, 8, 25),
    )
    assert descriptor.to_dict()["day"] == "2026-08-25"
