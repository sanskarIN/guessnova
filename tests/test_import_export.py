from pathlib import Path

import pytest

from guessnova.import_export import export_state, import_state


def test_export_import_round_trip(tmp_path: Path) -> None:
    payload = {"schema_version": 1, "profiles": {"Player": {}}}
    target = tmp_path / "backup.json"
    export_state(payload, target)
    assert import_state(target) == payload


def test_import_rejects_wrong_format(tmp_path: Path) -> None:
    target = tmp_path / "bad.json"
    target.write_text('{"format":"other","payload":{}}', encoding="utf-8")
    with pytest.raises(ValueError):
        import_state(target)
