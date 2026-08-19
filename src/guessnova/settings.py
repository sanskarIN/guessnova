"""User-facing settings with defensive deserialization."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .themes import THEMES


@dataclass(slots=True)
class Settings:
    theme: str = "nebula"
    reduced_motion: bool = False
    high_contrast: bool = False
    sound: bool = False
    show_smart_hints: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Settings":
        defaults = cls()
        theme = data.get("theme", defaults.theme)
        if not isinstance(theme, str) or theme not in THEMES:
            theme = defaults.theme

        def boolean(name: str, default: bool) -> bool:
            value = data.get(name, default)
            return value if isinstance(value, bool) else default

        return cls(
            theme=theme,
            reduced_motion=boolean("reduced_motion", defaults.reduced_motion),
            high_contrast=boolean("high_contrast", defaults.high_contrast),
            sound=boolean("sound", defaults.sound),
            show_smart_hints=boolean("show_smart_hints", defaults.show_smart_hints),
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
