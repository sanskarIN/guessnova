"""Command-line diagnostics for local GuessNova state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .diagnostics import DiagnosticReport, diagnose, repair
from .storage import Storage

console = Console()


def _as_dict(
    report: DiagnosticReport, *, repair_backup: Path | None = None
) -> dict[str, object]:
    return {
        "healthy": report.healthy,
        "state_exists": report.state_exists,
        "readable": report.readable,
        "source_schema_version": report.source_schema_version,
        "current_schema_version": report.current_schema_version,
        "active_profile": report.active_profile,
        "profile_count": report.profile_count,
        "history_entries": report.history_entries,
        "leaderboard_entries": report.leaderboard_entries,
        "deleted_profile_count": report.deleted_profile_count,
        "normalization_changed": report.normalization_changed,
        "issues": list(report.issues),
        "repair_backup": str(repair_backup) if repair_backup is not None else None,
    }


def _render(
    report: DiagnosticReport,
    *,
    as_json: bool,
    compact: bool,
    repair_backup: Path | None = None,
    repair_requested: bool = False,
) -> None:
    payload = _as_dict(report, repair_backup=repair_backup)
    if as_json:
        console.print_json(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return
    if compact:
        console.print(" · ".join(f"{key}={value}" for key, value in payload.items()))
        return

    table = Table(title="GuessNova Doctor · Local State")
    table.add_column("Check")
    table.add_column("Value")
    for key, value in payload.items():
        if key in {"issues", "repair_backup"}:
            continue
        table.add_row(key.replace("_", " ").title(), str(value))
    console.print(table)
    if report.issues:
        console.print("Issues:")
        for issue in report.issues:
            console.print(f"- {issue}")
    if repair_backup is not None:
        console.print(f"Pre-repair backup: {repair_backup}")
    elif repair_requested:
        console.print("No repair was needed.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="guessnova-doctor",
        description="Inspect or safely normalize local GuessNova state without network access.",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--compact", action="store_true", help="emit one concise text line")
    parser.add_argument(
        "--repair",
        action="store_true",
        help="write normalized state after creating an integrity-protected backup",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="confirm a requested repair without an interactive prompt",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="optional directory for the pre-repair backup",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    storage = Storage()
    try:
        report = diagnose(storage)
        backup: Path | None = None
        if args.repair:
            if not args.yes:
                response = console.input(
                    "Type REPAIR to create a backup and normalize local state: "
                ).strip()
                if response != "REPAIR":
                    if not args.json:
                        console.print("Repair cancelled.")
                    _render(
                        report,
                        as_json=args.json,
                        compact=args.compact,
                        repair_requested=True,
                    )
                    return 1
            backup = repair(storage, backup_dir=args.backup_dir)
            report = diagnose(storage)
        _render(
            report,
            as_json=args.json,
            compact=args.compact,
            repair_backup=backup,
            repair_requested=args.repair,
        )
        return 0 if report.healthy else 2
    except (OSError, ValueError) as exc:
        if args.json:
            console.print_json(
                json.dumps(
                    {"healthy": False, "error": str(exc)},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            console.print(f"Error: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
