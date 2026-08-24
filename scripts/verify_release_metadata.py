"""Verify release-facing version metadata stays synchronized."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from guessnova import __version__

ROOT = Path(__file__).resolve().parents[1]


def _project_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as stream:
        payload = tomllib.load(stream)
    project = payload.get("project")
    if not isinstance(project, dict):
        raise RuntimeError("pyproject.toml is missing [project]")
    version = project.get("version")
    if not isinstance(version, str) or not version:
        raise RuntimeError("pyproject.toml project.version is invalid")
    return version


def _citation_version() -> str:
    content = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    match = re.search(r"(?m)^version:\s*['\"]?([^'\"\s]+)['\"]?\s*$", content)
    if match is None:
        raise RuntimeError("CITATION.cff is missing version metadata")
    return match.group(1)


def main() -> int:
    project_version = _project_version()
    versions = {
        "pyproject.toml": project_version,
        "guessnova.__version__": __version__,
        "CITATION.cff": _citation_version(),
    }
    mismatches = {
        source: version for source, version in versions.items() if version != project_version
    }
    if mismatches:
        detail = ", ".join(f"{source}={version}" for source, version in mismatches.items())
        raise RuntimeError(
            f"release metadata differs from project version {project_version}: {detail}"
        )

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{project_version}]" not in changelog:
        raise RuntimeError(
            f"CHANGELOG.md has no release heading for project version {project_version}"
        )

    print(f"GuessNova release metadata is synchronized at {project_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
