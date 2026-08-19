import asyncio
from pathlib import Path

from textual.widgets import DataTable, Input, Select

from guessnova.engine import GuessGame
from guessnova.leaderboard import LeaderboardEntry
from guessnova.profile import Profile
from guessnova.storage import Storage
from guessnova.tui import GuessNovaApp


def test_workspace_leaderboard_filters_and_clears(tmp_path: Path) -> None:
    async def scenario() -> None:
        storage = Storage(tmp_path)
        storage.save_profile(Profile("Nova"))
        storage.save_leaderboard(
            [
                LeaderboardEntry(
                    "Alpha",
                    "hard",
                    "classic",
                    2,
                    5.0,
                    "2026-08-19T00:00:00Z",
                ),
                LeaderboardEntry(
                    "Beta",
                    "hard",
                    "classic",
                    3,
                    6.0,
                    "2026-08-19T00:01:00Z",
                ),
                LeaderboardEntry(
                    "Gamma",
                    "easy",
                    "timed",
                    4,
                    7.0,
                    "2026-08-19T00:02:00Z",
                ),
            ]
        )
        app = GuessNovaApp(profile_name="Nova", storage=storage, game=GuessGame(target=42))
        async with app.run_test() as pilot:
            await pilot.press("ctrl+4")
            await pilot.pause()
            table = app.query_one("#leaderboard-table", DataTable)
            assert table.row_count == 3

            app.query_one("#leaderboard-mode", Select).value = "classic"
            app.query_one("#leaderboard-difficulty", Select).value = "hard"
            app.query_one("#leaderboard-player", Input).value = "beta"
            await pilot.click("#leaderboard-apply")
            await pilot.pause()
            assert table.row_count == 1

            await pilot.click("#leaderboard-clear")
            await pilot.pause()
            assert table.row_count == 3

    asyncio.run(scenario())
