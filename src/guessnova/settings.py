"""User-facing settings with defensive deserialization."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .i18n import DEFAULT_LOCALE, available_locales
from .themes import THEMES


@dataclass(slots=True)
class Settings:
    theme: str = "nebula"
    locale: str = DEFAULT_LOCALE
    reduced_motion: bool = False
    high_contrast: bool = False
    sound: bool = False
    show_smart_hints: bool = True
    onboarding_complete: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Settings":
        defaults = cls()
        theme = data.get("theme", defaults.theme)
        if not isinstance(theme, str) or theme not in THEMES:
            theme = defaults.theme
        locale = data.get("locale", defaults.locale)
        if not isinstance(locale, str) or locale not in available_locales():
            locale = defaults.locale

        def boolean(name: str, default: bool) -> bool:
            value = data.get(name, default)
            return value if isinstance(value, bool) else default

        return cls(
            theme=theme,
            locale=locale,
            reduced_motion=boolean("reduced_motion", defaults.reduced_motion),
            high_contrast=boolean("high_contrast", defaults.high_contrast),
            sound=boolean("sound", defaults.sound),
            show_smart_hints=boolean("show_smart_hints", defaults.show_smart_hints),
            onboarding_complete=boolean("onboarding_complete", defaults.onboarding_complete),
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
