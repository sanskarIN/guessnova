"""Rich command-line interface."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme as RichTheme

from . import __version__
from .achievements import ACHIEVEMENT_LABELS
from .constants import (
    BMC_URL,
    BUSINESS_EMAILS,
    GITHUB_PROFILE_URL,
    PROJECT_URL,
    SUPPORT_EMAIL,
    WATERMARK,
)
from .daily import daily_game
from .domain import DIFFICULTIES, GameMode, GuessOutcome
from .engine import GuessGame, ReverseGuesser
from .history import HistoryEntry, filter_history, group_history
from .i18n import available_locales, text
from .import_export import export_state, import_state
from .leaderboard import LeaderboardEntry
from .profile_commands import configure_profiles_parser, run_profiles
from .replay import decode_replay, encode_replay
from .service import GameService
from .settings import Settings
from .storage import Storage
from .themes import THEMES, get_theme

console = Console()


def _configure_console(*, plain: bool, settings: Settings | None = None) -> None:
    global console
    active = settings or Settings()
    palette = get_theme("high-contrast" if active.high_contrast else active.theme)
    rich_theme = RichTheme(
        {
            "accent": palette["accent"],
            "success": f"bold {palette['success']}",
            "warning": palette["warning"],
            "error": f"bold {palette['error']}",
            "info": palette["info"],
            "hint": f"dim {palette['hint']}",
        }
    )
    console = Console(
        no_color=plain,
        color_system=None if plain else "auto",
        theme=rich_theme,
    )


def _presentation_settings(args: argparse.Namespace) -> Settings:
    command = getattr(args, "command", None)
    if command not in {
        "play",
        "stats",
        "history",
        "leaderboard",
        "settings",
        "profiles",
        "about",
    }:
        return Settings()
    try:
        return Storage().load_profile(getattr(args, "profile", None)).settings
    except (OSError, ValueError):
        return Settings()


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be at least 1")
    return parsed


def _deterministic_seed(value: int | None) -> int | None:
    if value is not None:
        return value
    env = os.getenv("GUESSNOVA_SEED")
    return int(env) if env else None


def _render_feedback(
    game: GuessGame,
    outcome: GuessOutcome,
    hint: str | None,
    *,
    locale: str,
) -> None:
    if outcome == GuessOutcome.CORRECT:
        console.print(f"[success]{text('play.correct', locale=locale)}[/success]")
    elif outcome == GuessOutcome.TOO_LOW:
        console.print(f"[info]{text('play.too_low', locale=locale)}[/info]")
    elif outcome == GuessOutcome.TOO_HIGH:
        console.print(f"[accent]{text('play.too_high', locale=locale)}[/accent]")
    elif outcome == GuessOutcome.OUT_OF_RANGE:
        console.print(f"[warning]{text('play.out_of_range', locale=locale)}[/warning]")
    elif outcome == GuessOutcome.TIMEOUT:
        console.print(f"[error]{text('play.timeout', locale=locale)}[/error]")
    elif outcome == GuessOutcome.EXHAUSTED:
        console.print(f"[error]{text('play.exhausted', locale=locale)}[/error]")
    if hint and not game.is_finished:
        console.print(f"[hint]{text('play.hint_prefix', locale=locale, hint=hint)}[/hint]")


def _show_onboarding(
    args: argparse.Namespace,
    storage: Storage,
    settings: Settings,
    *,
    profile_name: str,
) -> None:
    if settings.onboarding_complete:
        return
    locale = args.locale
    body = f"{text('onboarding.body', locale=locale)}\n{text('onboarding.settings', locale=locale)}"
    if args.compact:
        console.print(f"{text('onboarding.title', locale=locale)}: {body.replace(chr(10), ' ')}")
    else:
        console.print(Panel.fit(body, title=text("onboarding.title", locale=locale)))
    if not args.no_save:
        profile = storage.load_profile(profile_name)
        profile.settings.onboarding_complete = True
        storage.save_profile(profile)


def play(args: argparse.Namespace) -> int:
    storage = Storage()
    profile = storage.load_profile(args.profile)
    _show_onboarding(args, storage, profile.settings, profile_name=profile.name)
    show_hints = profile.settings.show_smart_hints if args.hints is None else args.hints
    game = (
        daily_game(date.fromisoformat(args.day), args.difficulty)
        if args.mode == GameMode.DAILY.value and args.day
        else daily_game(difficulty=args.difficulty)
        if args.mode == GameMode.DAILY.value
        else GuessGame(args.difficulty, GameMode(args.mode), _deterministic_seed(args.seed))
    )
    diff = game.difficulty
    heading = (
        f"GuessNova · {args.mode.title()} · {args.difficulty.title()} · "
        f"{diff.minimum}–{diff.maximum}"
    )
    if args.compact:
        console.print(heading)
    else:
        console.print(
            Panel.fit(
                f"[bold]GuessNova[/bold]\n{args.mode.title()} · {args.difficulty.title()} · "
                f"{diff.minimum}–{diff.maximum}\n"
                f"{text('play.hint_instruction', locale=args.locale)}"
            )
        )
    while not game.is_finished:
        try:
            raw = console.input(
                text("play.prompt", locale=args.locale, attempts_left=game.attempts_left)
            ).strip()
            command = raw.lower()
            if command in {"q", "quit", "exit"}:
                console.print(text("play.abandoned", locale=args.locale))
                return 1
            if command in {"h", "hint"}:
                try:
                    console.print(f"[hint]{game.request_hint(penalize=args.hint_penalty)}[/hint]")
                except RuntimeError as exc:
                    console.print(f"[warning]{escape(str(exc))}[/warning]")
                continue
            feedback = game.guess(int(raw))
        except ValueError:
            console.print(f"[warning]{text('play.input_invalid', locale=args.locale)}[/warning]")
            continue
        _render_feedback(
            game,
            feedback.outcome,
            feedback.hint if show_hints else None,
            locale=args.locale,
        )

    summary = game.summary()
    console.print(
        text(
            "play.summary",
            locale=args.locale,
            target=summary.target,
            attempts=summary.attempts,
            elapsed=summary.elapsed_seconds,
            hints=summary.hints_used,
        )
    )
    if args.no_save:
        return 0 if summary.won else 2
    profile, unlocked = GameService(storage).record(summary, args.profile)
    console.print(
        text(
            "play.progress",
            locale=args.locale,
            xp=profile.stats.xp,
            win_rate=profile.stats.win_rate,
        )
    )
    for achievement in sorted(unlocked):
        label = ACHIEVEMENT_LABELS.get(achievement, achievement)
        console.print(
            f"[warning]{text('achievement.unlocked', locale=args.locale, label=label)}[/warning]"
        )
    console.print(text("play.replay", locale=args.locale, code=encode_replay(summary)))
    return 0 if summary.won else 2


def reverse(args: argparse.Namespace) -> int:
    engine = ReverseGuesser()
    message = text("reverse.intro", locale=args.locale)
    console.print(message if args.compact else Panel.fit(message))
    while not engine.finished:
        guess = engine.next_guess()
        response = (
            console.input(text("reverse.prompt", locale=args.locale, guess=guess)).strip().lower()
        )
        try:
            engine.respond(response)
        except ValueError as exc:
            console.print(f"[warning]{escape(str(exc))}[/warning]")
            return 2
    console.print(
        f"[success]{text('reverse.solved', locale=args.locale, attempts=engine.attempts)}[/success]"
    )
    return 0


def stats(args: argparse.Namespace) -> int:
    profile = Storage().load_profile(args.profile)
    values = [
        (text("stats.games", locale=args.locale), str(profile.stats.games_played)),
        (text("stats.wins", locale=args.locale), str(profile.stats.games_won)),
        (text("stats.win_rate", locale=args.locale), f"{profile.stats.win_rate:.1%}"),
        (
            text("stats.average_guesses", locale=args.locale),
            f"{profile.stats.average_guesses:.2f}",
        ),
        (text("stats.current_streak", locale=args.locale), str(profile.stats.current_streak)),
        (text("stats.best_streak", locale=args.locale), str(profile.stats.best_streak)),
        (text("stats.xp", locale=args.locale), str(profile.stats.xp)),
        (
            text("stats.achievements", locale=args.locale),
            str(len(profile.stats.achievements)),
        ),
        (text("stats.history_entries", locale=args.locale), str(len(profile.history))),
    ]
    if args.compact:
        console.print(
            f"{profile.name}: " + " · ".join(f"{label}={value}" for label, value in values)
        )
        return 0
    table = Table(title=text("stats.title", locale=args.locale, profile=profile.name))
    table.add_column(text("stats.metric", locale=args.locale))
    table.add_column(text("stats.value", locale=args.locale), justify="right")
    for row in values:
        table.add_row(*row)
    console.print(table)
    return 0


def _render_history_rows(
    args: argparse.Namespace,
    profile_name: str,
    entries: Sequence[HistoryEntry],
    *,
    group_label: str | None = None,
) -> None:
    if args.compact:
        if group_label is not None:
            console.print(f"[{group_label}]")
        for entry in entries:
            result = (
                text("history.win", locale=args.locale)
                if entry.won
                else text("history.loss", locale=args.locale)
            )
            console.print(
                f"{entry.played_at} · {entry.mode}/{entry.difficulty} · {result} · "
                f"attempts={entry.attempts} · time={entry.elapsed_seconds:.2f}s"
            )
        return

    title = text("history.title", locale=args.locale, profile=profile_name)
    if group_label is not None:
        title += " · " + text("history.group", locale=args.locale, value=group_label)
    table = Table(title=title)
    table.add_column(text("history.when", locale=args.locale))
    table.add_column(text("history.mode", locale=args.locale))
    table.add_column(text("history.difficulty", locale=args.locale))
    table.add_column(text("history.result", locale=args.locale))
    table.add_column(text("history.attempts", locale=args.locale), justify="right")
    table.add_column(text("history.time", locale=args.locale), justify="right")
    for entry in entries:
        table.add_row(
            entry.played_at,
            entry.mode,
            entry.difficulty,
            text("history.win", locale=args.locale)
            if entry.won
            else text("history.loss", locale=args.locale),
            str(entry.attempts),
            f"{entry.elapsed_seconds:.2f}s",
        )
    console.print(table)


def history_cmd(args: argparse.Namespace) -> int:
    profile = Storage().load_profile(args.profile)
    filtered = filter_history(
        profile.history,
        mode=args.mode,
        difficulty=args.difficulty,
        result=args.result,
        query=args.search,
        since=args.since,
        until=args.until,
    )
    selected = list(reversed(filtered[-args.limit :]))
    if not selected:
        console.print(text("history.empty", locale=args.locale))
        return 0
    if args.group_by is None:
        _render_history_rows(args, profile.name, selected)
        return 0
    for label, entries in group_history(selected, by=args.group_by).items():
        _render_history_rows(args, profile.name, entries, group_label=label)
    return 0


def leaderboard_cmd(args: argparse.Namespace) -> int:
    entries = Storage().load_leaderboard()
    filtered: list[LeaderboardEntry] = [
        item
        for item in entries
        if (args.mode is None or item.mode == args.mode)
        and (args.difficulty is None or item.difficulty == args.difficulty)
    ]
    selected = filtered[: args.limit]
    if not selected:
        console.print(text("leaderboard.empty", locale=args.locale))
        return 0
    if args.compact:
        for index, entry in enumerate(selected, 1):
            console.print(
                f"{index}. {entry.player} · {entry.mode}/{entry.difficulty} · "
                f"attempts={entry.attempts} · time={entry.elapsed_seconds:.2f}s"
            )
        return 0
    table = Table(title=text("leaderboard.title", locale=args.locale))
    table.add_column("#", justify="right")
    table.add_column(text("leaderboard.player", locale=args.locale))
    table.add_column(text("history.mode", locale=args.locale))
    table.add_column(text("history.difficulty", locale=args.locale))
    table.add_column(text("history.attempts", locale=args.locale), justify="right")
    table.add_column(text("history.time", locale=args.locale), justify="right")
    for index, entry in enumerate(selected, 1):
        table.add_row(
            str(index),
            entry.player,
            entry.mode,
            entry.difficulty,
            str(entry.attempts),
            f"{entry.elapsed_seconds:.2f}s",
        )
    console.print(table)
    return 0


def settings_cmd(args: argparse.Namespace) -> int:
    storage = Storage()
    profile = storage.load_profile(args.profile)
    updates = {
        "theme": args.theme,
        "locale": args.locale_setting,
        "reduced_motion": args.reduced_motion,
        "high_contrast": args.high_contrast,
        "sound": args.sound,
        "show_smart_hints": args.smart_hints,
    }
    changed = False
    for attribute, value in updates.items():
        if value is not None and getattr(profile.settings, attribute) != value:
            setattr(profile.settings, attribute, value)
            changed = True
    if changed:
        storage.save_profile(profile)
    args.locale = profile.settings.locale
    _configure_console(plain=args.plain, settings=profile.settings)
    values = profile.settings.to_dict()
    if args.compact:
        console.print(" · ".join(f"{key}={value}" for key, value in values.items()))
    else:
        table = Table(title=text("settings.title", locale=args.locale, profile=profile.name))
        table.add_column(text("settings.setting", locale=args.locale))
        table.add_column(text("settings.value", locale=args.locale))
        for key, value in values.items():
            table.add_row(key.replace("_", " ").title(), str(value))
        console.print(table)
    if changed:
        console.print(text("settings.saved", locale=args.locale))
    return 0


def about_cmd(args: argparse.Namespace) -> int:
    lines = [
        f"GuessNova {__version__}",
        text("about.description", locale=args.locale),
        text("about.license", locale=args.locale),
        text("about.repository", locale=args.locale, url=PROJECT_URL),
        text("about.github", locale=args.locale, url=GITHUB_PROFILE_URL),
        text("about.business", locale=args.locale, email=BUSINESS_EMAILS[0]),
        text("about.business", locale=args.locale, email=BUSINESS_EMAILS[1]),
        text("about.support", locale=args.locale, email=SUPPORT_EMAIL),
        text("about.funding", locale=args.locale, url=BMC_URL),
        WATERMARK,
    ]
    rendered = "\n".join(lines)
    console.print(
        rendered
        if args.compact
        else Panel.fit(rendered, title=text("about.title", locale=args.locale))
    )
    return 0


def export_cmd(args: argparse.Namespace) -> int:
    storage = Storage()
    path = export_state(storage.load_raw(), Path(args.path))
    console.print(text("data.exported", locale=args.locale, path=path))
    return 0


def import_cmd(args: argparse.Namespace) -> int:
    payload = import_state(Path(args.path))
    Storage().save_raw(payload)
    console.print(text("data.import_complete", locale=args.locale))
    return 0


def replay_cmd(args: argparse.Namespace) -> int:
    summary = decode_replay(args.code)
    console.print(summary)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="guessnova",
        description=text("app.description"),
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        help="disable terminal color for simpler output",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="prefer concise text instead of rich tables/panels",
    )
    sub = parser.add_subparsers(dest="command")

    play_parser = sub.add_parser("play", help="play a challenge")
    play_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES), default="normal")
    play_parser.add_argument(
        "--mode",
        choices=[m.value for m in GameMode if m != GameMode.REVERSE],
        default="classic",
    )
    play_parser.add_argument("--seed", type=int)
    play_parser.add_argument("--day", help="ISO date for reproducible daily challenge")
    play_parser.add_argument("--profile")
    play_parser.add_argument(
        "--hints",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="override saved automatic smart-hint preference",
    )
    play_parser.add_argument(
        "--hint-penalty",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="charge or waive XP penalty for explicit range hints",
    )
    play_parser.add_argument("--no-save", action="store_true")
    play_parser.set_defaults(func=play)

    reverse_parser = sub.add_parser("reverse", help="let GuessNova guess your number")
    reverse_parser.set_defaults(func=reverse)

    stats_parser = sub.add_parser("stats", help="show local profile statistics")
    stats_parser.add_argument("--profile")
    stats_parser.set_defaults(func=stats)

    history_parser = sub.add_parser("history", help="show local session history")
    history_parser.add_argument("--profile")
    history_parser.add_argument(
        "--mode",
        choices=[m.value for m in GameMode if m != GameMode.REVERSE],
    )
    history_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES))
    history_parser.add_argument("--result", choices=("win", "loss"))
    history_parser.add_argument(
        "--search",
        help="match mode, difficulty, result, date, attempts, or seed",
    )
    history_parser.add_argument(
        "--since",
        type=date.fromisoformat,
        help="include entries on/after YYYY-MM-DD",
    )
    history_parser.add_argument(
        "--until",
        type=date.fromisoformat,
        help="include entries on/before YYYY-MM-DD",
    )
    history_parser.add_argument(
        "--group-by",
        choices=("day", "mode", "difficulty", "result"),
        help="group matching sessions before rendering",
    )
    history_parser.add_argument("--limit", type=_positive_int, default=20)
    history_parser.set_defaults(func=history_cmd)

    leaderboard_parser = sub.add_parser("leaderboard", help="show local best results")
    leaderboard_parser.add_argument(
        "--mode",
        choices=[m.value for m in GameMode if m != GameMode.REVERSE],
    )
    leaderboard_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES))
    leaderboard_parser.add_argument("--limit", type=_positive_int, default=10)
    leaderboard_parser.set_defaults(func=leaderboard_cmd)

    settings_parser = sub.add_parser("settings", help="show or update local profile settings")
    settings_parser.add_argument("--profile")
    settings_parser.add_argument("--theme", choices=sorted(THEMES))
    settings_parser.add_argument(
        "--locale",
        dest="locale_setting",
        choices=available_locales(),
    )
    settings_parser.add_argument(
        "--reduced-motion",
        action=argparse.BooleanOptionalAction,
        default=None,
    )
    settings_parser.add_argument(
        "--high-contrast",
        action=argparse.BooleanOptionalAction,
        default=None,
    )
    settings_parser.add_argument(
        "--sound",
        action=argparse.BooleanOptionalAction,
        default=None,
    )
    settings_parser.add_argument(
        "--smart-hints",
        action=argparse.BooleanOptionalAction,
        default=None,
    )
    settings_parser.set_defaults(func=settings_cmd)

    configure_profiles_parser(sub)

    about_parser = sub.add_parser(
        "about",
        help="show project, license, support, and funding details",
    )
    about_parser.set_defaults(func=about_cmd)

    export_parser = sub.add_parser("export", help="export local data")
    export_parser.add_argument("path")
    export_parser.set_defaults(func=export_cmd)

    import_parser = sub.add_parser("import", help="import local data")
    import_parser.add_argument("path")
    import_parser.set_defaults(func=import_cmd)

    replay_parser = sub.add_parser("replay", help="inspect a replay code")
    replay_parser.add_argument("code")
    replay_parser.set_defaults(func=replay_cmd)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    presentation = _presentation_settings(args)
    args.locale = presentation.locale
    _configure_console(plain=args.plain, settings=presentation)
    if not hasattr(args, "func"):
        parser.print_help()
        console.print(f"\n{WATERMARK} · Support: {BMC_URL}")
        return 0
    try:
        if args.command == "profiles":
            return run_profiles(args, console)
        return int(args.func(args))
    except (OSError, ValueError) as exc:
        console.print(f"[error]Error: {escape(str(exc))}[/error]")
        return 2


if __name__ == "__main__":
    sys.exit(main())
