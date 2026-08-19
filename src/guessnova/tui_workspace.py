"""Reusable local workspace helpers for the Textual interface.

The helpers in this module deliberately avoid Textual dependencies so profile,
history, settings, leaderboard, challenge configuration, and diagnostic state
can be exercised with ordinary unit tests as well as through the interactive TUI.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .daily import daily_game
from .diagnostics import DiagnosticReport, diagnose
from .domain import DIFFICULTIES, GameMode
from .engine import GuessGame
from .history import HistoryEntry, HistoryResult, filter_history
from .leaderboard import LeaderboardEntry
from .profile import Profile
from .settings import Settings
from .storage import Storage


@dataclass(frozen=True, slots=True)
class WorkspaceSnapshot:
    """Current local workspace state needed by non-gameplay TUI panes."""

    profile: Profile
    profile_names: tuple[str, ...]
    deleted_profile_names: tuple[str, ...]
    leaderboard_count: int
    diagnostics: DiagnosticReport


@dataclass(frozen=True, slots=True)
class ProfileSummary:
    """Small immutable statistics view for the active profile."""

    games_played: int
    games_won: int
    win_rate: float
    average_guesses: float
    current_streak: int
    best_streak: int
    xp: int
    achievement_count: int
    history_count: int


def build_workspace_game(
    *,
    mode: str,
    difficulty: str,
    seed_text: str = "",
    day_text: str = "",
) -> GuessGame:
    """Build one configured non-reverse challenge from TUI-friendly strings."""
    try:
        selected_mode = GameMode(mode)
    except ValueError as exc:
        raise ValueError(f"unknown game mode: {mode}") from exc
    if selected_mode == GameMode.REVERSE:
        raise ValueError("reverse mode uses its dedicated reverse interface")
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"unknown difficulty: {difficulty}")

    if selected_mode == GameMode.DAILY:
        try:
            selected_day = date.fromisoformat(day_text.strip()) if day_text.strip() else None
        except ValueError as exc:
            raise ValueError("daily challenge date must use YYYY-MM-DD") from exc
        return daily_game(selected_day, difficulty=difficulty)

    cleaned_seed = seed_text.strip()
    if cleaned_seed:
        try:
            seed = int(cleaned_seed)
        except ValueError as exc:
            raise ValueError("seed must be a whole number") from exc
    else:
        seed = None
    return GuessGame(difficulty_name=difficulty, mode=selected_mode, seed=seed)


def load_workspace_snapshot(
    storage: Storage, profile_name: str | None = None
) -> WorkspaceSnapshot:
    """Load a read-only snapshot through the normal persistence boundaries."""
    profile = storage.load_profile(profile_name)
    return WorkspaceSnapshot(
        profile=profile,
        profile_names=tuple(storage.list_profile_names()),
        deleted_profile_names=tuple(storage.list_deleted_profile_names()),
        leaderboard_count=len(storage.load_leaderboard()),
        diagnostics=diagnose(storage),
    )


def profile_summary(profile: Profile) -> ProfileSummary:
    stats = profile.stats
    return ProfileSummary(
        games_played=stats.games_played,
        games_won=stats.games_won,
        win_rate=stats.win_rate,
        average_guesses=stats.average_guesses,
        current_streak=stats.current_streak,
        best_streak=stats.best_streak,
        xp=stats.xp,
        achievement_count=len(stats.achievements),
        history_count=len(profile.history),
    )


def select_history(
    profile: Profile,
    *,
    mode: str | None = None,
    difficulty: str | None = None,
    result: HistoryResult | None = None,
    query: str | None = None,
    since: date | None = None,
    until: date | None = None,
    limit: int = 100,
) -> list[HistoryEntry]:
    """Return newest-first filtered history for workspace presentation."""
    if limit < 1:
        raise ValueError("history limit must be positive")
    filtered = filter_history(
        profile.history,
        mode=mode,
        difficulty=difficulty,
        result=result,
        query=query,
        since=since,
        until=until,
    )
    return list(reversed(filtered[-limit:]))


def select_leaderboard(
    entries: list[LeaderboardEntry],
    *,
    mode: str | None = None,
    difficulty: str | None = None,
    player: str | None = None,
    limit: int = 100,
) -> list[LeaderboardEntry]:
    """Return the already-ranked leaderboard after optional local filters."""
    if limit < 1:
        raise ValueError("leaderboard limit must be positive")
    player_filter = player.casefold().strip() if player else ""
    selected = [
        entry
        for entry in entries
        if (mode is None or entry.mode == mode)
        and (difficulty is None or entry.difficulty == difficulty)
        and (not player_filter or player_filter in entry.player.casefold())
    ]
    return selected[:limit]


def save_workspace_settings(
    storage: Storage,
    profile_name: str,
    *,
    theme: str,
    locale: str,
    reduced_motion: bool,
    high_contrast: bool,
    sound: bool,
    show_smart_hints: bool,
) -> Profile:
    """Persist validated settings for one profile while retaining onboarding state."""
    profile = storage.load_profile(profile_name)
    profile.settings = Settings.from_dict(
        {
            "theme": theme,
            "locale": locale,
            "reduced_motion": reduced_motion,
            "high_contrast": high_contrast,
            "sound": sound,
            "show_smart_hints": show_smart_hints,
            "onboarding_complete": profile.settings.onboarding_complete,
        }
    )
    storage.save_profile(profile)
    return profile
