"""Verify the committed compatibility baseline matches shipped contracts."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

from guessnova.challenge_descriptor import PORTABLE_CHALLENGE_DESCRIPTOR_VERSION
from guessnova.constants import REPLAY_VERSION, SCHEMA_VERSION
from guessnova.doctor_protocol import DOCTOR_REPORT_VERSION
from guessnova.import_export import EXPORT_VERSION, LEGACY_EXPORT_VERSION

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "compatibility.json"
PYPROJECT_PATH = ROOT / "pyproject.toml"
BROWSER_STATE_PATH = ROOT / "src" / "guessnova" / "web" / "browser-state.mjs"
CHALLENGE_DESCRIPTOR_PATH = ROOT / "src" / "guessnova" / "web" / "challenge-descriptor.mjs"


def _javascript_export(source: str, name: str) -> str:
    match = re.search(rf"^export const {re.escape(name)} = (.+?);$", source, re.MULTILINE)
    if match is None:
        raise RuntimeError(f"browser compatibility constant {name} is missing")
    return match.group(1).strip()


def main() -> int:
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    project = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))["project"]
    browser_source = BROWSER_STATE_PATH.read_text(encoding="utf-8")
    challenge_source = CHALLENGE_DESCRIPTOR_PATH.read_text(encoding="utf-8")

    browser_schema = int(_javascript_export(browser_source, "BROWSER_STATE_SCHEMA"))
    storage_key = json.loads(_javascript_export(browser_source, "STORAGE_KEY"))
    browser_descriptor_version = int(
        _javascript_export(challenge_source, "PORTABLE_CHALLENGE_DESCRIPTOR_VERSION")
    )
    if browser_descriptor_version != PORTABLE_CHALLENGE_DESCRIPTOR_VERSION:
        raise SystemExit(
            "portable challenge descriptor versions differ between Python and browser contracts: "
            f"python={PORTABLE_CHALLENGE_DESCRIPTOR_VERSION}, "
            f"browser={browser_descriptor_version}"
        )

    actual = {
        "package_version": project["version"],
        "python_requires": project["requires-python"],
        "python_state_schema": SCHEMA_VERSION,
        "backup_wrapper": EXPORT_VERSION,
        "legacy_backup_wrappers": [LEGACY_EXPORT_VERSION],
        "replay_format": REPLAY_VERSION,
        "doctor_report_protocol": DOCTOR_REPORT_VERSION,
        "browser_state_marker": browser_schema,
        "browser_storage_key": storage_key,
        "portable_interchange_version": None,
        "portable_challenge_descriptor_version": PORTABLE_CHALLENGE_DESCRIPTOR_VERSION,
    }

    if baseline != actual:
        rendered_expected = json.dumps(baseline, indent=2, sort_keys=True)
        rendered_actual = json.dumps(actual, indent=2, sort_keys=True)
        raise SystemExit(
            "compatibility.json does not match shipped contracts\n"
            f"expected baseline:\n{rendered_expected}\n"
            f"actual contracts:\n{rendered_actual}"
        )

    print("GuessNova compatibility baseline verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
