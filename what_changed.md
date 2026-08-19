# GuessNova — Complete Work Continuity, v1.0/v1.1 History, and v1.2 Reliability Checkpoint

## Current milestone

GuessNova `v1.1.0` is merged into `main` and remains the previously completed product checkpoint. The current reliability/portability continuation is **GuessNova `v1.2.0`** on:

- Branch: `release/v1.2.0-reliability-20260819`
- Pull request: `#8` — `feat: ship GuessNova 1.2 reliability and recovery`
- Base commit: `b3026ee1d964ad40a305179ca8ebef299c5de506`
- PR head immediately before this `what_changed.md` commit: `9baa9b8c4a13b6789bf89cd649c6a73fb63e24ec`
- PR commits before this handoff commit: **46 granular commits**
- Package version: `1.2.0`
- Runtime version: `1.2.0`
- Citation version: `1.2.0`
- Local state schema: `2`
- Backup wrapper version: `2`
- Replay format version: `1`
- Python requirement: `>=3.13`
- License: MIT
- Requested Git commit email: `sanskarin@outlook.in`

The v1.2 pull request is intentionally developed as many focused feature/fix/test/docs/build/CI commits. Preserve the history with a **normal merge**, not a squash merge, unless an explicit later instruction changes that requirement.

The prior release checkpoints remain part of this continuity record:

- v1.0 PR `#6` merge: `3cc6fec1945c97605506de7d004d7ef4436f48f3` — `feat: complete GuessNova v1.0 release audit`
- v1.0 follow-up checkpoint: `c20b1dc9737ea215f8b4d5262c36eeea90907c68`
- v1.1 PR `#7` normal merge: `b303b764c83dbbca5183ee5b974bd280e7fca0cd` — `feat: ship GuessNova 1.1 UX accessibility and portability`
- v1.1 post-merge checkpoint: `9a511102efc3b11bdf68a8ce7f7ca1692874df40`
- v1.2 planning commit placed on `main` before branching: `b3026ee1d964ad40a305179ca8ebef299c5de506` — `docs: define v1.2 reliability scope`

---

# 1. Product scope retained from v1.0 and v1.1

v1.2 is a reliability release. It does not remove or replace the completed gameplay, progression, accessibility, profile, localization, or terminal interfaces.

## 1.1 Core game modes

Retained:

- Classic number guessing.
- Timed mode with difficulty-specific time budgets.
- Streak-tagged mode.
- Reverse mode using bounded binary search.
- Deterministic Daily Challenge mode.
- Easy difficulty.
- Normal difficulty.
- Hard difficulty.
- Expert difficulty.
- Difficulty-specific numeric ranges.
- Difficulty-specific attempt budgets.
- Difficulty-specific timed limits.
- Out-of-range validation without consuming a valid attempt.
- Deterministic `--seed` support.
- Deterministic `GUESSNOVA_SEED` support.
- Reproducible date-based daily challenges.

## 1.2 Hint systems

Retained:

- automatic smart temperature/direction/parity feedback;
- explicit `hint` / `h` narrowed-range hints;
- explicit hints do not consume a guessing attempt;
- explicit hint usage count;
- optional XP penalty;
- `--hint-penalty` / `--no-hint-penalty`;
- saved per-profile smart-hint preference;
- saved smart-hint preference respected by Rich CLI and Textual TUI.

## 1.3 Game summaries and replay codes

Game summaries retain:

- mode;
- difficulty;
- target;
- won/lost state;
- attempts;
- elapsed seconds;
- complete valid guess sequence;
- optional deterministic seed;
- explicit-hint count;
- accumulated hint penalty.

Replay version remains **1**. v1.2 intentionally does not couple replay format version to state schema or backup wrapper version.

Replay validation retained from the v1 audit includes:

- maximum encoded size;
- URL-safe Base64 validation;
- envelope structure validation;
- digest length validation;
- constant-time digest comparison;
- UTF-8/JSON validation;
- object-root validation;
- exact supported replay version;
- required-field checks;
- unknown-field rejection except documented optional fields;
- valid mode/difficulty;
- target in difficulty range;
- bounded attempts;
- attempt/guess-count agreement;
- each guess inside the difficulty range;
- winning replay ending on target;
- losing replay not containing target;
- finite non-negative elapsed time;
- signed 64-bit seed bounds;
- bounded hint metadata.

Version-1 replay codes that predate optional hint metadata remain compatible through zero defaults.

---

# 2. Player progression, profiles, and history retained from v1.1

## 2.1 Progression

Profiles retain:

- games played;
- games won;
- win rate;
- average guesses;
- current streak;
- best streak;
- XP;
- achievements;
- settings;
- bounded session history.

## 2.2 Leaderboard

Validated local winning-result rows retain:

