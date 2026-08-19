import asyncio
from pathlib import Path

from textual.widgets import Input, Select, Switch

from guessnova.engine import GuessGame
from guessnova.profile import Profile
from guessnova.storage import Storage
from guessnova.tui import GuessNovaApp


def test_switching_profile_resets_unfinished_round_without_leaving_profiles_tab(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path)
        storage.save_profile(Profile("Alpha"))
        storage.create_profile("Beta", make_active=False)
        app = GuessNovaApp(profile_name="Alpha", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            app.query_one("#guess", Input).value = "10"
            await pilot.press("enter")
            await pilot.pause()
            assert app.game.attempts_used == 1

            await pilot.press("ctrl+2")
            await pilot.pause()
            app.query_one("#profile-select", Select).value = "Beta"
            await pilot.click("#profile-use")
            await pilot.pause()

            assert storage.active_profile_name() == "Beta"
            assert app.profile_name == "Beta"
            assert app.game.attempts_used == 0
            assert app.query_one("#workspace").active == "profiles"

    asyncio.run(scenario())


def test_profile_switch_keeps_launch_locale_until_restart(tmp_path: Path) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path)
        alpha = Profile("Alpha")
        alpha.settings.locale = "en"
        storage.save_profile(alpha)
        beta = Profile("Beta")
        beta.settings.locale = "hi"
        storage.save_profile(beta, make_active=False)

        app = GuessNovaApp(profile_name="Alpha", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            assert app.locale == "en"
            await pilot.press("ctrl+2")
            await pilot.pause()
            app.query_one("#profile-select", Select).value = "Beta"
            await pilot.click("#profile-use")
            await pilot.pause()

            assert app.locale == "en"
            assert app.query_one("#settings-locale", Select).value == "hi"

    asyncio.run(scenario())


def test_high_contrast_applies_on_launch_and_after_settings_save(tmp_path: Path) -> None:
    async def launch_enabled() -> None:
        storage = Storage(tmp_path / "enabled")
        profile = Profile("Nova")
        profile.settings.high_contrast = True
        storage.save_profile(profile)
        app = GuessNovaApp(profile_name="Nova", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            await pilot.pause()
            assert app.screen.has_class("high-contrast") is True

    async def save_enabled() -> None:
        storage = Storage(tmp_path / "saved")
        storage.save_profile(Profile("Nova"))
        app = GuessNovaApp(profile_name="Nova", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            assert app.screen.has_class("high-contrast") is False
            await pilot.press("ctrl+5")
            await pilot.pause()
            app.query_one("#settings-high-contrast", Switch).value = True
            await pilot.click("#settings-save")
            await pilot.pause()
            assert app.screen.has_class("high-contrast") is True
            assert storage.load_profile("Nova").settings.high_contrast is True

    asyncio.run(launch_enabled())
    asyncio.run(save_enabled())
