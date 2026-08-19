# Testing

GuessNova uses pytest with deterministic seeds, injected clocks, temporary directories, and Textual's test pilot so tests do not depend on production credentials or persistent user data.

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

CI also builds, validates, installs, starts the CLI, and smoke-tests distributions on Ubuntu, Windows, and macOS. Separate workflows perform CodeQL and dependency/secret checks.

## Coverage areas

- Classic/timed guessing outcomes, bounds, attempt exhaustion, and reproducible RNG.
- Automatic smart hints plus explicit narrowed-range hints and optional XP penalties.
- Reverse binary-search behavior and inconsistent responses.
- Daily challenge reproducibility.
- Achievements, XP, streaks, settings, and defensive profile serialization.
- Bounded session-history serialization, result/date/text filters, and grouping helpers.
- Safe profile lifecycle: create/list/use/rename/delete/trash/restore, active-profile changes, and leaderboard restoration.
- Atomic storage/migration behavior, corruption errors, normalized imported state, and bounded recoverable profile trash.
- Leaderboard ranking and serialization.
- Import/export validation and replay-code integrity/backward compatibility.
- English/Hindi catalog completeness, representative formatting, and English fallback behavior.
- CLI parser/settings/history/profile command integration.
- Textual pilot tests for initial focus, tab order, Enter submission, hint interaction, reset, and persisted winning results.
- End-to-end smoke coverage for gameplay, persistence, replay, backup/restore, achievements, leaderboard, and reverse mode.

## Regression policy

Every reproducible bug should receive a focused regression test where practical. Tests must not read or write the user's real GuessNova state; use pytest `tmp_path`, temporary directories, and environment monkeypatching.

## Determinism

Use explicit game targets, fixed seeds, fixed ISO dates, or injected clocks in tests. Never depend on today's challenge target, wall-clock timing, production state, or network services.

## Textual pilot testing

`tests/test_tui.py` uses `GuessNovaApp.run_test()` with Textual's pilot API and injected `Storage(tmp_path)`/deterministic `GuessGame(target=...)` instances. This keeps interactive checks reproducible and prevents test runs from touching a real user profile.

Pilot tests supplement rather than replace manual terminal review. Before release, complete `docs/accessibility_evidence_template.md` on the signed-off release candidate.

## Cross-platform package verification

The CI `platform-package` matrix runs on:

- `ubuntu-latest`
- `windows-latest`
- `macos-latest`

Each runner builds the source and wheel distributions, runs Twine metadata validation, installs the generated wheel, verifies `python -m guessnova --help`, and executes the smoke test. A failure on one platform is a release blocker until reproduced or documented as an infrastructure-only failure.
