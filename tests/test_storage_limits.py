from pathlib import Path

import pytest

from guessnova.constants import SCHEMA_VERSION
from guessnova.import_export import MAX_EXPORT_BYTES
from guessnova.storage import MAX_STATE_BYTES, Storage, read_state_payload


def test_backup_capacity_exceeds_state_capacity() -> None:
    assert MAX_EXPORT_BYTES > MAX_STATE_BYTES


def test_read_state_payload_rejects_content_over_configured_bound(
    tmp_path: Path, monkeypatch
) -> None:
    path = tmp_path / "state.json"
    path.write_bytes(b"{" + b"x" * 128 + b"}")
    monkeypatch.setattr("guessnova.storage.MAX_STATE_BYTES", 64)

    with pytest.raises(ValueError, match="too large"):
        read_state_payload(path)


def test_storage_load_raw_uses_bounded_reader(tmp_path: Path, monkeypatch) -> None:
    storage = Storage(tmp_path)
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_bytes(b"{" + b"x" * 128 + b"}")
    monkeypatch.setattr("guessnova.storage.MAX_STATE_BYTES", 64)

    with pytest.raises(ValueError, match="too large"):
        storage.load_raw()


def test_storage_save_rejects_rendered_state_over_configured_bound(
    tmp_path: Path, monkeypatch
) -> None:
    storage = Storage(tmp_path)
    monkeypatch.setattr("guessnova.storage.MAX_STATE_BYTES", 64)

    with pytest.raises(ValueError, match="too large to save"):
        storage.save_raw(
            {
                "schema_version": SCHEMA_VERSION,
                "active_profile": "Player",
                "profiles": {},
                "leaderboard": [],
                "deleted_profiles": {},
            }
        )
    assert storage.path.exists() is False
