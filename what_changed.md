# GuessNova — Work Continuity, v1.0 Baseline, and v1.1 Release Audit

## Current milestone

GuessNova `v1.0.0` is already merged into `main` and remains the stable baseline. The next complete implementation pass is now on:

- Branch: `release/v1.1.0-ux-accessibility-20260819`
- Pull request: `#7` — `feat: ship GuessNova 1.1 UX accessibility and portability`
- Base commit: `c20b1dc9737ea215f8b4d5262c36eeea90907c68`
- Code/metadata head before this handoff update: `1c8ea3c81cb63694d5feb02e9b9a9fd93dd50865`
- Package/runtime/citation version: `1.1.0`
- Requested Git commit email observed in repository commit metadata: `sanskarin@outlook.in`

The v1.1 PR is intentionally kept as a normal multi-commit branch so the granular history is preserved. It must not be squash-merged if the goal remains to retain the maximum meaningful commit history.

The prior v1.0 release-audit PR was `#6`, merged with:

- `3cc6fec1945c97605506de7d004d7ef4436f48f3` — `feat: complete GuessNova v1.0 release audit`

The follow-up v1.0 continuity commit on `main` was:

- `c20b1dc9737ea215f8b4d5262c36eeea90907c68` — `docs: record final merged v1 release audit and verification state`

---

# 1. Product state carried forward from v1.0

The following v1.0 functionality is retained and must not be removed by v1.1 work.

## 1.1 Gameplay

- Classic number guessing.
- Timed mode with difficulty-specific time budgets.
- Streak-tagged mode.
- Reverse mode using bounded binary search.
- Deterministic daily challenge mode.
- Easy, Normal, Hard, and Expert difficulty presets.
- Difficulty-specific ranges and attempt budgets.
- Out-of-range guesses do not consume an attempt.
- Deterministic `--seed` support.
- Deterministic `GUESSNOVA_SEED` environment-variable support.
- Automatic smart temperature/direction/parity feedback.
- Explicit narrowed-range hints requested with `hint` or `h`.
- Explicit hint requests do not consume attempts.
- Optional explicit-hint XP penalty.
- Optional `--no-hint-penalty` override.
- Reproducible game summaries.
- Replay codes with integrity protection and strict validation.
- Backward-compatible version-1 replay decoding for older payloads without later optional hint metadata.

## 1.2 Progression and local state

- Local profiles.
- Games played and games won.
- Win rate.
- Average guesses.
- Current streak and best streak.
- XP.
- Achievements.
- Local leaderboard.
- Bounded per-profile session history.
- Human-readable JSON export/import.
- Atomic local state writes.
- State normalization.
- Future-schema rejection.
- `GUESSNOVA_HOME` override.
- No mandatory account.
- No runtime telemetry, analytics, ads, or required network connection.

## 1.3 Interfaces

- Rich CLI through `guessnova`.
- Textual TUI through `guessnova-tui`.
- Module entry point through `python -m guessnova`.
- CLI commands for play, reverse, stats, history, leaderboard, settings, about, export, import, and replay inspection.
- `--plain` no-color output.
- `--compact` concise terminal rendering.
- Semantic terminal themes.
- High-contrast preference.
- Reduced-motion preference.
- Smart-hint preference.
- First-run onboarding.
- English message catalog and persisted locale architecture.

## 1.4 Security/reliability baseline

- Strict replay-code envelope and field validation.
- Maximum replay-code length.
- Constant-time checksum comparison.
- Difficulty/mode/attempt/guess/seed/timing/hint metadata validation.
- Maximum import/export sizes.
- Atomic backup writes.
- Defensive imported-state normalization.
- Bounded history.
- Clean CLI error boundary for expected `ValueError`/`OSError` failures.
- Rich-markup escaping for displayed exception text.
- CI, Ruff, strict mypy, pytest/coverage, compile, smoke, CodeQL, dependency audit, secret-material checks, Dependabot, and quality-gated tagged release automation.

