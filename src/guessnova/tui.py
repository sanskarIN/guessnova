"""Textual interface for a keyboard-first local GuessNova workspace."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Select,
    Static,
    Switch,
    TabbedContent,
    TabPane,
)

from .backup_inspection import inspect_backup
from .diagnostics import diagnose
from .domain import DIFFICULTIES, GameMode, GuessOutcome
from .engine import GuessGame
from .history import HistoryResult
from .i18n import available_locales, text
from .profile import Profile
from .service import GameService
from .storage import Storage
from .themes import THEMES
from .tui_widgets import GuessInput
from .tui_workspace import (
    profile_summary,
    save_workspace_settings,
    select_history,
    select_leaderboard,
)


class GuessNovaApp(App[None]):
    TITLE = text("app.name")
    SUB_TITLE = text("app.tagline")
    CSS = """
    Screen { layout: vertical; }
    #workspace { height: 1fr; width: 100%; }
    TabPane { padding: 1 2; }
    #play { align: center middle; }
    #card {
        width: 92%;
        max-width: 64;
        height: auto;
        padding: 2 4;
        border: round $accent;
    }
    #feedback { height: auto; min-height: 3; margin-top: 1; }
    .pane-scroll { height: 1fr; }
    .section { height: auto; margin-bottom: 1; padding: 1 2; border: round $accent; }
    .form-row { height: auto; margin-bottom: 1; }
    .form-row > * { margin-right: 1; }
    .form-row > *:last-child { margin-right: 0; }
    .field-label { width: 22; content-align: left middle; }
    .field-control { width: 1fr; }
    .status { height: auto; min-height: 2; margin-top: 1; }
    #history-table, #leaderboard-table { height: 1fr; min-height: 12; }
    Input { margin-top: 1; }
    #card Button { width: 100%; margin-top: 1; }
    Screen.high-contrast #card,
    Screen.high-contrast .section { border: double white; }
    Screen.high-contrast Button:focus,
    Screen.high-contrast Input:focus,
    Screen.high-contrast Select:focus,
    Screen.high-contrast Switch:focus { outline: solid yellow; }
    """
    BINDINGS = [
        Binding("ctrl+q", "quit", text("tui.binding.quit"), show=False, priority=True),
        Binding("ctrl+r", "reset", text("tui.binding.new_game"), show=False, priority=True),
        Binding("ctrl+1", "show_tab('play')", text("tui.tab.play"), show=False),
        Binding("ctrl+2", "show_tab('profiles')", text("tui.tab.profiles"), show=False),
        Binding("ctrl+3", "show_tab('history')", text("tui.tab.history"), show=False),
        Binding("ctrl+4", "show_tab('leaderboard')", text("leaderboard.title"), show=False),
        Binding("ctrl+5", "show_tab('settings')", text("tui.tab.settings"), show=False),
        Binding("ctrl+6", "show_tab('recovery')", text("tui.tab.recovery"), show=False),
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

    def _profile_options(self) -> list[tuple[str, str]]:
        return [(name, name) for name in self.storage.list_profile_names()]

    def _trash_options(self) -> list[tuple[str, str]]:
        return [(name, name) for name in self.storage.list_deleted_profile_names()]

    def _mode_options(self) -> list[tuple[str, str]]:
        return [
            (text("tui.history.all", locale=self.locale), "all"),
            *[(mode.value, mode.value) for mode in GameMode if mode != GameMode.REVERSE],
        ]

    def _difficulty_options(self) -> list[tuple[str, str]]:
        return [
            (text("tui.history.all", locale=self.locale), "all"),
            *[(name, name) for name in sorted(DIFFICULTIES)],
        ]

    def compose(self) -> ComposeResult:
        profile = self.storage.load_profile(self.profile_name)
        yield Header()
        with TabbedContent(initial="play", id="workspace"):
            with TabPane(text("tui.tab.play", locale=self.locale), id="play"):
                with Vertical(id="card"):
                    yield Static(
                        f"[b]{text('tui.title', locale=self.locale)}[/b]",
                        id="title",
                    )
                    yield Label(self._range_text(), id="range")
                    yield GuessInput(
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

            with TabPane(text("tui.tab.profiles", locale=self.locale), id="profiles"):
                with VerticalScroll(classes="pane-scroll"):
                    with Vertical(classes="section"):
                        yield Static("", id="profile-summary")
                        yield Static("", id="profile-achievements")
                        with Horizontal(classes="form-row"):
                            yield Select(
                                self._profile_options(),
                                prompt=text("tui.profile.saved", locale=self.locale),
                                allow_blank=True,
                                id="profile-select",
                                classes="field-control",
                            )
                            yield Button(
                                text("tui.profile.use", locale=self.locale),
                                id="profile-use",
                            )
                            yield Button(
                                text("tui.profile.refresh", locale=self.locale),
                                id="profile-refresh",
                            )
                        yield Input(
                            placeholder=text("tui.profile.name_placeholder", locale=self.locale),
                            max_length=64,
                            id="profile-name",
                        )
                        with Horizontal(classes="form-row"):
                            yield Button(
                                text("tui.profile.create", locale=self.locale),
                                id="profile-create",
                                variant="primary",
                            )
                            yield Button(
                                text("tui.profile.rename", locale=self.locale),
                                id="profile-rename",
                            )
                            yield Button(
                                text("tui.profile.delete", locale=self.locale),
                                id="profile-delete",
                                variant="error",
                            )
                        yield Static(
                            text("tui.profile.status_ready", locale=self.locale),
                            id="profile-status",
                            classes="status",
                        )
                    with Vertical(classes="section"):
                        yield Label(text("tui.profile.trash", locale=self.locale))
                        with Horizontal(classes="form-row"):
                            yield Select(
                                self._trash_options(),
                                prompt=text("tui.profile.trash", locale=self.locale),
                                allow_blank=True,
                                id="trash-select",
                                classes="field-control",
                            )
                            yield Button(
                                text("tui.profile.restore", locale=self.locale),
                                id="profile-restore",
                            )

            with TabPane(text("tui.tab.history", locale=self.locale), id="history"):
                with Vertical(classes="pane-scroll"):
                    with Horizontal(classes="form-row"):
                        yield Select(
                            [
                                (text("tui.history.all", locale=self.locale), "all"),
                                (text("history.win", locale=self.locale), "win"),
                                (text("history.loss", locale=self.locale), "loss"),
                            ],
                            value="all",
                            allow_blank=False,
                            id="history-result",
                            classes="field-control",
                        )
                        yield Select(
                            self._mode_options(),
                            value="all",
                            allow_blank=False,
                            id="history-mode",
                            classes="field-control",
                        )
                        yield Select(
                            self._difficulty_options(),
                            value="all",
                            allow_blank=False,
                            id="history-difficulty",
                            classes="field-control",
                        )
                    yield Input(
                        placeholder=text("tui.history.search_placeholder", locale=self.locale),
                        id="history-search",
                    )
                    with Horizontal(classes="form-row"):
                        yield Input(
                            placeholder=text("tui.history.since_placeholder", locale=self.locale),
                            id="history-since",
                            classes="field-control",
                        )
                        yield Input(
                            placeholder=text("tui.history.until_placeholder", locale=self.locale),
                            id="history-until",
                            classes="field-control",
                        )
                        yield Button(
                            text("tui.history.apply", locale=self.locale),
                            id="history-apply",
                            variant="primary",
                        )
                        yield Button(
                            text("tui.history.clear", locale=self.locale),
                            id="history-clear",
                        )
                    yield Static("", id="history-status", classes="status")
                    yield DataTable(id="history-table")

            with TabPane(text("leaderboard.title", locale=self.locale), id="leaderboard"):
                with Vertical(classes="pane-scroll"):
                    with Horizontal(classes="form-row"):
                        yield Select(
                            self._mode_options(),
                            value="all",
                            allow_blank=False,
                            id="leaderboard-mode",
                            classes="field-control",
                        )
                        yield Select(
                            self._difficulty_options(),
                            value="all",
                            allow_blank=False,
                            id="leaderboard-difficulty",
                            classes="field-control",
                        )
                    yield Input(
                        placeholder=text("leaderboard.player", locale=self.locale),
                        id="leaderboard-player",
                    )
                    with Horizontal(classes="form-row"):
                        yield Button(
                            text("tui.history.apply", locale=self.locale),
                            id="leaderboard-apply",
                            variant="primary",
                        )
                        yield Button(
                            text("tui.history.clear", locale=self.locale),
                            id="leaderboard-clear",
                        )
                    yield Static("", id="leaderboard-status", classes="status")
                    yield DataTable(id="leaderboard-table")

            with TabPane(text("tui.tab.settings", locale=self.locale), id="settings"):
                with VerticalScroll(classes="pane-scroll"):
                    with Vertical(classes="section"):
                        with Horizontal(classes="form-row"):
                            yield Label(
                                text("tui.settings.theme", locale=self.locale),
                                classes="field-label",
                            )
                            yield Select(
                                [(name, name) for name in sorted(THEMES)],
                                value=profile.settings.theme,
                                allow_blank=False,
                                id="settings-theme",
                                classes="field-control",
                            )
                        with Horizontal(classes="form-row"):
                            yield Label(
                                text("tui.settings.locale", locale=self.locale),
                                classes="field-label",
                            )
                            yield Select(
                                [(name, name) for name in available_locales()],
                                value=profile.settings.locale,
                                allow_blank=False,
                                id="settings-locale",
                                classes="field-control",
                            )
                        with Horizontal(classes="form-row"):
                            yield Label(
                                text("tui.settings.reduced_motion", locale=self.locale),
                                classes="field-label",
                            )
                            yield Switch(
                                value=profile.settings.reduced_motion,
                                animate=False,
                                id="settings-reduced-motion",
                            )
                        with Horizontal(classes="form-row"):
                            yield Label(
                                text("tui.settings.high_contrast", locale=self.locale),
                                classes="field-label",
                            )
                            yield Switch(
                                value=profile.settings.high_contrast,
                                animate=False,
                                id="settings-high-contrast",
                            )
                        with Horizontal(classes="form-row"):
                            yield Label(
                                text("tui.settings.sound", locale=self.locale),
                                classes="field-label",
                            )
                            yield Switch(
                                value=profile.settings.sound,
                                animate=False,
                                id="settings-sound",
                            )
                        with Horizontal(classes="form-row"):
                            yield Label(
                                text("tui.settings.smart_hints", locale=self.locale),
                                classes="field-label",
                            )
                            yield Switch(
                                value=profile.settings.show_smart_hints,
                                animate=False,
                                id="settings-smart-hints",
                            )
                        yield Button(
                            text("tui.settings.save", locale=self.locale),
                            id="settings-save",
                            variant="primary",
                        )
                        yield Static("", id="settings-status", classes="status")

            with TabPane(text("tui.tab.recovery", locale=self.locale), id="recovery"):
                with VerticalScroll(classes="pane-scroll"):
                    with Vertical(classes="section"):
                        yield Static(f"[b]{text('tui.recovery.title', locale=self.locale)}[/b]")
                        yield Static("", id="recovery-health", classes="status")
                        yield Static("", id="recovery-data")
                        yield Static("", id="recovery-schema")
                        yield Button(
                            text("tui.recovery.refresh", locale=self.locale),
                            id="recovery-refresh",
                        )
                    with Vertical(classes="section"):
                        yield Input(
                            placeholder=text("tui.recovery.backup_placeholder", locale=self.locale),
                            id="recovery-backup-path",
                        )
                        yield Button(
                            text("tui.recovery.verify", locale=self.locale),
                            id="recovery-verify",
                            variant="primary",
                        )
                        yield Static(
                            text("tui.recovery.read_only", locale=self.locale),
                            id="recovery-backup-status",
                            classes="status",
                        )
        yield Footer()

    def on_mount(self) -> None:
        self._configure_history_table()
        self._configure_leaderboard_table()
        self._apply_accessibility_preferences()
        self._refresh_workspace()
        self.query_one("#guess", Input).focus()

    def _configure_history_table(self) -> None:
        table = self.query_one("#history-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns(
            text("history.when", locale=self.locale),
            text("history.mode", locale=self.locale),
            text("history.difficulty", locale=self.locale),
            text("history.result", locale=self.locale),
            text("history.attempts", locale=self.locale),
            text("history.time", locale=self.locale),
        )

    def _configure_leaderboard_table(self) -> None:
        table = self.query_one("#leaderboard-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns(
            "#",
            text("leaderboard.player", locale=self.locale),
            text("history.mode", locale=self.locale),
            text("history.difficulty", locale=self.locale),
            text("history.attempts", locale=self.locale),
            text("history.time", locale=self.locale),
            text("history.when", locale=self.locale),
        )

    def _range_text(self) -> str:
        difficulty = self.game.difficulty
        return text(
            "tui.range",
            locale=self.locale,
            minimum=difficulty.minimum,
            maximum=difficulty.maximum,
            attempts_left=self.game.attempts_left,
        )

    def _reset_round(self, *, show_play: bool, focus: bool) -> None:
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
        if show_play:
            self.query_one("#workspace", TabbedContent).active = "play"
        if focus:
            field.focus()

    def _save_finished_result(self) -> None:
        if self._result_saved or not self.game.is_finished:
            return
        GameService(self.storage).record(self.game.summary(), self.profile_name)
        self._result_saved = True
        self._refresh_workspace()

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
            feedback.update(f"[yellow]{text('tui.outside_range', locale=self.locale)}[/yellow]")
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

    def _selected_string(self, selector: str) -> str | None:
        value = self.query_one(selector, Select).value
        return value if isinstance(value, str) else None

    def _set_profile_status(self, message: str) -> None:
        self.query_one("#profile-status", Static).update(message)

    def _achievement_labels(self, profile: Profile) -> str:
        labels: list[str] = []
        for achievement in sorted(profile.stats.achievements):
            try:
                labels.append(text(f"achievement.{achievement}", locale=self.locale))
            except KeyError:
                labels.append(achievement)
        return ", ".join(labels) if labels else "—"

    def _refresh_profile_widgets(self) -> None:
        profile = self.storage.load_profile(self.profile_name)
        summary = profile_summary(profile)
        self.query_one("#profile-summary", Static).update(
            text(
                "tui.profile.summary",
                locale=self.locale,
                profile=profile.name,
                games=summary.games_played,
                wins=summary.games_won,
                win_rate=summary.win_rate,
                xp=summary.xp,
                streak=summary.current_streak,
                best=summary.best_streak,
                achievements=summary.achievement_count,
            )
        )
        self.query_one("#profile-achievements", Static).update(
            f"{text('stats.achievements', locale=self.locale)}: {self._achievement_labels(profile)}"
        )
        profile_select = self.query_one("#profile-select", Select)
        profile_names = self.storage.list_profile_names()
        profile_select.set_options((name, name) for name in profile_names)
        if self.profile_name in profile_names:
            profile_select.value = self.profile_name

        trash_select = self.query_one("#trash-select", Select)
        trash_names = self.storage.list_deleted_profile_names()
        trash_select.set_options((name, name) for name in trash_names)

    def _load_profile_settings(self) -> None:
        profile = self.storage.load_profile(self.profile_name)
        self.query_one("#settings-theme", Select).value = profile.settings.theme
        self.query_one("#settings-locale", Select).value = profile.settings.locale
        self.query_one("#settings-reduced-motion", Switch).value = profile.settings.reduced_motion
        self.query_one("#settings-high-contrast", Switch).value = profile.settings.high_contrast
        self.query_one("#settings-sound", Switch).value = profile.settings.sound
        self.query_one("#settings-smart-hints", Switch).value = profile.settings.show_smart_hints

    def _apply_accessibility_preferences(self) -> None:
        profile = self.storage.load_profile(self.profile_name)
        self.screen.set_class(profile.settings.high_contrast, "high-contrast")

    def _refresh_workspace(self) -> None:
        self._refresh_profile_widgets()
        self._populate_history_table()
        self._populate_leaderboard_table()
        self._refresh_recovery()

    def _activate_profile(self, name: str) -> None:
        profile = self.storage.set_active_profile(name)
        self.profile_name = profile.name
        self.show_smart_hints = profile.settings.show_smart_hints
        self._load_profile_settings()
        self._apply_accessibility_preferences()
        self._reset_round(show_play=False, focus=False)
        self._refresh_workspace()

    def _profile_use(self) -> None:
        selected = self._selected_string("#profile-select")
        if selected is None:
            self._set_profile_status(text("tui.profile.no_selection", locale=self.locale))
            return
        try:
            self._activate_profile(selected)
        except ValueError as exc:
            self._set_profile_status(str(exc))
            return
        self._set_profile_status(
            text("profiles.activated", locale=self.locale, name=self.profile_name)
        )

    def _profile_create(self) -> None:
        field = self.query_one("#profile-name", Input)
        if not field.value.strip():
            self._set_profile_status(text("tui.profile.name_required", locale=self.locale))
            field.focus()
            return
        try:
            created = self.storage.create_profile(field.value, make_active=True)
            self.profile_name = created.name
            self.show_smart_hints = created.settings.show_smart_hints
        except ValueError as exc:
            self._set_profile_status(str(exc))
            field.focus()
            return
        field.value = ""
        self._load_profile_settings()
        self._apply_accessibility_preferences()
        self._reset_round(show_play=False, focus=False)
        self._refresh_workspace()
        self._set_profile_status(text("profiles.created", locale=self.locale, name=created.name))

    def _profile_rename(self) -> None:
        selected = self._selected_string("#profile-select")
        field = self.query_one("#profile-name", Input)
        if selected is None:
            self._set_profile_status(text("tui.profile.no_selection", locale=self.locale))
            return
        if not field.value.strip():
            self._set_profile_status(text("tui.profile.name_required", locale=self.locale))
            field.focus()
            return
        try:
            renamed = self.storage.rename_profile(selected, field.value)
        except ValueError as exc:
            self._set_profile_status(str(exc))
            field.focus()
            return
        if self.profile_name == selected:
            self.profile_name = renamed.name
        field.value = ""
        self._refresh_workspace()
        self._set_profile_status(text("profiles.renamed", locale=self.locale, name=renamed.name))

    def _profile_delete(self) -> None:
        selected = self._selected_string("#profile-select")
        field = self.query_one("#profile-name", Input)
        if selected is None:
            self._set_profile_status(text("tui.profile.no_selection", locale=self.locale))
            return
        if field.value.strip() != selected:
            self._set_profile_status(text("tui.profile.delete_type", locale=self.locale))
            field.focus()
            return
        deleting_active = self.profile_name == selected
        try:
            self.storage.delete_profile(selected)
        except ValueError as exc:
            self._set_profile_status(str(exc))
            return
        field.value = ""
        if deleting_active:
            profile = self.storage.load_profile(self.storage.active_profile_name())
            self.profile_name = profile.name
            self.show_smart_hints = profile.settings.show_smart_hints
            self._load_profile_settings()
            self._apply_accessibility_preferences()
            self._reset_round(show_play=False, focus=False)
        self._refresh_workspace()
        self._set_profile_status(text("profiles.deleted", locale=self.locale, name=selected))

    def _profile_restore(self) -> None:
        selected = self._selected_string("#trash-select")
        if selected is None:
            self._set_profile_status(text("tui.profile.no_trash_selection", locale=self.locale))
            return
        try:
            restored = self.storage.restore_profile(selected, make_active=True)
        except ValueError as exc:
            self._set_profile_status(str(exc))
            return
        self.profile_name = restored.name
        self.show_smart_hints = restored.settings.show_smart_hints
        self._load_profile_settings()
        self._apply_accessibility_preferences()
        self._reset_round(show_play=False, focus=False)
        self._refresh_workspace()
        self._set_profile_status(text("profiles.restored", locale=self.locale, name=restored.name))

    def _history_choice(self, selector: str) -> str | None:
        value = self._selected_string(selector)
        return None if value in {None, "all"} else value

    def _history_result(self) -> HistoryResult | None:
        value = self._history_choice("#history-result")
        if value == "win":
            return "win"
        if value == "loss":
            return "loss"
        return None

    def _history_date(self, selector: str) -> date | None:
        value = self.query_one(selector, Input).value.strip()
        return date.fromisoformat(value) if value else None

    def _populate_history_table(self) -> None:
        table = self.query_one("#history-table", DataTable)
        try:
            since = self._history_date("#history-since")
            until = self._history_date("#history-until")
        except ValueError:
            self.query_one("#history-status", Static).update(
                text("tui.history.invalid_date", locale=self.locale)
            )
            return
        profile = self.storage.load_profile(self.profile_name)
        entries = select_history(
            profile,
            mode=self._history_choice("#history-mode"),
            difficulty=self._history_choice("#history-difficulty"),
            result=self._history_result(),
            query=self.query_one("#history-search", Input).value or None,
            since=since,
            until=until,
            limit=100,
        )
        table.clear()
        for entry in entries:
            table.add_row(
                entry.played_at,
                entry.mode,
                entry.difficulty,
                text("history.win", locale=self.locale)
                if entry.won
                else text("history.loss", locale=self.locale),
                str(entry.attempts),
                f"{entry.elapsed_seconds:.2f}s",
            )
        self.query_one("#history-status", Static).update(
            text(
                "tui.history.count",
                locale=self.locale,
                count=len(entries),
                profile=profile.name,
            )
        )

    def _clear_history_filters(self) -> None:
        self.query_one("#history-result", Select).value = "all"
        self.query_one("#history-mode", Select).value = "all"
        self.query_one("#history-difficulty", Select).value = "all"
        self.query_one("#history-search", Input).value = ""
        self.query_one("#history-since", Input).value = ""
        self.query_one("#history-until", Input).value = ""
        self._populate_history_table()

    def _populate_leaderboard_table(self) -> None:
        entries = select_leaderboard(
            self.storage.load_leaderboard(),
            mode=self._history_choice("#leaderboard-mode"),
            difficulty=self._history_choice("#leaderboard-difficulty"),
            player=self.query_one("#leaderboard-player", Input).value or None,
            limit=100,
        )
        table = self.query_one("#leaderboard-table", DataTable)
        table.clear()
        for rank, entry in enumerate(entries, 1):
            table.add_row(
                str(rank),
                entry.player,
                entry.mode,
                entry.difficulty,
                str(entry.attempts),
                f"{entry.elapsed_seconds:.2f}s",
                entry.created_at,
            )
        self.query_one("#leaderboard-status", Static).update(
            f"{text('leaderboard.title', locale=self.locale)}: {len(entries)}"
        )

    def _clear_leaderboard_filters(self) -> None:
        self.query_one("#leaderboard-mode", Select).value = "all"
        self.query_one("#leaderboard-difficulty", Select).value = "all"
        self.query_one("#leaderboard-player", Input).value = ""
        self._populate_leaderboard_table()

    def _save_settings(self) -> None:
        theme = self._selected_string("#settings-theme")
        locale = self._selected_string("#settings-locale")
        if theme is None or locale is None:
            return
        profile = save_workspace_settings(
            self.storage,
            self.profile_name,
            theme=theme,
            locale=locale,
            reduced_motion=self.query_one("#settings-reduced-motion", Switch).value,
            high_contrast=self.query_one("#settings-high-contrast", Switch).value,
            sound=self.query_one("#settings-sound", Switch).value,
            show_smart_hints=self.query_one("#settings-smart-hints", Switch).value,
        )
        self.show_smart_hints = profile.settings.show_smart_hints
        self._apply_accessibility_preferences()
        self.query_one("#settings-status", Static).update(
            text(
                "tui.settings.saved",
                locale=self.locale,
                profile=profile.name,
            )
        )
        self._refresh_profile_widgets()
        self._refresh_recovery()

    def _refresh_recovery(self) -> None:
        report = diagnose(self.storage)
        if report.healthy:
            health = text("tui.recovery.healthy", locale=self.locale)
        else:
            health = text(
                "tui.recovery.attention",
                locale=self.locale,
                issues="; ".join(report.issues) or "unknown",
            )
        self.query_one("#recovery-health", Static).update(health)
        self.query_one("#recovery-data", Static).update(
            text(
                "tui.recovery.data_dir",
                locale=self.locale,
                path=self.storage.data_dir,
            )
        )
        source = report.source_schema_version if report.source_schema_version is not None else "-"
        self.query_one("#recovery-schema", Static).update(
            text(
                "tui.recovery.schema",
                locale=self.locale,
                source=source,
                current=report.current_schema_version,
                profiles=report.profile_count,
                history=report.history_entries,
                leaderboard=report.leaderboard_entries,
                trash=report.deleted_profile_count,
            )
        )

    def _verify_backup(self) -> None:
        field = self.query_one("#recovery-backup-path", Input)
        status = self.query_one("#recovery-backup-status", Static)
        path = field.value.strip()
        if not path:
            status.update(
                text(
                    "tui.recovery.backup_invalid",
                    locale=self.locale,
                    error="backup path is required",
                )
            )
            field.focus()
            return
        try:
            inspection = inspect_backup(Path(path).expanduser())
        except (OSError, ValueError) as exc:
            status.update(
                text(
                    "tui.recovery.backup_invalid",
                    locale=self.locale,
                    error=str(exc),
                )
            )
            field.focus()
            return
        integrity = inspection.integrity_algorithm or "legacy"
        status.update(
            text(
                "tui.recovery.backup_valid",
                locale=self.locale,
                version=inspection.export_version,
                source=inspection.schema_version,
                normalized=inspection.normalized_schema_version,
                integrity=integrity,
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "submit":
            self._submit_guess()
        elif button_id == "hint":
            self._show_hint()
        elif button_id == "profile-use":
            self._profile_use()
        elif button_id == "profile-refresh":
            self._refresh_workspace()
        elif button_id == "profile-create":
            self._profile_create()
        elif button_id == "profile-rename":
            self._profile_rename()
        elif button_id == "profile-delete":
            self._profile_delete()
        elif button_id == "profile-restore":
            self._profile_restore()
        elif button_id == "history-apply":
            self._populate_history_table()
        elif button_id == "history-clear":
            self._clear_history_filters()
        elif button_id == "leaderboard-apply":
            self._populate_leaderboard_table()
        elif button_id == "leaderboard-clear":
            self._clear_leaderboard_filters()
        elif button_id == "settings-save":
            self._save_settings()
        elif button_id == "recovery-refresh":
            self._refresh_recovery()
        elif button_id == "recovery-verify":
            self._verify_backup()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "guess":
            self._submit_guess()
        elif event.input.id == "history-search":
            self._populate_history_table()
        elif event.input.id == "leaderboard-player":
            self._populate_leaderboard_table()
        elif event.input.id == "recovery-backup-path":
            self._verify_backup()

    def on_guess_input_new_round_requested(self, _event: GuessInput.NewRoundRequested) -> None:
        self.action_reset()

    def _focus_tab(self, tab_id: str) -> None:
        if tab_id == "play":
            self.query_one("#guess", Input).focus()
        elif tab_id == "profiles":
            self.query_one("#profile-name", Input).focus()
        elif tab_id == "history":
            self.query_one("#history-search", Input).focus()
        elif tab_id == "leaderboard":
            self.query_one("#leaderboard-player", Input).focus()
        elif tab_id == "settings":
            self.query_one("#settings-theme", Select).focus()
        elif tab_id == "recovery":
            self.query_one("#recovery-backup-path", Input).focus()

    def action_show_tab(self, tab_id: str) -> None:
        self.query_one("#workspace", TabbedContent).active = tab_id
        self._focus_tab(tab_id)

    def action_reset(self) -> None:
        self._reset_round(show_play=True, focus=True)


def run() -> None:
    GuessNovaApp().run()
