# Testing

GuessNova uses pytest with deterministic seeds, injected clocks, and temporary directories so tests do not depend on production credentials or persistent user data.

## Full local quality suite

```bash
python -m pip install -e '.[dev]'
ruff check .
ruff format --check .
mypy src/guessnova
pytest --cov=guessnova --cov-report=term-missing
python -m compileall -q src tests scripts
python scripts/smoke_test.py
```

CI also builds the wheel/source distribution and validates package metadata with Twine. Separate workflows perform CodeQL and dependency/secret checks.

## Coverage areas

- Classic/timed guessing outcomes, bounds, attempt exhaustion, and reproducible RNG.
- Automatic smart hints plus explicit narrowed-range hints and optional XP penalties.
- Reverse binary-search behavior and inconsistent responses.
- Daily challenge reproducibility.
- Achievements, XP, streaks, settings, and defensive profile serialization.
- Bounded session-history serialization and invalid-input filtering.
- Atomic storage/migration behavior, corruption errors, and normalized imported state.
- Leaderboard ranking and serialization.
- Import/export validation and replay-code integrity/backward compatibility.
- Input/path safety helpers, application-service coordination, and CLI parser/settings/history behavior.
- End-to-end smoke coverage for gameplay, persistence, replay, backup/restore, achievements, leaderboard, and reverse mode.

## Regression policy

Every reproducible bug should receive a focused regression test where practical. Tests must not read or write the user's real GuessNova state; use pytest `tmp_path`, temporary directories, and environment monkeypatching.

## Determinism

Use explicit game targets, fixed seeds, fixed ISO dates, or injected clocks in tests. Never depend on today's challenge target, wall-clock timing, production state, or network services.

## UI testing

Core rules remain outside the UI so most behavior can be tested without terminal automation. Textual pilot/widget tests should cover critical interactive states as the TUI evolves, supplemented by keyboard/manual accessibility checks.