---

# 2. v1.1 implementation completed on the release branch

## 2.1 Reusable advanced history queries

`src/guessnova/history.py` now contains reusable query helpers rather than leaving history filtering inside presentation code.

Added:

- `HistoryResult = Literal["win", "loss"]`.
- `HistoryGroup = Literal["day", "mode", "difficulty", "result"]`.
- ISO timestamp-to-date parsing helper.
- `filter_history(...)` supporting:
  - mode filter;
  - difficulty filter;
  - win/loss filter;
  - free-text search;
  - `since` date;
  - `until` date.
- Free-text matching covers timestamp, mode, difficulty, result, attempt count, and seed.
- Unparseable dates are excluded when a date-bound filter is requested.
- `group_history(...)` supporting grouping by day, mode, difficulty, or result.
- Group insertion order follows first-seen result order.
- Unsupported group values fail explicitly.

Existing bounded history serialization/deserialization remains in place.

## 2.2 Richer history CLI

`guessnova history` now supports:

```text
--mode
--difficulty
--result win|loss
--search TEXT
--since YYYY-MM-DD
--until YYYY-MM-DD
--group-by day|mode|difficulty|result
--limit POSITIVE_INTEGER
```

Examples documented in README:

```bash
guessnova history --result win --difficulty hard
guessnova history --since 2026-08-01 --until 2026-08-31
guessnova history --search daily --group-by mode
guessnova --plain --compact history --group-by result
```

History rendering was typed with `Sequence[HistoryEntry]` to avoid list-invariance problems under strict mypy.

Leaderboard `--limit` now uses the same positive-integer validation instead of accepting zero/negative limits.

## 2.3 Safe local profile lifecycle

A complete local profile-management surface was added.

Commands:

```bash
guessnova profiles list
guessnova profiles create NAME
guessnova profiles use NAME
guessnova profiles rename CURRENT NEW
guessnova profiles delete NAME
guessnova profiles trash
guessnova profiles restore NAME
```

Additional options:

```text
profiles create NAME --no-activate
profiles delete NAME --yes
profiles restore NAME --no-activate
```

Storage APIs added:

- `list_profile_names()`.
- `active_profile_name()`.
- `create_profile()`.
- `set_active_profile()`.
- `rename_profile()`.
- `delete_profile()`.
- `list_deleted_profile_names()`.
- `restore_profile()`.

Behavior:

- Duplicate live profile creation is rejected.
- Switching to a missing profile is rejected.
- Rename to an existing live profile name is rejected.
- Renaming a profile updates its local leaderboard rows.
- Deleting a profile removes it from the live profile map.
- Deleting a profile removes its active leaderboard rows.
- The profile and removed leaderboard rows are moved into recoverable local trash.
- Deleting the active profile selects another remaining profile when one exists.
- When no live profile remains, the normal default profile name remains the fallback for future use.
- Restoring a profile restores profile data and retained leaderboard rows.
- Restore is rejected if a live profile with the same normalized name already exists.
- Restore is rejected when no matching trash record exists.

## 2.4 Recoverable deletion / undo semantics

New constant:

```text
MAX_DELETED_PROFILES = 20
```

Top-level normalized state now includes additive `deleted_profiles` data.

Each valid trash record contains:

- deletion timestamp;
- normalized profile payload;
- retained normalized leaderboard rows owned by that profile.

Trash behavior:

- bounded to the newest 20 deleted profiles;
- normalized on load/save;
- malformed trash records are discarded;
- included in normal backup/export state;
- restored only when there is no live-name collision.

Profile deletion normally requires the user to type the exact normalized profile name. `--yes` is available only for intentional non-interactive/scripted use.

This is deliberately recoverable deletion, not secure erasure. `PRIVACY.md` now explains that complete local deletion requires deleting the GuessNova application-data directory and separately deleting any user-created export copies.

## 2.5 Hindi localization shipped

The localization architecture now proves end-to-end multi-locale behavior rather than being English-only scaffolding.

