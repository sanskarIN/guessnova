from guessnova.settings import Settings


def test_settings_round_trip() -> None:
    settings = Settings(
        theme="mono",
        locale="hi",
        reduced_motion=True,
        onboarding_complete=True,
    )
    assert Settings.from_dict(settings.to_dict()) == settings


def test_unknown_settings_are_ignored() -> None:
    settings = Settings.from_dict({"theme": "nebula", "future_key": True})
    assert settings.theme == "nebula"


def test_invalid_setting_types_fall_back_to_safe_defaults() -> None:
    settings = Settings.from_dict(
        {
            "theme": "not-a-theme",
            "locale": "zz",
            "reduced_motion": "yes",
            "high_contrast": 1,
            "sound": None,
            "show_smart_hints": [],
            "onboarding_complete": "done",
        }
    )
    assert settings == Settings()


def test_supported_locales_are_preserved() -> None:
    assert Settings.from_dict({"locale": "en"}).locale == "en"
    assert Settings.from_dict({"locale": "hi"}).locale == "hi"
