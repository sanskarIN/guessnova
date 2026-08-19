"""Read-only inspection for validated GuessNova backup files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .import_export import LEGACY_EXPORT_VERSION, load_validated_export


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
    validated = load_validated_export(source)
    payload = validated.payload
    return BackupInspection(
        path=validated.path,
        size_bytes=validated.size_bytes,
        export_version=validated.version,
        schema_version=validated.schema_version,
        legacy_wrapper=validated.version == LEGACY_EXPORT_VERSION,
        integrity_protected=validated.integrity_protected,
        integrity_algorithm=validated.integrity_algorithm,
        profile_count=_collection_count(payload.get("profiles")),
        leaderboard_entries=_collection_count(payload.get("leaderboard")),
        deleted_profile_count=_collection_count(payload.get("deleted_profiles")),
    )
