import asyncio
from pathlib import Path

from textual.widgets import Input, Select

from guessnova.domain import GameMode
from guessnova.engine import GuessGame
from guessnova.storage import Storage
from guessnova.tui_challenge_app import GuessNovaApp


def test_seeded_configured_reset_replays_same_target(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            app.query_one("#challenge-mode", Select).value = "streak"
            app.query_one("#challenge-difficulty", Select).value = "expert"
            app.query_one("#challenge-seed", Input).value = "731"
            await pilot.click("#challenge-start")
            await pilot.pause()
            target = app.game.target_value

            app.query_one("#guess", Input).value = str(
                app.game.difficulty.minimum
                if app.game.difficulty.minimum != target
                else app.game.difficulty.maximum
            )
            await pilot.press("enter")
            await pilot.pause()
            assert app.game.attempts_used == 1

            await pilot.press("ctrl+r")
            await pilot.pause()

            assert app.game.mode == GameMode.STREAK
            assert app.game.seed == 731
            assert app.game.target_value == target
            assert app.game.attempts_used == 0
            assert app.focused is not None
            assert app.focused.id == "guess"

    asyncio.run(scenario())


def test_daily_configured_reset_replays_same_date_seed_and_target(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            app.query_one("#challenge-mode", Select).value = "daily"
            app.query_one("#challenge-difficulty", Select).value = "normal"
            app.query_one("#challenge-day", Input).value = "2026-08-19"
            await pilot.click("#challenge-start")
            await pilot.pause()

            original_seed = app.game.seed
            original_target = app.game.target_value

            await pilot.press("ctrl+r")
            await pilot.pause()

            assert app.challenge_configuration is not None
            assert app.challenge_configuration.day_text == "2026-08-19"
            assert app.game.mode == GameMode.DAILY
            assert app.game.seed == original_seed
            assert app.game.target_value == original_target

    asyncio.run(scenario())
