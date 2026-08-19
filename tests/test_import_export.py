import json
from pathlib import Path

import pytest

from guessnova.import_export import MAX_EXPORT_BYTES, export_state, import_state


def test_export_import_round_trip(tmp_path: Path) -> None:
    payload = {"schema_version": 1, "profiles": {"Player": {}}}
    target = tmp_path / "backup.json"
    export_state(payload, target)
    assert import_state(target) == payload
    assert [path.name for path in tmp_path.iterdir()] == ["backup.json"]


def test_import_rejects_wrong_format(tmp_path: Path) -> None:
    target = tmp_path / "bad.json"
    target.write_text('{"format":"other","version":1,"payload":{}}', encoding="utf-8")
    with pytest.raises(ValueError, match="GuessNova"):
        import_state(target)


@pytest.mark.parametrize("version", [None, True, 0, 2, "1"])
def test_import_rejects_invalid_or_unsupported_versions(tmp_path: Path, version: object) -> None:
    target = tmp_path / "bad-version.json"
    target.write_text(
        json.dumps({"format": "guessnova-export", "version": version, "payload": {}}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="version|schema"):
        import_state(target)


def test_import_rejects_invalid_json(tmp_path: Path) -> None:
    target = tmp_path / "broken.json"
    target.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        import_state(target)


def test_import_rejects_oversized_file_before_parsing(tmp_path: Path) -> None:
    target = tmp_path / "huge.json"
    target.write_bytes(b"x" * (MAX_EXPORT_BYTES + 1))
    with pytest.raises(ValueError, match="too large"):
        import_state(target)
