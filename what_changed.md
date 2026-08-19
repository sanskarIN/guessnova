# GuessNova — Complete Work Continuity and v1.2 Merged Reliability Checkpoint

## Current milestone

**GuessNova `v1.2.0` reliability and recovery implementation is merged into `main`.**

The v1.2 work was developed on:

- Branch: `release/v1.2.0-reliability-20260819`
- Pull request: `#8` — `feat: ship GuessNova 1.2 reliability and recovery`
- Base commit: `b3026ee1d964ad40a305179ca8ebef299c5de506`
- Final PR head: `4fba45c35be87adbb94b64fde5792fb505bbc945`
- Merge commit: `f17594b16426513850c9a1c118d8fcec225702cd`
- Merge method: **normal merge**, not squash
- v1.2 PR commits preserved: **47 granular commits**
- Merge author identity: `Sanskar <sanskarin@outlook.in>`
- GitHub merge verification: valid signed merge commit
- Package version: `1.2.0`
- Runtime version: `1.2.0`
- Citation version: `1.2.0`
- Local state schema: `2`
- Backup wrapper version: `2`
- Replay format version: `1`
- Python requirement: `>=3.13`
- License: MIT

The v1.2 merge intentionally preserved the feature/fix/test/docs/build/CI commit history instead of collapsing it into a squash commit.

Previous milestones retained in repository history:

- v1.0 audit PR `#6` merge: `3cc6fec1945c97605506de7d004d7ef4436f48f3`
- v1.0 follow-up checkpoint: `c20b1dc9737ea215f8b4d5262c36eeea90907c68`
- v1.1 PR `#7` normal merge: `b303b764c83dbbca5183ee5b974bd280e7fca0cd`
- v1.1 post-merge checkpoint: `9a511102efc3b11bdf68a8ce7f7ca1692874df40`
- v1.2 planning commit on main: `b3026ee1d964ad40a305179ca8ebef299c5de506`

This file is the current continuation source of truth after the v1.2 merge.

---

# 1. Product foundation retained

v1.2 is a reliability/portability release. It preserves the completed gameplay and UX foundation rather than replacing it.

## 1.1 Game modes and difficulty

Retained:

- Classic number guessing.
- Timed mode with difficulty-specific time budgets.
- Streak-tagged mode.
- Reverse mode with bounded binary search.
- Deterministic Daily Challenge mode.
- Easy, Normal, Hard, and Expert difficulty presets.
- Difficulty-specific numeric ranges.
- Difficulty-specific attempt limits.
- Difficulty-specific timed limits.
- Out-of-range validation without consuming a valid attempt.
- Deterministic `--seed` support.
- Deterministic `GUESSNOVA_SEED` support.
- Date-derived deterministic daily challenges.

## 1.2 Hint systems

Retained:

- automatic smart temperature/direction/parity hints;
- explicit `hint` / `h` narrowed-range hints;
- explicit hints do not consume a guessing attempt;
- explicit hint counters;
- optional winning-XP penalty;
- `--hint-penalty` and `--no-hint-penalty`;
- per-profile smart-hint preference;
- Rich CLI and Textual TUI honoring the saved smart-hint preference.

## 1.3 Game summaries and replay compatibility

Game summaries retain:

- mode;
- difficulty;
- target;
- win/loss state;
- attempts;
- elapsed seconds;
- guess sequence;
- optional deterministic seed;
- explicit-hint count;
- accumulated hint penalty.

Replay format remains version `1`. v1.2 intentionally does not couple replay format to state-schema or backup-wrapper versions.

Replay validation retained from the production audit includes:

- maximum encoded length;
- URL-safe Base64/envelope validation;
- integrity digest validation;
- constant-time digest comparison;
- UTF-8/JSON validation;
- object-root validation;
- exact replay version;
- required fields;
- field allowlist;
- known mode/difficulty;
- target bounds;
- attempt bounds;
- attempt/guess-count agreement;
- guess bounds;
- winning replay target consistency;
- losing replay target consistency;
- finite non-negative elapsed time;
- signed 64-bit seed bounds;
- bounded hint metadata.

