"""Application service coordinating game results and persisted profile data."""

from __future__ import annotations

from .achievements import apply_summary
from .domain import GameSummary
from .history import append_history, entry_from_summary as history_entry_from_summary
from .leaderboard import entry_from_summary
from .profile import Profile
from .storage import Storage
from .summary_validation import validate_game_summary


class GameService:
    def __init__(self, storage: Storage | None = None) -> None:
        self.storage = storage or Storage()

    def record(
        self, summary: GameSummary, profile_name: str | None = None
    ) -> tuple[Profile, set[str]]:
        validate_game_summary(summary)
        profile = self.storage.load_profile(profile_name)
        unlocked = apply_summary(profile.stats, summary)
        profile.history = append_history(profile.history, history_entry_from_summary(summary))
        leaderboard_entry = entry_from_summary(profile.name, summary)
        self.storage.save_completed_round(profile, leaderboard_entry)
        return profile, unlocked
