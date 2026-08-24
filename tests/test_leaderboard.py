import pytest

from guessnova.domain import GameMode, GameSummary
from guessnova.leaderboard import (
    MAX_LEADERBOARD_ENTRIES,
    LeaderboardEntry,
    add_entry,
    deserialize,
    entry_from_summary,
    serialize,
)


def test_only_wins_become_entries() -> None:
    loss = GameSummary(GameMode.CLASSIC, "normal", 1, False, 9, 5.0)
    assert entry_from_summary("Player", loss) is None


def test_entries_sort_by_attempts_then_time() -> None:
    a = LeaderboardEntry("A", "normal", "classic", 4, 2.0, "2026-01-01")
    b = LeaderboardEntry("B", "normal", "classic", 3, 9.0, "2026-01-01")
    assert add_entry([a], b)[0].player == "B"


def test_serialization_round_trip() -> None:
    entries = [LeaderboardEntry("A", "normal", "classic", 4, 2.0, "2026-01-01")]
    assert deserialize(serialize(entries)) == entries


def test_deserializer_rejects_invalid_entry_fields() -> None:
    invalid = [
        {
            "player": ["A"],
            "difficulty": "normal",
            "mode": "classic",
            "attempts": 1,
            "elapsed_seconds": 1.0,
            "created_at": "now",
        },
        {
            "player": "A",
            "difficulty": "unknown",
            "mode": "classic",
            "attempts": 1,
            "elapsed_seconds": 1.0,
            "created_at": "now",
        },
        {
            "player": "A",
            "difficulty": "normal",
            "mode": "reverse",
            "attempts": 1,
            "elapsed_seconds": 1.0,
            "created_at": "now",
        },
        {
            "player": "A",
            "difficulty": "normal",
            "mode": "classic",
            "attempts": -1,
            "elapsed_seconds": 1.0,
            "created_at": "now",
        },
        {
            "player": "A",
            "difficulty": "normal",
            "mode": "classic",
            "attempts": 1,
            "elapsed_seconds": float("inf"),
            "created_at": "now",
        },
    ]
    assert deserialize(invalid) == []


def test_deserializer_canonicalizes_and_bounds_imported_entries() -> None:
    items = [
        {
            "player": f"Player {index}",
            "difficulty": "normal",
            "mode": "classic",
            "attempts": 9 - (index % 9),
            "elapsed_seconds": float(MAX_LEADERBOARD_ENTRIES * 2 - index),
            "created_at": f"2026-01-{(index % 28) + 1:02d}",
        }
        for index in range(MAX_LEADERBOARD_ENTRIES * 2)
    ]

    restored = deserialize(items)
    assert len(restored) == MAX_LEADERBOARD_ENTRIES
    assert restored == sorted(restored, key=lambda entry: entry.score_key)


def test_leaderboard_limit_must_be_positive() -> None:
    entry = LeaderboardEntry("A", "normal", "classic", 1, 1.0, "2026-01-01")
    with pytest.raises(ValueError, match="positive"):
        add_entry([], entry, limit=0)
