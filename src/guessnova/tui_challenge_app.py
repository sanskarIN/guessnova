"""Challenge-enabled Textual application layered over the stable local workspace."""

from __future__ import annotations

from textual.containers import Vertical
from textual.widgets import Button, Input, Select, Static, TabbedContent

from .engine import GuessGame
from .i18n import text
from .storage import Storage
from .tui import GuessNovaApp as WorkspaceApp
from .tui_challenge import challenge_status
from .tui_challenge_widgets import ChallengeSetup
from .tui_workspace import ChallengeConfiguration, parse_workspace_challenge


class GuessNovaApp(WorkspaceApp):
    """Full workspace with validated in-Play challenge configuration."""

    def __init__(
        self,
        *,
        profile_name: str | None = None,
        game: GuessGame | None = None,
        storage: Storage | None = None,
    ) -> None:
        super().__init__(profile_name=profile_name, game=game, storage=storage)
        self.challenge_configuration: ChallengeConfiguration | None = None

    async def on_mount(self) -> None:
        super().on_mount()
        card = self.query_one("#card", Vertical)
        await card.mount(
            ChallengeSetup(
                mode=self.game.mode,
                difficulty=self.game.difficulty_name,
                seed=self.game.seed,
                locale=self.locale,
            ),
            before="#title",
        )
        self.query_one("#guess", Input).focus()

    def _challenge_value(self, selector: str) -> str | None:
        value = self.query_one(selector, Select).value
        return value if isinstance(value, str) else None

    def _start_configured_challenge(self) -> None:
        mode = self._challenge_value("#challenge-mode")
        difficulty = self._challenge_value("#challenge-difficulty")
        if mode is None or difficulty is None:
            return

        seed_field = self.query_one("#challenge-seed", Input)
        day_field = self.query_one("#challenge-day", Input)
        status = self.query_one("#challenge-status", Static)
        try:
            configuration = parse_workspace_challenge(
                mode=mode,
                difficulty=difficulty,
                seed_text=seed_field.value,
                day_text=day_field.value,
            )
            game = configuration.build_game()
        except ValueError as exc:
            status.update(
                text(
                    "tui.challenge.invalid",
                    locale=self.locale,
                    error=str(exc),
                )
            )
            if mode == "daily":
                day_field.focus()
            else:
                seed_field.focus()
            return

        self.challenge_configuration = configuration
        self.game = game
        self._result_saved = False
        seed_field.value = configuration.seed_text
        day_field.value = configuration.day_text
        self.query_one("#range", Static).update(self._range_text())
        self.query_one("#feedback", Static).update("")
        guess = self.query_one("#guess", Input)
        guess.value = ""
        status.update(challenge_status(configuration, locale=self.locale))
        guess.focus()

    def _reset_round(self, *, show_play: bool, focus: bool) -> None:
        if self.challenge_configuration is None:
            super()._reset_round(show_play=show_play, focus=focus)
            return

        self.game = self.challenge_configuration.build_game()
        self._result_saved = False
        self.query_one("#range", Static).update(self._range_text())
        self.query_one("#feedback", Static).update("")
        field = self.query_one("#guess", Input)
        field.value = ""
        if show_play:
            self.query_one("#workspace", TabbedContent).active = "play"
        if focus:
            field.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "challenge-start":
            self._start_configured_challenge()
            return
        super().on_button_pressed(event)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id in {"challenge-seed", "challenge-day"}:
            self._start_configured_challenge()
            return
        super().on_input_submitted(event)


def run() -> None:
    GuessNovaApp().run()
