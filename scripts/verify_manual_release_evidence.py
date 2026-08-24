"""Validate truthful manual release evidence before a tagged release can publish."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CHECKS = (
    "keyboard_only",
    "high_contrast",
    "reduced_motion",
    "english_catalog",
    "hindi_catalog",
    "screenshots",
    "demo_media",
)


def _non_empty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _valid_reviewed_at(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_evidence(payload: object, *, version: str) -> list[str]:
    """Return validation errors for one release-evidence payload."""
    if not isinstance(payload, dict):
        return ["evidence root must be a JSON object"]

    errors: list[str] = []
    if payload.get("release") != version:
        errors.append(f"release must equal {version}")
    if payload.get("status") != "approved":
        errors.append("status must be approved")

    reviewer = payload.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        errors.append("reviewer must be a non-empty string")
    if not _valid_reviewed_at(payload.get("reviewed_at")):
        errors.append("reviewed_at must be a timezone-aware ISO-8601 timestamp")

    checks = payload.get("checks")
    if not isinstance(checks, dict):
        errors.append("checks must be a JSON object")
    else:
        for check in REQUIRED_CHECKS:
            if checks.get(check) is not True:
                errors.append(f"checks.{check} must be true")

    evidence = payload.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence must be a JSON object")
    else:
        if not _non_empty_strings(evidence.get("screenshots")):
            errors.append("evidence.screenshots must contain at least one reference")
        if not _non_empty_strings(evidence.get("demo_media")):
            errors.append("evidence.demo_media must contain at least one reference")

    return errors


def evidence_path(version: str) -> Path:
    return ROOT / "docs" / "release_evidence" / f"v{version}.json"


def load_evidence(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"release evidence file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"release evidence is invalid JSON: {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Release version without the v prefix")
    parser.add_argument(
        "--evidence",
        type=Path,
        help="Optional evidence JSON path; defaults to docs/release_evidence/vVERSION.json",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = args.evidence or evidence_path(args.version)
    try:
        payload = load_evidence(path)
    except RuntimeError as exc:
        print(f"Release evidence rejected: {exc}")
        return 1

    errors = validate_evidence(payload, version=args.version)
    if errors:
        print(f"Release evidence for v{args.version} is not approved:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Manual release evidence for v{args.version} is approved: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