Legacy version-1 replay payloads without later optional hint fields continue to load with zero defaults.

---

# 2. Profiles, progression, leaderboard, and history retained

## 2.1 Profile progression

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

Validated local leaderboard rows retain:

- player name;
- mode;
- difficulty;
- attempts;
- elapsed time;
- creation timestamp.

Profile rename/delete/restore keeps matching local leaderboard data coherent.

## 2.3 History

Per-profile history remains bounded to the newest 200 entries.

Valid history records retain:

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

CLI examples:

```bash
guessnova history --limit 20
guessnova history --result win --difficulty hard
guessnova history --since 2026-08-01 --until 2026-08-31
guessnova history --search daily --group-by mode
guessnova --plain --compact history --group-by result
```

History and leaderboard limits reject non-positive values.

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

Storage lifecycle APIs retained:

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
- missing-profile activation rejected;
- rename collision rejected;
- leaderboard player name follows profile rename;
- deleting the active profile selects a remaining live profile where possible;
- orphaned active-profile references normalize to an existing live profile where possible;
- restore collision rejected;
- missing trash record rejected.

Recoverable trash remains bounded by `MAX_DELETED_PROFILES = 20`.

---

# 3. Localization, accessibility, and TUI retained

## 3.1 Locales

Shipped offline catalogs:

- `en` — English, default/fallback.
- `hi` — Hindi.

Locale remains stored per profile. Catalog completeness is tested through `catalog_missing_keys(locale)`.

Stable machine identifiers remain untranslated, including commands, environment variables, mode/difficulty IDs, schema keys, replay fields, backup markers, and doctor JSON keys.

## 3.2 Textual TUI

Retained:

- injected deterministic `Storage`/`GuessGame` support;
- active profile locale;
- saved smart-hint preference;
- localized core labels;
- explicit Range Hint button;
- deterministic initial focus;
- predictable tab/focus order;
- refocus after interactions/errors;
- persisted results through `GameService`;
- exactly-once completed-round save guard;
- priority `R` reset and `Q` quit bindings;
- adaptive layout;
- reset preserving difficulty/mode/seed.

Textual pilot coverage remains for focus, submission, hint interactions, reset, persistence, preference loading, and deterministic seeded reset.

## 3.3 Accessibility

Retained:

- keyboard-first CLI/TUI;
- descriptive text instead of color-only meaning;
- `--plain` no-color output;
- `--compact` concise output;
- high-contrast preference;
- reduced-motion preference;
- timed interaction only in opt-in timed mode;
- recoverable destructive profile action;
- predictable TUI focus.

Manual release-candidate evidence remains separate from automated tests:

- `docs/accessibility_evidence_template.md`
- `docs/media/README.md`

Real screenshots/demo media must originate from the exact signed-off build. No fabricated media was added to falsely complete a release-evidence checkbox.

---

# 4. v1.2 schema-2 migration

## 4.1 Real schema boundary

`src/guessnova/constants.py` now defines:

```text
SCHEMA_VERSION = 2
```

Schema 2 formally makes `deleted_profiles` a canonical top-level state container.

This is a real compatibility boundary: v1.1 had written recoverable profile trash additively while still using schema version 1.

## 4.2 Migration sequence

`storage._migrate(...)` now:

1. validates `schema_version` as a non-boolean integer;
2. rejects negative versions;
3. rejects future versions;
4. migrates schema 0 to schema 1 with baseline `profiles` and `active_profile`;
5. migrates schema 1 to schema 2 with `deleted_profiles` defaulted only when missing;
6. preserves existing v1.1 additive trash;
7. requires migration to reach current schema 2;
8. passes migrated state through normal validation/normalization.

