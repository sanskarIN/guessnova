import asyncio
from pathlib import Path

from textual.widgets import Input, Select, TabbedContent

from guessnova.engine import GuessGame
from guessnova.profile import Profile
from guessnova.storage import Storage
from guessnova.tui import GuessNovaApp


def test_workspace_shortcuts_switch_tabs_and_text_fields_keep_letters(tmp_path: Path) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path)
        storage.save_profile(Profile("Nova"))
        app = GuessNovaApp(storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            await pilot.press("ctrl+2")
            await pilot.pause()
            assert app.query_one("#workspace", TabbedContent).active == "profiles"

            field = app.query_one("#profile-name", Input)
            field.focus()
            await pilot.press("q", "r")
            assert field.value == "qr"
            assert app.is_running is True

            await pilot.press("ctrl+1")
            await pilot.pause()
            assert app.query_one("#workspace", TabbedContent).active == "play"

    asyncio.run(scenario())


def test_workspace_profile_create_rename_delete_and_restore(tmp_path: Path) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path)
        storage.save_profile(Profile("Alpha"))
        app = GuessNovaApp(profile_name="Alpha", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            await pilot.press("ctrl+2")
            await pilot.pause()

            name = app.query_one("#profile-name", Input)
            name.value = "Beta"
            await pilot.click("#profile-create")
            await pilot.pause()
            assert storage.active_profile_name() == "Beta"
            assert storage.list_profile_names() == ["Alpha", "Beta"]

            select = app.query_one("#profile-select", Select)
            select.value = "Beta"
            name.value = "Gamma"
            await pilot.click("#profile-rename")
            await pilot.pause()
            assert storage.active_profile_name() == "Gamma"
            assert storage.list_profile_names() == ["Alpha", "Gamma"]

            select.value = "Gamma"
            name.value = "wrong"
            await pilot.click("#profile-delete")
            await pilot.pause()
            assert "Gamma" in storage.list_profile_names()

            name.value = "Gamma"
            await pilot.click("#profile-delete")
            await pilot.pause()
            assert storage.list_profile_names() == ["Alpha"]
            assert storage.list_deleted_profile_names() == ["Gamma"]

            trash = app.query_one("#trash-select", Select)
            trash.value = "Gamma"
            await pilot.click("#profile-restore")
            await pilot.pause()
            assert storage.active_profile_name() == "Gamma"
            assert storage.list_profile_names() == ["Alpha", "Gamma"]
            assert storage.list_deleted_profile_names() == []

    asyncio.run(scenario())
