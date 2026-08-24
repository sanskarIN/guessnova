import json
from pathlib import Path

import pytest

from guessnova.constants import SCHEMA_VERSION
from guessnova.diagnostics import diagnose, repair
from guessnova.import_export import import_state
from guessnova.storage import Storage


def test_diagnose_fresh_storage_is_healthy(tmp_path: Path) -> None:
    report = diagnose(Storage(tmp_path))
    assert report.state_exists is False
    assert report.readable is True
    assert report.healthy is True
    assert report.current_schema_version == SCHEMA_VERSION


def test_diagnose_reports_schema_migration_and_normalization(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "active_profile": "Missing",
                "profiles": {"Alpha": {"name": "Alpha", "stats": {}, "settings": {}}},
                "leaderboard": [],
                "future": "drop-me",
            }
        ),
        encoding="utf-8",
    )
    report = diagnose(storage)
    assert report.readable is True
    assert report.healthy is False
    assert report.source_schema_version == 1
    assert report.current_schema_version == 2
    assert report.active_profile == "Alpha"
    assert report.profile_count == 1
    assert report.normalization_changed is True
    assert any("migrate" in issue for issue in report.issues)


def test_diagnose_invalid_json_is_not_repairable(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_text("{broken", encoding="utf-8")
    report = diagnose(storage)
    assert report.readable is False
    assert report.healthy is False
    with pytest.raises(ValueError, match="not safely repairable"):
        repair(storage)


def test_diagnose_oversized_state_is_not_repairable(tmp_path: Path, monkeypatch) -> None:
    storage = Storage(tmp_path)
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_bytes(b"{" + b"x" * 128 + b"}")
    monkeypatch.setattr("guessnova.storage.MAX_STATE_BYTES", 64)

    report = diagnose(storage)
    assert report.readable is False
    assert report.healthy is False
    assert any("too large" in issue for issue in report.issues)
    with pytest.raises(ValueError, match="not safely repairable"):
        repair(storage)


def test_diagnose_future_schema_is_not_repairable(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_text(
        json.dumps({"schema_version": SCHEMA_VERSION + 1, "profiles": {}}),
        encoding="utf-8",
    )
    report = diagnose(storage)
    assert report.readable is False
    assert report.healthy is False
    assert report.source_schema_version == SCHEMA_VERSION + 1
    assert any("newer" in issue for issue in report.issues)
    with pytest.raises(ValueError, match="not safely repairable"):
        repair(storage)


def test_diagnose_non_object_state_is_not_repairable(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_text("[]", encoding="utf-8")
    report = diagnose(storage)
    assert report.readable is False
    assert any("root" in issue for issue in report.issues)
    with pytest.raises(ValueError, match="not safely repairable"):
        repair(storage)


def test_repair_creates_integrity_protected_backup_before_rewrite(tmp_path: Path) -> None:
    storage = Storage(tmp_path / "data")
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    original = {
        "schema_version": 1,
        "active_profile": "Legacy",
        "profiles": {"Legacy": {"name": "Legacy", "stats": {}, "settings": {}}},
        "leaderboard": [],
    }
    storage.path.write_text(json.dumps(original), encoding="utf-8")

    backup = repair(storage, backup_dir=tmp_path / "backups")
    assert backup is not None
    assert backup.exists()
    assert import_state(backup) == original
    repaired = storage.load_raw()
    assert repaired["schema_version"] == SCHEMA_VERSION
    assert repaired["deleted_profiles"] == {}
    assert diagnose(storage).healthy is True


def test_repair_returns_none_when_state_is_already_normalized(tmp_path: Path) -> None:
    storage = Storage(tmp_path)
    storage.save_raw(
        {
            "schema_version": SCHEMA_VERSION,
            "active_profile": "Player",
            "profiles": {},
            "leaderboard": [],
            "deleted_profiles": {},
        }
    )
    assert repair(storage) is None
