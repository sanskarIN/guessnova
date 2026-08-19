"""Textual interface for an app-like terminal experience."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Input, Label, Static

from .domain import GuessOutcome
from .engine import GuessGame
from .i18n import text
from .service import GameService
from .storage import Storage


class GuessNovaApp(App[None]):
    TITLE = text("app.name")
    SUB_TITLE = text("app.tagline")
    CSS = """
    Screen { align: center middle; }
    #card { width: 92%; max-width: 64; height: auto; padding: 2 4; border: round $accent; }
    #feedback { height: auto; min-height: 3; margin-top: 1; }
    Input { margin-top: 1; }
    Button { width: 100%; margin-top: 1; }
    """
    BINDINGS = [
        Binding("q", "quit", text("tui.binding.quit"), priority=True),
        Binding("r", "reset", text("tui.binding.new_game"), priority=True),
    ]

    def __init__(
        self,
        *,
        profile_name: str | None = None,
        game: GuessGame | None = None,
        storage: Storage | None = None,
    ) -> None:
        super().__init__()
        self.storage = storage or Storage()
        profile = self.storage.load_profile(profile_name)
        self.profile_name = profile.name
        self.locale = profile.settings.locale
        self.show_smart_hints = profile.settings.show_smart_hints
        self.game = game or GuessGame()
        self._result_saved = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="card"):
            yield Static(
                f"[b]{text('tui.title', locale=self.locale)}[/b]",
                id="title",
            )
            yield Label(self._range_text(), id="range")
            yield Input(
                placeholder=text("tui.input_placeholder", locale=self.locale),
                type="integer",
                id="guess",
            )
            yield Button(
                text("tui.submit", locale=self.locale),
                id="submit",
                variant="primary",
            )
            yield Button(text("tui.hint", locale=self.locale), id="hint")
            yield Static("", id="feedback")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#guess", Input).focus()

    def _range_text(self) -> str:
        difficulty = self.game.difficulty
        return text(
            "tui.range",
            locale=self.locale,
            minimum=difficulty.minimum,
            maximum=difficulty.maximum,
            attempts_left=self.game.attempts_left,
        )

    def _save_finished_result(self) -> None:
        if self._result_saved or not self.game.is_finished:
            return
        GameService(self.storage).record(self.game.summary(), self.profile_name)
        self._result_saved = True

    def _submit_guess(self) -> None:
        field = self.query_one("#guess", Input)
        feedback = self.query_one("#feedback", Static)
        if not field.value:
            feedback.update(text("tui.enter_first", locale=self.locale))
            field.focus()
            return
        try:
            result = self.game.guess(int(field.value))
        except (ValueError, RuntimeError) as exc:
            feedback.update(str(exc))
            field.focus()
            return
        field.value = ""
        self.query_one("#range", Label).update(self._range_text())
        if result.outcome == GuessOutcome.CORRECT:
            self._save_finished_result()
            feedback.update(
                f"[b green]{text('tui.correct', locale=self.locale, target=self.game.target_value)}"
                "[/b green]"
            )
        elif result.outcome in {GuessOutcome.EXHAUSTED, GuessOutcome.TIMEOUT}:
            self._save_finished_result()
            feedback.update(
                f"[b red]{text('tui.round_over', locale=self.locale, target=self.game.target_value)}"
                "[/b red]"
            )
        elif result.outcome == GuessOutcome.OUT_OF_RANGE:
            feedback.update(
                f"[yellow]{text('tui.outside_range', locale=self.locale)}[/yellow]"
            )
        elif self.show_smart_hints and result.hint:
            feedback.update(result.hint)
        else:
            feedback.update(result.outcome.value)
        field.focus()

    def _show_hint(self) -> None:
        feedback = self.query_one("#feedback", Static)
        try:
            feedback.update(self.game.request_hint())
        except RuntimeError as exc:
            feedback.update(str(exc))
        self.query_one("#guess", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self._submit_guess()
        elif event.button.id == "hint":
            self._show_hint()

    def on_input_submitted(self, _event: Input.Submitted) -> None:
        self._submit_guess()

    def action_reset(self) -> None:
        self.game = GuessGame(
            difficulty_name=self.game.difficulty_name,
            mode=self.game.mode,
            seed=self.game.seed,
        )
        self._result_saved = False
        self.query_one("#range", Label).update(self._range_text())
        self.query_one("#feedback", Static).update("")
        field = self.query_one("#guess", Input)
        field.value = ""
        field.focus()


def run() -> None:
    GuessNovaApp().run()
