"""Application service coordinating game results and persisted profile data."""

from __future__ import annotations

from .achievements import apply_summary
from .domain import GameSummary
from .history import append_history, entry_from_summary as history_entry_from_summary
from .leaderboard import add_entry, entry_from_summary
from .profile import Profile
from .storage import Storage


class GameService:
    def __init__(self, storage: Storage | None = None) -> None:
        self.storage = storage or Storage()

    def record(self, summary: GameSummary, profile_name: str | None = None) -> tuple[Profile, set[str]]:
        profile = self.storage.load_profile(profile_name)
        leaderboard = self.storage.load_leaderboard()
        unlocked = apply_summary(profile.stats, summary)
        profile.history = append_history(profile.history, history_entry_from_summary(summary))
        entry = entry_from_summary(profile.name, summary)
        if entry is not None:
            leaderboard = add_entry(leaderboard, entry)
        self.storage.save_profile_and_leaderboard(profile, leaderboard)
        return profile, unlocked
