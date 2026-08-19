import asyncio

from textual.app import App, ComposeResult
from textual.widgets import Input, Select

from guessnova.domain import GameMode
from guessnova.tui_challenge_widgets import ChallengeSetup


class ChallengeWidgetApp(App[None]):
    def __init__(self, widget: ChallengeSetup) -> None:
        super().__init__()
        self.widget = widget

    def compose(self) -> ComposeResult:
        yield self.widget


def test_challenge_widget_loads_current_mode_difficulty_and_seed() -> None:
    async def scenario() -> None:
        app = ChallengeWidgetApp(
            ChallengeSetup(
                mode=GameMode.TIMED,
                difficulty="hard",
                seed=20260819,
                locale="en",
            )
        )
        async with app.run_test() as pilot:
            await pilot.pause()
            assert app.query_one("#challenge-mode", Select).value == "timed"
            assert app.query_one("#challenge-difficulty", Select).value == "hard"
            assert app.query_one("#challenge-seed", Input).value == "20260819"
            assert app.query_one("#challenge-day", Input).value == ""

    asyncio.run(scenario())


def test_challenge_widget_never_exposes_reverse_as_numeric_setup_default() -> None:
    async def scenario() -> None:
        app = ChallengeWidgetApp(
            ChallengeSetup(
                mode=GameMode.REVERSE,
                difficulty="normal",
                seed=None,
                locale="en",
            )
        )
        async with app.run_test() as pilot:
            await pilot.pause()
            selector = app.query_one("#challenge-mode", Select)
            assert selector.value == "classic"
            assert all(value != "reverse" for _label, value in selector._options)

    asyncio.run(scenario())
