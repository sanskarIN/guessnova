from pathlib import Path

from guessnova.leaderboard import LeaderboardEntry
from guessnova.profile import Profile
from guessnova.storage import Storage


def _entry(player: str, attempts: int) -> LeaderboardEntry:
    return LeaderboardEntry(
        player,
        "normal",
        "classic",
        attempts,
        float(attempts),
        f"2026-08-20T00:00:0{attempts}+00:00",
    )


def test_completed_round_preserves_existing_leaderboard_entries(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.save_leaderboard([_entry("Existing", 3)])

    profile = Profile("New Player")
    profile.stats.games_played = 1
    profile.stats.games_won = 1
    storage.save_completed_round(profile, _entry("New Player", 2))

    entries = storage.load_leaderboard()
    assert [entry.player for entry in entries] == ["New Player", "Existing"]
    restored = storage.load_profile("New Player")
    assert restored.stats.games_won == 1


def test_completed_loss_keeps_existing_leaderboard_unchanged(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    existing = _entry("Existing", 3)
    storage.save_leaderboard([existing])

    profile = Profile("Loser")
    profile.stats.games_played = 1
    storage.save_completed_round(profile, None)

    assert storage.load_leaderboard() == [existing]
    assert storage.load_profile("Loser").stats.games_played == 1
