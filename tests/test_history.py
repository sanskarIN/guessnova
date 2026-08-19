from datetime import date

import pytest

from guessnova.domain import GameMode, GameSummary
from guessnova.history import (
    MAX_HISTORY_ENTRIES,
    HistoryEntry,
    append_history,
    deserialize,
    entry_from_summary,
    filter_history,
    group_history,
    serialize,
)


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


def _entry(
    played_at: str,
    *,
    mode: str = "classic",
    difficulty: str = "normal",
    won: bool = True,
    attempts: int = 3,
    seed: int | None = 7,
) -> HistoryEntry:
    return HistoryEntry(mode, difficulty, won, attempts, 1.5, seed, played_at)


def test_filter_history_supports_structured_date_and_text_filters() -> None:
    entries = [
        _entry("2026-08-17T08:00:00+00:00", won=False, seed=10),
        _entry("2026-08-18T08:00:00+00:00", difficulty="hard", seed=20),
        _entry("2026-08-19T08:00:00+00:00", mode="daily", seed=30),
    ]
    assert filter_history(entries, result="loss") == [entries[0]]
    assert filter_history(entries, difficulty="hard") == [entries[1]]
    assert filter_history(entries, since=date(2026, 8, 18)) == entries[1:]
    assert filter_history(entries, until=date(2026, 8, 18)) == entries[:2]
    assert filter_history(entries, query="30") == [entries[2]]
    assert filter_history(entries, query="DAILY") == [entries[2]]


def test_filter_history_excludes_unparseable_dates_when_date_filtering() -> None:
    entry = _entry("not-a-date")
    assert filter_history([entry], since=date(2026, 8, 1)) == []


def test_group_history_supports_release_ui_groupings() -> None:
    entries = [
        _entry("2026-08-18T08:00:00+00:00", won=True),
        _entry("2026-08-18T09:00:00+00:00", won=False),
        _entry("2026-08-19T08:00:00+00:00", mode="daily", difficulty="hard"),
    ]
    assert list(group_history(entries, by="day")) == ["2026-08-18", "2026-08-19"]
    assert list(group_history(entries, by="mode")) == ["classic", "daily"]
    assert list(group_history(entries, by="difficulty")) == ["normal", "hard"]
    assert list(group_history(entries, by="result")) == ["win", "loss"]


def test_group_history_rejects_unknown_grouping() -> None:
    with pytest.raises(ValueError, match="unsupported history grouping"):
        group_history([_entry("2026-08-19T08:00:00+00:00")], by="unknown")  # type: ignore[arg-type]
