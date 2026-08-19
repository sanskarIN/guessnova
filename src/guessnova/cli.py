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

from .achievements import ACHIEVEMENT_LABELS
from .constants import BMC_URL, WATERMARK
from .daily import daily_game
from .domain import DIFFICULTIES, GameMode, GuessOutcome
from .engine import GuessGame, ReverseGuesser
from .import_export import export_state, import_state
from .leaderboard import LeaderboardEntry
from .replay import decode_replay, encode_replay
from .service import GameService
from .storage import Storage

console = Console()


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
    game = (
        daily_game(date.fromisoformat(args.day), args.difficulty)
        if args.mode == GameMode.DAILY.value and args.day
        else daily_game(difficulty=args.difficulty)
        if args.mode == GameMode.DAILY.value
        else GuessGame(args.difficulty, GameMode(args.mode), _deterministic_seed(args.seed))
    )
    diff = game.difficulty
    console.print(Panel.fit(f"[bold]GuessNova[/bold]\n{args.mode.title()} · {args.difficulty.title()} · {diff.minimum}–{diff.maximum}"))
    while not game.is_finished:
        try:
            raw = console.input(f"Guess [{game.attempts_left} left] › ").strip()
            if raw.lower() in {"q", "quit", "exit"}:
                console.print("Challenge abandoned.")
                return 1
            feedback = game.guess(int(raw))
        except ValueError:
            console.print("[yellow]Enter a whole number, or q to quit.[/yellow]")
            continue
        _render_feedback(game, feedback.outcome, feedback.hint)

    summary = game.summary()
    console.print(f"Target: [bold]{summary.target}[/bold] · Attempts: {summary.attempts} · {summary.elapsed_seconds:.1f}s")
    if args.no_save:
        return 0 if summary.won else 2
    profile, unlocked = GameService().record(summary, args.profile)
    console.print(f"XP: {profile.stats.xp} · Win rate: {profile.stats.win_rate:.0%}")
    for achievement in sorted(unlocked):
        console.print(f"[bold yellow]Achievement unlocked:[/bold yellow] {ACHIEVEMENT_LABELS.get(achievement, achievement)}")
    console.print(f"Replay: {encode_replay(summary)}")
    return 0 if summary.won else 2


def reverse(_args: argparse.Namespace) -> int:
    engine = ReverseGuesser()
    console.print(Panel.fit("Think of a number from 1 to 100. GuessNova will find it."))
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
    table = Table(title=f"{profile.name} · Statistics")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    values = [
        ("Games", str(profile.stats.games_played)),
        ("Wins", str(profile.stats.games_won)),
        ("Win rate", f"{profile.stats.win_rate:.1%}"),
        ("Best streak", str(profile.stats.best_streak)),
        ("XP", str(profile.stats.xp)),
        ("Achievements", str(len(profile.stats.achievements))),
    ]
    for row in values:
        table.add_row(*row)
    console.print(table)
    return 0


def leaderboard_cmd(args: argparse.Namespace) -> int:
    entries = Storage().load_leaderboard()
    table = Table(title="Local Leaderboard")
    table.add_column("#", justify="right")
    table.add_column("Player")
    table.add_column("Mode")
    table.add_column("Difficulty")
    table.add_column("Attempts", justify="right")
    table.add_column("Time", justify="right")
    filtered: list[LeaderboardEntry] = [
        item for item in entries
        if (args.mode is None or item.mode == args.mode)
        and (args.difficulty is None or item.difficulty == args.difficulty)
    ]
    for index, entry in enumerate(filtered[: args.limit], 1):
        table.add_row(str(index), entry.player, entry.mode, entry.difficulty, str(entry.attempts), f"{entry.elapsed_seconds:.2f}s")
    if filtered:
        console.print(table)
    else:
        console.print("No leaderboard entries yet.")
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
    sub = parser.add_subparsers(dest="command")

    play_parser = sub.add_parser("play", help="play a challenge")
    play_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES), default="normal")
    play_parser.add_argument("--mode", choices=[m.value for m in GameMode if m != GameMode.REVERSE], default="classic")
    play_parser.add_argument("--seed", type=int)
    play_parser.add_argument("--day", help="ISO date for reproducible daily challenge")
    play_parser.add_argument("--profile")
    play_parser.add_argument("--no-save", action="store_true")
    play_parser.set_defaults(func=play)

    reverse_parser = sub.add_parser("reverse", help="let GuessNova guess your number")
    reverse_parser.set_defaults(func=reverse)

    stats_parser = sub.add_parser("stats", help="show local profile statistics")
    stats_parser.add_argument("--profile")
    stats_parser.set_defaults(func=stats)

    leaderboard_parser = sub.add_parser("leaderboard", help="show local best results")
    leaderboard_parser.add_argument("--mode", choices=[m.value for m in GameMode if m != GameMode.REVERSE])
    leaderboard_parser.add_argument("--difficulty", choices=sorted(DIFFICULTIES))
    leaderboard_parser.add_argument("--limit", type=int, default=10)
    leaderboard_parser.set_defaults(func=leaderboard_cmd)

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
    if not hasattr(args, "func"):
        parser.print_help()
        console.print(f"\n{WATERMARK} · Support: {BMC_URL}")
        return 0
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
