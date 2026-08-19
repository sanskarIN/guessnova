"""Validated local import/export helpers."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from .constants import SCHEMA_VERSION

MAX_EXPORT_BYTES = 2_000_000
EXPORT_FORMAT = "guessnova-export"


def export_state(payload: dict[str, object], destination: Path) -> Path:
    destination = destination.expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    wrapped = {"format": EXPORT_FORMAT, "version": SCHEMA_VERSION, "payload": payload}
    rendered = json.dumps(wrapped, indent=2, sort_keys=True) + "\n"
    if len(rendered.encode("utf-8")) > MAX_EXPORT_BYTES:
        raise ValueError("export is too large")

    temp_path: Path | None = None
    try:
        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=destination.parent,
            delete=False,
        ) as temp:
            temp.write(rendered)
            temp.flush()
            os.fsync(temp.fileno())
            temp_path = Path(temp.name)
        temp_path.replace(destination)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)
    return destination


def import_state(source: Path) -> dict[str, object]:
    source = source.expanduser()
    if source.stat().st_size > MAX_EXPORT_BYTES:
        raise ValueError("export file is too large")
    try:
        wrapped = json.loads(source.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("export contains invalid JSON") from exc
    if not isinstance(wrapped, dict) or wrapped.get("format") != EXPORT_FORMAT:
        raise ValueError("not a GuessNova export")

    version = wrapped.get("version")
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError("export version is invalid")
    if version > SCHEMA_VERSION:
        raise ValueError("export uses a newer schema")
    if version != SCHEMA_VERSION:
        raise ValueError("export uses an unsupported schema")

    payload = wrapped.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("export payload is invalid")
    return payload
