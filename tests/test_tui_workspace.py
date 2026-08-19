from datetime import UTC, datetime
from pathlib import Path

from guessnova.history import HistoryEntry
from guessnova.profile import Profile
from guessnova.storage import Storage
from guessnova.tui_workspace import (
    load_workspace_snapshot,
    profile_summary,
    save_workspace_settings,
    select_history,
)


def test_workspace_snapshot_uses_local_profile_trash_leaderboard_and_diagnostics(
    tmp_path: Path,
) -> None:
    storage = Storage(tmp_path)
    alpha = Profile("Alpha")
    alpha.stats.games_played = 2
    alpha.stats.games_won = 1
    storage.save_profile(alpha)
    storage.create_profile("Beta", make_active=False)
    storage.delete_profile("Beta")

    snapshot = load_workspace_snapshot(storage, "Alpha")

    assert snapshot.profile.name == "Alpha"
    assert snapshot.profile_names == ("Alpha",)
    assert snapshot.deleted_profile_names == ("Beta",)
    assert snapshot.leaderboard_count == 0
    assert snapshot.diagnostics.healthy is True


def test_profile_summary_derives_stats_without_mutating_profile() -> None:
    profile = Profile("Nova")
    profile.stats.games_played = 4
    profile.stats.games_won = 2
    profile.stats.total_guesses = 8
    profile.stats.current_streak = 1
    profile.stats.best_streak = 2
    profile.stats.xp = 120
    profile.stats.achievements = {"first_win", "streak_5"}

    summary = profile_summary(profile)

    assert summary.games_played == 4
    assert summary.games_won == 2
    assert summary.win_rate == 0.5
    assert summary.average_guesses == 4.0
    assert summary.current_streak == 1
    assert summary.best_streak == 2
    assert summary.xp == 120
    assert summary.achievement_count == 2
    assert summary.history_count == 0


def test_select_history_filters_and_returns_newest_first() -> None:
    profile = Profile("Nova")
    profile.history = [
        HistoryEntry(
            mode="classic",
            difficulty="easy",
            won=True,
            attempts=3,
            elapsed_seconds=5.0,
            seed=1,
            played_at=datetime(2026, 8, 17, tzinfo=UTC).isoformat(),
        ),
        HistoryEntry(
            mode="timed",
            difficulty="hard",
            won=False,
            attempts=10,
            elapsed_seconds=40.0,
            seed=2,
            played_at=datetime(2026, 8, 18, tzinfo=UTC).isoformat(),
        ),
        HistoryEntry(
            mode="classic",
            difficulty="hard",
            won=True,
            attempts=5,
            elapsed_seconds=9.0,
            seed=3,
            played_at=datetime(2026, 8, 19, tzinfo=UTC).isoformat(),
        ),
    ]

    selected = select_history(profile, mode="classic", difficulty="hard", result="win")

    assert [entry.seed for entry in selected] == [3]
    assert select_history(profile, result="win", limit=1)[0].seed == 3


def test_save_workspace_settings_preserves_onboarding_state(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    profile = Profile("Nova")
    profile.settings.onboarding_complete = True
    storage.save_profile(profile)

    updated = save_workspace_settings(
        storage,
        "Nova",
        theme="mono",
        locale="hi",
        reduced_motion=True,
        high_contrast=True,
        sound=True,
        show_smart_hints=False,
    )

    assert updated.settings.theme == "mono"
    assert updated.settings.locale == "hi"
    assert updated.settings.reduced_motion is True
    assert updated.settings.high_contrast is True
    assert updated.settings.sound is True
    assert updated.settings.show_smart_hints is False
    assert updated.settings.onboarding_complete is True
    assert storage.load_profile("Nova").settings.to_dict() == updated.settings.to_dict()
