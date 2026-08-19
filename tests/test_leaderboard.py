from guessnova.domain import GameMode, GameSummary
from guessnova.leaderboard import LeaderboardEntry, add_entry, deserialize, entry_from_summary, serialize


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