- player name;
- mode;
- difficulty;
- attempts;
- elapsed time;
- creation timestamp.

Profile rename/delete/restore keeps matching leaderboard data coherent.

## 2.3 Session history

Per-profile history remains capped at the newest **200** entries. Valid records retain:

- mode;
- difficulty;
- win/loss result;
- attempts;
- elapsed seconds;
- optional seed;
- played timestamp.

History query helpers support:

- mode;
- difficulty;
- result;
- free-text query;
- since date;
- until date;
- grouping by day;
- grouping by mode;
- grouping by difficulty;
- grouping by result.

CLI examples retained:

```bash
guessnova history --limit 20
guessnova history --result win --difficulty hard
guessnova history --since 2026-08-01 --until 2026-08-31
guessnova history --search daily --group-by mode
guessnova --plain --compact history --group-by result
```

History/leaderboard limits reject non-positive values.

## 2.4 Recoverable profile lifecycle

Commands retained:

```bash
guessnova profiles list
guessnova profiles create NAME
guessnova profiles use NAME
guessnova profiles rename CURRENT NEW
guessnova profiles delete NAME
guessnova profiles trash
guessnova profiles restore NAME
```

Options retained:

```text
profiles create NAME --no-activate
profiles delete NAME --yes
profiles restore NAME --no-activate
```

Storage APIs retained:

- `list_profile_names()`;
- `active_profile_name()`;
- `create_profile()`;
- `set_active_profile()`;
- `rename_profile()`;
- `delete_profile()`;
- `list_deleted_profile_names()`;
- `restore_profile()`.

Profile safeguards retained:

- duplicate live names rejected;
- missing profile activation rejected;
- rename collision rejected;
- leaderboard player name follows profile rename;
- deleting active profile selects a remaining live profile where possible;
- orphaned imported active-profile reference normalizes to an existing live profile where possible;
- restore collision rejected;
- missing trash record rejected.

Recoverable trash remains bounded by:

```text
MAX_DELETED_PROFILES = 20
```

Deleted-profile records retain deletion timestamp, normalized profile payload, and removed leaderboard rows for recovery.

---

# 3. Localization and Textual interface retained from v1.1

## 3.1 Shipped locales

- `en` — English, default and fallback.
- `hi` — complete Hindi catalog.

Per-profile locale remains persisted. `catalog_missing_keys(locale)` provides completeness validation. Stable machine identifiers remain untranslated.

Examples:

```bash
guessnova settings --locale en
guessnova settings --locale hi
```

## 3.2 Stable identifiers

These remain compatibility identifiers rather than translated display strings:

- commands;
- environment variables;
- mode IDs;
- difficulty IDs;
- achievement IDs;
- state-schema keys;
- replay field names;
- backup markers/version fields;
- doctor JSON keys.

## 3.3 Textual TUI behavior

Retained:

- injected `Storage`/`GuessGame` for deterministic testing;
- active-profile locale;
- saved smart-hint preference;
- localized labels;
- Range Hint button;
- initial numeric-input focus;
- predictable focus order;
- refocus after invalid/valid interactions;
- result persistence through `GameService`;
- exactly-once completed-round persistence guard;
- priority `R` reset and `Q` quit;
- adaptive card width;
- reset preserving difficulty/mode/seed;
- deterministic seeded reset.

Pilot tests retain focus, submission, hint, reset, persistence, saved-setting, and deterministic-reset coverage.

---

# 4. Accessibility and real release evidence retained

Accessibility-oriented behavior retained:

- keyboard-first CLI;
- keyboard-first TUI;
- descriptive text in addition to color;
- `--plain` no-color output;
- `--compact` concise output;
- high-contrast preference;
- reduced-motion preference;
- timed input restricted to timed mode;
- predictable TUI focus;
- recoverable destructive profile action;
- English/Hindi offline presentation.

Manual release evidence remains intentionally separate from automated tests:

- `docs/accessibility_evidence_template.md`
- `docs/media/README.md`

No fabricated screenshot/demo is added merely to complete a roadmap item. Real media must originate from the exact signed-off release build and record provenance.

---

# 5. v1.2 real schema boundary

## 5.1 State schema advanced to 2

`src/guessnova/constants.py` now defines:

```text
SCHEMA_VERSION = 2
```

The schema change is not an invented version bump. Schema 2 formally makes `deleted_profiles` a canonical top-level state container.

GuessNova v1.1 had already written `deleted_profiles` additively while keeping schema version 1. That creates a real compatibility boundary worth formalizing without losing old v1.1 state.

## 5.2 Explicit migration sequence

`storage._migrate(...)` now performs:

1. Validate `schema_version` as a non-boolean integer.
2. Reject negative schema values.
3. Reject versions greater than current `SCHEMA_VERSION`.
4. Schema 0:
   - add baseline `profiles` when missing;
   - add baseline `active_profile` when missing;
   - advance to schema 1.