The schema-1-to-schema-2 migration is intentionally idempotent for v1.1 files that already have the trash field.

## 4.3 Migration fixtures

Committed fixtures:

- `tests/fixtures/state/schema1_legacy.json`
- `tests/fixtures/state/schema1_with_trash.json`

They cover:

- a schema-1 profile state without trash;
- a schema-1 state already containing v1.1 recoverable trash.

Tests verify progression preservation, canonical empty trash where missing, retained existing trash, schema-0 forward migration, and future-schema rejection.

Fixture policy is documented: add schema-3 fixtures only when schema 3 exists as a concrete compatibility change.

---

# 5. Backup wrapper v2

## 5.1 Separate version domains

Current compatibility values:

```text
SCHEMA_VERSION = 2
EXPORT_VERSION = 2
LEGACY_EXPORT_VERSION = 1
REPLAY_VERSION = 1
```

State-schema, backup-envelope, and replay versions are intentionally independent.

The decision is recorded in:

- `docs/adr/0004-separate-backup-and-state-versions.md`

## 5.2 Backup-v2 structure

Current backup envelope contains:

```json
{
  "format": "guessnova-export",
  "version": 2,
  "schema_version": 2,
  "integrity": {
    "algorithm": "sha256",
    "payload_sha256": "<digest>"
  },
  "payload": {
    "schema_version": 2
  }
}
```

The wrapper schema field records the embedded payload's **actual** schema version.

A pre-repair backup may therefore be wrapper version 2 while truthfully containing a schema-1 original payload.

## 5.3 Canonical integrity digest

Backup SHA-256 is calculated from canonical UTF-8 JSON using:

- sorted keys;
- compact separators;
- `ensure_ascii=False`.

Import compares supplied/expected digests using `hmac.compare_digest`.

## 5.4 Validation

Backup import validates:

- exact GuessNova format marker;
- integer non-boolean wrapper version;
- unsupported old wrapper version;
- future wrapper version;
- object payload;
- state-schema type/range;
- future state schema;
- integrity metadata object for wrapper v2;
- exact `sha256` algorithm marker;
- digest string/type/length;
- wrapper/payload schema agreement;
- payload integrity;
- maximum file size;
- UTF-8/JSON validity.

Export rejects future-schema payloads.

## 5.5 Legacy backup compatibility

GuessNova <=1.1 backup wrapper version 1 remains importable when its embedded state schema is supported.

Legacy payload migration occurs when current `Storage` persists it, rather than pretending the imported data was already in schema 2.

## 5.6 Security boundary

Backup SHA-256 is documented as corruption/tamper detection only. It is not encryption, a digital signature, secret-key authentication, or proof of origin against an attacker able to rewrite the payload and unkeyed digest.

---

# 6. Local diagnostics and repair

## 6.1 Diagnostics module

Added:

- `src/guessnova/diagnostics.py`

`DiagnosticReport` exposes:

- state existence;
- safe readability/normalizability;
- source schema;
- current schema;
- active profile;
- live profile count;
- history entry count;
- leaderboard entry count;
- deleted profile count;
- normalization-change flag;
- issue list;
- computed healthy status.

## 6.2 Read-only diagnosis

`diagnose(storage)`:

- makes no network call;
- does not write state;
- treats missing state as a healthy fresh install;
- reports invalid UTF-8/JSON;
- reports non-object state;
- reports source schema where possible;
- runs normalization in memory;
- reports migration/normalization requirements;
- reports unsupported future schema;
- reports aggregate local-state counts.

## 6.3 Backup-before-write repair

`repair(storage, backup_dir=...)`:

1. diagnoses state;
2. returns without writing when no state exists;
3. refuses state that cannot be safely normalized;
4. reads/normalizes the original object;
5. returns without writing if already normalized;
6. generates a timestamped non-colliding backup name;
7. exports the original payload using backup wrapper v2;
8. writes normalized state only after successful backup creation;
9. returns the backup path.

