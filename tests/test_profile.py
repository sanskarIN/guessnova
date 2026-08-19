from guessnova.domain import GameMode, GameSummary
from guessnova.history import entry_from_summary
from guessnova.profile import Profile


def test_profile_round_trip() -> None:
    profile = Profile("Nova Player")
    profile.stats.games_played = 5
    profile.stats.achievements.add("first_win")
    profile.history.append(
        entry_from_summary(
            GameSummary(GameMode.CLASSIC, "normal", 42, True, 2, 1.0, (10, 42), 7),
            played_at="2026-08-19T00:00:00+00:00",
        )
    )
    restored = Profile.from_dict(profile.to_dict())
    assert restored.name == "Nova Player"
    assert restored.stats.games_played == 5
    assert restored.stats.achievements == {"first_win"}
    assert restored.history == profile.history


def test_profile_sanitizes_name() -> None:
    assert Profile("  A<script>B  ").name == "AscriptB"


def test_profile_loads_legacy_payload_without_history() -> None:
    restored = Profile.from_dict({"name": "Legacy", "stats": {}, "settings": {}})
    assert restored.history == []


def test_profile_normalizes_untrusted_stat_values() -> None:
    restored = Profile.from_dict(
        {
            "name": 123,
            "stats": {
                "games_played": "2",
                "games_won": 99,
                "current_streak": -5,
                "best_streak": 999,
                "total_guesses": "oops",
                "xp": True,
                "achievements": ["first_win", 7, "x" * 100],
                "future": "ignored",
            },
            "settings": {},
        }
    )
    assert restored.name == "Player"
    assert restored.stats.games_played == 2
    assert restored.stats.games_won == 2
    assert restored.stats.current_streak == 0
    assert restored.stats.best_streak == 2
    assert restored.stats.total_guesses == 0
    assert restored.stats.xp == 0
    assert restored.stats.achievements == {"first_win"}
