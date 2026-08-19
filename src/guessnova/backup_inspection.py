"""Read-only inspection for validated GuessNova backup files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .import_export import EXPORT_VERSION, LEGACY_EXPORT_VERSION, import_state


@dataclass(frozen=True, slots=True)
class BackupInspection:
    path: Path
    size_bytes: int
    export_version: int
    schema_version: int
    legacy_wrapper: bool
    integrity_protected: bool
    integrity_algorithm: str | None
    profile_count: int
    leaderboard_entries: int
    deleted_profile_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "size_bytes": self.size_bytes,
            "export_version": self.export_version,
            "schema_version": self.schema_version,
            "legacy_wrapper": self.legacy_wrapper,
            "integrity_protected": self.integrity_protected,
            "integrity_algorithm": self.integrity_algorithm,
            "profile_count": self.profile_count,
            "leaderboard_entries": self.leaderboard_entries,
            "deleted_profile_count": self.deleted_profile_count,
        }


def _collection_count(value: object) -> int:
    return len(value) if isinstance(value, (dict, list)) else 0


def inspect_backup(source: Path) -> BackupInspection:
    """Validate a backup and return non-secret structural metadata without importing it."""
    source = source.expanduser()
    payload = import_state(source)
    wrapped = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(wrapped, dict):  # import_state already enforces this invariant.
        raise ValueError("not a GuessNova export")

    version = wrapped.get("version")
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError("export version is invalid")
    if version not in {LEGACY_EXPORT_VERSION, EXPORT_VERSION}:
        raise ValueError("export version is unsupported")

    schema = payload.get("schema_version", 0)
    if isinstance(schema, bool) or not isinstance(schema, int):
        raise ValueError("export schema version is invalid")

    integrity = wrapped.get("integrity")
    algorithm = integrity.get("algorithm") if isinstance(integrity, dict) else None
    integrity_algorithm = algorithm if isinstance(algorithm, str) else None

    return BackupInspection(
        path=source,
        size_bytes=source.stat().st_size,
        export_version=version,
        schema_version=schema,
        legacy_wrapper=version == LEGACY_EXPORT_VERSION,
        integrity_protected=version == EXPORT_VERSION,
        integrity_algorithm=integrity_algorithm,
        profile_count=_collection_count(payload.get("profiles")),
        leaderboard_entries=_collection_count(payload.get("leaderboard")),
        deleted_profile_count=_collection_count(payload.get("deleted_profiles")),
    )