Unreadable JSON, non-object state, and future schemas are not force-overwritten.

---

# 7. Packaged `guessnova-doctor`

## 7.1 Entry points

Current package scripts:

```text
guessnova
guessnova-tui
guessnova-doctor
```

`guessnova-doctor` maps to `guessnova.doctor_cli:main`.

## 7.2 Diagnostic modes

```bash
guessnova-doctor
guessnova-doctor --compact
guessnova-doctor --json
```

Normal diagnostic mode does not modify state.

## 7.3 Repair modes

```bash
guessnova-doctor --repair
guessnova-doctor --repair --yes
guessnova-doctor --repair --yes --backup-dir ./repair-backups
```

Interactive repair requires typing `REPAIR` unless `--yes` is supplied.

## 7.4 JSON scripting safety

A static audit found and fixed a real pre-merge defect: `--json --repair` without `--yes` could have printed an interactive prompt before JSON.

Final behavior:

- normal JSON output is one parseable JSON document;
- JSON repair with `--yes` is one parseable JSON document;
- expected JSON error paths return one JSON error document;
- `--json --repair` without `--yes` does not prompt;
- it returns structured JSON explaining that `--yes` is required.

Regression tests explicitly fail if JSON mode attempts an interactive prompt.

## 7.5 Exit codes

- healthy: `0`;
- attention/expected error: `2`;
- cancelled interactive repair: `1`.

---

# 8. v1.2 automated coverage

## 8.1 Storage/migration

Coverage includes:

- schema-0 migration to current schema;
- schema-1 fixture without trash;
- schema-1 fixture with existing trash;
- progression preservation;
- future-schema rejection;
- invalid JSON;
- invalid profiles container;
- untrusted profile/leaderboard normalization;
- orphaned active-profile normalization;
- deleted-profile normalization;
- active-profile selection after delete;
- leaderboard round trip.

## 8.2 Backup import/export

Coverage includes:

- backup-v2 round trip;
- wrapper version 2;
- embedded schema provenance;
- SHA-256 marker/digest;
- schema-1 source backup provenance;
- legacy wrapper-v1 compatibility;
- wrong format;
- invalid wrapper-version types;
- unsupported/future wrapper versions;
- future schema rejection;
- future-schema export rejection;
- payload tamper rejection;
- wrapper/payload schema mismatch rejection;
- missing integrity metadata;
- unsupported integrity algorithm;
- invalid digest length;
- invalid digest type;
- invalid JSON;
- oversized input.

## 8.3 Diagnostics/repair

Coverage includes:

- fresh state health;
- schema-1 migration attention;
- normalization attention;
- invalid JSON refusal;
- future-schema refusal;
- non-object refusal;
- pre-repair backup creation;
- original payload readability from backup;
- schema-2 repaired state;
- healthy post-repair diagnosis;
- no-op repair when normalized.

## 8.4 Doctor CLI

Coverage includes:

- fresh JSON output;
- schema-1 attention exit;
- interactive cancellation;
- state unchanged after cancellation;
- confirmed repair;
- explicit backup directory;
- JSON repair output;
- JSON repair backup path;
- JSON repair without `--yes` not prompting;
- structured missing-`--yes` JSON error.

## 8.5 Existing suites retained

Existing tests continue covering engine outcomes, timed behavior, hints, achievements, profiles, settings, history, leaderboard, service orchestration, daily challenge, RNG, replay fuzz-style malformed inputs, security helpers, localization, CLI commands, and Textual pilot behavior.

---

# 9. End-to-end smoke coverage

`scripts/smoke_test.py` now checks the previous application flow plus v1.2 reliability behavior:

