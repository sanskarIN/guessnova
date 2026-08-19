from guessnova.domain import GameMode, GameSummary
from guessnova.history import MAX_HISTORY_ENTRIES, append_history, deserialize, entry_from_summary, serialize


def summary(*, won: bool = True, seed: int | None = 7) -> GameSummary:
    return GameSummary(GameMode.CLASSIC, "normal", 42, won, 3, 1.25, (10, 30, 42), seed)


def test_history_entry_round_trip() -> None:
    entry = entry_from_summary(summary(), played_at="2026-08-19T00:00:00+00:00")
    restored = deserialize(serialize([entry]))
    assert restored == [entry]


def test_history_is_bounded_to_recent_entries() -> None:
    entries = []
    for index in range(MAX_HISTORY_ENTRIES + 3):
        entry = entry_from_summary(
            summary(seed=index), played_at=f"2026-08-19T00:00:{index:02d}+00:00"
        )
        entries = append_history(entries, entry)
    assert len(entries) == MAX_HISTORY_ENTRIES
    assert entries[-1].seed == MAX_HISTORY_ENTRIES + 2


def test_history_deserializer_skips_invalid_items() -> None:
    invalid = [
        {"mode": "classic"},
        "broken",
        1,
        {
            "mode": "unknown",
            "difficulty": "normal",
            "won": True,
            "attempts": 1,
            "elapsed_seconds": 1.0,
            "seed": None,
            "played_at": "now",
        },
        {
            "mode": "classic",
            "difficulty": "normal",
            "won": "false",
            "attempts": -1,
            "elapsed_seconds": -1.0,
            "seed": False,
            "played_at": "now",
        },
    ]
    assert deserialize(invalid) == []
