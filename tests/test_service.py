from pathlib import Path

from guessnova.domain import GameMode, GameSummary
from guessnova.service import GameService
from guessnova.storage import Storage


def test_service_records_result(tmp_path: Path) -> None:
    service = GameService(Storage(tmp_path))
    summary = GameSummary(GameMode.CLASSIC, "normal", 42, True, 2, 1.0, (20, 42))
    profile, unlocked = service.record(summary, "Tester")
    assert profile.stats.games_played == 1
    assert "first_win" in unlocked


def test_service_adds_win_to_leaderboard(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    service = GameService(storage)
    summary = GameSummary(GameMode.CLASSIC, "normal", 42, True, 3, 1.0, (20, 30, 42))
    service.record(summary, "Tester")
    entries = storage.load_leaderboard()
    assert len(entries) == 1
    assert entries[0].player == "Tester"
