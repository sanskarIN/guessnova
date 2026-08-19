"""Validate local links in repository Markdown documentation.

External URLs are intentionally not fetched: this checker is deterministic, offline, and
suitable for CI. It verifies that repository-local link and image targets exist and do not
escape the repository root.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

INLINE_LINK_RE = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?:<(?P<angle>[^>\n]+)>|(?P<plain>[^\s)\n]+))"
)
REFERENCE_LINK_RE = re.compile(
    r"(?m)^\s{0,3}\[(?!\^)[^\]\n]+\]:\s*(?:<(?P<angle>[^>\n]+)>|(?P<plain>\S+))"
)
HTML_LINK_RE = re.compile(r"(?i)\b(?:href|src)\s*=\s*[\"'](?P<target>[^\"']+)[\"']")
INLINE_CODE_RE = re.compile(r"(?P<ticks>`+)[^\n]*?(?P=ticks)")
SKIP_DIRECTORIES = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "build",
        "dist",
        "htmlcov",
        "venv",
    }
)


@dataclass(frozen=True, slots=True)
class LinkIssue:
    """One invalid repository-local documentation target."""

    source: Path
    target: str
    reason: str


def _strip_fenced_code(content: str) -> str:
    """Remove fenced code content so documentation examples are not treated as links."""

    output: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    for line in content.splitlines():
        stripped = line.lstrip()
        if fence_character is None:
            match = re.match(r"(`{3,}|~{3,})", stripped)
            if match is not None:
                fence = match.group(1)
                fence_character = fence[0]
                fence_length = len(fence)
                output.append("")
                continue
            output.append(line)
            continue

        closing_pattern = rf"{re.escape(fence_character)}{{{fence_length},}}\s*"
        if re.fullmatch(closing_pattern, stripped):
            fence_character = None
            fence_length = 0
        output.append("")

    return "\n".join(output)


def _iter_targets(content: str) -> list[str]:
    """Collect Markdown/reference/HTML link targets outside code examples."""

    searchable = INLINE_CODE_RE.sub("", _strip_fenced_code(content))
    targets: list[str] = []

    for pattern in (INLINE_LINK_RE, REFERENCE_LINK_RE):
        for match in pattern.finditer(searchable):
            target = match.groupdict().get("angle") or match.groupdict().get("plain")
            if target:
                targets.append(target.strip())

    for match in HTML_LINK_RE.finditer(searchable):
        targets.append(match.group("target").strip())

    return targets


def _markdown_files(root: Path) -> list[Path]:
    """Return repository Markdown files while excluding generated/tool directories."""

    return sorted(
        path
        for path in root.rglob("*.md")
        if path.is_file() and not any(part in SKIP_DIRECTORIES for part in path.parts)
    )


def _local_target(root: Path, source: Path, target: str) -> tuple[Path | None, str | None]:
    """Resolve a local link target or explain why it should be ignored/rejected."""

    if not target or target.startswith("#") or target.startswith("//"):
        return None, None

    try:
        parsed = urlsplit(target)
    except ValueError:
        return None, "invalid link syntax"

    if parsed.scheme:
        return None, None

    decoded_path = unquote(parsed.path)
    if not decoded_path:
        return None, None

    root_resolved = root.resolve()
    if decoded_path.startswith("/"):
        candidate = root_resolved / decoded_path.lstrip("/")
    else:
        candidate = source.parent / decoded_path
    candidate = candidate.resolve()

    if not candidate.is_relative_to(root_resolved):
        return candidate, "target escapes repository root"

    return candidate, None


def check_repository(root: Path) -> list[LinkIssue]:
    """Return all invalid local Markdown link targets under *root*."""

    root = root.resolve()
    issues: list[LinkIssue] = []

    for source in _markdown_files(root):
        content = source.read_text(encoding="utf-8")
        for target in _iter_targets(content):
            candidate, resolution_error = _local_target(root, source, target)
            if resolution_error is not None:
                issues.append(LinkIssue(source, target, resolution_error))
                continue
            if candidate is not None and not candidate.exists():
                issues.append(LinkIssue(source, target, "target does not exist"))

    return issues


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check repository-local links in Markdown documentation without network access."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root to scan (defaults to the parent of scripts/).",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    root = args.root.resolve()
    issues = check_repository(root)
    markdown_count = len(_markdown_files(root))

    if issues:
        print(f"Documentation link check failed with {len(issues)} issue(s):")
        for issue in issues:
            try:
                source = issue.source.relative_to(root)
            except ValueError:
                source = issue.source
            print(f"- {source}: {issue.target!r} — {issue.reason}")
        return 1

    print(f"Documentation links OK: {markdown_count} Markdown file(s) checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
