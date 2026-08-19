"""Presentation helpers for configured Textual challenges."""

from __future__ import annotations

from .domain import GameMode
from .i18n import text
from .tui_workspace import ChallengeConfiguration


def challenge_detail(configuration: ChallengeConfiguration, *, locale: str) -> str:
    """Return a localized, target-free challenge identity detail."""
    if configuration.mode == GameMode.DAILY:
        return text(
            "tui.challenge.day_detail",
            locale=locale,
            day=configuration.day_text,
        )
    if configuration.seed is not None:
        return text(
            "tui.challenge.seed_detail",
            locale=locale,
            seed=configuration.seed,
        )
    return text("tui.challenge.random_detail", locale=locale)


def challenge_status(configuration: ChallengeConfiguration, *, locale: str) -> str:
    """Return a localized status line without exposing the hidden target."""
    return text(
        "tui.challenge.active",
        locale=locale,
        mode=configuration.mode_value,
        difficulty=configuration.difficulty,
        detail=challenge_detail(configuration, locale=locale),
    )
