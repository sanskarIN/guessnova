import json
from pathlib import Path

from guessnova.constants import SCHEMA_VERSION
from guessnova.doctor_cli import main
from guessnova.import_export import export_state
from guessnova.storage import Storage


def test_doctor_json_reports_fresh_state(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))
    assert main(["--json"]) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["kind"] == "state"
    assert payload["healthy"] is True
    assert payload["state_exists"] is False
    assert payload["current_schema_version"] == 2


def test_doctor_reports_attention_for_schema1_state(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))
    storage = Storage()
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "active_profile": "Legacy",
                "profiles": {"Legacy": {"name": "Legacy", "stats": {}, "settings": {}}},
                "leaderboard": [],
            }
        ),
        encoding="utf-8",
    )
    assert main(["--compact"]) == 2


def test_doctor_repair_requires_confirmation_and_can_repair(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path / "data"))
    storage = Storage()
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "active_profile": "Legacy",
                "profiles": {"Legacy": {"name": "Legacy", "stats": {}, "settings": {}}},
                "leaderboard": [],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("guessnova.doctor_cli.console.input", lambda _prompt: "NO")
    assert main(["--repair"]) == 1
    assert json.loads(storage.path.read_text(encoding="utf-8"))["schema_version"] == 1

    backups = tmp_path / "backups"
    assert main(["--repair", "--yes", "--backup-dir", str(backups)]) == 0
    assert storage.load_raw()["schema_version"] == 2
    assert len(list(backups.glob("*.guessnova.json"))) == 1


def test_doctor_json_repair_emits_single_json_document(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path / "data"))
    storage = Storage()
    storage.data_dir.mkdir(parents=True, exist_ok=True)
    storage.path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "active_profile": "Legacy",
                "profiles": {"Legacy": {"name": "Legacy", "stats": {}, "settings": {}}},
                "leaderboard": [],
            }
        ),
        encoding="utf-8",
    )
    assert main(["--json", "--repair", "--yes"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["kind"] == "state"
    assert payload["healthy"] is True
    assert payload["repair_backup"] is not None


def test_doctor_json_repair_without_yes_is_noninteractive(capsys) -> None:
    assert main(["--json", "--repair"]) == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["healthy"] is False
    assert "requires --yes" in payload["error"]


def test_doctor_can_target_explicit_data_directory(tmp_path: Path, capsys) -> None:
    data_dir = tmp_path / "alternate-data"
    storage = Storage(data_dir)
    storage.save_profile(storage.load_profile("Nova"))

    assert main(["--json", "--data-dir", str(data_dir)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["kind"] == "state"
    assert payload["state_exists"] is True
    assert payload["active_profile"] == "Nova"
    assert payload["profile_count"] == 1


def test_doctor_verifies_backup_without_importing(tmp_path: Path, capsys) -> None:
    backup = tmp_path / "backup.json"
    export_state(
        {"schema_version": SCHEMA_VERSION, "profiles": {"Nova": {"name": "Nova"}}},
        backup,
    )

    assert main(["--json", "--verify-backup", str(backup)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["kind"] == "backup"
    assert payload["valid"] is True
    assert payload["integrity_protected"] is True
    assert payload["profile_count"] == 1


def test_doctor_rejects_backup_verification_with_repair(tmp_path: Path, capsys) -> None:
    backup = tmp_path / "backup.json"
    export_state({"schema_version": SCHEMA_VERSION}, backup)

    assert main(["--json", "--verify-backup", str(backup), "--repair", "--yes"]) == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["healthy"] is False
    assert "cannot be combined" in payload["error"]
