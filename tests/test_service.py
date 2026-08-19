from pathlib import Path

from guessnova.domain import GameMode, GameSummary
from guessnova.service import GameService
from guessnova.storage import Storage


def test_service_records_result_and_history(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    service = GameService(storage)
    summary = GameSummary(GameMode.CLASSIC, "normal", 42, True, 2, 1.0, (20, 42), 7)
    profile, unlocked = service.record(summary, "Tester")
    assert profile.stats.games_played == 1
    assert "first_win" in unlocked
    assert len(profile.history) == 1
    assert profile.history[0].mode == "classic"
    assert profile.history[0].seed == 7
    assert storage.load_profile("Tester").history == profile.history


def test_service_adds_win_to_leaderboard(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    service = GameService(storage)
    summary = GameSummary(GameMode.CLASSIC, "normal", 42, True, 3, 1.0, (20, 30, 42))
    service.record(summary, "Tester")
    entries = storage.load_leaderboard()
    assert len(entries) == 1
    assert entries[0].player == "Tester"


def test_service_records_loss_in_history_without_leaderboard_entry(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    summary = GameSummary(GameMode.CLASSIC, "easy", 42, False, 10, 3.5, tuple(range(10)))
    profile, _ = GameService(storage).record(summary, "Tester")
    assert profile.history[-1].won is False
    assert storage.load_leaderboard() == []
