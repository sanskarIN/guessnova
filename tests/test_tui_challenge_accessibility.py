import asyncio
from pathlib import Path

from textual.widgets import Input

from guessnova.engine import GuessGame
from guessnova.storage import Storage
from guessnova.tui_challenge_app import GuessNovaApp


def test_challenge_workspace_preserves_guess_first_keyboard_flow(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            assert app.focused is not None
            assert app.focused.id == "guess"

            await pilot.press("tab")
            assert app.focused is not None
            assert app.focused.id == "submit"

            await pilot.press("tab")
            assert app.focused is not None
            assert app.focused.id == "hint"

    asyncio.run(scenario())


def test_challenge_fields_receive_plain_q_and_r_without_global_actions(tmp_path: Path) -> None:
    async def scenario() -> None:
        game = GuessGame(seed=731)
        target = game.target_value
        app = GuessNovaApp(storage=Storage(tmp_path), game=game)
        async with app.run_test() as pilot:
            seed = app.query_one("#challenge-seed", Input)
            seed.value = ""
            seed.focus()
            await pilot.press("q", "r")
            await pilot.pause()

            assert seed.value == "qr"
            assert app.is_running is True
            assert app.game.target_value == target
            assert app.game.attempts_used == 0

    asyncio.run(scenario())


def test_challenge_setup_is_reachable_backward_from_guess(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            assert app.focused is not None
            assert app.focused.id == "guess"

            await pilot.press("shift+tab")
            await pilot.pause()

            assert app.focused is not None
            assert app.focused.id == "challenge-start"

    asyncio.run(scenario())
