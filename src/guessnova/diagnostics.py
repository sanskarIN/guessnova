"""Local-only state diagnostics and repair helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .constants import DEFAULT_PROFILE, SCHEMA_VERSION
from .import_export import export_state
from .storage import Storage, normalize_state


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    state_exists: bool
    readable: bool
    source_schema_version: int | None
    current_schema_version: int
    active_profile: str
    profile_count: int
    history_entries: int
    leaderboard_entries: int
    deleted_profile_count: int
    normalization_changed: bool
    issues: tuple[str, ...]

    @property
    def healthy(self) -> bool:
        return self.readable and not self.issues


def _count_collection(value: object) -> int:
    return len(value) if isinstance(value, (dict, list)) else 0


def _history_count(profiles: object) -> int:
    if not isinstance(profiles, dict):
        return 0
    total = 0
    for raw_profile in profiles.values():
        if not isinstance(raw_profile, dict):
            continue
        history = raw_profile.get("history")
        if isinstance(history, list):
            total += len(history)
    return total


def _source_schema(payload: dict[str, object]) -> int | None:
    value = payload.get("schema_version", 0)
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def diagnose(storage: Storage) -> DiagnosticReport:
    """Inspect the state file without mutating it or making network calls."""
    if not storage.path.exists():
        return DiagnosticReport(
            state_exists=False,
            readable=True,
            source_schema_version=None,
            current_schema_version=SCHEMA_VERSION,
            active_profile=DEFAULT_PROFILE,
            profile_count=0,
            history_entries=0,
            leaderboard_entries=0,
            deleted_profile_count=0,
            normalization_changed=False,
            issues=(),
        )

    try:
        decoded = json.loads(storage.path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return DiagnosticReport(
            state_exists=True,
            readable=False,
            source_schema_version=None,
            current_schema_version=SCHEMA_VERSION,
            active_profile=DEFAULT_PROFILE,
            profile_count=0,
            history_entries=0,
            leaderboard_entries=0,
            deleted_profile_count=0,
            normalization_changed=False,
            issues=("state file cannot be decoded as valid UTF-8 JSON",),
        )

    if not isinstance(decoded, dict):
        return DiagnosticReport(
            state_exists=True,
            readable=False,
            source_schema_version=None,
            current_schema_version=SCHEMA_VERSION,
            active_profile=DEFAULT_PROFILE,
            profile_count=0,
            history_entries=0,
            leaderboard_entries=0,
            deleted_profile_count=0,
            normalization_changed=False,
            issues=("state file root is not an object",),
        )

    payload: dict[str, object] = decoded
    source_schema = _source_schema(payload)
    try:
        normalized = normalize_state(payload)
    except ValueError as exc:
        return DiagnosticReport(
            state_exists=True,
            readable=False,
            source_schema_version=source_schema,
            current_schema_version=SCHEMA_VERSION,
            active_profile=DEFAULT_PROFILE,
            profile_count=0,
            history_entries=0,
            leaderboard_entries=0,
            deleted_profile_count=0,
            normalization_changed=False,
            issues=(str(exc),),
        )

    issues: list[str] = []
    if source_schema != SCHEMA_VERSION:
        issues.append(
            f"state schema {source_schema if source_schema is not None else 'invalid'} "
            f"will migrate to {SCHEMA_VERSION}"
        )
    if normalized != payload:
        issues.append("state normalization would change stored data")

    profiles = normalized.get("profiles", {})
    leaderboard = normalized.get("leaderboard", [])
    deleted = normalized.get("deleted_profiles", {})
    return DiagnosticReport(
        state_exists=True,
        readable=True,
        source_schema_version=source_schema,
        current_schema_version=SCHEMA_VERSION,
        active_profile=str(normalized.get("active_profile", DEFAULT_PROFILE)),
        profile_count=_count_collection(profiles),
        history_entries=_history_count(profiles),
        leaderboard_entries=_count_collection(leaderboard),
        deleted_profile_count=_count_collection(deleted),
        normalization_changed=normalized != payload,
        issues=tuple(issues),
    )


def repair(storage: Storage, *, backup_dir: Path | None = None) -> Path | None:
    """Normalize a readable state file, creating a backup before rewriting it."""
    report = diagnose(storage)
    if not report.state_exists:
        return None
    if not report.readable:
        raise ValueError("state is not safely repairable; restore or replace the invalid state file")

    decoded = json.loads(storage.path.read_text(encoding="utf-8"))
    if not isinstance(decoded, dict):
        raise ValueError("state file root must be an object")
    payload: dict[str, object] = decoded
    normalized = normalize_state(payload)
    if normalized == payload:
        return None

    destination_root = (backup_dir or storage.data_dir).expanduser()
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    backup = destination_root / f"state-pre-repair-{timestamp}.guessnova.json"
    counter = 1
    while backup.exists():
        backup = destination_root / f"state-pre-repair-{timestamp}-{counter}.guessnova.json"
        counter += 1
    export_state(payload, backup)
    storage.save_raw(normalized)
    return backup