Shipped catalogs:

- `en` — English, default/fallback.
- `hi` — Hindi.

The Hindi catalog includes every English catalog key.

New/updated localization behavior:

- `available_locales()` returns stable shipped locale IDs.
- `catalog_missing_keys(locale)` identifies missing English-reference keys in a shipped locale.
- Automated tests require the Hindi catalog to have no missing English keys.
- Named formatting placeholders are tested.
- Unknown locale values still fall back to English.
- Unknown message keys still fail as development errors.
- Per-profile locale persistence now explicitly tests Hindi.
- Full profile serialization now explicitly tests Hindi locale preservation.

Catalog-backed presentation includes onboarding, gameplay status/prompts, reverse-mode messages, statistics/history headings, settings, profile-management messages, About/data-transfer messages, and Textual core labels.

Stable machine identifiers remain untranslated:

- mode IDs;
- difficulty IDs;
- command names;
- environment variables;
- achievement IDs;
- schema keys;
- replay field names.

Engine-generated semantic hint prose remains a domain string for now. `docs/localization.md` explicitly documents that it should be converted to semantic hint data before translating it, rather than coupling serialized/domain behavior to display text.

## 2.6 Textual TUI persistence and interaction improvements

The TUI now uses injectable storage/game dependencies for deterministic testing.

Added/changed:

- optional `profile_name` injection;
- optional `GuessGame` injection;
- optional `Storage` injection;
- active profile locale loading;
- localized core labels;
- explicit Range Hint button;
- initial focus on numeric guess input;
- input re-focus after empty input, valid guesses, errors, and hints;
- persisted completed rounds through the same `GameService` used by CLI gameplay;
- exactly-once result-save guard for a finished TUI round;
- reset preserves the current difficulty and mode;
- reset clears result-save state;
- priority `R` reset binding;
- priority `Q` quit binding;
- adaptive width (`92%`, maximum 64 columns) for the main card.

## 2.7 Textual pilot tests

`tests/test_tui.py` uses Textual's `run_test()` pilot with deterministic injected games and temporary storage.

Coverage includes:

- initial focus is the guess input;
- Tab order from input to submit to range-hint button;
- Enter submission from the numeric input;
- winning round becomes finished/won;
- winning TUI result is persisted;
- persisted games-played/games-won increment exactly as expected;
- range-hint interaction increments hint count;
- range hint does not consume an attempt;
- hint interaction returns focus to guess input;
- reset clears attempts;
- reset starts an unfinished round;
- reset returns focus to guess input.

No `pytest-asyncio` dependency was added; pilot scenarios use `asyncio.run(...)` directly.

## 2.8 Accessibility release evidence

Created:

- `docs/accessibility_evidence_template.md`.

The template requires manual release-candidate evidence for:

- release version/tag/commit;
- OS/terminal/font scale/locale;
- keyboard-only CLI gameplay;
- keyboard-only reverse mode;
- profile lifecycle controls;
- typed deletion confirmation;
- history browsing/filtering;
- plain/compact output;
- no-color semantic clarity;
- TUI initial focus;
- TUI tab order;
- Enter submission;
- hint behavior;
- reset/quit bindings;
- completed-result persistence;
- narrow-terminal behavior;
- increased font scale;
- high contrast;
- reduced motion;
- English rendering;
- Hindi rendering;
- defect disposition;
- release sign-off.

Automated tests are explicitly documented as supplemental, not a substitute for the manual accessibility evidence pass.

## 2.9 Release media provenance

Created:

- `docs/media/README.md`.

Rules:

- no mock terminal screenshots may be presented as release captures;
- no reconstructed/fabricated demo may be presented as a real release recording;
- media must come from a signed-off release candidate;
- media must identify the exact source commit/tag;
- deterministic gameplay should be used where practical;
- private terminal history, home paths, usernames, credentials, tokens, or unrelated data must be removed from the capture environment;
- recommended screenshot/demo filenames are documented.