5. Schema 1:
   - `setdefault("deleted_profiles", {})`;
   - preserve existing v1.1 additive trash when already present;
   - advance to schema 2.
6. Require migration to reach current schema 2.
7. Continue normal state reconstruction/validation.

This migration is intentionally idempotent for v1.1 schema-1 files that already contain deleted-profile trash.

## 5.3 Committed migration fixtures

Added:

- `tests/fixtures/state/schema1_legacy.json`
- `tests/fixtures/state/schema1_with_trash.json`

The first fixture represents schema-1 state without deleted-profile trash. The second represents schema-1 state already containing the additive v1.1 trash field.

Fixture tests verify:

- schema 1 reaches schema 2;
- existing profile progression survives;
- absent trash becomes an empty canonical object;
- existing trash is preserved;
- schema 0 still migrates forward;
- future schema remains rejected.

The fixture policy is documented: do not invent schema-3 fixtures before schema 3 has a concrete design.

---

# 6. Backup wrapper v2

## 6.1 Independent compatibility domain

Backup envelope versioning is now separate from state-schema versioning.

Current values:

```text
SCHEMA_VERSION = 2
EXPORT_VERSION = 2
LEGACY_EXPORT_VERSION = 1
REPLAY_VERSION = 1
```

These numbers happen to overlap for state/export in v1.2, but they are intentionally separate domains and may diverge in future releases.

## 6.2 Backup-v2 envelope

A v2 backup contains:

```json
{
  "format": "guessnova-export",
  "version": 2,
  "schema_version": 2,
  "integrity": {
    "algorithm": "sha256",
    "payload_sha256": "<64-character digest>"
  },
  "payload": {
    "schema_version": 2
  }
}
```

The wrapper records the **actual embedded payload schema**, not blindly the running application's current schema.

That matters for repair: a v2 backup wrapper can truthfully contain a schema-1 original payload immediately before schema-2 normalization.

## 6.3 Canonical digest input

The backup digest uses canonical UTF-8 JSON generated with:

- sorted keys;
- compact separators;
- `ensure_ascii=False`.

SHA-256 is calculated over those payload bytes.

Import compares the supplied digest to the expected digest using `hmac.compare_digest`.

## 6.4 Backup validation

Import validates:

- GuessNova export marker;
- wrapper version type;
- unsupported old wrapper versions;
- future wrapper versions;
- embedded payload object type;
- state-schema value type/range;
- future state schema;
- v2 integrity metadata object;
- integrity algorithm exactly `sha256`;
- digest type;
- digest length;
- wrapper/payload schema agreement;
- payload SHA-256 integrity;
- maximum file size;
- UTF-8/JSON validity.

Export validates the source payload schema and rejects a payload from a future schema.

## 6.5 Legacy wrapper-v1 compatibility

GuessNova <=1.1 backup wrapper version 1 remains readable when the embedded state schema is supported.

Legacy import does not pretend the payload is already current. It returns the supported payload and current `Storage.save_raw(...)` performs the real forward migration/normalization when persisted.

## 6.6 Integrity boundary

The documentation consistently states:

- SHA-256 here detects corruption/ordinary modification;
- it is not encryption;
- it is not a digital signature;
- it is not secret-key authentication;
- it does not prove origin against an attacker able to rewrite payload and unkeyed digest.

No secrets should be stored in replay codes, state files, normal backups, repair backups, fixtures, or public issue attachments.

---

# 7. Local diagnostics and safe repair

## 7.1 New diagnostics module

Created:

- `src/guessnova/diagnostics.py`

`DiagnosticReport` contains:

- `state_exists`;
- `readable`;
- `source_schema_version`;
- `current_schema_version`;
- `active_profile`;
- `profile_count`;
- `history_entries`;
- `leaderboard_entries`;
- `deleted_profile_count`;
- `normalization_changed`;
- `issues`;
- computed `healthy` status.

## 7.2 Read-only diagnose behavior

`diagnose(storage)`:

- performs no network call;
- does not mutate state;
- reports a missing state file as a healthy fresh state;
- catches invalid UTF-8/JSON;
- rejects/report non-object state;
- captures source schema where possible;
- invokes normal state normalization in memory;
- reports unsupported/future schema without overwriting;
- reports schema migration requirement;
- reports normalization differences;
- reports aggregate live profile/history/leaderboard/trash counts;
- reports normalized active profile.

## 7.3 Repair behavior

`repair(storage, backup_dir=...)` is conservative:

1. diagnose first;
2. return without writing if no state file exists;
3. refuse state that is not safely normalizable;
4. re-read and normalize the original object;
5. return without writing if already normalized;
6. choose a timestamped pre-repair backup name;
7. avoid an existing backup filename with a numeric suffix;
8. export the **original payload** through backup wrapper v2;
9. only after successful backup creation, write normalized state through `Storage.save_raw(...)`;
10. return the created backup path.

