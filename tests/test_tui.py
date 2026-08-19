import asyncio
from pathlib import Path

from textual.widgets import Input

from guessnova.engine import GuessGame
from guessnova.storage import Storage
from guessnova.tui import GuessNovaApp


def test_tui_focus_order_is_keyboard_predictable(tmp_path: Path) -> None:
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


def test_tui_input_submission_persists_winning_result(tmp_path: Path) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path)
        app = GuessNovaApp(
            profile_name="Tester",
            storage=storage,
            game=GuessGame(target=42),
        )
        async with app.run_test() as pilot:
            field = app.query_one("#guess", Input)
            field.value = "42"
            await pilot.press("enter")
            await pilot.pause()
            assert app.game.won is True
            assert app.game.is_finished is True
            assert storage.load_profile("Tester").stats.games_played == 1
            assert storage.load_profile("Tester").stats.games_won == 1

    asyncio.run(scenario())


def test_tui_hint_button_does_not_consume_attempt_and_returns_focus(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            before = app.game.attempts_left
            await pilot.click("#hint")
            await pilot.pause()
            assert app.game.hints_used == 1
            assert app.game.attempts_left == before
            assert app.focused is not None
            assert app.focused.id == "guess"

    asyncio.run(scenario())


def test_tui_reset_clears_round_and_refocuses_input(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = GuessNovaApp(storage=Storage(tmp_path), game=GuessGame(target=42))
        async with app.run_test() as pilot:
            app.query_one("#guess", Input).value = "10"
            await pilot.press("enter")
            assert app.game.attempts_used == 1
            await pilot.press("r")
            await pilot.pause()
            assert app.game.attempts_used == 0
            assert app.game.is_finished is False
            assert app.focused is not None
            assert app.focused.id == "guess"

    asyncio.run(scenario())
