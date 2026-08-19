import json
from pathlib import Path

from guessnova.constants import SCHEMA_VERSION
from guessnova.entrypoint import main
from guessnova.import_export import export_state


def test_primary_entrypoint_routes_doctor_json_to_explicit_data_dir(
    tmp_path: Path, capsys
) -> None:
    assert main(["doctor", "--json", "--data-dir", str(tmp_path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["kind"] == "state"
    assert payload["state_exists"] is False


def test_primary_entrypoint_forwards_global_compact_flag_to_doctor(
    tmp_path: Path, capsys
) -> None:
    assert main(["--compact", "doctor", "--data-dir", str(tmp_path)]) == 0
    output = capsys.readouterr().out
    assert "kind=state" in output
    assert "state_exists=False" in output


def test_primary_entrypoint_forwards_global_plain_flag_to_doctor(
    tmp_path: Path, capsys
) -> None:
    assert main(["--plain", "doctor", "--data-dir", str(tmp_path)]) == 0
    output = capsys.readouterr().out
    assert "GuessNova Doctor" in output


def test_primary_entrypoint_routes_backup_verification(tmp_path: Path, capsys) -> None:
    backup = tmp_path / "backup.json"
    export_state({"schema_version": SCHEMA_VERSION, "profiles": {}}, backup)

    assert main(["doctor", "--json", "--verify-backup", str(backup)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["kind"] == "backup"
    assert payload["valid"] is True


def test_primary_help_mentions_recovery_command(capsys) -> None:
    assert main(["--help"]) == 0
    output = capsys.readouterr().out
    assert "guessnova doctor --help" in output
