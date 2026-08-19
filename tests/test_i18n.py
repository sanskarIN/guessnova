import pytest

from guessnova.i18n import DEFAULT_LOCALE, available_locales, text


def test_english_is_the_default_shipped_locale() -> None:
    assert DEFAULT_LOCALE == "en"
    assert available_locales() == ("en",)


def test_messages_format_named_values() -> None:
    assert text("reverse.solved", attempts=7) == "Solved in 7 guesses."


def test_unknown_locale_falls_back_to_english() -> None:
    assert text("play.correct", locale="future") == "Correct! A new star is born."


def test_unknown_key_is_rejected() -> None:
    with pytest.raises(KeyError):
        text("missing.key")


def test_missing_format_value_is_rejected_cleanly() -> None:
    with pytest.raises(ValueError):
        text("reverse.solved")