Real screenshots/demo media remain intentionally uncommitted until an exact build is manually captured. This is a manual release-candidate task, not missing source code.

## 2.10 Cross-platform packaging verification

CI now includes a `platform-package` matrix for:

- `ubuntu-latest`;
- `windows-latest`;
- `macos-latest`.

Each platform job:

1. checks out the exact commit;
2. installs Python 3.13;
3. installs `build` and `twine`;
4. builds source/wheel distributions;
5. runs Twine validation;
6. installs the generated wheel;
7. runs `python -m guessnova --help`;
8. runs the end-to-end smoke test.

Bash is explicitly selected for distribution-glob steps so Windows runner wildcard behavior does not make those checks shell-dependent.

## 2.11 Tagged-release cross-platform gate

The tag-triggered release workflow now has both:

- strict `verify` job;
- three-platform `platform-package` matrix.

`build-release` requires both groups to succeed before GitHub release artifacts can be created.

The release `verify` job enforces:

- tag/project-version match;
- Ruff lint;
- Ruff formatting;
- strict mypy;
- pytest coverage run;
- compileall;
- release metadata synchronization;
- end-to-end smoke test;
- dependency audit.

## 2.12 Release metadata synchronization

Created:

- `scripts/verify_release_metadata.py`.

It verifies:

- `pyproject.toml` project version is valid;
- `guessnova.__version__` equals project version;
- `CITATION.cff` version equals project version;
- `CHANGELOG.md` contains a heading for that version.

Current synchronized version:

```text
1.1.0
```

The verifier is run by normal CI and by the tag release workflow.

## 2.13 Package typing marker

Created:

- `src/guessnova/py.typed`.

This marks the distributed package as supplying inline typing information.

## 2.14 Smoke test expanded for v1.1

`scripts/smoke_test.py` now exercises:

- deterministic winning gameplay;
- profile progression;
- first-win achievement;
- leaderboard insertion;
- win history filtering;
- replay encode/decode;
- profile rename;
- active-profile rename behavior;
- leaderboard rename behavior;
- recoverable profile deletion;
- trash listing;
- profile restoration;
- leaderboard restoration;
- Hindi catalog completeness;
- representative Hindi formatting;
- export/import;
- reverse binary search.

The same smoke test is used by local checks, strict CI, platform package jobs, and tagged-release verification.

## 2.15 Makefile quality parity

`Makefile` now exposes:

- `install`;
- `test`;
- `lint`;
- `format`;
- `type`;
- `compile`;
- `metadata`;
- `smoke`;
- `check`;
- `build`.

`make check` runs lint, format, strict typing, tests, compile, metadata verification, and smoke coverage.

## 2.16 Source distribution metadata coverage

`MANIFEST.in` now explicitly includes:

- README;
- license;
- changelog;
- citation metadata;
- code of conduct;
- contribution guide;
- privacy policy;
- roadmap;
- security policy;
- support document;
- `what_changed.md`;
- SVG assets;
- Markdown documentation tree.

## 2.17 Citation/version metadata

`CITATION.cff` is updated to version `1.1.0` with release date `2026-08-19`, matching the planned v1.1 release line.

`pyproject.toml` is `1.1.0`.

`src/guessnova/__init__.py` exposes `__version__ = "1.1.0"`.

`CHANGELOG.md` contains a full `1.1.0` section.

## 2.18 Privacy documentation

`PRIVACY.md` now explicitly documents:

- local profile/settings/stats/history/leaderboard data;
- recoverable deleted-profile records;
- no runtime telemetry/analytics/ads/account requirement;
- backup contents;
- recoverable profile-delete behavior;
- 20-profile trash bound;
- difference between recoverable profile deletion and complete application-data deletion;
- separately deleting user-created backup copies when complete removal is desired.

---

# 3. v1.1 test coverage added/expanded

## 3.1 History

Tests cover:

- round-trip serialization;
- bounded retention;
- invalid record rejection;
- structured result filter;
- difficulty filter;
- date `since` filter;
- date `until` filter;
- case-insensitive text search;
- seed text search;
- unparseable timestamp behavior under date filters;
- grouping by day;
- grouping by mode;
- grouping by difficulty;
- grouping by result;
- unsupported grouping rejection.

## 3.2 Profile lifecycle

Tests cover:

- create;
- list;
- switch active profile;
- duplicate create rejection;
- missing switch rejection;
- rename;
- active-profile rename;
- leaderboard rename;
- live-name collision rejection;
- delete to trash;
- leaderboard removal on delete;
- bounded trash retention;
- restore;
- XP restoration;
- leaderboard restoration;
- live-name collision on restore;
- missing trash-record rejection.

## 3.3 State normalization

Additional tests cover:

- schema-0 migration gaining empty deleted-profile trash;
- malformed deleted-profile record rejection;
- normalized deleted profile payload;
- normalized retained trash leaderboard;
- active-profile fallback after deleting the active profile.

## 3.4 CLI integration

Additional tests cover:

- parsing advanced history filters;
- parsed ISO date boundaries;
- grouping parser values;
- positive history limits;
- profile create through CLI;
- profile rename through CLI;
- profile delete through CLI;
- profile restore through CLI;
- filtered/grouped saved history through CLI;
- zero history limit rejection.

## 3.5 Localization

Tests cover:

- English remains default;
- English and Hindi are listed;
- Hindi representative formatted message;
- no missing Hindi catalog keys;
- unknown locale English fallback;
- unsupported catalog-validation locale rejection;
- unknown message-key rejection;
- missing format-value rejection;
- Hindi settings round trip;
- English settings preservation;
- Hindi full-profile serialization.

## 3.6 Textual TUI

Tests cover:

- initial focus;
- Tab ordering;
- input submission;
- winning state;
- local result persistence;
- range hint;
- no attempt consumption for hint;
- focus restoration;
- reset behavior.

---

# 4. Documentation updated for v1.1

Updated/created documentation includes:

- `README.md` — full v1.1 features, history/profile commands, Hindi, TUI, portability, release evidence.
- `CHANGELOG.md` — v1.1 additions/changes/compatibility.
- `ROADMAP.md` — v1.1 completed engineering items and remaining real-media capture gate.
- `PRIVACY.md` — recoverable deletion and backup implications.
- `docs/data_format.md` — deleted-profile state format and compatibility.
- `docs/DATA_FORMAT.md` — concise synchronized reference.
- `docs/localization.md` — English/Hindi catalogs and contributor rules.
- `docs/testing.md` — strict local suite, pilot tests, profile/history/localization coverage, platform matrix.
- `docs/TESTING.md` — synchronized concise test reference.
- `docs/accessibility.md` — active focus/binding/profile-delete/plain/compact/localization guidance.
- `docs/ACCESSIBILITY.md` — synchronized concise accessibility reference.
- `docs/accessibility_evidence_template.md` — manual RC evidence checklist.
- `docs/release.md` — complete v1.1 release gates.
- `docs/RELEASING.md` — synchronized concise release reference.
- `docs/media/README.md` — authentic release-media capture rules.
- `CITATION.cff` — v1.1 metadata.
- `MANIFEST.in` — expanded source-distribution metadata/document inclusion.
- `Makefile` — strict quality target parity.

Older useful documentation was not deleted merely because both uppercase concise references and lowercase canonical guides exist. Where topics overlap, concise uppercase pages now point readers to the canonical detailed page instead of silently remaining stale.

---

# 5. v1.1 commit map

The branch intentionally uses many focused commits.

## 5.1 Feature/test commits

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
- `c91d25c7` — `test: extend smoke flow across 1.1 profile history and locale features`
- `68e9eaea` — `test: cover deleted profile state normalization`
- `54721709` — `fix: tighten history renderer typing and formatting`
- `f6c4ecbe` — `style: format profile command handlers for strict checks`
- `599056e5` — `test: verify Hindi locale persists in profile settings`
- `cabe3c09` — `test: cover locale through profile serialization`

