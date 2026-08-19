"""Textual widgets for configuring numeric GuessNova challenges."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label, Select, Static

from .domain import DIFFICULTIES, GameMode
from .i18n import text


class ChallengeSetup(Vertical):
    """Keyboard-friendly challenge controls mounted ahead of the Play guess field."""

    DEFAULT_CSS = """
    ChallengeSetup {
        height: auto;
        margin-bottom: 1;
        padding: 1;
        border: round $accent;
    }
    ChallengeSetup > .challenge-row {
        height: auto;
        margin-bottom: 1;
    }
    ChallengeSetup > .challenge-row > * {
        margin-right: 1;
    }
    ChallengeSetup > .challenge-row > *:last-child {
        margin-right: 0;
    }
    ChallengeSetup Select {
        width: 1fr;
    }
    ChallengeSetup #challenge-start {
        width: 100%;
        margin-top: 1;
    }
    ChallengeSetup #challenge-fields-label,
    ChallengeSetup #challenge-help,
    ChallengeSetup #challenge-status {
        height: auto;
        min-height: 1;
        margin-top: 1;
    }
    """

    def __init__(
        self,
        *,
        mode: GameMode,
        difficulty: str,
        seed: int | None,
        locale: str,
    ) -> None:
        super().__init__(id="challenge-setup")
        self.initial_mode = mode if mode != GameMode.REVERSE else GameMode.CLASSIC
        self.initial_difficulty = difficulty if difficulty in DIFFICULTIES else "normal"
        self.initial_seed = None if self.initial_mode == GameMode.DAILY else seed
        self.locale = locale

    def compose(self) -> ComposeResult:
        yield Label(f"[b]{text('tui.challenge.title', locale=self.locale)}[/b]")
        yield Static(
            f"{text('tui.challenge.mode', locale=self.locale)} / "
            f"{text('tui.challenge.difficulty', locale=self.locale)}",
            id="challenge-fields-label",
        )
        with Horizontal(classes="challenge-row"):
            yield Select(
                [(mode.value, mode.value) for mode in GameMode if mode != GameMode.REVERSE],
                value=self.initial_mode.value,
                allow_blank=False,
                id="challenge-mode",
            )
            yield Select(
                [(name, name) for name in sorted(DIFFICULTIES)],
                value=self.initial_difficulty,
                allow_blank=False,
                id="challenge-difficulty",
            )
        yield Input(
            value="" if self.initial_seed is None else str(self.initial_seed),
            placeholder=text("tui.challenge.seed_placeholder", locale=self.locale),
            id="challenge-seed",
        )
        yield Input(
            placeholder=text("tui.challenge.day_placeholder", locale=self.locale),
            id="challenge-day",
        )
        yield Button(
            text("tui.challenge.start", locale=self.locale),
            id="challenge-start",
            variant="primary",
        )
        yield Static(
            text("tui.challenge.help", locale=self.locale),
            id="challenge-help",
        )
        yield Static("", id="challenge-status")

    def on_mount(self) -> None:
        self._sync_mode_fields()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "challenge-mode":
            self._sync_mode_fields()

    def _sync_mode_fields(self) -> None:
        mode = self.query_one("#challenge-mode", Select).value
        daily = mode == GameMode.DAILY.value
        self.query_one("#challenge-seed", Input).disabled = daily
        self.query_one("#challenge-day", Input).disabled = not daily
