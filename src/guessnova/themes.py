"""Semantic theme definitions used by terminal interfaces."""

from __future__ import annotations

THEMES: dict[str, dict[str, str]] = {
    "nebula": {
        "accent": "bright_magenta",
        "success": "bright_green",
        "warning": "yellow",
        "error": "bright_red",
        "info": "bright_cyan",
        "hint": "bright_black",
    },
    "aurora": {
        "accent": "bright_cyan",
        "success": "green",
        "warning": "bright_yellow",
        "error": "bright_red",
        "info": "cyan",
        "hint": "white",
    },
    "mono": {
        "accent": "white",
        "success": "white",
        "warning": "white",
        "error": "white",
        "info": "white",
        "hint": "bright_black",
    },
    "high-contrast": {
        "accent": "bright_white",
        "success": "bright_white",
        "warning": "bright_yellow",
        "error": "bright_red",
        "info": "bright_cyan",
        "hint": "white",
    },
}


def get_theme(name: str) -> dict[str, str]:
    return THEMES.get(name, THEMES["nebula"])
