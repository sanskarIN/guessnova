"""Validated local import/export helpers."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

from .constants import SCHEMA_VERSION

MAX_EXPORT_BYTES = 6_000_000
EXPORT_FORMAT = "guessnova-export"
EXPORT_VERSION = 2
LEGACY_EXPORT_VERSION = 1
INTEGRITY_ALGORITHM = "sha256"


@dataclass(frozen=True, slots=True)
class ValidatedExport:
    """A validated backup envelope and its single-read payload."""

    path: Path
    size_bytes: int
    version: int
    schema_version: int
    integrity_protected: bool
    integrity_algorithm: str | None
    payload: dict[str, object]


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


def _read_bounded_json(source: Path) -> tuple[dict[str, object], int]:
    try:
        with source.open("rb") as handle:
            raw = handle.read(MAX_EXPORT_BYTES + 1)
    except OSError:
        raise
    if len(raw) > MAX_EXPORT_BYTES:
        raise ValueError("export file is too large")
    try:
        text = raw.decode("utf-8")
        wrapped = json.loads(text)
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("export contains invalid JSON") from exc
    if not isinstance(wrapped, dict) or wrapped.get("format") != EXPORT_FORMAT:
        raise ValueError("not a GuessNova export")
    return wrapped, len(raw)


def load_validated_export(source: Path) -> ValidatedExport:
    """Read and validate one backup envelope without importing or rewriting state."""
    source = source.expanduser()
    wrapped, size_bytes = _read_bounded_json(source)
    version = _validate_version(wrapped.get("version"))
    payload = wrapped.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("export payload is invalid")

    if version == LEGACY_EXPORT_VERSION:
        # GuessNova <=1.1 coupled wrapper version to schema version. Keep those
        # backups readable; Storage.save_raw performs any required migration.
        schema_version = _payload_schema_version(payload)
        return ValidatedExport(
            path=source,
            size_bytes=size_bytes,
            version=version,
            schema_version=schema_version,
            integrity_protected=False,
            integrity_algorithm=None,
            payload=payload,
        )

    wrapper_schema = _validate_schema_version(wrapped.get("schema_version"))
    payload_schema = _payload_schema_version(payload)
    if wrapper_schema != payload_schema:
        raise ValueError("export schema metadata does not match payload")
    _validate_integrity(wrapped, payload)
    return ValidatedExport(
        path=source,
        size_bytes=size_bytes,
        version=version,
        schema_version=payload_schema,
        integrity_protected=True,
        integrity_algorithm=INTEGRITY_ALGORITHM,
        payload=payload,
    )


def import_state(source: Path) -> dict[str, object]:
    return load_validated_export(source).payload
