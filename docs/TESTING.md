# Testing

This is the concise testing reference. The canonical detailed strategy is [`testing.md`](testing.md).

The automated suite covers deterministic gameplay, timed/reverse/daily behavior, hints, achievements, profile serialization and recoverable lifecycle operations, bounded/filtered/grouped history, schema-2 migration fixtures, bounded atomic local storage, backup-v2 integrity and legacy compatibility, backup importability preflight, Doctor state/backup/repair behavior, leaderboard ordering, replay integrity, English/Hindi catalogs, CLI routing/parsing, service coordination, and Textual pilot interactions.

## Full development checks

```bash
python -m pip install -e '.[dev]'
ruff check .
ruff format --check .
mypy src/guessnova
pytest --cov=guessnova --cov-report=term-missing
python -m compileall -q src tests scripts
python scripts/verify_release_metadata.py
python scripts/smoke_test.py
python -m guessnova --help
python -m guessnova doctor --help
python -m guessnova.doctor_cli --help
```

CI additionally builds, validates, installs, checks the game CLI plus both Doctor entry paths, verifies Doctor version output, and smoke-tests package artifacts on Ubuntu, Windows, and macOS. Security checks and CodeQL run separately.

## Migration, state, and backup reliability

Committed fixtures under `tests/fixtures/state/` verify real schema-1-to-schema-2 compatibility. State tests verify bounded reads/writes and oversized input/output rejection. Backup tests verify wrapper/state version separation, one bounded validated read, SHA-256 payload integrity, schema provenance, legacy wrapper-v1 compatibility, tamper rejection, current normalization preview, and rejection of checksum-valid but unimportable payloads.

The suite also enforces `MAX_EXPORT_BYTES > MAX_STATE_BYTES` so any accepted repairable state can fit inside its mandatory pre-repair backup envelope.

## Doctor/repair

Recommended route: `guessnova doctor`. Compatibility route: `guessnova-doctor`.

Tests cover report protocol version `1`, `state`/`backup`/`error` kinds, stable exit codes, explicit `--data-dir`, read-only `--verify-backup`, package-aligned `--version`, safe confirmation, JSON non-interactivity, backup-before-write repair, and refusal of unreadable/non-object/oversized/future-schema state.

## Deterministic manual test

```bash
GUESSNOVA_HOME=./.tmp-guessnova GUESSNOVA_SEED=1234 guessnova play --no-save
guessnova doctor --json --data-dir ./.tmp-guessnova
```

## UI and accessibility evidence

Textual pilot tests cover initial focus, tab order, Enter submission, range hints, reset, and persisted results. Manual release review must still complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md) on the exact release candidate.

Tests must never depend on network access or a user's real profile/state directory.
