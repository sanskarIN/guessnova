"""Textual interface for an app-like terminal experience."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Input, Label, Static

from .domain import GuessOutcome
from .engine import GuessGame


class GuessNovaApp(App[None]):
    TITLE = "GuessNova"
    SUB_TITLE = "Number Guessing, Supernova Style"
    CSS = """
    Screen { align: center middle; }
    #card { width: 64; height: auto; padding: 2 4; border: round $accent; }
    #feedback { height: 3; margin-top: 1; }
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
            yield Static("[b]Guess the hidden number[/b]", id="title")
            yield Label(self._range_text(), id="range")
            yield Input(placeholder="Enter a whole number", type="integer", id="guess")
            yield Button("Launch Guess", id="submit", variant="primary")
            yield Static("", id="feedback")
        yield Footer()

    def _range_text(self) -> str:
        d = self.game.difficulty
        return f"Range {d.minimum}–{d.maximum} · {self.game.attempts_left} attempts"

    def _submit_guess(self) -> None:
        field = self.query_one("#guess", Input)
        feedback = self.query_one("#feedback", Static)
        if not field.value:
            feedback.update("Enter a number first.")
            return
        try:
            result = self.game.guess(int(field.value))
        except (ValueError, RuntimeError) as exc:
            feedback.update(str(exc))
            return
        field.value = ""
        self.query_one("#range", Label).update(self._range_text())
        if result.outcome == GuessOutcome.CORRECT:
            feedback.update(f"[b green]Correct! The target was {self.game.target}.[/b green] Press R for a new game.")
        elif result.outcome in {GuessOutcome.EXHAUSTED, GuessOutcome.TIMEOUT}:
            feedback.update(f"[b red]Round over. Target: {self.game.target}.[/b red] Press R for a new game.")
        elif result.outcome == GuessOutcome.OUT_OF_RANGE:
            feedback.update("[yellow]Outside the current range.[/yellow]")
        else:
            feedback.update(result.hint or result.outcome.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self._submit_guess()

    def on_input_submitted(self, _event: Input.Submitted) -> None:
        self._submit_guess()

    def action_reset(self) -> None:
        self.game = GuessGame()
        self.query_one("#range", Label).update(self._range_text())
        self.query_one("#feedback", Static).update("")
        self.query_one("#guess", Input).value = ""


def run() -> None:
    GuessNovaApp().run()
