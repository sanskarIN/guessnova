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


@dataclass(frozen=True, slots=True)
class ChallengeConfiguration:
    """Validated, presentation-friendly configuration for one numeric challenge."""

    mode: GameMode
    difficulty: str
    seed: int | None = None
    day: date | None = None

    def __post_init__(self) -> None:
        try:
            selected_mode = GameMode(self.mode)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"unknown game mode: {self.mode}") from exc
        object.__setattr__(self, "mode", selected_mode)

        if selected_mode == GameMode.REVERSE:
            raise ValueError("reverse mode uses its dedicated reverse interface")
        if not isinstance(self.difficulty, str) or self.difficulty not in DIFFICULTIES:
            raise ValueError(f"unknown difficulty: {self.difficulty}")
        if self.seed is not None and (
            not isinstance(self.seed, int) or isinstance(self.seed, bool)
        ):
            raise ValueError("seed must be a whole number")
        if self.day is not None and not isinstance(self.day, date):
            raise ValueError("challenge day must be a date")
        if selected_mode == GameMode.DAILY and self.day is None:
            raise ValueError("daily challenge requires a resolved date")
        if selected_mode != GameMode.DAILY and self.day is not None:
            raise ValueError("only daily challenges can carry a challenge date")
        if selected_mode == GameMode.DAILY and self.seed is not None:
            raise ValueError("daily challenges derive their seed from the challenge date")

    @property
    def mode_value(self) -> str:
        return self.mode.value

    @property
    def seed_text(self) -> str:
        return "" if self.seed is None else str(self.seed)

    @property
    def day_text(self) -> str:
        return "" if self.day is None else self.day.isoformat()

    def build_game(self) -> GuessGame:
        """Build a fresh game that exactly matches this validated configuration."""
        if self.mode == GameMode.DAILY:
            if self.day is None:  # pragma: no cover - guarded by __post_init__
                raise RuntimeError("daily challenge date is unavailable")
            return daily_game(self.day, difficulty=self.difficulty)
        return GuessGame(
            difficulty_name=self.difficulty,
            mode=self.mode,
            seed=self.seed,
        )


def parse_workspace_challenge(
    *,
    mode: str,
    difficulty: str,
    seed_text: str = "",
    day_text: str = "",
    today: date | None = None,
) -> ChallengeConfiguration:
    """Validate TUI-friendly challenge fields without constructing widget state."""
    try:
        selected_mode = GameMode(mode)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"unknown game mode: {mode}") from exc
    if selected_mode == GameMode.REVERSE:
        raise ValueError("reverse mode uses its dedicated reverse interface")
    if not isinstance(difficulty, str) or difficulty not in DIFFICULTIES:
        raise ValueError(f"unknown difficulty: {difficulty}")

    if selected_mode == GameMode.DAILY:
        cleaned_day = day_text.strip()
        try:
            selected_day = date.fromisoformat(cleaned_day) if cleaned_day else (today or date.today())
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError("daily challenge date must use YYYY-MM-DD") from exc
        return ChallengeConfiguration(
            mode=selected_mode,
            difficulty=difficulty,
            day=selected_day,
        )

    try:
        cleaned_seed = seed_text.strip()
    except AttributeError as exc:
        raise ValueError("seed must be a whole number") from exc
    if cleaned_seed:
        try:
            seed = int(cleaned_seed)
        except ValueError as exc:
            raise ValueError("seed must be a whole number") from exc
    else:
        seed = None
    return ChallengeConfiguration(
        mode=selected_mode,
        difficulty=difficulty,
        seed=seed,
    )


def build_workspace_game(
    *,
    mode: str,
    difficulty: str,
    seed_text: str = "",
    day_text: str = "",
) -> GuessGame:
    """Build one configured non-reverse challenge from TUI-friendly strings."""
    return parse_workspace_challenge(
        mode=mode,
        difficulty=difficulty,
        seed_text=seed_text,
        day_text=day_text,
    ).build_game()


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