Unreadable JSON, non-object state, and future unsupported schemas are not force-written.

---

# 8. Packaged `guessnova-doctor`

## 8.1 Entry point

`pyproject.toml` now exposes:

```text
guessnova-doctor = "guessnova.doctor_cli:main"
```

Existing entry points remain:

```text
guessnova
guessnova-tui
```

## 8.2 Doctor output modes

Supported:

```bash
guessnova-doctor
guessnova-doctor --compact
guessnova-doctor --json
```

Normal doctor runs are read-only.

## 8.3 Repair commands

Supported:

```bash
guessnova-doctor --repair
guessnova-doctor --repair --yes
guessnova-doctor --repair --yes --backup-dir ./repair-backups
```

Interactive repair requires typing `REPAIR` unless `--yes` is explicitly supplied.

## 8.4 JSON scripting contract

The JSON mode is intentionally treated as a scripting contract.

Implemented fixes ensure:

- normal JSON output is one parseable JSON document;
- repair with `--json --repair --yes` is one parseable JSON document;
- expected error paths return one JSON error document;
- `--json --repair` **without `--yes` does not prompt**;
- instead it returns a single JSON error explaining that `--yes` is required to avoid interactive output.

This prevents terminal prompt text from corrupting JSON consumed by scripts.

## 8.5 Exit behavior

- healthy diagnostic result: `0`;
- attention/error result: `2`;
- cancelled interactive repair: `1`.

---

# 9. v1.2 regression coverage

## 9.1 Storage/migration

Expanded `tests/test_storage.py` covers:

- save/load profile;
- schema-0 migration to current schema;
- committed schema-1 legacy fixture migration;
- committed schema-1-with-trash fixture migration;
- future schema rejection;
- invalid JSON;
- invalid profiles container;
- untrusted profile/leaderboard normalization;
- orphaned active-profile normalization;
- deleted-profile normalization;
- active profile selection after delete;
- leaderboard round trip.

## 9.2 Backup import/export

Expanded `tests/test_import_export.py` covers:

- backup-v2 round trip;
- wrapper version equals 2;
- embedded schema metadata;
- SHA-256 algorithm marker;
- digest length;
- schema-1 source payload exported with truthful schema provenance;
- legacy wrapper-v1 import;
- wrong format rejection;
- invalid wrapper version types;
- unsupported wrapper versions;
- future wrapper versions;
- future schema in legacy backup rejection;
- export of future-schema payload rejection;
- payload tamper detection;
- wrapper/payload schema mismatch rejection;
- missing integrity metadata;
- unsupported integrity algorithm;
- invalid digest length;
- invalid digest type;
- invalid JSON;
- oversized file rejection.

## 9.3 Diagnostics/repair

`tests/test_diagnostics.py` covers:

- fresh missing state as healthy;
- schema-1 migration/normalization attention;
- normalized active profile report;
- invalid JSON not repairable;
- future schema not repairable;
- non-object state not repairable;
- pre-repair backup creation;
- original payload recoverable from backup;
- repaired state reaches schema 2;
- healthy report after repair;
- no-op repair on already-normalized state.

## 9.4 Doctor CLI

`tests/test_doctor_cli.py` covers:

- fresh JSON diagnostic output;
- JSON parseability;
- schema-1 attention exit;
- interactive cancellation;
- state unchanged after cancelled repair;
- confirmed repair;
- explicit backup directory;
- repair backup creation;
- schema-2 repaired state;
- JSON repair single-document output;
- JSON repair backup path;
- JSON repair without `--yes` never prompting;
- JSON structured error for missing `--yes`.

## 9.5 Existing regression suites retained

The v1/v1.1 suites remain in place for:

- engine outcomes;
- timed behavior;
- hints;
- achievements;
- replay parsing/fuzz-style malformed inputs;
- profile normalization;
- settings;
- themes;
- history queries/grouping;
- profile lifecycle/trash;
- leaderboard;
- service orchestration;
- daily challenge;
- RNG;
- security helpers;
- CLI behavior;
- localization;
- Textual pilot behavior.

---

# 10. v1.2 end-to-end smoke flow

`scripts/smoke_test.py` now exercises the previous product path plus the new reliability path.

It verifies:

