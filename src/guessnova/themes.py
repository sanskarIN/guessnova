"""Theme definitions used by terminal interfaces."""

THEMES = {
    "nebula": {"accent": "bright_magenta", "good": "bright_green", "warn": "yellow"},
    "aurora": {"accent": "bright_cyan", "good": "green", "warn": "bright_yellow"},
    "mono": {"accent": "white", "good": "white", "warn": "white"},
    "high-contrast": {"accent": "bright_white", "good": "bright_white", "warn": "bright_white"},
}


def get_theme(name: str) -> dict[str, str]:
    return THEMES.get(name, THEMES["nebula"])
