"""Validated local import/export helpers."""

from __future__ import annotations

import json
from pathlib import Path

from .constants import SCHEMA_VERSION


def export_state(payload: dict[str, object], destination: Path) -> Path:
    destination = destination.expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    wrapped = {"format": "guessnova-export", "version": SCHEMA_VERSION, "payload": payload}
    destination.write_text(json.dumps(wrapped, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination


def import_state(source: Path) -> dict[str, object]:
    wrapped = json.loads(source.expanduser().read_text(encoding="utf-8"))
    if not isinstance(wrapped, dict) or wrapped.get("format") != "guessnova-export":
        raise ValueError("not a GuessNova export")
    if int(wrapped.get("version", -1)) > SCHEMA_VERSION:
        raise ValueError("export uses a newer schema")
    payload = wrapped.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("export payload is invalid")
    return payload