1. deterministic winning game;
2. progression;
3. first-win achievement;
4. leaderboard;
5. winning-history query;
6. persisted schema 2;
7. healthy current-state diagnostics;
8. replay round trip;
9. profile rename;
10. active-profile rename;
11. leaderboard rename;
12. profile deletion/trash;
13. profile restoration;
14. leaderboard restoration;
15. Hindi catalog completeness;
16. Hindi formatted message;
17. backup-v2 export;
18. wrapper version 2;
19. embedded schema metadata;
20. SHA-256 digest presence;
21. backup import;
22. isolated schema-1 legacy state;
23. doctor migration attention;
24. pre-repair backup;
25. repair backup preserving schema-1 original;
26. repaired schema 2;
27. healthy post-repair diagnostics;
28. reverse binary-search completion.

The smoke flow is reused by CI/package/release verification.

---

# 10. CI, portability, security, and release automation

## 10.1 Strict CI job

Requires:

- Python 3.13;
- development extras;
- `ruff check .`;
- `ruff format --check .`;
- strict `mypy src/guessnova`;
- pytest coverage;
- compileall;
- release metadata verification;
- smoke test.

## 10.2 Cross-platform package matrix

Runs on:

- Ubuntu latest;
- Windows latest;
- macOS latest.

Each platform:

1. builds source/wheel distributions;
2. validates with Twine;
3. installs the generated wheel;
4. verifies `python -m guessnova --help`;
5. verifies `guessnova-doctor --help`;
6. runs the smoke test.

## 10.3 Release workflow

Tagged release remains blocked on strict verification and all three package runners.

Release verification includes exact tag/package version, Ruff, formatting, strict mypy, tests, compile, release metadata, smoke, dependency audit, and cross-platform package checks.

## 10.4 Security/CodeQL

Retained:

- `pip-audit` dependency auditing;
- common secret-pattern rejection;
- push/PR/scheduled security runs;
- Python CodeQL;
- concurrency cancellation for superseded PR runs.

---

# 11. Package and source-distribution details

Release metadata is synchronized at:

```text
1.2.0
```

Files checked by `scripts/verify_release_metadata.py` include:

- `pyproject.toml` project version;
- `guessnova.__version__`;
- `CITATION.cff`;
- `CHANGELOG.md` release heading.

`src/guessnova/py.typed` remains present.

`MANIFEST.in` now includes migration fixtures:

```text
recursive-include tests/fixtures *.json
```

Root governance/docs/assets continue to be included as previously configured.

---

# 12. Documentation completed for v1.2

Added/updated:

- `docs/v1_2_reliability_plan.md`
- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `CITATION.cff`
- `PRIVACY.md`
- `SECURITY.md`
- `SUPPORT.md`
- `CONTRIBUTING.md`
- `.github/pull_request_template.md`
- `docs/data_format.md`
- `docs/DATA_FORMAT.md`
- `docs/architecture.md`
- `docs/adr/0004-separate-backup-and-state-versions.md`
- `docs/testing.md`
- `docs/TESTING.md`
- `docs/release.md`
- `docs/RELEASING.md`
- `docs/setup.md`
- `docs/troubleshooting.md`
- `docs/development.md`
- `what_changed.md`

Existing branding, accessibility, localization, performance, game-mode, GitHub repository operations, release-media, and governance documentation remains retained.

---

# 13. v1.2 PR commit map

PR #8 preserved **47 granular commits**.

## 13.1 Schema migration

- `128f026a` — `build: advance local state schema to version 2`
- `fd9aa1b3` — `feat: add explicit schema 1 to 2 migration`
- `678fca13` — `test: add legacy schema 1 migration fixture`
- `638991e6` — `test: add schema 1 recoverable trash fixture`
- `a18b0614` — `test: cover schema 2 migrations with fixtures`

## 13.2 Backup versioning/integrity

- `d5cc8c2f` — `feat: add versioned backup integrity metadata`
- `05238f51` — `test: cover backup integrity and legacy compatibility`
- `4079341e` — `fix: preserve source schema provenance in backups`
- `7b0d6c95` — `test: verify backup schema provenance and mismatch rejection`
- `9cef78a3` — `test: harden backup v2 metadata validation`

