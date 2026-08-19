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
```

`make check` runs the core lint/format/type/test/compile/metadata/smoke sequence plus entry-point verification on systems with Make available.

CI also builds, validates, installs, launches the game CLI, primary Doctor route, standalone Doctor compatibility entry point, Doctor version output, and smoke-tests distributions on Ubuntu, Windows, and macOS. Separate workflows perform CodeQL and dependency/secret checks.

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
- Textual pilot tests for initial focus, tab order, Enter submission, hint interaction, reset, and persisted winning results.
- End-to-end smoke coverage for gameplay, persistence, schema 2, replay, backup integrity/importability, Doctor state/backup routes, diagnostics/repair, achievements, leaderboard, localization, and reverse mode.

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

## Regression policy

Every reproducible bug should receive a focused regression test where practical. Tests must not read or write the user's real GuessNova state; use pytest `tmp_path`, temporary directories, and environment monkeypatching.

## Property-testing dependency decision

No property-testing dependency is added in v1.3. The current failure classes are covered by deterministic replay malformed-input suites, migration fixtures, state-normalization cases, bounded-I/O tests, backup-tamper/importability checks, and explicit Doctor/repair regressions. Revisit Hypothesis or another property-testing tool only when a reproducible defect demonstrates materially better coverage than these deterministic suites.

## Determinism

Use explicit game targets, fixed seeds, fixed ISO dates, injected clocks, committed fixtures, or temporary directories in tests. Never depend on today's challenge target, wall-clock timing, production state, or network services.

## Textual pilot testing

`tests/test_tui.py` uses `GuessNovaApp.run_test()` with Textual's pilot API and injected `Storage(tmp_path)`/deterministic `GuessGame(target=...)` instances. This keeps interactive checks reproducible and prevents test runs from touching a real user profile.

Pilot tests supplement rather than replace manual terminal review. Before release, complete `docs/accessibility_evidence_template.md` on the signed-off release candidate.

## Cross-platform package verification

The CI `platform-package` matrix runs on:

- `ubuntu-latest`
- `windows-latest`
- `macos-latest`

Each runner builds source/wheel distributions, runs Twine metadata validation, installs the generated wheel, verifies:

```bash
python -m guessnova --help
guessnova doctor --help
guessnova-doctor --help
guessnova-doctor --version
```

and then executes the smoke test. A failure on one platform is a release blocker until reproduced or documented as an infrastructure-only failure.
