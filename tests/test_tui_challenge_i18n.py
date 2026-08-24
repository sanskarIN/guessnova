from guessnova.i18n import catalog_missing_keys, text


def test_challenge_workspace_messages_format_in_both_locales() -> None:
    for locale in ("en", "hi"):
        active = text(
            "tui.challenge.active",
            locale=locale,
            mode="daily",
            difficulty="hard",
            detail=text(
                "tui.challenge.day_detail",
                locale=locale,
                day="2026-08-19",
            ),
        )
        invalid = text(
            "tui.challenge.invalid",
            locale=locale,
            error="seed must be a whole number",
        )

        assert "daily" in active
        assert "hard" in active
        assert "2026-08-19" in active
        assert "seed must be a whole number" in invalid


def test_hindi_challenge_catalog_stays_complete() -> None:
    assert catalog_missing_keys("hi") == set()
