import asyncio
from pathlib import Path

from textual.widgets import Button, Input, Select, Static

from guessnova.engine import GuessGame
from guessnova.storage import Storage
from guessnova.tui_challenge_app import GuessNovaApp


async def _activate_button(app: GuessNovaApp, pilot, selector: str) -> None:
    app.query_one(selector, Button).focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def test_invalid_seed_preserves_active_round_and_attempts(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            guess = app.query_one("#guess", Input)
            guess.value = "10"
            await pilot.press("enter")
            await pilot.pause()

            active_game = app.game
            assert active_game.attempts_used == 1

            app.query_one("#challenge-mode", Select).value = "classic"
            app.query_one("#challenge-seed", Input).value = "nova"
            await _activate_button(app, pilot, "#challenge-start")

            assert app.game is active_game
            assert app.game.attempts_used == 1
            assert app.game.target_value == 42
            assert app.challenge_configuration is None
            assert "whole number" in str(app.query_one("#challenge-status", Static).render())
            assert app.focused is not None
            assert app.focused.id == "challenge-seed"

    asyncio.run(scenario())


def test_invalid_daily_date_preserves_active_round(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            active_game = app.game
            app.query_one("#challenge-mode", Select).value = "daily"
            app.query_one("#challenge-day", Input).value = "19-08-2026"

            await _activate_button(app, pilot, "#challenge-start")

            assert app.game is active_game
            assert app.game.target_value == 42
            assert app.challenge_configuration is None
            assert "YYYY-MM-DD" in str(app.query_one("#challenge-status", Static).render())
            assert app.focused is not None
            assert app.focused.id == "challenge-day"

    asyncio.run(scenario())
