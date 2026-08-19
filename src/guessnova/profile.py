"""Player profile model and serialization."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .domain import PlayerStats
from .security import sanitize_profile_name
from .settings import Settings


@dataclass(slots=True)
class Profile:
    name: str = "Player"
    stats: PlayerStats = field(default_factory=PlayerStats)
    settings: Settings = field(default_factory=Settings)

    def __post_init__(self) -> None:
        self.name = sanitize_profile_name(self.name)

    def to_dict(self) -> dict[str, object]:
        stats = asdict(self.stats)
        stats["achievements"] = sorted(self.stats.achievements)
        return {
            "name": self.name,
            "stats": stats,
            "settings": self.settings.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Profile":
        stats_data = dict(data.get("stats", {})) if isinstance(data.get("stats", {}), dict) else {}
        achievements = stats_data.get("achievements", [])
        stats_data["achievements"] = set(achievements if isinstance(achievements, list) else [])
        stats = PlayerStats(**stats_data)
        settings_data = data.get("settings", {})
        settings = Settings.from_dict(settings_data if isinstance(settings_data, dict) else {})
        return cls(name=str(data.get("name", "Player")), stats=stats, settings=settings)
