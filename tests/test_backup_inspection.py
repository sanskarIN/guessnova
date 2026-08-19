import json
from pathlib import Path

import pytest

from guessnova.backup_inspection import inspect_backup
from guessnova.constants import SCHEMA_VERSION
from guessnova.import_export import EXPORT_FORMAT, EXPORT_VERSION, export_state


def test_inspect_backup_reports_current_wrapper_metadata(tmp_path: Path) -> None:
    target = tmp_path / "backup.json"
    export_state(
        {
            "schema_version": SCHEMA_VERSION,
            "profiles": {"Player": {"name": "Player"}},
            "leaderboard": [{"ignored": "invalid row is still payload metadata"}],
            "deleted_profiles": {"Old": {}},
        },
        target,
    )

    inspection = inspect_backup(target)
    assert inspection.path == target
    assert inspection.export_version == EXPORT_VERSION
    assert inspection.schema_version == SCHEMA_VERSION
    assert inspection.legacy_wrapper is False
    assert inspection.integrity_protected is True
    assert inspection.integrity_algorithm == "sha256"
    assert inspection.profile_count == 1
    assert inspection.leaderboard_entries == 1
    assert inspection.deleted_profile_count == 1
    assert inspection.size_bytes == target.stat().st_size


def test_inspect_backup_reports_legacy_wrapper_without_integrity(tmp_path: Path) -> None:
    target = tmp_path / "legacy.json"
    target.write_text(
        json.dumps(
            {
                "format": EXPORT_FORMAT,
                "version": 1,
                "payload": {
                    "schema_version": 1,
                    "profiles": {"Legacy": {"name": "Legacy"}},
                    "leaderboard": [],
                },
            }
        ),
        encoding="utf-8",
    )

    inspection = inspect_backup(target)
    assert inspection.export_version == 1
    assert inspection.schema_version == 1
    assert inspection.legacy_wrapper is True
    assert inspection.integrity_protected is False
    assert inspection.integrity_algorithm is None
    assert inspection.profile_count == 1


def test_inspect_backup_reuses_integrity_validation(tmp_path: Path) -> None:
    target = tmp_path / "tampered.json"
    export_state({"schema_version": SCHEMA_VERSION, "profiles": {}}, target)
    wrapped = json.loads(target.read_text(encoding="utf-8"))
    wrapped["payload"]["profiles"] = {"Injected": {}}
    target.write_text(json.dumps(wrapped), encoding="utf-8")

    with pytest.raises(ValueError, match="integrity check"):
        inspect_backup(target)
