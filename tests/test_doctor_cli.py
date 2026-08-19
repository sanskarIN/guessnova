import json
from pathlib import Path

from guessnova.doctor_cli import main
from guessnova.storage import Storage


def test_doctor_json_reports_fresh_state(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))
    assert main(["--json"]) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
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


def test_doctor_json_repair_requires_yes_without_prompt(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setenv("GUESSNOVA_HOME", str(tmp_path))

    def fail_if_prompted(_prompt: str) -> str:
        raise AssertionError("JSON mode must not prompt")

    monkeypatch.setattr("guessnova.doctor_cli.console.input", fail_if_prompted)
    assert main(["--json", "--repair"]) == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["healthy"] is False
    assert "requires --yes" in payload["error"]


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
    assert payload["healthy"] is True
    assert payload["repair_backup"] is not None