1. deterministic winning gameplay;
2. profile progression;
3. first-win achievement;
4. leaderboard insertion;
5. filtered winning history;
6. schema 2 in persisted state;
7. current-state doctor health;
8. replay round trip;
9. profile rename;
10. active-profile rename behavior;
11. leaderboard rename behavior;
12. profile deletion to recoverable trash;
13. profile restore;
14. leaderboard restoration;
15. Hindi catalog completeness;
16. representative Hindi formatting;
17. backup-v2 export;
18. wrapper version 2;
19. embedded schema metadata;
20. SHA-256 digest presence;
21. backup import;
22. synthetic legacy schema-1 state;
23. doctor reporting that legacy state requires attention;
24. repair backup creation;
25. repair backup preserving schema-1 original;
26. repaired state reaching schema 2;
27. repaired state doctor health;
28. reverse binary-search completion.

The smoke test remains deterministic/local and is reused by CI/package/release jobs.

---

# 11. CI and release portability

## 11.1 Strict CI test job

`.github/workflows/ci.yml` continues to require:

1. Python 3.13;
2. development extras;
3. `ruff check .`;
4. `ruff format --check .`;
5. strict `mypy src/guessnova`;
6. pytest with coverage;
7. compileall over source/tests/scripts;
8. release metadata synchronization;
9. full smoke test.

Superseded PR runs are cancelled by workflow concurrency.

## 11.2 Cross-platform package matrix

CI platform matrix remains:

- Ubuntu latest;
- Windows latest;
- macOS latest.

Each runner now:

1. checks out the exact commit;
2. uses Python 3.13;
3. installs build/Twine;
4. builds source/wheel distributions;
5. validates distributions with Twine;
6. installs the generated wheel;
7. verifies `python -m guessnova --help`;
8. verifies `guessnova-doctor --help`;
9. runs the full smoke test.

This extends v1.1 portability coverage to the new packaged maintenance command.

## 11.3 Release workflow

Tagged release verification retains:

- exact tag/project-version match;
- Ruff lint;
- Ruff formatting;
- strict mypy;
- pytest coverage;
- compileall;
- release metadata check;
- smoke test;
- dependency audit;
- Ubuntu/Windows/macOS package matrix.

The release package matrix now also verifies `guessnova-doctor --help`.

`build-release` remains blocked until strict verification **and** cross-platform package verification succeed.

## 11.4 Security and CodeQL

Retained:

- `pip-audit` dependency auditing;
- common secret-material rejection;
- push/PR/scheduled security runs;
- Python CodeQL for main, PRs, and schedule;
- concurrency cancellation of superseded PR runs.

---

# 12. Package and distribution work

## 12.1 Package metadata

Current release-facing values:

```text
pyproject project.version = 1.2.0
guessnova.__version__ = 1.2.0
CITATION.cff version = 1.2.0
CHANGELOG top release = 1.2.0
Python = >=3.13
License = MIT
```

The existing release metadata verifier checks package/runtime/citation/changelog synchronization.

## 12.2 Typed package

`src/guessnova/py.typed` from v1.1 remains present.

## 12.3 Source-distribution fixtures

`MANIFEST.in` now additionally includes:

```text
recursive-include tests/fixtures *.json
```

This preserves migration fixtures in source-distribution context for contributors/release audits while the runtime wheel remains focused on the package.

Other root governance/docs/assets remain explicitly included as before.

---

# 13. v1.2 documentation completed

Added/updated:

- `docs/v1_2_reliability_plan.md` — explicit v1.2 scope and compatibility goals.
- `README.md` — schema 2, backup v2, doctor commands, privacy, entry points, architecture, CI.
- `CHANGELOG.md` — complete 1.2.0 release entry.
- `ROADMAP.md` — v1.2 reliability tasks completed and v1.3 candidates separated.
- `CITATION.cff` — 1.2.0.
- `PRIVACY.md` — doctor/repair/pre-repair backup privacy.
- `SECURITY.md` — backup integrity and repair safety boundaries.
- `SUPPORT.md` — privacy-safe doctor diagnostic guidance.
- `CONTRIBUTING.md` — schema/fixture/version/integrity/doctor contributor rules.
- `.github/pull_request_template.md` — v1.2 persistence/backup/doctor validation checklist.
- `docs/data_format.md` — canonical schema-2/backup-v2/doctor specification.
- `docs/DATA_FORMAT.md` — concise synchronized data reference.
- `docs/architecture.md` — diagnostics/backup/doctor module boundaries.
- `docs/adr/0004-separate-backup-and-state-versions.md` — accepted version-domain decision.
- `docs/testing.md` — migration, backup-integrity, diagnostics/repair strategy.
- `docs/TESTING.md` — concise synchronized testing reference.
- `docs/release.md` — schema/backup/doctor release gates.
- `docs/RELEASING.md` — concise synchronized release reference.
- `docs/setup.md` — installed doctor entry point and safe usage.
- `docs/troubleshooting.md` — doctor, schema migration, backup rejection, JSON scripting guidance.
- `docs/development.md` — schema migration and backup/doctor engineering workflow.
- `what_changed.md` — this complete continuity record.

