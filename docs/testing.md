# Testing

GuessNova uses pytest with deterministic seeds, injected clocks, and temporary directories so tests do not depend on production credentials or persistent user data.

## Run the suite

```bash
pytest
```

With coverage support:

```bash
pytest --cov=guessnova --cov-report=term-missing
```

## Coverage areas

- Classic and timed guessing outcomes, bounds, attempt exhaustion, and reproducible RNG.
- Reverse binary-search behavior and inconsistent responses.
- Daily challenge reproducibility and smart hints.
- Achievements, XP, streaks, settings, and profile serialization.
- Atomic storage/migration behavior and default application-data selection.
- Leaderboard ranking and serialization.
- Import/export validation and replay-code integrity.
- Input/path safety helpers, application-service coordination, and CLI parser behavior.

## Regression policy

Every reproducible bug should receive a focused regression test where practical. Tests must not read or write the user's real GuessNova state; use pytest `tmp_path` and environment monkeypatching.

## UI testing

Core rules remain outside the UI so most behavior can be tested without terminal automation. Textual pilot/widget tests should cover critical interactive states as the TUI evolves, supplemented by keyboard/manual accessibility checks.
