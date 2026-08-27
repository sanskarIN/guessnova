import json
from pathlib import Path

from scripts.verify_manual_release_evidence import main, validate_evidence


def approved_payload() -> dict[str, object]:
    return {
        "release": "1.5.0",
        "status": "approved",
        "reviewer": "Release Reviewer",
        "reviewed_at": "2026-08-24T18:30:00+05:30",
        "checks": {
            "keyboard_only": True,
            "high_contrast": True,
            "reduced_motion": True,
            "english_catalog": True,
            "hindi_catalog": True,
            "screenshots": True,
            "demo_media": True,
        },
        "evidence": {
            "screenshots": ["release-evidence/screenshots/v1.5.0-home.png"],
            "demo_media": ["release-evidence/demo/v1.5.0.webm"],
            "notes": "Reviewed against the intended release candidate.",
        },
    }


def test_approved_manual_evidence_is_accepted() -> None:
    assert validate_evidence(approved_payload(), version="1.5.0") == []


def test_pending_manual_evidence_is_rejected() -> None:
    payload = approved_payload()
    payload["status"] = "pending"
    checks = payload["checks"]
    assert isinstance(checks, dict)
    checks["keyboard_only"] = False

    errors = validate_evidence(payload, version="1.5.0")

    assert "status must be approved" in errors
    assert "checks.keyboard_only must be true" in errors


def test_release_version_and_timezone_are_required() -> None:
    payload = approved_payload()
    payload["release"] = "2.0.0"
    payload["reviewed_at"] = "2026-08-24T18:30:00"

    errors = validate_evidence(payload, version="1.5.0")

    assert "release must equal 1.5.0" in errors
    assert "reviewed_at must be a timezone-aware ISO-8601 timestamp" in errors


def test_screenshot_and_demo_references_are_required() -> None:
    payload = approved_payload()
    evidence = payload["evidence"]
    assert isinstance(evidence, dict)
    evidence["screenshots"] = []
    evidence["demo_media"] = [""]

    errors = validate_evidence(payload, version="1.5.0")

    assert "evidence.screenshots must contain at least one reference" in errors
    assert "evidence.demo_media must contain at least one reference" in errors


def test_cli_rejects_pending_manifest(tmp_path: Path, capsys) -> None:
    payload = approved_payload()
    payload["status"] = "pending"
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert main(["--version", "1.5.0", "--evidence", str(path)]) == 1
    assert "is not approved" in capsys.readouterr().out


def test_cli_accepts_approved_manifest(tmp_path: Path, capsys) -> None:
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(approved_payload()), encoding="utf-8")

    assert main(["--version", "1.5.0", "--evidence", str(path)]) == 0
    assert "is approved" in capsys.readouterr().out
