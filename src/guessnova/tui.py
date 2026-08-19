"""Textual interface for an app-like terminal experience."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Input, Label, Static

from .domain import GuessOutcome
from .engine import GuessGame
from .i18n import text


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
    BINDINGS = [("q", "quit", "Quit"), ("r", "reset", "New Game")]

    def __init__(self) -> None:
        super().__init__()
        self.game = GuessGame()

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="card"):
            yield Static(f"[b]{text('tui.title')}[/b]", id="title")
            yield Label(self._range_text(), id="range")
            yield Input(placeholder=text("tui.input_placeholder"), type="integer", id="guess")
            yield Button(text("tui.submit"), id="submit", variant="primary")
            yield Button("Range Hint", id="hint")
            yield Static("", id="feedback")
        yield Footer()

    def _range_text(self) -> str:
        difficulty = self.game.difficulty
        return text(
            "tui.range",
            minimum=difficulty.minimum,
            maximum=difficulty.maximum,
            attempts_left=self.game.attempts_left,
        )

    def _submit_guess(self) -> None:
        field = self.query_one("#guess", Input)
        feedback = self.query_one("#feedback", Static)
        if not field.value:
            feedback.update(text("tui.enter_first"))
            return
        try:
            result = self.game.guess(int(field.value))
        except (ValueError, RuntimeError) as exc:
            feedback.update(str(exc))
            return
        field.value = ""
        self.query_one("#range", Label).update(self._range_text())
        if result.outcome == GuessOutcome.CORRECT:
            feedback.update(
                f"[b green]{text('tui.correct', target=self.game.target_value)}[/b green]"
            )
        elif result.outcome in {GuessOutcome.EXHAUSTED, GuessOutcome.TIMEOUT}:
            feedback.update(
                f"[b red]{text('tui.round_over', target=self.game.target_value)}[/b red]"
            )
        elif result.outcome == GuessOutcome.OUT_OF_RANGE:
            feedback.update(f"[yellow]{text('tui.outside_range')}[/yellow]")
        else:
            feedback.update(result.hint or result.outcome.value)

    def _show_hint(self) -> None:
        feedback = self.query_one("#feedback", Static)
        try:
            feedback.update(self.game.request_hint())
        except RuntimeError as exc:
            feedback.update(str(exc))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self._submit_guess()
        elif event.button.id == "hint":
            self._show_hint()

    def on_input_submitted(self, _event: Input.Submitted) -> None:
        self._submit_guess()

    def action_reset(self) -> None:
        self.game = GuessGame()
        self.query_one("#range", Label).update(self._range_text())
        self.query_one("#feedback", Static).update("")
        self.query_one("#guess", Input).value = ""


def run() -> None:
    GuessNovaApp().run()