Existing architecture decisions, branding, accessibility, localization, performance, game-mode, GitHub operations, media, and governance docs are retained.

---

# 14. v1.2 roadmap decisions

Completed:

- real schema-2 boundary;
- schema-1 migration fixtures;
- schema-0/schema-1 forward migration;
- future-schema rejection;
- backup/state version separation;
- backup-v2 SHA-256 integrity;
- wrapper/payload schema agreement;
- legacy backup-v1 compatibility;
- local diagnostics;
- backup-before-write repair;
- packaged doctor entry point;
- game + doctor cross-platform package checks;
- second complete Hindi locale from v1.1 retained;
- property-testing dependency reassessment.

Property-testing decision:

No new property-testing dependency is added in v1.2 because current observed defect classes are covered by deterministic migration fixtures, replay malformed-input tests, state normalization cases, backup mutation/integrity tests, and doctor/repair regressions. Reconsider only after a reproducible defect demonstrates material coverage benefit.

Future maintainability candidates are moved to v1.3 rather than silently expanding v1.2 scope.

---

# 15. v1.2 granular PR commit map

The v1.2 PR contained **46 commits before this handoff commit**. The commit history is intentionally granular.

## 15.1 Schema migration and fixtures

- `128f026a` — `build: advance local state schema to version 2`
- `fd9aa1b3` — `feat: add explicit schema 1 to 2 migration`
- `678fca13` — `test: add legacy schema 1 migration fixture`
- `638991e6` — `test: add schema 1 recoverable trash fixture`
- `a18b0614` — `test: cover schema 2 migrations with fixtures`

## 15.2 Backup-v2 implementation and tests

- `d5cc8c2f` — `feat: add versioned backup integrity metadata`
- `05238f51` — `test: cover backup integrity and legacy compatibility`
- `4079341e` — `fix: preserve source schema provenance in backups`
- `7b0d6c95` — `test: verify backup schema provenance and mismatch rejection`
- `9cef78a3` — `test: harden backup v2 metadata validation`

## 15.3 Diagnostics and doctor

- `170f64f6` — `feat: add local state diagnostics and safe repair`
- `71e80e71` — `test: cover diagnostics migration and repair flow`
- `a2158945` — `feat: add local GuessNova doctor command`
- `0cc28cd8` — `test: cover doctor command output and repair confirmation`
- `57a5724b` — `fix: keep doctor json output machine readable`
- `7eed9060` — `test: keep doctor repair json parseable`
- `ab345c02` — `test: cover unsupported future schema diagnostics`
- `45cd882f` — `fix: require explicit yes for json repair mode`
- `9baa9b8c` — `test: prevent interactive prompts in doctor json mode`

## 15.4 Package/version/release metadata

- `70fdcc49` — `build: expose guessnova doctor console command`
- `769d0b61` — `build: bump GuessNova package to 1.2.0`
- `a3db2ba5` — `build: expose GuessNova 1.2.0 runtime version`
- `5e1e0537` — `docs: update citation metadata for 1.2.0`
- `9314f11b` — `docs: add GuessNova 1.2.0 reliability changelog`
- `eb916696` — `build: include migration fixtures in source distribution`

## 15.5 Smoke, CI, and release automation

- `db675695` — `test: extend smoke flow through schema2 backup and diagnostics`
- `7368dbe9` — `ci: verify doctor entry point from built wheels`
- `a3198a2a` — `ci: verify doctor entry point in release matrix`

## 15.6 Architecture/data/testing/release documentation

- `17656278` — `docs: document schema2 and backup v2 integrity format`
- `94458ca3` — `docs: align concise data reference with schema2 backup v2`
- `c368e2ca` — `docs: complete v1.2 reliability roadmap`
- `6933ecab` — `docs: record backup and state version separation decision`
- `8f836903` — `docs: document v1.2 diagnostics and backup architecture`
- `cf2dfdf5` — `docs: expand testing guide for v1.2 migrations and doctor`
- `2e336642` — `docs: align concise testing reference with v1.2`
- `42930a17` — `docs: extend release checklist for schema2 and doctor`
- `cc9cb274` — `docs: align concise releasing reference with v1.2`
- `f91aae43` — `docs: add v1.2 reliability development workflow`

## 15.7 Privacy/security/support/setup/repository documentation

- `a747268d` — `docs: document local doctor and repair backup privacy`
- `d368e885` — `docs: document backup integrity and repair safety boundaries`
- `fbc6d94f` — `docs: add doctor setup and verification commands`
- `137a20ed` — `docs: add schema2 backup and doctor troubleshooting`
- `0e2b21d4` — `docs: add schema backup and doctor contribution rules`
- `48ee8080` — `docs: update README for GuessNova 1.2 reliability`
- `9c108612` — `docs: add v1.2 reliability checks to pull request template`
- `026bef3f` — `docs: add privacy-safe doctor support guidance`

