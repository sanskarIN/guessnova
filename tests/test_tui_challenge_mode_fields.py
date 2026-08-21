import asyncio

from textual.app import App, ComposeResult
from textual.widgets import Input, Select

from guessnova.domain import GameMode
from guessnova.tui_challenge_widgets import ChallengeSetup


class ModeFieldApp(App[None]):
    def compose(self) -> ComposeResult:
        yield ChallengeSetup(
            mode=GameMode.CLASSIC,
            difficulty="normal",
            seed=731,
            locale="en",
        )


def test_challenge_mode_enables_only_relevant_seed_or_date_field() -> None:
    async def scenario() -> None:
        app = ModeFieldApp()
        async with app.run_test() as pilot:
            seed = app.query_one("#challenge-seed", Input)
            day = app.query_one("#challenge-day", Input)
            mode = app.query_one("#challenge-mode", Select)

            assert seed.disabled is False
            assert day.disabled is True

            mode.value = "daily"
            await pilot.pause()
            assert seed.disabled is True
            assert day.disabled is False

            mode.value = "timed"
            await pilot.pause()
            assert seed.disabled is False
            assert day.disabled is True

    asyncio.run(scenario())
