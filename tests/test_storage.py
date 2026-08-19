import json
from pathlib import Path

import pytest

from guessnova.profile import Profile
from guessnova.storage import Storage, normalize_state


def test_storage_save_and_load_profile(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    profile = Profile("Sanskar")
    profile.stats.xp = 99
    storage.save_profile(profile)
    restored = storage.load_profile()
    assert restored.name == "Sanskar"
    assert restored.stats.xp == 99


def test_storage_migrates_v0(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    path.write_text(json.dumps({}), encoding="utf-8")
    payload = Storage(tmp_path).load_raw()
    assert payload["schema_version"] == 1
    assert "profiles" in payload


def test_storage_rejects_future_version(tmp_path: Path) -> None:
    (tmp_path / "state.json").write_text('{"schema_version":999}', encoding="utf-8")
    with pytest.raises(ValueError, match="newer"):
        Storage(tmp_path).load_raw()


def test_storage_rejects_invalid_json(tmp_path: Path) -> None:
    (tmp_path / "state.json").write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        Storage(tmp_path).load_raw()


def test_storage_rejects_invalid_profiles_container() -> None:
    with pytest.raises(ValueError, match="profiles"):
        normalize_state({"schema_version": 1, "profiles": []})


def test_storage_normalizes_untrusted_profile_and_leaderboard_data() -> None:
    normalized = normalize_state(
        {
            "schema_version": 1,
            "active_profile": 123,
            "profiles": {
                "Tester": {
                    "name": "Tester",
                    "stats": {"games_played": "2", "games_won": 9},
                },
                4: "ignored",
            },
            "leaderboard": ["bad"],
            "unexpected": "dropped",
        }
    )
    assert normalized["active_profile"] == "Player"
    assert "unexpected" not in normalized
    assert normalized["leaderboard"] == []
    profiles = normalized["profiles"]
    assert isinstance(profiles, dict)
    assert profiles["Tester"]["stats"]["games_won"] == 2  # type: ignore[index]


def test_storage_leaderboard_round_trip(tmp_path: Path) -> None:
    from guessnova.leaderboard import LeaderboardEntry

    entry = LeaderboardEntry("A", "normal", "classic", 3, 1.2, "2026-08-19")
    storage = Storage(tmp_path)
    storage.save_leaderboard([entry])
    assert storage.load_leaderboard() == [entry]