This `what_changed.md` commit is the next separate documentation commit and should be added to the final PR commit count after it lands.

---

# 16. Complete preserved v1.1 PR commit map

The v1.1 PR retained **56 focused commits** and was normal-merged.

## 16.1 History/profile/localization/TUI implementation

- `373ee6d3` — `feat: add reusable history filtering and grouping`
- `29401237` — `test: cover history query and grouping helpers`
- `baba4140` — `chore: define bounded profile trash retention`
- `ed7812bb` — `feat: add safe local profile lifecycle and undo storage`
- `67a1b5d9` — `test: cover profile lifecycle rename delete and restore`
- `55fef822` — `feat: add profile management command handlers`
- `02bb2c5f` — `feat: add complete Hindi locale and profile messages`
- `33da6a0f` — `test: verify Hindi catalog completeness and formatting`
- `4b335fb9` — `feat: integrate richer history and profile management CLI`
- `a7d993b9` — `test: cover profile and advanced history CLI integration`
- `d49380a6` — `feat: persist TUI results and improve keyboard focus`
- `d9a71179` — `test: add Textual pilot coverage for focus submit reset and hints`
- `e874599c` — `fix: make TUI reset and quit bindings globally reliable`
- `0250d6a2` — `test: harden profile lifecycle edge cases and trash bounds`

## 16.2 Accessibility/docs/release preparation

- `4c5df0b9` — `docs: add accessibility release evidence template`
- `401892e0` — `docs: define verified release media workflow`
- `57caee28` — `docs: add GuessNova 1.1.0 changelog`
- `753268cb` — `docs: document recoverable profile trash format`
- `cfb2b3ef` — `docs: document shipped English and Hindi locales`
- `d5bd9e0e` — `docs: expand testing guide for v1.1 UI and portability`
- `c1e2f078` — `docs: connect accessibility guidance to release evidence`
- `818a2d05` — `docs: extend release checklist for portability and accessibility`
- `fdf7ecb0` — `docs: advance roadmap through v1.1 and portability work`
- `299fbb85` — `docs: update README for GuessNova 1.1.0`

## 16.3 Packaging/CI/metadata work

- `280c5aa0` — `ci: verify package and smoke flow across major platforms`
- `7cb8bcca` — `ci: make distribution glob checks portable on windows`
- `606e371f` — `build: bump package metadata to 1.1.0`
- `dd6ae022` — `build: expose GuessNova 1.1.0 runtime version`
- `f1e0f117` — `docs: update citation metadata for 1.1.0`
- `bf86bf40` — `docs: clarify recoverable profile deletion privacy`
- `17024c1d` — `docs: align concise releasing reference with 1.1 process`
- `97c1f185` — `docs: align concise testing reference with 1.1 suite`
- `bc4af975` — `docs: align concise accessibility reference with 1.1 controls`
- `97b9a3eb` — `docs: align concise data format reference with recoverable profiles`
- `c91d25c7` — `test: extend smoke flow across 1.1 profile history and locale features`
- `68e9eaea` — `test: cover deleted profile state normalization`
- `dc1478c4` — `build: align make targets with strict quality gates`
- `2bb0b6b1` — `build: include governance and citation metadata in source distribution`
- `54721709` — `fix: tighten history renderer typing and formatting`
- `f6c4ecbe` — `style: format profile command handlers for strict checks`
- `599056e5` — `test: verify Hindi locale persists in profile settings`
- `cabe3c09` — `test: cover locale through profile serialization`
- `ada21dcd` — `ci: gate releases on cross-platform package verification`
- `a3007e5e` — `build: add release metadata consistency verifier`
- `6a1915bb` — `ci: verify synchronized release metadata`
- `d3eae2ee` — `build: add release metadata make target`
- `5c0aef53` — `ci: verify metadata before publishing release artifacts`
- `1c8ea3c8` — `build: mark GuessNova package as typed`

## 16.4 Final v1.1 audit/fix/documentation commits

- `bbd14834` — `docs: record complete GuessNova 1.1 continuation checkpoint`
- `3764de3c` — `fix: honor TUI hint preference and deterministic reset`
- `cbededf3` — `test: cover TUI saved hint preference and seeded reset`
- `3913b40e` — `style: format advanced history regression tests`
- `a7216b74` — `fix: normalize orphaned active profile references`
- `ce50d515` — `test: cover orphaned active profile normalization`
- `0434395e` — `docs: align contribution guide with 1.1 quality gates`
- `f74c76bc` — `docs: strengthen pull request validation checklist`

v1.1 merge:

- `b303b764c83dbbca5183ee5b974bd280e7fca0cd`

v1.1 post-merge continuity commit:

