"""Rich command-line interface."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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
from .import_export import export_state, import_state
from .leaderboard import LeaderboardEntry
from .replay import decode_replay, encode_replay
from .service import GameService
from .storage import Storage
from .themes import THEMES

console = Console()


def _configure_console(*, plain: bool) -> None:
    global console
    console = Console(no_color=plain, color_system=None if plain else "auto")


def _deterministic_seed(value: int | None) -> int | None:
    if value is not None:
        return value
    env = os.getenv("GUESSNOVA_SEED")
    return int(env) if env else None


def _render_feedback(game: GuessGame, outcome: GuessOutcome, hint: str | None) -> None:
    if outcome == GuessOutcome.CORRECT:
        console.print("[bold green]Correct! A new star is born.[/bold green]")
    elif outcome == GuessOutcome.TOO_LOW:
        console.print("[cyan]Too low.[/cyan]")
    elif outcome == GuessOutcome.TOO_HIGH:
        console.print("[magenta]Too high.[/magenta]")
    elif outcome == GuessOutcome.OUT_OF_RANGE:
        console.print("[yellow]That number is outside this challenge range.[/yellow]")
    elif outcome == GuessOutcome.TIMEOUT:
        console.print("[bold red]Time expired.[/bold red]")
    elif outcome == GuessOutcome.EXHAUSTED:
        console.print("[bold red]No attempts remain.[/bold red]")
    if hint and not game.is_finished:
        console.print(f"[dim]Hint: {hint}[/dim]")


def play(args: argparse.Namespace) -> int:
    storage = Storage()
    profile = storage.load_profile(args.profile)
    show_hints = profile.settings.show_smart_hints if args.hints is None else args.hints
    game = (
        daily_game(date.fromisoformat(args.day), args.difficulty)
        if args.mode == GameMode.DAILY.value and args.day
        else daily_game(difficulty=args.difficulty)
        if args.mode == GameMode.DAILY.value
        else GuessGame(args.difficulty, GameMode(args.mode), _deterministic_seed(args.seed))
    )
    diff = game.difficulty
    heading = f"GuessNova · {args.mode.title()} · {args.difficulty.title()} · {diff.minimum}–{diff.maximum}"
    if args.compact:
        console.print(heading)
    else:
        console.print(
            Panel.fit(
                f"[bold]GuessNova[/bold]\n{args.mode.title()} · {args.difficulty.title()} · "
                f"{diff.minimum}–{diff.maximum}\nType 'hint' for a narrowed range clue."
            )
        )
    while not game.is_finished:
        try:
            raw = console.input(f"Guess [{game.attempts_left} left] › ").strip()
            command = raw.lower()
            if command in {"q", "quit", "exit"}:
                console.print("Challenge abandoned.")
                return 1
            if command in {"h", "hint"}:
                try:
                    console.print(
                        f"[dim]{game.request_hint(penalize=args.hint_penalty)}[/dim]"
                    )
                except RuntimeError as exc:
                    console.print(f"[yellow]{exc}[/yellow]")
                continue
            feedback = game.guess(int(raw))
        except ValueError:
            console.print("[yellow]Enter a whole number, 'hint', or q to quit.[/yellow]")
            continue
        _render_feedback(game, feedback.outcome, feedback.hint if show_hints else None)

    summary = game.summary()
    console.print(
        f"Target: [bold]{summary.target}[/bold] · Attempts: {summary.attempts} · "
        f"{summary.elapsed_seconds:.1f}s · Hints: {summary.hints_used}"
    )
    if args.no_save:
        return 0 if summary.won else 2
    profile, unlocked = GameService(storage).record(summary, args.profile)
    console.print(f"XP: {profile.stats.xp} · Win rate: {profile.stats.win_rate:.0%}")
    for achievement in sorted(unlocked):
        console.print(
            f"[bold yellow]Achievement unlocked:[/bold yellow] "
            f"{ACHIEVEMENT_LABELS.get(achievement, achievement)}"
        )
    console.print(f"Replay: {encode_replay(summary)}")
    return 0 if summary.won else 2


def reverse(args: argparse.Namespace) -> int:
    engine = ReverseGuesser()
    message = "Think of a number from 1 to 100. GuessNova will find it."
    console.print(message if args.compact else Panel.fit(message))
    while not engine.finished:
        guess = engine.next_guess()
        response = console.input(f"Is it {guess}? [higher/lower/correct] › ").strip().lower()
        try:
            engine.respond(response)
        except ValueError as exc:
            console.print(f"[yellow]{exc}[/yellow]")
            return 2
    console.print(f"[bold green]Solved in {engine.attempts} guesses.[/bold green]")
    return 0


def stats(args: argparse.Namespace) -> int:
    profile = Storage().load_profile(args.profile)
    values = [
        ("Games", str(profile.stats.games_played)),
        ("Wins", str(profile.stats.games_won)),
        ("Win rate", f"{profile.stats.win_rate:.1%}"),
        ("Average guesses", f"{profile.stats.average_guesses:.2f}"),
        ("Current streak", str(profile.stats.current_streak)),
        ("Best streak", str(profile.stats.best_streak)),
        ("XP", str(profile.stats.xp)),
        ("Achievements", str(len(profile.stats.achievements))),
        ("History entries", str(len(profile.history))),
    ]
    if args.compact:
        console.print(
            f"{profile.name}: " + " · ".join(f"{label}={value}" for label, value in values)
        )
        return 0
    table = Table(title=f"{profile.name} · Statistics")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    for row in values:
        table.add_row(*row)
    console.print(table)
    return 0


def history_cmd(args: argparse.Namespace) -> int:
    profile = Storage().load_profile(args.profile)
    filtered = [
        entry
        for entry in profile.history
        if (args.mode is None or entry.mode == args.mode)
        and (args.difficulty is None or entry.difficulty == args.difficulty)
    ]
    selected = list(reversed(filtered[-args.limit :]))
    if not selected:
        console.print("No matching session history yet.")
        return 0
    if args.compact:
        for entry in selected:
            result = "win" if entry.won else "loss"
            console.print(
                f"{entry.played_at} · {entry.mode}/{entry.difficulty} · {result} · "
                f"attempts={entry.attempts} · time={entry.elapsed_seconds:.2f}s"
            )
        return 0
    table = Table(title=f"{profile.name} · Session History")
    table.add_column("When")
    table.add_column("Mode")
    table.add_column("Difficulty")
    table.add_column("Result")
    table.add_column("Attempts", justify="right")
    table.add_column("Time", justify="right")
    for entry in selected:
        table.add_row(
            entry.played_at,
            entry.mode,
            entry.difficulty,
            "Win" if entry.won else "Loss",
            str(entry.attempts),
            f"{entry.elapsed_seconds:.2f}s",
        )
    console.print(table)
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
        console.print("No leaderboard entries yet.")
        return 0
    if args.compact:
        for index, entry in enumerate(selected, 1):
            console.print(
                f"{index}. {entry.player} · {entry.mode}/{entry.difficulty} · "
                f"attempts={entry.attempts} · time={entry.elapsed_seconds:.2f}s"
            )
        return 0
    table = Table(title="Local Leaderboard")
    table.add_column("#", justify="right")
    table.add_column("Player")
    table.add_column("Mode")
    table.add_column("Difficulty")
    table.add_column("Attempts", justify="right")
    table.add_column("Time", justify="right")
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
    values = profile.settings.to_dict()
    if args.compact:
        console.print(" · ".join(f"{key}={value}" for key, value in values.items()))
    else:
        table = Table(title=f"{profile.name} · Settings")
        table.add_column("Setting")
        table.add_column("Value")
        for key, value in values.items():
            table.add_row(key.replace("_", " ").title(), str(value))
        console.print(table)
    if changed:
        console.print("Settings saved locally.")
    return 0


def about_cmd(args: argparse.Namespace) -> int:
    lines = [
        f"GuessNova {__version__}",
        "Privacy-first open-source number guessing game",
        "License: MIT",
        f"Repository: {PROJECT_URL}",
        f"GitHub: {GITHUB_PROFILE_URL}",
        f"Business: {BUSINESS_EMAILS[0]}",
        f"Business: {BUSINESS_EMAILS[1]}",
        f"Support: {SUPPORT_EMAIL}",
        f"Buy Me a Coffee: {BMC_URL}",
        WATERMARK,
    ]
    text = "\n".join(lines)
    console.print(text if args.compact else Panel.fit(text, title="About GuessNova"))
    return 0


def export_cmd(args: argparse.Namespace) -> int:
    storage = Storage()
    path = export_state(storage.load_raw(), Path(args.path))
    console.print(f"Exported to {path}")
    return 0


def import_cmd(args: argparse.Namespace) -> int:
    payload = import_state(Path(args.path))
    Storage().save_raw(payload)
    console.print("Import complete.")
    return 0


def replay_cmd(args: argparse.Namespace) -> int:
    summary = decode_replay(args.code)
    console.print(summary)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="guessnova", description="A modern number guessing game")
    parser.add_argument("--plain", action="store_true", help="disable terminal color for simpler output")
    parser.add_argument(
        "--compact", action="store_true", help="prefer concise text instead of rich tables/panels"
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
        "--mode", choices=[m.value for m in GameMode if m != GameMode.REVERSE]
    )
    history_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES))
    history_parser.add_argument("--limit", type=int, default=20)
    history_parser.set_defaults(func=history_cmd)

    leaderboard_parser = sub.add_parser("leaderboard", help="show local best results")
    leaderboard_parser.add_argument(
        "--mode", choices=[m.value for m in GameMode if m != GameMode.REVERSE]
    )
    leaderboard_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES))
    leaderboard_parser.add_argument("--limit", type=int, default=10)
    leaderboard_parser.set_defaults(func=leaderboard_cmd)

    settings_parser = sub.add_parser("settings", help="show or update local profile settings")
    settings_parser.add_argument("--profile")
    settings_parser.add_argument("--theme", choices=sorted(THEMES))
    settings_parser.add_argument(
        "--reduced-motion", action=argparse.BooleanOptionalAction, default=None
    )
    settings_parser.add_argument(
        "--high-contrast", action=argparse.BooleanOptionalAction, default=None
    )
    settings_parser.add_argument("--sound", action=argparse.BooleanOptionalAction, default=None)
    settings_parser.add_argument(
        "--smart-hints", action=argparse.BooleanOptionalAction, default=None
    )
    settings_parser.set_defaults(func=settings_cmd)

    about_parser = sub.add_parser(
        "about", help="show project, license, support, and funding details"
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
    _configure_console(plain=args.plain)
    if not hasattr(args, "func"):
        parser.print_help()
        console.print(f"\n{WATERMARK} · Support: {BMC_URL}")
        return 0
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
