"""Report repository-local release readiness without fabricating external/manual evidence."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
from typing import Any

from scripts.verify_manual_release_evidence import evidence_path, load_evidence, validate_evidence

ROOT = Path(__file__).resolve().parents[1]


def project_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as stream:
        payload = tomllib.load(stream)
    project = payload.get("project")
    if not isinstance(project, dict):
        raise RuntimeError("pyproject.toml is missing [project]")
    version = project.get("version")
    if not isinstance(version, str) or not version:
        raise RuntimeError("pyproject.toml project.version is invalid")
    return version


def build_report(target_version: str) -> dict[str, Any]:
    current_version = project_version()
    path = evidence_path(target_version)
    evidence_errors: list[str]
    try:
        payload = load_evidence(path)
    except RuntimeError as exc:
        evidence_errors = [str(exc)]
    else:
        evidence_errors = validate_evidence(payload, version=target_version)

    manual_approved = not evidence_errors
    next_major_ready = all(
        (ROOT / path_name).is_file()
        for path_name in (
            "compatibility.json",
            "docs/v2_roadmap.md",
            "docs/v2_release_checklist.md",
        )
    )

    if not manual_approved:
        next_action = "complete_truthful_manual_release_evidence"
    elif current_version != target_version:
        next_action = "advance_release_metadata_and_run_exact_head_gates"
    else:
        next_action = "run_exact_head_tagged_release_gates"

    return {
        "current_package_version": current_version,
        "target_release_version": target_version,
        "manual_evidence": {
            "approved": manual_approved,
            "path": str(path.relative_to(ROOT)),
            "errors": evidence_errors,
        },
        "next_major_preparation": {
            "baseline_files_present": next_major_ready,
            "development_entry_blocked": not manual_approved,
        },
        "next_action": next_action,
        "note": (
            "External CI/Security/CodeQL status is intentionally not inferred by this offline report. "
            "Those gates must be verified on the exact candidate commit."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-version", required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = build_report(args.target_version)
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        manual = report["manual_evidence"]
        print(f"Current package: {report['current_package_version']}")
        print(f"Target release: {report['target_release_version']}")
        print(f"Manual evidence approved: {manual['approved']}")
        print(f"Next action: {report['next_action']}")
        for error in manual["errors"]:
            print(f"- {error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
