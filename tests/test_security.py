from pathlib import Path

import pytest

from guessnova.security import bounded_int, ensure_within, sanitize_profile_name


def test_sanitize_profile_name() -> None:
    assert sanitize_profile_name("  Nova<>Player!! ") == "NovaPlayer"


def test_bounded_int() -> None:
    assert bounded_int("5", 1, 10) == 5
    with pytest.raises(ValueError):
        bounded_int(11, 1, 10)


def test_ensure_within(tmp_path: Path) -> None:
    inside = tmp_path / "data" / "file.json"
    assert ensure_within(tmp_path, inside) == inside.resolve()
    with pytest.raises(ValueError):
        ensure_within(tmp_path, tmp_path / ".." / "escape")
