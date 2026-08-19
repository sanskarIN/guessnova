"""Command-line diagnostics for local GuessNova state and backups."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from . import __version__
from .backup_inspection import BackupInspection, inspect_backup
from .diagnostics import DiagnosticReport, diagnose, repair
from .doctor_protocol import DOCTOR_REPORT_VERSION, EXIT_ATTENTION, EXIT_CANCELLED, EXIT_OK
from .storage import Storage

console = Console()


def _as_dict(
    report: DiagnosticReport, *, repair_backup: Path | None = None
) -> dict[str, object]:
    return {
        "report_version": DOCTOR_REPORT_VERSION,
        "kind": "state",
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


def _backup_dict(inspection: BackupInspection) -> dict[str, object]:
    return {
        "report_version": DOCTOR_REPORT_VERSION,
        "kind": "backup",
        "valid": True,
        **inspection.to_dict(),
    }


def _render_state(
    report: DiagnosticReport,
    *,
    output_console: Console,
    as_json: bool,
    compact: bool,
    repair_backup: Path | None = None,
    repair_requested: bool = False,
) -> None:
    payload = _as_dict(report, repair_backup=repair_backup)
    if as_json:
        output_console.print_json(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return
    if compact:
        output_console.print(" · ".join(f"{key}={value}" for key, value in payload.items()))
        return

    table = Table(title="GuessNova Doctor · Local State")
    table.add_column("Check")
    table.add_column("Value")
    for key, value in payload.items():
        if key in {"report_version", "kind", "issues", "repair_backup"}:
            continue
        table.add_row(key.replace("_", " ").title(), str(value))
    output_console.print(table)
    if report.issues:
        output_console.print("Issues:")
        for issue in report.issues:
            output_console.print(f"- {issue}")
    if repair_backup is not None:
        output_console.print(f"Pre-repair backup: {repair_backup}")
    elif repair_requested:
        output_console.print("No repair was needed.")


def _render_backup(
    inspection: BackupInspection,
    *,
    output_console: Console,
    as_json: bool,
    compact: bool,
) -> None:
    payload = _backup_dict(inspection)
    if as_json:
        output_console.print_json(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return
    if compact:
        output_console.print(" · ".join(f"{key}={value}" for key, value in payload.items()))
        return

    table = Table(title="GuessNova Doctor · Backup")
    table.add_column("Check")
    table.add_column("Value")
    for key, value in payload.items():
        if key in {"report_version", "kind"}:
            continue
        table.add_row(key.replace("_", " ").title(), str(value))
    output_console.print(table)


def _render_json_error(message: str, *, output_console: Console) -> None:
    output_console.print_json(
        json.dumps(
            {
                "report_version": DOCTOR_REPORT_VERSION,
                "kind": "error",
                "healthy": False,
                "error": message,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def configure_doctor_options(
    parser: argparse.ArgumentParser,
    *,
    include_compact: bool = True,
    include_plain: bool = True,
) -> None:
    """Attach reusable doctor options to a standalone or subcommand parser."""
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    if include_compact:
        parser.add_argument("--compact", action="store_true", help="emit one concise text line")
    if include_plain:
        parser.add_argument("--plain", action="store_true", help="disable terminal color")
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
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="inspect a specific GuessNova data directory instead of the default",
    )
    parser.add_argument(
        "--verify-backup",
        type=Path,
        help="validate a GuessNova backup and report structural metadata without importing it",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"GuessNova Doctor {__version__}",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="guessnova-doctor",
        description="Inspect or safely normalize local GuessNova state without network access.",
    )
    configure_doctor_options(parser)
    return parser


def _validate_mode(args: argparse.Namespace) -> str | None:
    verify_backup = getattr(args, "verify_backup", None)
    if verify_backup is None:
        return None
    conflicting = any(
        (
            getattr(args, "repair", False),
            getattr(args, "yes", False),
            getattr(args, "backup_dir", None) is not None,
            getattr(args, "data_dir", None) is not None,
        )
    )
    if conflicting:
        return "--verify-backup cannot be combined with repair or state-directory options"
    return None


def run_doctor(args: argparse.Namespace, output_console: Console | None = None) -> int:
    """Run doctor behavior for either CLI entry point."""
    active_console = output_console or console
    compact = bool(getattr(args, "compact", False))
    as_json = bool(getattr(args, "json", False))
    repair_requested = bool(getattr(args, "repair", False))
    confirmed = bool(getattr(args, "yes", False))

    mode_error = _validate_mode(args)
    if mode_error is not None:
        if as_json:
            _render_json_error(mode_error, output_console=active_console)
        else:
            active_console.print(f"Error: {mode_error}")
        return EXIT_ATTENTION

    if as_json and repair_requested and not confirmed:
        _render_json_error(
            "--json --repair requires --yes to avoid an interactive prompt",
            output_console=active_console,
        )
        return EXIT_ATTENTION

    verify_backup = getattr(args, "verify_backup", None)
    try:
        if isinstance(verify_backup, Path):
            inspection = inspect_backup(verify_backup)
            _render_backup(
                inspection,
                output_console=active_console,
                as_json=as_json,
                compact=compact,
            )
            return EXIT_OK

        data_dir = getattr(args, "data_dir", None)
        storage = Storage(data_dir if isinstance(data_dir, Path) else None)
        report = diagnose(storage)
        backup: Path | None = None
        if repair_requested:
            if not confirmed:
                response = active_console.input(
                    "Type REPAIR to create a backup and normalize local state: "
                ).strip()
                if response != "REPAIR":
                    active_console.print("Repair cancelled.")
                    _render_state(
                        report,
                        output_console=active_console,
                        as_json=False,
                        compact=compact,
                        repair_requested=True,
                    )
                    return EXIT_CANCELLED
            backup_dir = getattr(args, "backup_dir", None)
            backup = repair(
                storage,
                backup_dir=backup_dir if isinstance(backup_dir, Path) else None,
            )
            report = diagnose(storage)
        _render_state(
            report,
            output_console=active_console,
            as_json=as_json,
            compact=compact,
            repair_backup=backup,
            repair_requested=repair_requested,
        )
        return EXIT_OK if report.healthy else EXIT_ATTENTION
    except (OSError, ValueError) as exc:
        if as_json:
            _render_json_error(str(exc), output_console=active_console)
        else:
            active_console.print(f"Error: {exc}")
        return EXIT_ATTENTION


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    active_console = (
        Console(no_color=True, color_system=None) if getattr(args, "plain", False) else console
    )
    return run_doctor(args, active_console)


if __name__ == "__main__":
    sys.exit(main())
