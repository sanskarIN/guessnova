import pytest

from guessnova.i18n import DEFAULT_LOCALE, available_locales, catalog_missing_keys, text


def test_english_remains_default_with_hindi_shipped() -> None:
    assert DEFAULT_LOCALE == "en"
    assert available_locales() == ("en", "hi")


def test_messages_format_named_values() -> None:
    assert text("reverse.solved", attempts=7) == "Solved in 7 guesses."
    assert text("reverse.solved", locale="hi", attempts=7) == "7 अनुमानों में हल हो गया।"


def test_tui_workspace_messages_format_in_both_locales() -> None:
    values = {
        "profile": "Nova",
        "games": 10,
        "wins": 6,
        "win_rate": 0.6,
        "xp": 250,
        "streak": 2,
        "best": 4,
        "achievements": 3,
    }
    assert "Nova" in text("tui.profile.summary", **values)
    assert "Nova" in text("tui.profile.summary", locale="hi", **values)

    backup_values = {
        "version": 2,
        "source": 1,
        "normalized": 2,
        "integrity": "sha256",
    }
    assert "sha256" in text("tui.recovery.backup_valid", **backup_values)
    assert "sha256" in text("tui.recovery.backup_valid", locale="hi", **backup_values)


def test_hindi_catalog_has_every_english_key() -> None:
    assert catalog_missing_keys("hi") == set()


def test_unknown_locale_falls_back_to_english() -> None:
    assert text("play.correct", locale="future") == "Correct! A new star is born."


def test_unknown_catalog_validation_locale_is_rejected() -> None:
    with pytest.raises(ValueError, match="unsupported locale"):
        catalog_missing_keys("future")


def test_unknown_key_is_rejected() -> None:
    with pytest.raises(KeyError):
        text("missing.key")


def test_missing_format_value_is_rejected_cleanly() -> None:
    with pytest.raises(ValueError):
        text("reverse.solved")
