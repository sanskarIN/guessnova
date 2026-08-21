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
node --test tests/web/*.mjs
node --check src/guessnova/web/app.js
node --check src/guessnova/web/browser-state.mjs
node --check src/guessnova/web/game-engine.mjs
node --check src/guessnova/web/sw.js
python scripts/verify_web_package.py
python -m compileall -q src tests scripts
python scripts/verify_release_metadata.py
python scripts/smoke_test.py
python -m guessnova --help
python -m guessnova doctor --help
python -m guessnova.doctor_cli --help
python -m guessnova web --help
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
python -c "from guessnova.tui_challenge_app import GuessNovaApp; print(GuessNovaApp.TITLE)"
```

`make check` runs the core quality sequence plus entry-point checks on systems with Make available. Run the explicit Node/PWA checks above whenever browser code or packaging changes.

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
guessnova web --help
guessnova-web --help
python scripts/verify_web_package.py
```

## Engineering rules

- Keep `engine.py` and domain rules independent of terminal rendering, diagnostics, backup envelopes, command dispatch, and filesystem I/O.
- Keep Python/browser rule parity explicit where cross-client behavior must match; protect shared Daily vectors and Reverse invariants with tests in both languages.
- Keep `entrypoint.py` as routing only; do not duplicate gameplay or recovery business logic there.
- Keep reusable Textual-independent workspace data/configuration logic in `tui_workspace.py` when widget/focus knowledge is unnecessary.
- Keep challenge parsing and deterministic construction in `ChallengeConfiguration`/`parse_workspace_challenge(...)`, not inside widgets.
- Keep challenge status presentation target-free; never expose the hidden target merely to identify a configured round.
- Keep small reusable widget-specific keyboard responsibilities in focused widgets such as `GuessInput` and `ChallengeSetup` instead of making single-letter commands global across unrelated text fields.
- Keep `tui.py` as the stable six-pane workspace. Keep challenge-specific mounting/start/reset routing in the additive `tui_challenge_app.py` layer rather than duplicating Profiles, History, Leaderboard, Settings, or Recovery behavior.
- Replace an active challenge only after parsing and replacement-game construction both succeed; validation failure must leave the current game and result-save state unchanged.
- Use deterministic seeds, explicit targets, dates, committed migration fixtures, or injected clocks in automated tests.
- Keep state-schema, backup-wrapper, replay, Doctor-report, and browser-state versions as separate compatibility domains.
- Introduce a new state schema only for a real canonical format boundary and add representative fixtures from the prior supported schema.
- Preserve older supported backup wrappers explicitly rather than guessing unknown versions.
- Treat imported/local JSON and browser localStorage as untrusted and normalize them through their dedicated boundaries.
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
- Preserve the browser/PWA package contract when editing build metadata or workflows; mobile/browser support must not be accidentally dropped while changing Python/TUI behavior.

## Textual workspace and challenge workflow

The current Textual design deliberately separates stable workspace responsibilities from challenge-specific behavior:

```text
tui.py                    stable six-pane composition, focus, events, persistence orchestration
tui_widgets.py            focused reusable stable widget behavior (for example Play-only R/Q)
tui_workspace.py          Textual-independent queries/configuration/persistence helpers
tui_challenge.py          localized target-free challenge presentation
tui_challenge_widgets.py  challenge form controls and mode-aware field behavior
tui_challenge_app.py      additive challenge integration over the stable workspace
```

When changing the workspace or Challenge Setup:

1. decide whether the change requires Textual widget knowledge;
2. if not, prefer a helper in `tui_workspace.py` and cover it with ordinary pytest tests;
3. keep challenge input validation in `parse_workspace_challenge(...)` / `ChallengeConfiguration` instead of duplicating rules in widgets;
4. if the change is a reusable widget-level interaction, keep it in a focused widget class rather than broad app-global handlers;
5. preserve `tui.py` as the stable workspace and keep challenge-only integration in `tui_challenge_app.py`;
6. add or update focused Textual pilot coverage for focus/keyboard/mounted-widget behavior;
7. use `Storage(tmp_path)` and deterministic/injected `GuessGame` objects in tests;
8. preserve the six-pane direct shortcuts and useful first focus in each pane;
9. preserve Play-local plain `R`/`Q` plus global `Ctrl+R`/`Ctrl+Q` without stealing ordinary characters from challenge/profile/search/path text fields;
10. preserve exactly-once completed-round persistence through `GameService`;
11. make configured challenge replacement transactional so malformed seed/date values cannot destroy an active round;
12. rebuild seeded/Daily configured resets from validated configuration, never by storing/exposing the hidden target;
13. reset unfinished gameplay before active-profile ownership changes;
14. keep profile deletion exact-name-confirmed and recoverable;
15. keep History/Leaderboard based on existing validated local data;
16. keep Settings based on the existing settings/profile model;
17. keep one mounted TUI linguistically consistent unless full atomic relocalization is implemented;
18. keep Recovery diagnostics/backup verification read-only unless a separately reviewed design preserves Doctor safety guarantees;
19. update both English and Hindi catalogs for normal presentation copy;
20. update accessibility/release evidence when focus/interaction changes.

Stable workspace pilot suites intentionally split concerns rather than one giant test:

- `tests/test_tui.py` — Play focus, submission, hint, persistence, Play-local reset/quit;
- `tests/test_tui_workspace_app.py` — pane navigation, text-input shortcut isolation, profile lifecycle;
- `tests/test_tui_workspace_data.py` — History, Settings, Recovery;
- `tests/test_tui_workspace_leaderboard.py` — Leaderboard filtering;
- `tests/test_tui_workspace_accessibility.py` — profile-round isolation, launch-locale stability, high contrast.

Challenge-specific suites are similarly focused:

- `tests/test_tui_challenge_configuration.py` — parser/configuration runtime invariants and deterministic construction;
- `tests/test_tui_challenge_presenter.py` / `tests/test_tui_challenge_game_status.py` — target-free identity presentation;
- `tests/test_tui_challenge_i18n.py` — bilingual challenge formatting;
- `tests/test_tui_challenge_widgets.py` / `tests/test_tui_challenge_mode_fields.py` — control defaults and mode-aware fields;
- `tests/test_tui_challenge_app.py` — seeded and Daily starts;
- `tests/test_tui_challenge_safety.py` — non-destructive invalid configuration;
- `tests/test_tui_challenge_reset.py` — deterministic configured reset;
- `tests/test_tui_challenge_accessibility.py` / `tests/test_tui_challenge_initial_status.py` — focus, keyboard behavior, and startup identity.

See [`tui_challenges.md`](tui_challenges.md) and [`adr/0005-additive-textual-challenge-layer.md`](adr/0005-additive-textual-challenge-layer.md) before making architectural changes to this boundary.

## Browser/PWA workflow

Browser changes should preserve the local-only deployment and storage model:

- keep gameplay usable without an account, telemetry, analytics, cloud sync, or remote leaderboard;
- keep browser persistence isolated from Python schema-2 storage unless an explicitly reviewed interchange design is introduced;
- normalize localStorage through `browser-state.mjs` rather than trusting parsed JSON directly;
- keep service-worker assets synchronized with the actual module set and advance cache names when required for safe refresh;
- retain fixed Python/JavaScript Daily parity vectors;
- run every `tests/web/*.mjs` test, not a narrower filename glob;
- syntax-check `app.js`, `browser-state.mjs`, `game-engine.mjs`, and `sw.js`;
- run `scripts/verify_web_package.py` against source and installed-wheel contexts covered by CI.

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

CI, CodeQL, and Security checks run for pull requests. Superseded runs are cancelled so the newest commit is the verification target. The package matrix builds/installs on Ubuntu, Windows, and macOS and verifies the game CLI, stable Textual workspace import, challenge-enabled Textual app import, primary Doctor route, standalone Doctor entry point/version, both web entry points, bundled PWA assets, and smoke flow.

Repository-level branch protection, labels, Discussions, milestones, and release guidance are documented in [`github_repository.md`](github_repository.md). Documentation does not imply branch protection is enabled unless repository metadata confirms it.

## Commit style

Prefer focused Conventional Commits such as `feat: add ...`, `fix: handle ...`, `test: cover ...`, `docs: document ...`, `refactor: simplify ...`, `perf: optimize ...`, `build: configure ...`, `ci: verify ...`, and `chore: maintain ...`.

The requested Git identity email is `sanskarin@outlook.in`.
