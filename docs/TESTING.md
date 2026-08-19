# Testing

This is the concise testing reference. The canonical detailed strategy is [`testing.md`](testing.md).

The automated suite covers deterministic gameplay, timed/reverse/daily behavior, hints, achievements, profile serialization and recoverable lifecycle operations, bounded/filtered/grouped history, schema-2 migration fixtures, bounded atomic local storage, backup-v2 integrity and legacy compatibility, backup importability preflight, Doctor state/backup/repair behavior, leaderboard ordering, replay integrity, English/Hindi catalogs, CLI routing/parsing, service coordination, reusable TUI workspace/challenge helpers, and focused Textual pilot interactions across all six panes plus v1.5 Challenge Setup.

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
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
python -c "from guessnova.tui_challenge_app import GuessNovaApp; print(GuessNovaApp.TITLE)"
```

`make check` includes both Textual import checks.

CI additionally builds, validates, installs, imports both the stable workspace and shipped challenge app, checks the game CLI plus both Doctor entry paths, verifies Doctor version output, and smoke-tests package artifacts on Ubuntu, Windows, and macOS. Security checks and CodeQL run separately.

Final release claims require successful exact-head workflow conclusions; configured jobs alone are not evidence of a pass.

## Migration, state, and backup reliability

Committed fixtures under `tests/fixtures/state/` verify real schema-1-to-schema-2 compatibility. State tests verify bounded reads/writes and oversized input/output rejection. Backup tests verify wrapper/state version separation, one bounded validated read, SHA-256 payload integrity, schema provenance, legacy wrapper-v1 compatibility, tamper rejection, current normalization preview, and rejection of checksum-valid but unimportable payloads.

The suite also enforces `MAX_EXPORT_BYTES > MAX_STATE_BYTES` so any accepted repairable state can fit inside its mandatory pre-repair backup envelope.

## Doctor/repair

Recommended route: `guessnova doctor`. Compatibility route: `guessnova-doctor`.

Tests cover report protocol version `1`, `state`/`backup`/`error` kinds, stable exit codes, explicit `--data-dir`, read-only `--verify-backup`, package-aligned `--version`, safe confirmation, JSON non-interactivity, backup-before-write repair, and refusal of unreadable/non-object/oversized/future-schema state.

## TUI workspace and v1.5 challenge setup

UI-independent tests cover workspace snapshots, profile summaries, validated challenge configuration/parsing, deterministic seeded/Daily reconstruction, newest-first history filtering, leaderboard filtering that preserves rank order, and validated settings persistence.

Textual pilot suites cover:

- initial Play focus and Guess → Submit → Hint forward-Tab behavior;
- Ctrl+1…Ctrl+6 pane navigation;
- ordinary `q`/`r` typing in workspace/challenge text fields;
- profile create/use/rename/delete/restore;
- exact-name deletion confirmation;
- active-profile unfinished-round isolation;
- history filters and invalid dates;
- leaderboard filters;
- settings persistence and smart-hint behavior;
- launch-locale stability;
- high-contrast launch/save behavior;
- read-only backup verification;
- Challenge Setup mode/difficulty/seed/date behavior;
- Reverse exclusion from numeric setup;
- seeded and Daily configured starts;
- invalid-config current-round preservation;
- mode-aware seed/date enablement;
- target-free active challenge status;
- deterministic configured reset;
- backward keyboard access into challenge setup.

## Deterministic manual test

```bash
GUESSNOVA_HOME=./.tmp-guessnova GUESSNOVA_SEED=1234 guessnova play --no-save
guessnova doctor --json --data-dir ./.tmp-guessnova
guessnova-tui
```

## UI and accessibility evidence

Automated Textual pilot coverage supplements rather than replaces manual review. The exact release candidate must complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md), including Challenge Setup, every workspace pane, keyboard shortcut, profile lifecycle action, high-contrast path, localization path, and read-only Recovery flow.

Tests must never depend on network access or a user's real profile/state directory.