## 5.2 Documentation/release commits

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
- `f1e0f117` — `docs: update citation metadata for 1.1.0`
- `bf86bf40` — `docs: clarify recoverable profile deletion privacy`
- `17024c1d` — `docs: align concise releasing reference with 1.1 process`
- `97c1f185` — `docs: align concise testing reference with 1.1 suite`
- `bc4af975` — `docs: align concise accessibility reference with 1.1 controls`
- `97b9a3eb` — `docs: align concise data format reference with recoverable profiles`

## 5.3 Build/CI/package commits

- `280c5aa0` — `ci: verify package and smoke flow across major platforms`
- `7cb8bcca` — `ci: make distribution glob checks portable on windows`
- `606e371f` — `build: bump package metadata to 1.1.0`
- `dd6ae022` — `build: expose GuessNova 1.1.0 runtime version`
- `dc1478c4` — `build: align make targets with strict quality gates`
- `2bb0b6b1` — `build: include governance and citation metadata in source distribution`
- `ada21dcd` — `ci: gate releases on cross-platform package verification`
- `a3007e5e` — `build: add release metadata consistency verifier`
- `6a1915bb` — `ci: verify synchronized release metadata`
- `d3eae2ee` — `build: add release metadata make target`
- `5c0aef53` — `ci: verify metadata before publishing release artifacts`
- `1c8ea3c8` — `build: mark GuessNova package as typed`

This checkpoint update itself is intentionally another focused documentation commit.

---

# 6. Compatibility rules for v1.1

v1.1 intentionally keeps state schema version `1` because the new data is additive and has safe defaults.

Compatibility guarantees in this implementation:

- schema-1 files without `deleted_profiles` load with empty trash;
- profiles without history still load;
- profiles without locale still default to English;
- profiles without onboarding state still receive the safe default;
- earlier replay version-1 codes remain readable when they omit later optional hint metadata;
- stable serialized mode/difficulty/achievement/schema/replay identifiers are not translated;
- existing live leaderboard rows remain valid;
- profile rename rewrites matching local leaderboard player names;
- deleted-profile leaderboard rows can be restored through trash;
- future schema versions are rejected instead of destructively downgraded.

No schema-2 migration was invented because no incompatible schema-2 change exists yet. The roadmap explicitly retains schema-2 fixtures for the time a real schema-2 design is introduced.

---

# 7. Security/privacy review for v1.1 changes

The new profile/history/localization/TUI work does not introduce a runtime network dependency.

Review points:

- Profile names continue through existing sanitization.
- Profile rename/create collision checks are explicit.
- Profile delete is recoverable and confirmed.
- Trash is bounded.
- Trash is normalized.
- Trash leaderboards go through existing typed leaderboard deserialization.
- Imported backups still pass through state normalization before persistence.
- Hindi/localization is fully offline.
- No translation service/API is used.
- TUI persistence uses the existing local `GameService`/`Storage` path.
- TUI test storage uses temporary directories.
- New tests do not use production user state.
- No new secrets are required.
- Secret-material and dependency audits remain enabled.
- CodeQL remains enabled.
- Release artifacts remain blocked behind verification jobs.

---

# 8. Current verification status for this v1.1 checkpoint

## 8.1 What is known from the prior stable baseline

The v1.0 implementation had previously completed local core validation recorded in the earlier checkpoint, including:

```text
PYTHONPATH=src pytest -q
39 tests passed
```

and successful compile/smoke/CLI-help checks for that earlier code state.

Those historical results are not misrepresented as validation of the new v1.1 code.

## 8.2 v1.1 GitHub Actions state

During v1.1 development, pull-request-triggered CI, CodeQL, and Security-check runs were repeatedly created for the current PR as commits landed.

The branch uses CI concurrency cancellation so superseded runs do not waste runners. Earlier queued runs therefore may be cancelled when newer commits are pushed.

