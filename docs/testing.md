# Testing

GuessNova uses pytest with deterministic seeds, injected clocks, temporary directories, committed migration fixtures, and Textual's test pilot so tests do not depend on production credentials or persistent user data.

## Full local quality suite

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

`make check` runs the core lint/format/type/test/compile/metadata/smoke sequence plus entry-point and both Textual application import checks on systems with Make available.

CI also builds, validates, installs, imports both the stable v1.4 Textual workspace and the shipped v1.5 challenge-enabled application, launches the game CLI, primary Doctor route, standalone Doctor compatibility entry point, Doctor version output, and smoke-tests distributions on Ubuntu, Windows, and macOS. Separate workflows perform CodeQL and dependency/secret checks.

A configured workflow is not a passed workflow. Final release evidence requires successful conclusions for the exact release-candidate head.

## Coverage areas

- Classic/timed guessing outcomes, bounds, attempt exhaustion, and reproducible RNG.
- Automatic smart hints plus explicit narrowed-range hints and optional XP penalties.
- Reverse binary-search behavior and inconsistent responses.
- Daily challenge reproducibility.
- Achievements, XP, streaks, settings, and defensive profile serialization.
- Bounded session-history serialization, result/date/text filters, and grouping helpers.
- Safe profile lifecycle: create/list/use/rename/delete/trash/restore, active-profile changes, and leaderboard restoration.
- Schema-0/schema-1 to schema-2 migration and future-schema rejection.
- Committed migration fixtures for schema-1 state with and without existing recoverable trash.
- Bounded local state reads/writes, oversized state rejection, atomic persistence, corruption errors, normalized imported state, orphaned active-profile repair, and bounded recoverable profile trash.
- Backup wrapper v2 format/version/schema validation and SHA-256 payload integrity.
- Single-read bounded backup validation through `ValidatedExport`.
- Backup wrapper/payload schema mismatch rejection.
- Legacy version-1 backup compatibility.
- Backup preflight proving current state normalization/importability before reporting a backup as valid.
- Rejection of checksum-valid but structurally unimportable backup payloads.
- Local diagnostics for fresh, migratable, normalized, oversized, future-schema, and unreadable state.
- Repair refusal for unsafe state and pre-repair backup creation before normalized writes.
- Repair-capacity invariant: `MAX_EXPORT_BYTES > MAX_STATE_BYTES`.
- Script-safe Doctor JSON report version `1` and `state`/`backup`/`error` kinds.
- Stable Doctor exit codes and package-aligned `--version` output.
- Both `guessnova doctor` and `guessnova-doctor` routing/behavior.
- Leaderboard ranking and serialization.
- Replay-code integrity/backward compatibility.
- English/Hindi catalog completeness, representative formatting, and English fallback behavior.
- CLI parser/settings/history/profile command integration.
- Textual Play focus, tab order, Enter submission, hint interaction, reset, and persisted winning results.
- Textual six-pane workspace navigation and focus shortcuts.
- Text-field preservation of ordinary `q`/`r` input while global Ctrl bindings remain available.
- Textual profile create/use/rename/delete/restore and exact-name deletion confirmation.
- Active-profile round isolation so unfinished gameplay is reset before ownership changes.
- Textual history result/mode/difficulty/search/date filtering and invalid-date behavior.
- Textual leaderboard mode/difficulty/player filtering.
- Textual settings persistence, immediate smart-hint behavior, launch-locale stability, and high-contrast class behavior.
- Textual read-only diagnostics and backup verification.
- UI-independent workspace snapshots, profile summaries, challenge construction, history selection, leaderboard selection, and settings persistence.
- v1.5 immutable challenge configuration invariants and parsing.
- v1.5 seed/date normalization and validation.
- v1.5 target-free localized challenge identity presentation.
- v1.5 challenge widget defaults and Reverse exclusion.
- v1.5 mode-aware seed/date enablement.
- v1.5 seeded and Daily configured-round startup.
- v1.5 invalid seed/date preservation of the active round and attempt state.
- v1.5 deterministic seeded/Daily reset from validated configuration.
- v1.5 initial challenge identity without target disclosure.
- v1.5 guess-first focus, backward challenge reachability, and ordinary `q`/`r` challenge-field input.
- End-to-end smoke coverage for gameplay, persistence, schema 2, replay, backup integrity/importability, Doctor state/backup routes, diagnostics/repair, achievements, leaderboard, localization, workspace/challenge helpers, and reverse mode.

## Migration fixtures

State migrations are tested with repository fixtures under:

```text
tests/fixtures/state/
```

Current fixtures include:

- `schema1_legacy.json` — schema-1 state without `deleted_profiles`;
- `schema1_with_trash.json` — schema-1 state already containing the additive v1.1 recoverable-trash field.

Fixtures represent real compatibility boundaries and must not be invented for a schema that does not exist. Add schema-2 fixtures only when a real schema-3 design requires migration.

## State size-bound tests

`tests/test_storage_limits.py` verifies:

- state input above the configured bound is rejected before decoding;
- normal `Storage.load_raw()` uses the bounded reader;
- oversized normalized state is rejected before final persistence;
- backup capacity remains larger than accepted state capacity.

Tests monkeypatch the module limit to small values instead of constructing multi-megabyte fixtures.

## Backup integrity and preflight tests

Backup tests verify independently:

- wrapper version handling;
- embedded payload schema provenance;
- legacy wrapper-v1 compatibility;
- future wrapper/schema rejection;
- integrity metadata presence/type;
- digest mismatch after payload tampering;
- wrapper/payload schema mismatch;
- oversized/invalid JSON rejection;
- single-read validated metadata;
- current normalization preview;
- checksum-valid but unimportable state rejection;
- atomic completed output.

