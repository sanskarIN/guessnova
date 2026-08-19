# Development

Use Python 3.13+ and install the development extras:

```bash
python -m pip install -e '.[dev]'
```

## Quality loop

Run the same core checks enforced by CI before opening a pull request:

```bash
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

`make check` runs the core quality sequence plus entry-point and both Textual app import checks on systems with Make available.

Before a release also build and validate the package:

```bash
python -m pip install build twine pip-audit
python -m build
python -m twine check dist/*
pip-audit
```

After installing a built wheel, verify:

```bash
guessnova --help
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
python -c "from guessnova.tui_challenge_app import GuessNovaApp; print(GuessNovaApp.TITLE)"
guessnova doctor --help
guessnova-doctor --help
guessnova-doctor --version
```

## Engineering rules

- Keep `engine.py` and domain rules independent of terminal rendering, diagnostics, backup envelopes, command dispatch, and filesystem I/O.
- Keep `entrypoint.py` as routing only; do not duplicate gameplay or recovery business logic there.
- Keep reusable Textual-independent workspace data/configuration logic in `tui_workspace.py` when widget/focus knowledge is unnecessary.
- Keep v1.5 challenge parsing/configuration free of Textual dependencies so validation/determinism can be tested with ordinary pytest.
- Keep target-free challenge presentation in `tui_challenge.py`; do not reveal the hidden target in identity/status text.
- Keep challenge form composition/mode-aware field state in `tui_challenge_widgets.py`; widgets must not implement persistence or target-selection rules.
- Keep v1.5 integration in `tui_challenge_app.py` additive over the stable v1.4 `tui.GuessNovaApp` unless a future architecture decision explicitly replaces that boundary.
- Parse and construct a replacement challenge before mutating the active round. Validation failures must leave current target/attempt/result-save state intact.
- Keep Reverse out of ordinary numeric challenge setup until a dedicated interaction is implemented.
- Keep small reusable widget-specific keyboard responsibilities in focused widgets such as `GuessInput` instead of making single-letter commands global across unrelated text fields.
- Keep `tui.py` responsible for the stable six-pane composition, focus, events, and orchestration over existing application/local-adapter APIs rather than introducing parallel persistence rules.
- Use deterministic seeds, explicit targets, dates, committed migration fixtures, or injected clocks in automated tests.
- For blank-Daily-date parser tests, inject `today`; do not depend on the runner's real date.
- Keep state-schema, backup-wrapper, replay, and Doctor-report versions as separate compatibility domains.
- Introduce a new state schema only for a real canonical format boundary and add representative fixtures from the prior supported schema.
- Do not persist transient challenge-form state merely to justify a schema increment.
- Preserve older supported backup wrappers explicitly rather than guessing unknown versions.
- Treat imported/local JSON as untrusted and normalize it through storage/profile boundaries.
- Bound file reads before UTF-8/JSON parsing when the file is under application control or is user-selected input.
- Treat backup SHA-256 as integrity/change detection, not authentication, signing, encryption, or proof of origin.
- Keep filesystem writes atomic and local by default.
- A repair operation must create a readable backup before a required normalization write and must refuse data it cannot safely decode/normalize.
- Backup preflight must prove current importability/normalizability before reporting a backup as valid.
- Keep Doctor `--json` stable as one machine-readable JSON document with an explicit report version.
- Do not change Doctor exit-code meaning without an explicit compatibility decision and tests.
- Prefer clear typed dataclasses and small focused functions.
- Keep strict mypy clean; avoid broad ignores that hide real type errors.
- Add regression tests for confirmed bugs.
- Do not commit credentials, private endpoints, real player data, local state, exports, repair backups, Doctor reports containing private profile names, caches, virtual environments, or build outputs.
- Keep changes accessible in keyboard-only flows and avoid relying only on color for status.
- Preserve `--plain` and `--compact` output paths when adding Rich presentation features.
- Add new UI colors through semantic theme roles rather than hard-coded meaning-bearing colors.

## Textual workspace workflow

The v1.5 workspace separates stable workspace behavior from challenge-specific behavior:

```text
tui.py                    stable six-pane workspace, core Play events/focus
tui_widgets.py            focused reusable widget behavior (for example GuessInput R/Q)
tui_workspace.py          Textual-independent workspace queries/configuration helpers
tui_challenge.py          localized target-free challenge presentation
tui_challenge_widgets.py  challenge form and mode-aware field state
tui_challenge_app.py      additive challenge integration; shipped guessnova-tui app
```

See [`adr/0005-additive-textual-challenge-layer.md`](adr/0005-additive-textual-challenge-layer.md).

When changing the workspace:

1. decide whether the change requires Textual widget knowledge;
2. if not, prefer a helper in `tui_workspace.py` and cover it with ordinary pytest tests;
3. if it is challenge identity/status formatting, keep it in `tui_challenge.py` and keep target data out of the presenter contract;
4. if it is challenge form composition/state, keep it in `tui_challenge_widgets.py`;
5. if it is v1.5 challenge-to-stable-workspace orchestration, keep it in `tui_challenge_app.py`;
6. keep unrelated pane/core workspace orchestration in `tui.py`;
7. if the change is a reusable widget-level interaction, keep it in a focused widget class rather than broad app-global handlers;
8. add or update a focused Textual pilot suite for focus/keyboard/mounted-widget behavior;
9. use `Storage(tmp_path)` and deterministic/injected `GuessGame` objects in tests;
10. preserve the six-pane direct shortcuts and useful first focus in each pane;
11. preserve Guess as initial focus and Guess → Submit → Range Hint forward-Tab gameplay flow;
12. preserve Play-local plain `R`/`Q` plus global `Ctrl+R`/`Ctrl+Q` without stealing ordinary characters from challenge/other text fields;
13. preserve exactly-once completed-round persistence through `GameService`;
14. reset unfinished gameplay before active-profile ownership changes;
15. keep profile deletion exact-name-confirmed and recoverable;
16. keep History/Leaderboard based on existing validated local data;
17. keep Settings based on the existing settings/profile model;
18. keep one mounted TUI linguistically consistent unless full atomic relocalization is implemented;
19. keep Recovery diagnostics/backup verification read-only unless a separately reviewed design preserves Doctor safety guarantees;
20. update both English and Hindi catalogs for normal presentation copy;
21. update accessibility/release evidence when focus/interaction changes.

Challenge-specific review additionally requires:

1. Reverse remains excluded from numeric setup;
2. difficulty values come from `DIFFICULTIES` rather than a second rule table;
3. non-Daily seed parses as a whole number;
4. Daily resolves an ISO date and does not accept a manual seed;
5. invalid configuration does not replace the current game;
6. deterministic configured reset reconstructs from validated metadata, not widget text;
7. challenge status does not expose the hidden target;
8. successful start returns focus to Guess;
9. irrelevant seed/date controls remain disabled;
10. new presentation strings are added to all shipped catalogs.

Current focused pilot suites intentionally split concerns rather than one giant test.

Stable workspace suites:

- `tests/test_tui.py` — Play focus, submission, hint, persistence, Play-local reset/quit;
- `tests/test_tui_workspace_app.py` — pane navigation, text-input shortcut isolation, profile lifecycle;
- `tests/test_tui_workspace_data.py` — History, Settings, Recovery;
- `tests/test_tui_workspace_leaderboard.py` — Leaderboard filtering;
- `tests/test_tui_workspace_accessibility.py` — profile-round isolation, launch-locale stability, high contrast.

v1.5 challenge suites:

- `tests/test_tui_challenge_configuration.py` — parser/model invariants and determinism;
- `tests/test_tui_challenge_i18n.py` — localized challenge catalog coverage;
- `tests/test_tui_challenge_presenter.py` and `tests/test_tui_challenge_game_status.py` — target-free status;
- `tests/test_tui_challenge_widgets.py` and `tests/test_tui_challenge_mode_fields.py` — form defaults/state;
- `tests/test_tui_challenge_app.py` — configured journeys;
- `tests/test_tui_challenge_safety.py` — invalid-config preservation;
- `tests/test_tui_challenge_reset.py` — configured deterministic reset;
- `tests/test_tui_challenge_initial_status.py` — mounted active identity;
- `tests/test_tui_challenge_accessibility.py` — focus and shortcut isolation.

## State migration workflow

When a state schema changes:

1. document the concrete compatibility boundary;
2. increment `SCHEMA_VERSION`;
3. add a deterministic migration step from the immediately previous supported schema;
4. add committed old-schema fixtures under `tests/fixtures/state/`;
5. prove important data survives migration;
6. keep future-schema rejection;
7. update canonical/concise data docs, changelog, roadmap, release docs, and `what_changed.md`.

Do not bump the backup wrapper merely because the state schema changed. `EXPORT_VERSION` changes only when the backup envelope itself changes. Do not bump `DOCTOR_REPORT_VERSION` unless the machine-readable Doctor contract changes incompatibly.

## State size-bound workflow

If `MAX_STATE_BYTES` changes:

- keep reads limited to the configured maximum plus one byte;
- keep writes size checked after normalization/serialization and before final persistence;
- retain focused small-bound tests via monkeypatching rather than committing huge fixtures;
- ensure `MAX_EXPORT_BYTES > MAX_STATE_BYTES` remains true so repair backups can represent any accepted state.

## Backup workflow

Changes in `import_export.py` or `backup_inspection.py` must be reviewed for:

- one bounded source read;
- legacy compatibility;
- future-version rejection;
- wrapper/payload schema agreement;
- integrity validation;
- current state normalization/importability;
- read-only preflight behavior;
- atomic export output;
- clear integrity-vs-authenticity wording.

A checksum-valid envelope is not sufficient for Doctor or TUI Recovery to call a backup valid if the embedded state cannot pass current normalization.

## Doctor and repair workflow

Changes in `diagnostics.py`, `doctor_cli.py`, `doctor_protocol.py`, `entrypoint.py`, or storage/backup dependencies should be reviewed together for:

- primary `guessnova doctor` routing;
- standalone `guessnova-doctor` compatibility;
- `python -m guessnova` routing parity;
- explicit `--data-dir` isolation;
- backup verification conflicts remaining read-only;
- stable report version/kinds/exit codes;
- JSON output remaining one document;
- `--json --repair` requiring `--yes`;
- backup-before-repair ordering;
- safe failure without destructive overwrite;
- privacy-safe support output.

## Repository workflow

CI, CodeQL, and Security checks run for pull requests. Superseded runs are cancelled so the newest commit is the verification target. The package matrix builds/installs on Ubuntu, Windows, and macOS and verifies the game CLI, stable Textual workspace import, shipped challenge-app import, primary Doctor route, standalone Doctor entry point, Doctor version output, and smoke flow.

Repository-level branch protection, labels, Discussions, milestones, and release guidance are documented in [`github_repository.md`](github_repository.md). Documentation does not imply branch protection is enabled unless repository metadata confirms it.

## Commit style

Prefer focused Conventional Commits such as `feat: add ...`, `fix: handle ...`, `test: cover ...`, `docs: document ...`, `refactor: simplify ...`, `perf: optimize ...`, `build: configure ...`, `ci: verify ...`, and `chore: maintain ...`.

The requested Git identity email is `sanskarin@outlook.in`.
