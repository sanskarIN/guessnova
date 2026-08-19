# Testing

This is the concise testing reference. The canonical detailed strategy is [`testing.md`](testing.md).

The automated suite covers deterministic gameplay, timed/reverse/daily behavior, hints, achievements, profile serialization and recoverable lifecycle operations, bounded/filtered/grouped history, atomic local storage, migration, leaderboard ordering, replay integrity, import/export validation, English/Hindi catalogs, CLI parsing, service coordination, and Textual pilot interactions.

## Full development checks

```bash
python -m pip install -e '.[dev]'
ruff check .
ruff format --check .
mypy src/guessnova
pytest --cov=guessnova --cov-report=term-missing
python -m compileall -q src tests scripts
python scripts/smoke_test.py
```

CI additionally builds, validates, installs, launches, and smoke-tests package artifacts on Ubuntu, Windows, and macOS. Security checks and CodeQL run separately.

## Deterministic manual test

```bash
GUESSNOVA_HOME=./.tmp-guessnova GUESSNOVA_SEED=1234 guessnova play --no-save
```

## UI and accessibility evidence

Textual pilot tests cover initial focus, tab order, Enter submission, range hints, reset, and persisted results. Manual release review must still complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md) on the exact release candidate.

Tests must never depend on network access or a user's real profile/state directory.
