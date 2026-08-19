# Testing

This is the concise testing reference. The canonical detailed strategy is [`testing.md`](testing.md).

The automated suite covers deterministic gameplay, timed/reverse/daily behavior, hints, achievements, profile serialization and recoverable lifecycle operations, bounded/filtered/grouped history, schema-2 migration fixtures, atomic local storage, backup-v2 integrity and legacy compatibility, local doctor/repair behavior, leaderboard ordering, replay integrity, English/Hindi catalogs, CLI parsing, service coordination, and Textual pilot interactions.

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
```

CI additionally builds, validates, installs, checks both the game and doctor packaged entry points, and smoke-tests package artifacts on Ubuntu, Windows, and macOS. Security checks and CodeQL run separately.

## Migration and backup reliability

Committed fixtures under `tests/fixtures/state/` verify real schema-1-to-schema-2 compatibility. Backup tests verify wrapper/state version separation, SHA-256 payload integrity, schema provenance, legacy wrapper-v1 import, and tamper rejection.

## Doctor/repair

Diagnostic and repair tests use isolated temporary state. Repair must create a readable pre-repair backup before normalization and must refuse unreadable/non-object state. JSON doctor output must remain one parseable document.

## Deterministic manual test

```bash
GUESSNOVA_HOME=./.tmp-guessnova GUESSNOVA_SEED=1234 guessnova play --no-save
GUESSNOVA_HOME=./.tmp-guessnova guessnova-doctor --json
```

## UI and accessibility evidence

Textual pilot tests cover initial focus, tab order, Enter submission, range hints, reset, and persisted results. Manual release review must still complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md) on the exact release candidate.

Tests must never depend on network access or a user's real profile/state directory.
