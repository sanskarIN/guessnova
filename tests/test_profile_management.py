from pathlib import Path

import pytest

from guessnova.leaderboard import LeaderboardEntry
from guessnova.profile import Profile
from guessnova.storage import Storage


def test_profile_create_list_and_switch(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.create_profile("Alpha")
    storage.create_profile("Beta", make_active=False)
    assert storage.list_profile_names() == ["Alpha", "Beta"]
    assert storage.active_profile_name() == "Alpha"
    assert storage.set_active_profile("Beta").name == "Beta"
    assert storage.active_profile_name() == "Beta"


def test_create_profile_rejects_duplicate(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.create_profile("Alpha")
    with pytest.raises(ValueError, match="already exists"):
        storage.create_profile("Alpha")


def test_rename_profile_updates_active_profile_and_leaderboard(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    profile = Profile("Alpha")
    storage.save_profile(profile)
    storage.save_leaderboard(
        [LeaderboardEntry("Alpha", "normal", "classic", 3, 1.2, "2026-08-19")]
    )
    renamed = storage.rename_profile("Alpha", "Nova")
    assert renamed.name == "Nova"
    assert storage.list_profile_names() == ["Nova"]
    assert storage.active_profile_name() == "Nova"
    assert storage.load_leaderboard()[0].player == "Nova"


def test_delete_profile_moves_profile_and_scores_to_bounded_trash(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.create_profile("Alpha")
    storage.save_leaderboard(
        [LeaderboardEntry("Alpha", "normal", "classic", 3, 1.2, "2026-08-19")]
    )
    storage.delete_profile("Alpha")
    assert storage.list_profile_names() == []
    assert storage.list_deleted_profile_names() == ["Alpha"]
    assert storage.load_leaderboard() == []


def test_restore_profile_recovers_profile_and_leaderboard(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    profile = storage.create_profile("Alpha")
    profile.stats.xp = 99
    storage.save_profile(profile)
    storage.save_leaderboard(
        [LeaderboardEntry("Alpha", "hard", "daily", 2, 0.8, "2026-08-19")]
    )
    storage.delete_profile("Alpha")
    restored = storage.restore_profile("Alpha")
    assert restored.stats.xp == 99
    assert storage.active_profile_name() == "Alpha"
    assert storage.list_deleted_profile_names() == []
    assert storage.load_leaderboard()[0].player == "Alpha"


def test_restore_profile_rejects_name_collision(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.create_profile("Alpha")
    storage.delete_profile("Alpha")
    storage.create_profile("Alpha")
    with pytest.raises(ValueError, match="already exists"):
        storage.restore_profile("Alpha")