## 13.3 Diagnostics/doctor

- `170f64f6` — `feat: add local state diagnostics and safe repair`
- `71e80e71` — `test: cover diagnostics migration and repair flow`
- `a2158945` — `feat: add local GuessNova doctor command`
- `0cc28cd8` — `test: cover doctor command output and repair confirmation`
- `57a5724b` — `fix: keep doctor json output machine readable`
- `7eed9060` — `test: keep doctor repair json parseable`
- `ab345c02` — `test: cover unsupported future schema diagnostics`
- `45cd882f` — `fix: require explicit yes for json repair mode`
- `9baa9b8c` — `test: prevent interactive prompts in doctor json mode`

## 13.4 Package/version metadata

- `70fdcc49` — `build: expose guessnova doctor console command`
- `769d0b61` — `build: bump GuessNova package to 1.2.0`
- `a3db2ba5` — `build: expose GuessNova 1.2.0 runtime version`
- `5e1e0537` — `docs: update citation metadata for 1.2.0`
- `9314f11b` — `docs: add GuessNova 1.2.0 reliability changelog`
- `eb916696` — `build: include migration fixtures in source distribution`

## 13.5 Smoke/CI/release automation

- `db675695` — `test: extend smoke flow through schema2 backup and diagnostics`
- `7368dbe9` — `ci: verify doctor entry point from built wheels`
- `a3198a2a` — `ci: verify doctor entry point in release matrix`

## 13.6 Architecture/data/testing/release documentation

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

## 13.7 Privacy/security/support/repository documentation

- `a747268d` — `docs: document local doctor and repair backup privacy`
- `d368e885` — `docs: document backup integrity and repair safety boundaries`
- `fbc6d94f` — `docs: add doctor setup and verification commands`
- `137a20ed` — `docs: add schema2 backup and doctor troubleshooting`
- `0e2b21d4` — `docs: add schema backup and doctor contribution rules`
- `48ee8080` — `docs: update README for GuessNova 1.2 reliability`
- `9c108612` — `docs: add v1.2 reliability checks to pull request template`
- `026bef3f` — `docs: add privacy-safe doctor support guidance`

## 13.8 Complete handoff commit inside PR

- `4fba45c3` — `docs: record complete GuessNova 1.2 reliability checkpoint`

PR merge commit:

- `f17594b16426513850c9a1c118d8fcec225702cd` — `feat: ship GuessNova 1.2 reliability and recovery`

This current file update is a **post-merge main-branch checkpoint** and is intentionally separate from the 47 preserved PR commits.

---

# 14. Preserved v1.1 PR commit map

PR #7 retained **56 focused commits**.

## 14.1 History/profile/localization/TUI

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

## 14.2 Accessibility/docs/release

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

## 14.3 Packaging/CI/metadata

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

## 14.4 Final v1.1 audit fixes/docs

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

---

# 15. v1.0 production-audit foundation retained

The v1.0 audit remains in the current codebase, including:

- deterministic engine;
- all core modes/difficulties;
- Rich CLI;
- Textual TUI;
- profiles/stats/XP/achievements;
- leaderboard;
- bounded history;
- replay codes;
- import/export;
- atomic local persistence;
- defensive profile/settings/history/leaderboard normalization;
- replay malformed-input hardening;
- size/format boundaries;
- user-safe CLI error boundary;
- semantic terminal themes;
- high contrast;
- reduced motion preference;
- onboarding;
- localization-ready architecture;
- strict Ruff/mypy/pytest/compile/smoke gates;
- CodeQL/security/release workflows;
- governance/security/privacy/support docs;
- editable branding assets;
- MIT licensing;
- `Made by the Sanskar` identity.

v1.0 audit merge:

- `3cc6fec1945c97605506de7d004d7ef4436f48f3`

