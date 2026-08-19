import json
from pathlib import Path

import pytest

from guessnova.constants import SCHEMA_VERSION
from guessnova.import_export import (
    EXPORT_FORMAT,
    EXPORT_VERSION,
    MAX_EXPORT_BYTES,
    export_state,
    import_state,
    load_validated_export,
)


def test_export_import_round_trip(tmp_path: Path) -> None:
    payload = {"schema_version": SCHEMA_VERSION, "profiles": {"Player": {}}}
    target = tmp_path / "backup.json"
    export_state(payload, target)
    assert import_state(target) == payload
    assert [path.name for path in tmp_path.iterdir()] == ["backup.json"]

    wrapped = json.loads(target.read_text(encoding="utf-8"))
    assert wrapped["version"] == EXPORT_VERSION == 2
    assert wrapped["schema_version"] == SCHEMA_VERSION
    assert wrapped["integrity"]["algorithm"] == "sha256"
    assert len(wrapped["integrity"]["payload_sha256"]) == 64


def test_load_validated_export_reports_current_metadata(tmp_path: Path) -> None:
    payload = {"schema_version": SCHEMA_VERSION, "profiles": {"Nova": {}}}
    target = tmp_path / "backup.json"
    export_state(payload, target)

    validated = load_validated_export(target)
    assert validated.path == target
    assert validated.size_bytes == target.stat().st_size
    assert validated.version == EXPORT_VERSION
    assert validated.schema_version == SCHEMA_VERSION
    assert validated.integrity_protected is True
    assert validated.integrity_algorithm == "sha256"
    assert validated.payload == payload


def test_export_records_legacy_payload_schema_for_repair_backup(tmp_path: Path) -> None:
    payload = {"schema_version": 1, "profiles": {}}
    target = tmp_path / "legacy-source-backup.json"
    export_state(payload, target)
    wrapped = json.loads(target.read_text(encoding="utf-8"))
    assert wrapped["version"] == EXPORT_VERSION
    assert wrapped["schema_version"] == 1
    assert import_state(target) == payload


def test_import_accepts_legacy_version1_backup(tmp_path: Path) -> None:
    payload = {"schema_version": 1, "profiles": {"Legacy": {"name": "Legacy"}}}
    target = tmp_path / "legacy.json"
    target.write_text(
        json.dumps({"format": EXPORT_FORMAT, "version": 1, "payload": payload}),
        encoding="utf-8",
    )
    assert import_state(target) == payload
    validated = load_validated_export(target)
    assert validated.version == 1
    assert validated.schema_version == 1
    assert validated.integrity_protected is False
    assert validated.integrity_algorithm is None


def test_import_rejects_wrong_format(tmp_path: Path) -> None:
    target = tmp_path / "bad.json"
    target.write_text('{"format":"other","version":1,"payload":{}}', encoding="utf-8")
    with pytest.raises(ValueError, match="GuessNova"):
        import_state(target)


@pytest.mark.parametrize("version", [None, True, 0, 3, "2"])
def test_import_rejects_invalid_or_unsupported_versions(tmp_path: Path, version: object) -> None:
    target = tmp_path / "bad-version.json"
    target.write_text(
        json.dumps({"format": EXPORT_FORMAT, "version": version, "payload": {}}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="version"):
        import_state(target)


def test_import_rejects_future_schema_in_legacy_backup(tmp_path: Path) -> None:
    target = tmp_path / "future.json"
    target.write_text(
        json.dumps(
            {
                "format": EXPORT_FORMAT,
                "version": 1,
                "payload": {"schema_version": SCHEMA_VERSION + 1},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="newer schema"):
        import_state(target)


def test_export_rejects_future_payload_schema(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="newer schema"):
        export_state(
            {"schema_version": SCHEMA_VERSION + 1},
            tmp_path / "future-export.json",
        )


def test_import_rejects_tampered_version2_payload(tmp_path: Path) -> None:
    target = tmp_path / "backup.json"
    export_state({"schema_version": SCHEMA_VERSION, "profiles": {}}, target)
    wrapped = json.loads(target.read_text(encoding="utf-8"))
    wrapped["payload"]["profiles"] = {"Injected": {}}
    target.write_text(json.dumps(wrapped), encoding="utf-8")
    with pytest.raises(ValueError, match="integrity check"):
        import_state(target)


def test_import_rejects_schema_metadata_mismatch(tmp_path: Path) -> None:
    target = tmp_path / "backup.json"
    export_state({"schema_version": 1, "profiles": {}}, target)
    wrapped = json.loads(target.read_text(encoding="utf-8"))
    wrapped["schema_version"] = 2
    target.write_text(json.dumps(wrapped), encoding="utf-8")
    with pytest.raises(ValueError, match="does not match"):
        import_state(target)


def test_import_rejects_missing_integrity_metadata(tmp_path: Path) -> None:
    target = tmp_path / "missing-integrity.json"
    target.write_text(
        json.dumps(
            {
                "format": EXPORT_FORMAT,
                "version": EXPORT_VERSION,
                "schema_version": SCHEMA_VERSION,
                "payload": {"schema_version": SCHEMA_VERSION},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="integrity"):
        import_state(target)


@pytest.mark.parametrize(
    ("integrity", "message"),
    [
        ({"algorithm": "md5", "payload_sha256": "0" * 64}, "algorithm"),
        ({"algorithm": "sha256", "payload_sha256": "short"}, "digest"),
        ({"algorithm": "sha256", "payload_sha256": 7}, "digest"),
    ],
)
def test_import_rejects_invalid_integrity_metadata(
    tmp_path: Path, integrity: object, message: str
) -> None:
    payload = {"schema_version": SCHEMA_VERSION}
    target = tmp_path / "bad-integrity.json"
    target.write_text(
        json.dumps(
            {
                "format": EXPORT_FORMAT,
                "version": EXPORT_VERSION,
                "schema_version": SCHEMA_VERSION,
                "integrity": integrity,
                "payload": payload,
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=message):
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