The SHA-256 integrity digest is treated as corruption/change detection only. Tests must not describe it as authentication, encryption, origin proof, or digital signing.

## Doctor/repair tests

Diagnostic tests use isolated `Storage(tmp_path)`, explicit `--data-dir`, or `GUESSNOVA_HOME` values. Repair tests must verify the original payload remains recoverable from the pre-repair backup and malformed/non-object/oversized/future-schema state is never silently overwritten.

Doctor JSON should always produce one parseable JSON document for normal state reports, backup reports, and handled error paths. JSON repair requires `--yes` so no interactive prompt can corrupt stdout.

Doctor protocol regression tests cover:

- `report_version == 1`;
- `kind` values;
- exit code constants;
- package-matching Doctor version output;
- state-directory targeting;
- backup verification conflicts;
- primary and standalone entry routes.

## Textual workspace helper tests

`tests/test_tui_workspace.py` exercises logic that intentionally has no Textual dependency:

- deterministic seeded challenge construction;
- reproducible daily-date challenge construction;
- invalid seed/date and Reverse-mode separation;
- workspace snapshots;
- profile statistics derivation;
- newest-first history selection;
- leaderboard filters while preserving rank order;
- settings validation/persistence while retaining onboarding state.

v1.5 adds `tests/test_tui_challenge_configuration.py` for the presentation-friendly challenge model and parser. It verifies:

- valid seeded configuration;
- blank Daily date resolution through an injected date;
- deterministic seeded/Daily reconstruction;
- Reverse separation;
- malformed mode/difficulty/seed/date rejection;
- impossible manual configuration invariants.

Keeping these helpers outside widget code allows domain/application behavior to be verified independently from rendering/focus behavior.

## Textual pilot suites

The Textual workspace is covered by focused pilot suites rather than one oversized scenario.

Retained v1.4 suites:

- `tests/test_tui.py` — original gameplay/focus/persistence regressions;
- `tests/test_tui_workspace_app.py` — pane shortcuts and profile lifecycle;
- `tests/test_tui_workspace_data.py` — history, settings, and Recovery;
- `tests/test_tui_workspace_leaderboard.py` — leaderboard filters;
- `tests/test_tui_workspace_accessibility.py` — round isolation, launch-locale stability, and high contrast.

v1.5 challenge suites:

- `tests/test_tui_challenge_i18n.py` — new catalog formatting/completeness;
- `tests/test_tui_challenge_presenter.py` — target-free localized identity;
- `tests/test_tui_challenge_widgets.py` — form defaults and Reverse fallback;
- `tests/test_tui_challenge_mode_fields.py` — mode-aware field state;
- `tests/test_tui_challenge_app.py` — seeded/Daily configured journeys;
- `tests/test_tui_challenge_safety.py` — invalid-config round preservation;
- `tests/test_tui_challenge_reset.py` — deterministic configured resets;
- `tests/test_tui_challenge_game_status.py` — existing-game target-free status;
- `tests/test_tui_challenge_initial_status.py` — mounted initial identity;
- `tests/test_tui_challenge_accessibility.py` — focus/keyboard regression coverage.

All use isolated temporary state and deterministic/injected games where applicable so tests cannot modify a user's actual data.

Pilot tests supplement rather than replace manual terminal review. Before release, complete `docs/accessibility_evidence_template.md` on the exact signed-off release candidate.

## Regression policy

Every reproducible bug should receive a focused regression test where practical. Tests must not read or write the user's real GuessNova state; use pytest `tmp_path`, temporary directories, and environment monkeypatching.

## Property-testing dependency decision

No property-testing dependency is added merely for v1.5. Current challenge/workspace failure classes are directly covered by deterministic parser/invariant tests and Textual pilot tests, while persistence/replay/backup boundaries retain their existing malformed-input suites. Revisit Hypothesis or another property-testing tool only when a reproducible defect demonstrates materially better coverage than these deterministic suites.

## Determinism

Use explicit game targets, fixed seeds, fixed ISO dates, injected clocks, committed fixtures, or temporary directories in tests. Never depend on today's challenge target, wall-clock timing, production state, or network services.

Blank-Daily-date parser behavior should be tested with the parser's injected `today` argument rather than relying on the test runner's current calendar date.

## Cross-platform package verification

The CI `platform-package` matrix runs on:

- `ubuntu-latest`
- `windows-latest`
- `macos-latest`

Each runner builds source/wheel distributions, runs Twine metadata validation, installs the generated wheel, verifies:

```bash
python -m guessnova --help
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
python -c "from guessnova.tui_challenge_app import GuessNovaApp; print(GuessNovaApp.TITLE)"
guessnova doctor --help
guessnova-doctor --help
guessnova-doctor --version
```

and then executes the smoke test. A failure on one platform is a release blocker until reproduced or documented as an infrastructure-only failure.

The tagged-release package matrix performs the same two Textual import checks before release artifacts can be built by the dependent release job.

## Local execution limitation in the current continuation environment

The available execution environment for this v1.5 continuation cannot resolve GitHub or package-index hosts. Local dependency-backed execution is therefore not claimed. Static review and committed regression coverage continue, while GitHub-hosted workflows provide exact-head execution when runners are available.

Do not convert this limitation into a local Ruff/mypy/pytest/build pass. Any concrete final-head workflow failure must be inspected at the failed job/step and fixed with a focused regression before release verification can be called successful.
