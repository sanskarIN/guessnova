import asyncio
from datetime import UTC, datetime
from pathlib import Path

from textual.widgets import DataTable, Input, Select, Static, Switch

from guessnova.constants import SCHEMA_VERSION
from guessnova.engine import GuessGame
from guessnova.history import HistoryEntry
from guessnova.import_export import export_state
from guessnova.profile import Profile
from guessnova.storage import Storage
from guessnova.tui import GuessNovaApp


def test_workspace_history_filters_use_active_profile_history(tmp_path: Path) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path)
        profile = Profile("Nova")
        profile.history = [
            HistoryEntry(
                mode="classic",
                difficulty="easy",
                won=True,
                attempts=3,
                elapsed_seconds=4.0,
                seed=1,
                played_at=datetime(2026, 8, 17, tzinfo=UTC).isoformat(),
            ),
            HistoryEntry(
                mode="timed",
                difficulty="hard",
                won=False,
                attempts=10,
                elapsed_seconds=40.0,
                seed=2,
                played_at=datetime(2026, 8, 18, tzinfo=UTC).isoformat(),
            ),
            HistoryEntry(
                mode="classic",
                difficulty="hard",
                won=True,
                attempts=5,
                elapsed_seconds=9.0,
                seed=3,
                played_at=datetime(2026, 8, 19, tzinfo=UTC).isoformat(),
            ),
        ]
        storage.save_profile(profile)
        app = GuessNovaApp(profile_name="Nova", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            await pilot.press("ctrl+3")
            await pilot.pause()
            table = app.query_one("#history-table", DataTable)
            assert table.row_count == 3

            app.query_one("#history-result", Select).value = "win"
            app.query_one("#history-difficulty", Select).value = "hard"
            await pilot.click("#history-apply")
            await pilot.pause()
            assert table.row_count == 1

            app.query_one("#history-since", Input).value = "not-a-date"
            await pilot.click("#history-apply")
            await pilot.pause()
            assert table.row_count == 1

            await pilot.click("#history-clear")
            await pilot.pause()
            assert table.row_count == 3

    asyncio.run(scenario())


def test_workspace_settings_persist_without_restarting_app(tmp_path: Path) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path)
        storage.save_profile(Profile("Nova"))
        app = GuessNovaApp(profile_name="Nova", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            await pilot.press("ctrl+4")
            await pilot.pause()
            app.query_one("#settings-theme", Select).value = "mono"
            app.query_one("#settings-locale", Select).value = "hi"
            app.query_one("#settings-reduced-motion", Switch).value = True
            app.query_one("#settings-high-contrast", Switch).value = True
            app.query_one("#settings-sound", Switch).value = True
            app.query_one("#settings-smart-hints", Switch).value = False
            await pilot.click("#settings-save")
            await pilot.pause()

            saved = storage.load_profile("Nova").settings
            assert saved.theme == "mono"
            assert saved.locale == "hi"
            assert saved.reduced_motion is True
            assert saved.high_contrast is True
            assert saved.sound is True
            assert saved.show_smart_hints is False
            assert app.show_smart_hints is False

    asyncio.run(scenario())


def test_workspace_recovery_verifies_backup_without_importing(tmp_path: Path) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path / "data")
        storage.save_profile(Profile("Nova"))
        backup = export_state(storage.load_raw(), tmp_path / "backup.json")
        before = storage.load_raw()

        app = GuessNovaApp(profile_name="Nova", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            await pilot.press("ctrl+5")
            await pilot.pause()
            app.query_one("#recovery-backup-path", Input).value = str(backup)
            await pilot.click("#recovery-verify")
            await pilot.pause()

            assert storage.load_raw() == before
            assert storage.load_raw()["schema_version"] == SCHEMA_VERSION
            rendered = str(app.query_one("#recovery-backup-status", Static).render())
            assert "wrapper 2" in rendered

    asyncio.run(scenario())
