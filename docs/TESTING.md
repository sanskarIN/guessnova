# Testing

The automated suite covers deterministic gameplay, timed behavior, reverse guessing, daily seeds, hints, achievements, profile serialization, atomic local storage, migration, leaderboard ordering, replay integrity, import/export validation, security helpers, settings, CLI parsing, and service coordination.

## Run tests

```bash
pytest
```

## Full development checks

```bash
ruff check .
python -m compileall -q src tests
python scripts/smoke_test.py
```

## Deterministic manual test

```bash
GUESSNOVA_HOME=./.tmp-guessnova GUESSNOVA_SEED=1234 guessnova play --no-save
```

## Test design

Core tests inject targets, seeds, clocks, and temporary data directories. Tests should not depend on internet access or a user's real profile data.
