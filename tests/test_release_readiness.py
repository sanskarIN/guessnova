import json

from scripts.release_readiness import build_report, main


def test_release_readiness_report_exposes_required_contract() -> None:
    report = build_report("1.5.0")

    assert isinstance(report["current_package_version"], str)
    assert report["target_release_version"] == "1.5.0"
    manual = report["manual_evidence"]
    assert isinstance(manual, dict)
    assert manual["path"] == "docs/release_evidence/v1.5.0.json"
    assert isinstance(manual["approved"], bool)
    assert isinstance(manual["errors"], list)
    preparation = report["next_major_preparation"]
    assert isinstance(preparation, dict)
    assert preparation["baseline_files_present"] is True
    assert isinstance(preparation["development_entry_blocked"], bool)
    assert report["next_action"] in {
        "complete_truthful_manual_release_evidence",
        "advance_release_metadata_and_run_exact_head_gates",
        "run_exact_head_tagged_release_gates",
    }
    assert "CI/Security/CodeQL" in report["note"]


def test_release_readiness_cli_emits_json(capsys) -> None:
    assert main(["--target-version", "1.5.0", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["target_release_version"] == "1.5.0"
    assert "manual_evidence" in payload
    assert "next_major_preparation" in payload
