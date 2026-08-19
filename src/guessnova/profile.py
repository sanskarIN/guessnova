"""Player profile model and defensive serialization."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .domain import PlayerStats
from .history import HistoryEntry, deserialize as deserialize_history, serialize as serialize_history
from .security import sanitize_profile_name
from .settings import Settings


def _nonnegative_int(data: dict[str, object], key: str) -> int:
    value = data.get(key, 0)
    if isinstance(value, bool):
        return 0
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, parsed)


@dataclass(slots=True)
class Profile:
    name: str = "Player"
    stats: PlayerStats = field(default_factory=PlayerStats)
    settings: Settings = field(default_factory=Settings)
    history: list[HistoryEntry] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.name = sanitize_profile_name(self.name)

    def to_dict(self) -> dict[str, object]:
        stats = asdict(self.stats)
        stats["achievements"] = sorted(self.stats.achievements)
        return {
            "name": self.name,
            "stats": stats,
            "settings": self.settings.to_dict(),
            "history": serialize_history(self.history),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Profile":
        raw_stats = data.get("stats", {})
        stats_data = raw_stats if isinstance(raw_stats, dict) else {}
        raw_achievements = stats_data.get("achievements", [])
        achievements = {
            item
            for item in raw_achievements
            if isinstance(item, str) and 0 < len(item) <= 64
        } if isinstance(raw_achievements, list) else set()
        stats = PlayerStats(
            games_played=_nonnegative_int(stats_data, "games_played"),
            games_won=_nonnegative_int(stats_data, "games_won"),
            current_streak=_nonnegative_int(stats_data, "current_streak"),
            best_streak=_nonnegative_int(stats_data, "best_streak"),
            total_guesses=_nonnegative_int(stats_data, "total_guesses"),
            xp=_nonnegative_int(stats_data, "xp"),
            achievements=achievements,
        )
        stats.games_won = min(stats.games_won, stats.games_played)
        stats.current_streak = min(stats.current_streak, stats.games_won)
        stats.best_streak = max(stats.current_streak, min(stats.best_streak, stats.games_won))
        settings_data = data.get("settings", {})
        settings = Settings.from_dict(settings_data if isinstance(settings_data, dict) else {})
        raw_name = data.get("name", "Player")
        name = raw_name if isinstance(raw_name, str) else "Player"
        return cls(
            name=name,
            stats=stats,
            settings=settings,
            history=deserialize_history(data.get("history", [])),
        )
