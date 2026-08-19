from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_docs_links.py"


def _run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_docs_link_checker_accepts_valid_local_external_and_fragment_links(
    tmp_path: Path,
) -> None:
    docs = tmp_path / "docs"
    assets = tmp_path / "assets"
    docs.mkdir()
    assets.mkdir()
    (docs / "guide.md").write_text("# Guide\n", encoding="utf-8")
    (assets / "logo.svg").write_text("<svg></svg>\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "\n".join(
            [
                "# Project",
                "[Guide](docs/guide.md#usage)",
                "[External](https://example.com/docs)",
                "[Section](#project)",
                "![Logo](assets/logo.svg)",
            ]
        ),
        encoding="utf-8",
    )

    result = _run_checker(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Documentation links OK" in result.stdout


def test_docs_link_checker_reports_missing_local_target(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "# Project\n[Missing](docs/missing.md)\n",
        encoding="utf-8",
    )

    result = _run_checker(tmp_path)

    assert result.returncode == 1
    assert "docs/missing.md" in result.stdout
    assert "target does not exist" in result.stdout


def test_docs_link_checker_handles_reference_html_and_code_examples(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    assets = tmp_path / "assets"
    docs.mkdir()
    assets.mkdir()
    (docs / "reference.md").write_text("# Reference\n", encoding="utf-8")
    (assets / "banner.png").write_bytes(b"png")
    (tmp_path / "README.md").write_text(
        "\n".join(
            [
                "# Project",
                "[Reference][ref]",
                "[ref]: docs/reference.md",
                '<img src="assets/banner.png" alt="Banner">',
                "```markdown",
                "[Example only](missing/example.md)",
                "```",
                "`[Inline example](missing/inline.md)`",
            ]
        ),
        encoding="utf-8",
    )

    result = _run_checker(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr


def test_docs_link_checker_rejects_paths_outside_repository(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.md"
    outside.write_text("outside\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "# Project\n[Outside](../outside.md)\n",
        encoding="utf-8",
    )

    result = _run_checker(tmp_path)

    assert result.returncode == 1
    assert "target escapes repository root" in result.stdout