- `9a511102efc3b11bdf68a8ce7f7ca1692874df40`

---

# 17. v1.0 audit capabilities retained

The original production audit remains part of the codebase and includes:

- deterministic gameplay engine;
- all core modes/difficulties;
- Rich CLI;
- Textual TUI;
- profiles/stats/XP/achievements;
- leaderboard;
- session history;
- replay codes;
- import/export;
- atomic local persistence;
- profile/settings/history/leaderboard normalization;
- replay malformed-input hardening;
- backup size/format validation;
- user-safe CLI error boundary;
- semantic terminal themes;
- high contrast;
- reduced motion preference;
- onboarding;
- localization-ready architecture;
- strict Ruff/mypy/pytest/compile/smoke gates;
- CodeQL/security/release workflows;
- project governance/security/privacy/support docs;
- editable branding assets;
- MIT licensing;
- `Made by the Sanskar` project identity.

The v1.0 audit merge commit remains:

- `3cc6fec1945c97605506de7d004d7ef4436f48f3`

---

# 18. Verification status and environment limitations

## 18.1 Local execution environment

An attempt was made to clone the v1.2 branch into the available execution/container environment to run the exact repository suite locally.

The clone could not reach GitHub because DNS/network access was unavailable in that execution environment (`Could not resolve host: github.com`).

Therefore this checkpoint **does not claim a local full-suite pass** for the exact v1.2 head.

Repository-side GitHub Actions remain the authoritative executable verification path for the branch.

## 18.2 Static review already performed

Before this handoff, source-level review covered:

- schema migration ordering and future-version rejection;
- v1.1 additive trash preservation during schema-1-to-2 migration;
- truthful source-schema backup provenance;
- wrapper/payload schema agreement;
- SHA-256 digest validation and constant-time comparison;
- legacy wrapper-v1 import behavior;
- repair ordering: backup before state write;
- refusal to repair unreadable/future/non-object state;
- doctor result/exit semantics;
- JSON output parseability;
- discovery and fix of the `--json --repair` interactive-prompt defect;
- cross-platform packaged doctor entry-point checks;
- privacy/security wording that avoids overclaiming unkeyed integrity.

## 18.3 Pull-request workflow state

PR #8 was opened as a draft after the implementation/audit pass. Because this handoff commit changes the PR head, CI/CodeQL/Security must be checked against the **new exact head after this file is committed**.

Do not treat a workflow from `9baa9b8c...` or an earlier superseded commit as final verification for the handoff head.

If the final-head workflows fail, inspect the exact failed step/log and fix the smallest reproducible issue with a focused commit and regression test. If they remain queued without failure, record the exact run IDs/status rather than claiming success.

---

# 19. Release-candidate manual gates

The implementation/source work does not fabricate evidence that only a real release candidate can produce.

Before an immutable `v1.2.0` tag:

1. observe successful required automated checks for the exact selected commit;
2. verify package/runtime/citation/changelog versions at 1.2.0;
3. verify schema-1 fixtures migrate to schema 2;
4. verify backup v2 round trip and deliberate tamper rejection;
5. verify legacy backup-v1 import;
6. verify doctor JSON and backup-before-write repair in isolated state;
7. complete manual accessibility evidence;
8. verify English/Hindi visible flows;
9. capture any desired real terminal screenshots/demo only from the signed-off build;
10. record exact media provenance;
11. tag the immutable selected commit as `v1.2.0` only after release gates are satisfied.

Published tags must not be moved/re-written. A defect after release should become a new patch release.

---

# 20. Remaining future work deliberately outside v1.2

Not v1.2 source blockers:

- real signed-off screenshot/demo capture;
- additional manual accessibility observations;
- optional `guessnova doctor` main-CLI subcommand in addition to `guessnova-doctor` if future CLI consolidation justifies it;
- schema-3 migration fixtures only when schema 3 is real;
- third locale only with complete/native-quality review;
- package artifact signing/provenance enhancements if real registry publishing is introduced;
- property-testing library only if a reproducible gap demonstrates material benefit;
- richer multi-screen Textual profile/history/settings UI;
- optional TypeScript/Web/PWA edition only if offline/privacy/deterministic/replay/keyboard compatibility is preserved.

---

# 21. Project identity and support

- Project: **GuessNova**
- Repository: `https://github.com/sanskarIN/guessnova`
- GitHub profile: `https://github.com/sanskarIN`
- License: MIT
- Credit: **Made by the Sanskar**
- Business: `sanskarin@outlook.in`
- Business: `sanskarin.business@gmail.com`
- Support: `supportramsandesh@gmail.com`
- Buy Me a Coffee: `https://buymeacoffee.com/sanskarIN`

GuessNova remains fully usable without donation, account creation, telemetry, analytics, cloud sync, or required runtime network access.
