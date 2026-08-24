import asyncio
from pathlib import Path

from textual.widgets import Button, Input, Select, Static

from guessnova.domain import GameMode
from guessnova.engine import GuessGame
from guessnova.storage import Storage
from guessnova.tui_challenge_app import GuessNovaApp
from guessnova.tui_workspace import build_workspace_game


async def _activate_button(app: GuessNovaApp, pilot, selector: str) -> None:
    app.query_one(selector, Button).focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def test_challenge_app_starts_seeded_timed_round(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            app.query_one("#challenge-mode", Select).value = "timed"
            app.query_one("#challenge-difficulty", Select).value = "hard"
            app.query_one("#challenge-seed", Input).value = "20260819"

            await _activate_button(app, pilot, "#challenge-start")

            expected = build_workspace_game(
                mode="timed",
                difficulty="hard",
                seed_text="20260819",
            )
            assert app.game.mode == GameMode.TIMED
            assert app.game.difficulty_name == "hard"
            assert app.game.seed == 20260819
            assert app.game.target_value == expected.target_value
            assert app.query_one("#challenge-day", Input).value == ""
            assert "seed 20260819" in str(app.query_one("#challenge-status", Static).render())
            assert app.focused is not None
            assert app.focused.id == "guess"

    asyncio.run(scenario())


def test_challenge_app_daily_round_normalizes_date_and_ignores_seed(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            app.query_one("#challenge-mode", Select).value = "daily"
            app.query_one("#challenge-difficulty", Select).value = "easy"
            app.query_one("#challenge-seed", Input).value = "999"
            app.query_one("#challenge-day", Input).value = "2026-08-19"

            await _activate_button(app, pilot, "#challenge-start")

            assert app.game.mode == GameMode.DAILY
            assert app.game.difficulty_name == "easy"
            assert app.challenge_configuration is not None
            assert app.challenge_configuration.seed is None
            assert app.challenge_configuration.day_text == "2026-08-19"
            assert app.query_one("#challenge-seed", Input).value == ""
            assert app.query_one("#challenge-day", Input).value == "2026-08-19"

    asyncio.run(scenario())
