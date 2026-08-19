from guessnova.settings import Settings
from guessnova.themes import THEMES, get_theme


REQUIRED_ROLES = {"accent", "success", "warning", "error", "info", "hint"}


def test_every_theme_defines_all_semantic_roles() -> None:
    assert THEMES
    for palette in THEMES.values():
        assert set(palette) == REQUIRED_ROLES
        assert all(palette.values())


def test_unknown_theme_falls_back_to_nebula() -> None:
    assert get_theme("unknown") == THEMES["nebula"]


def test_settings_accepts_high_contrast_theme() -> None:
    settings = Settings.from_dict({"theme": "high-contrast", "high_contrast": True})
    assert settings.theme == "high-contrast"
    assert settings.high_contrast is True