At this checkpoint, the v1.1 branch has been intentionally frozen except for this `what_changed.md` update. A new final workflow set should be observed for the resulting head.

Required final checks:

- CI strict test job:
  - install `.[dev]`;
  - Ruff lint;
  - Ruff format check;
  - strict mypy;
  - pytest with coverage;
  - compileall;
  - release metadata verifier;
  - smoke test.
- CI package jobs:
  - Ubuntu;
  - Windows;
  - macOS.
- Security checks:
  - dependency audit;
  - committed secret-material rejection.
- CodeQL Python analysis.

Do not claim these final-head checks passed until GitHub reports success for the exact final commit.

## 8.3 Environment limitations

This ChatGPT execution environment does not provide a normal editable local checkout of the connected GitHub repository through the GitHub connector, so the exact connected branch is being verified using GitHub Actions rather than falsely reporting commands as run locally against a checkout that was not present.

The connector allows repository reads/writes, PR management, workflow status/jobs/log inspection, and merging. It does not expose every repository administration setting; therefore settings such as branch protection are documented but are not falsely claimed to have been enabled through source-file commits.

---

# 9. Remaining release-candidate-only work

## 9.1 Real screenshots/demo

Source code and capture instructions are complete, but real screenshots/demo recordings must be captured manually from the exact signed-off build.

This remains the one intentionally incomplete v1.1 roadmap item because generating a mock image and labeling it as a real terminal capture would be misleading.

Required evidence/capture docs already exist:

- `docs/accessibility_evidence_template.md`
- `docs/media/README.md`

## 9.2 Manual accessibility evidence

The checklist exists, but its release-candidate observation fields must be completed by a person on the exact build/terminal being signed off. Automated pilot tests cannot truthfully substitute for terminal scaling, visual contrast, and screen-reader/manual keyboard observations.

---

# 10. Merge/release procedure from this checkpoint

1. Read the newest PR head after this file update.
2. Observe CI, CodeQL, and Security checks for that exact head.
3. If a check fails, inspect the failed job steps/log and create a focused fix + regression test/documentation update.
4. Re-run/observe the exact new head.
5. Mark PR `#7` ready for review only after the implementation is stable.
6. Merge with normal `merge` method, not squash, to preserve the granular commit history requested for this project.
7. Record the actual merge commit in `what_changed.md` on `main`.
8. Do not create `v1.1.0` until the release gates and manual release-candidate requirements are satisfied.
9. If `v1.1.0` is tagged, the tag must exactly match `project.version = 1.1.0`; the release workflow will reject a mismatch.
10. Do not rewrite a published tag. Any defect after release should be fixed through a new patch version.

---

# 11. Project identity retained

- Project: **GuessNova**
- Repository: `https://github.com/sanskarIN/guessnova`
- GitHub profile: `https://github.com/sanskarIN`
- License: MIT
- Credit: **Made by the Sanskar**
- Business: `sanskarin@outlook.in`
- Business: `sanskarin.business@gmail.com`
- Support: `supportramsandesh@gmail.com`
- Buy Me a Coffee: `https://buymeacoffee.com/sanskarIN`

No runtime feature is paywalled behind funding.

---

# 12. Optional future work after v1.1

Not blockers for the Python terminal v1.1 implementation:

- real signed-off release screenshots/demo capture;
- completed manual accessibility evidence for a specific tag candidate;
- schema-2 migrations only when a real incompatible schema-2 design exists;
- evaluation of property-testing dependencies if future parser/state defects justify the added dependency;
- further offline locales;
- semantic localization of engine hint meaning after hint semantics are separated from display text;
- richer multi-screen Textual profile/history/settings UI if desired;
- optional TypeScript/Web/PWA edition only if deterministic rules, privacy-first behavior, keyboard accessibility, offline usability, and compatibility are preserved.

This file must be updated again after PR `#7` verification/merge so the final merge SHA and exact workflow conclusions are recorded rather than inferred.
