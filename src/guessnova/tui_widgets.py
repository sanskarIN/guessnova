"""Small Textual widgets that keep workspace keyboard responsibilities local."""

from __future__ import annotations

from textual.binding import Binding
from textual.message import Message
from textual.widgets import Input


class GuessInput(Input):
    """Numeric guess input with Play-local single-letter shortcuts."""

    class NewRoundRequested(Message):
        """Request a new round without making R global to every text field."""

    BINDINGS = [
        Binding("r", "new_round", "New Game", show=False),
        Binding("q", "quit_app", "Quit", show=False),
    ]

    def action_new_round(self) -> None:
        self.post_message(self.NewRoundRequested())

    def action_quit_app(self) -> None:
        self.app.exit()
