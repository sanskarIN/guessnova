"""Validated local import/export helpers."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from .constants import SCHEMA_VERSION

MAX_EXPORT_BYTES = 2_000_000
EXPORT_FORMAT = "guessnova-export"
EXPORT_VERSION = 2
LEGACY_EXPORT_VERSION = 1
INTEGRITY_ALGORITHM = "sha256"


def _payload_digest(payload: dict[str, object]) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _validate_schema_version(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("export schema version is invalid")
    if value < 0:
        raise ValueError("export schema version is invalid")
    if value > SCHEMA_VERSION:
        raise ValueError("export uses a newer schema")
    return value


def _payload_schema_version(payload: dict[str, object]) -> int:
    return _validate_schema_version(payload.get("schema_version", 0))


def export_state(payload: dict[str, object], destination: Path) -> Path:
    destination = destination.expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload_schema = _payload_schema_version(payload)
    wrapped = {
        "format": EXPORT_FORMAT,
        "version": EXPORT_VERSION,
        "schema_version": payload_schema,
        "integrity": {
            "algorithm": INTEGRITY_ALGORITHM,
            "payload_sha256": _payload_digest(payload),
        },
        "payload": payload,
    }
    rendered = json.dumps(wrapped, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
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


def _validate_version(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("export version is invalid")
    if value < LEGACY_EXPORT_VERSION:
        raise ValueError("export uses an unsupported version")
    if value > EXPORT_VERSION:
        raise ValueError("export uses a newer version")
    return value


def _validate_integrity(wrapped: dict[str, object], payload: dict[str, object]) -> None:
    integrity = wrapped.get("integrity")
    if not isinstance(integrity, dict):
        raise ValueError("export integrity metadata is missing")
    if integrity.get("algorithm") != INTEGRITY_ALGORITHM:
        raise ValueError("export integrity algorithm is unsupported")
    digest = integrity.get("payload_sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ValueError("export integrity digest is invalid")
    expected = _payload_digest(payload)
    if not hmac.compare_digest(digest, expected):
        raise ValueError("export integrity check failed")


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

    version = _validate_version(wrapped.get("version"))
    payload = wrapped.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("export payload is invalid")

    if version == LEGACY_EXPORT_VERSION:
        # GuessNova <=1.1 coupled wrapper version to schema version. Keep those
        # backups readable; Storage.save_raw performs the forward migration.
        _payload_schema_version(payload)
        return payload

    wrapper_schema = _validate_schema_version(wrapped.get("schema_version"))
    payload_schema = _payload_schema_version(payload)
    if wrapper_schema != payload_schema:
        raise ValueError("export schema metadata does not match payload")
    _validate_integrity(wrapped, payload)
    return payload