---

# 16. Exact v1.2 verification state at merge

Final v1.2 PR head:

```text
4fba45c35be87adbb94b64fde5792fb505bbc945
```

Immediately before/after the normal merge, GitHub reported these pull-request workflow states for that exact head:

- CI run `32217423563`: `queued`, no conclusion.
- CodeQL run `32217423549`: `queued`, no conclusion.
- Security checks run `32217423559`: `pending`, no conclusion.

CI job-level state at the final head showed all four CI jobs queued:

- `test (3.13)`;
- `package (ubuntu-latest)`;
- `package (windows-latest)`;
- `package (macos-latest)`.

No final-head workflow returned a failure conclusion before the merge.

This file **does not claim queued/pending workflows passed**.

The GitHub-hosted runner queue continued the same saturation pattern observed during the v1.0/v1.1 continuation work. Superseded runs can be cancelled by concurrency and must not be interpreted as test failures.

If these exact-head runs later execute and expose a reproducible failure, the next continuation should inspect the exact failed job/step/log and apply the smallest focused regression fix with a new commit.

---

# 17. Local verification limitation

A direct clone of the v1.2 branch was attempted in the available execution/container environment to run the exact repository suite locally.

The execution environment could not resolve `github.com` and therefore could not clone the repository. No local full-suite result is invented from that failed network attempt.

Repository-side verification added for v1.2 remains:

- strict CI;
- three-platform package matrix;
- CodeQL;
- dependency/security workflow;
- deterministic unit tests;
- committed migration fixtures;
- expanded smoke test;
- static file-by-file audit.

Static audit before merge specifically reviewed:

- migration ordering;
- v1.1 trash preservation;
- future-schema rejection;
- backup version separation;
- source-schema provenance;
- wrapper/payload schema agreement;
- SHA-256 integrity validation;
- constant-time digest comparison;
- legacy backup compatibility;
- repair backup-before-write ordering;
- refusal of unreadable/future/non-object state;
- doctor output/exit behavior;
- JSON scripting behavior;
- cross-platform doctor packaging;
- privacy/security wording.

The audit found the JSON-repair prompt defect and fixed it with dedicated regression coverage before merge.

---

# 18. Release-candidate gates that remain intentionally manual

Do not create/move a `v1.2.0` release tag solely because the implementation is merged.

Before a release tag:

1. observe successful required automated checks for the selected exact release commit;
2. verify package/runtime/citation/changelog values remain `1.2.0`;
3. verify schema-1 fixtures migrate to schema 2;
4. verify backup-v2 round trip;
5. deliberately modify a backup and confirm integrity rejection;
6. verify legacy wrapper-v1 import;
7. verify `guessnova-doctor --json`;
8. verify backup-before-write repair in isolated state;
9. complete manual accessibility evidence;
10. verify English and Hindi visible paths;
11. capture desired real screenshots/demo only from the exact signed-off build;
12. record media provenance;
13. tag the immutable selected commit as `v1.2.0` only after release gates are satisfied.

Published tags should not be rewritten. A post-release defect should become a new patch release.

---

# 19. Future work deliberately outside v1.2

Not v1.2 source blockers:

- real signed-off screenshot/demo capture;
- manual release-candidate accessibility observations;
- optional `guessnova doctor` subcommand in addition to the packaged `guessnova-doctor` entry point if future CLI consolidation justifies it;
- schema-3 migration/fixtures only when schema 3 is real;
- third reviewed locale only with complete/native-quality review;
- artifact signing/provenance enhancements if a real registry publishing workflow is introduced;
- property-testing library only after a reproducible coverage gap demonstrates value;
- richer multi-screen Textual profile/history/settings UI;
- optional TypeScript/Web/PWA edition only if privacy, offline behavior, deterministic rules, replay compatibility, and keyboard accessibility remain intact.

---

# 20. Project identity

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
