import asyncio
from pathlib import Path

from textual.widgets import Static

from guessnova.domain import GameMode
from guessnova.engine import GuessGame
from guessnova.storage import Storage
from guessnova.tui_challenge_app import GuessNovaApp


def test_play_shows_initial_classic_challenge_identity(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(
            storage=Storage(tmp_path),
            game=GuessGame(
                difficulty_name="hard",
                mode=GameMode.CLASSIC,
                seed=731,
                target=42,
            ),
        )
        async with app.run_test() as pilot:
            await pilot.pause()
            rendered = str(app.query_one("#challenge-status", Static).render())
            assert "classic" in rendered
            assert "hard" in rendered
            assert "731" in rendered
            assert "42" not in rendered

    asyncio.run(scenario())


def test_play_shows_existing_daily_seed_without_target(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(
            storage=Storage(tmp_path),
            game=GuessGame(
                difficulty_name="easy",
                mode=GameMode.DAILY,
                seed=20260819,
                target=42,
            ),
        )
        async with app.run_test() as pilot:
            await pilot.pause()
            rendered = str(app.query_one("#challenge-status", Static).render())
            assert "daily" in rendered
            assert "20260819" in rendered
            assert "42" not in rendered

    asyncio.run(scenario())
