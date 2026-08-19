# GuessNova — Work Continuity and Final v1 Release Audit

## Current milestone

**GuessNova `v1.0.0` Python terminal edition implementation and release audit are merged into `main`.**

The release-audit work was developed as a dedicated branch and merged through pull request `#6` with merge commit:

- `3cc6fec1945c97605506de7d004d7ef4436f48f3` — `feat: complete GuessNova v1.0 release audit`

The merge intentionally used a normal merge instead of squash so the granular audit history remains available for review.

The optional future TypeScript/Web/PWA edition remains a roadmap item and is not required for the Python terminal edition.

---

## 1. Delivered product scope

### 1.1 Core gameplay

Implemented and retained:

- Classic number-guessing mode.
- Timed mode with difficulty-specific time budgets.
- Streak-tagged gameplay with persistent current/best streak statistics.
- Reverse mode using bounded binary search.
- Deterministic Daily Challenge mode using date-derived deterministic seed logic.
- Easy, Normal, Hard, and Expert difficulty presets.
- Difficulty-specific ranges, attempt limits, and timed limits.
- Range validation that does not consume an attempt for invalid out-of-range guesses.
- Deterministic `--seed` and `GUESSNOVA_SEED` support.
- Automatic smart temperature/direction/parity hints.
- Explicit narrowed-range hints requested with `hint`/`h` during CLI gameplay.
- Optional explicit-hint XP penalties through `--hint-penalty` / `--no-hint-penalty`.
- Hint requests do not consume a guessing attempt.
- Game summaries containing mode, difficulty, target, result, attempts, elapsed time, guesses, optional seed, hint count, and hint penalty.
- Checksum-protected replay codes.
- Replay backward compatibility for version-1 payloads that predate explicit-hint metadata.

### 1.2 Player progression and local data

Implemented and retained:

- Local player profiles.
- Games played/won statistics.
- Win rate.
- Average guesses for wins.
- Current streak and best streak.
- XP progression.
- Achievement/badge tracking.
- Local leaderboard.
- Bounded per-profile session history.
- Session-history mode/difficulty/result/attempt/time/seed/timestamp records.
- Session history capped at the most recent 200 records per profile.
- Human-readable JSON backup/export and import.
- Versioned state schema.
- Migration baseline and future-schema rejection.
- Atomic local state writes using temporary file + flush/fsync + replacement.
- `GUESSNOVA_HOME` override for isolated/custom local data directories.
- Defensive normalization of local/imported profile, settings, history, leaderboard, and top-level state data.

### 1.3 CLI interface

The Rich CLI includes:

- `guessnova play`
- `guessnova reverse`
- `guessnova stats`
- `guessnova history`
- `guessnova leaderboard`
- `guessnova settings`
- `guessnova about`
- `guessnova export`
- `guessnova import`
- `guessnova replay`
- `python -m guessnova`

Additional CLI behavior added during the audit:

- `--plain` mode to disable terminal color.
- `--compact` mode to prefer concise text over Rich panels/tables where appropriate.
- Profile-aware saved semantic themes.
- High-contrast terminal palette.
- Reduced-motion preference persistence.
- Smart-hint preference persistence and per-round override.
- Locale preference persistence.
- First-run onboarding for saved play sessions.
- Onboarding explains basic controls, local-only data behavior, and settings.
- `--no-save` onboarding does not persist state.
- Graceful top-level handling of expected `ValueError`/`OSError` failures so malformed replay codes, missing import files, corrupt local state, invalid dates, and similar expected user/data errors return a clean error message and failure code instead of a Python traceback.
- Error text passed into Rich markup is escaped before display.

### 1.4 Textual TUI

The Textual interface includes:

- App title/subtitle.
- Responsive/adaptive centered card layout.
- Whole-number input.
- Submit button.
- Range-hint button.
- Attempt/range status.
- Correct/wrong/out-of-range/round-over feedback.
- Keyboard `Q` quit binding.
- Keyboard `R` new-game binding.
- Externalized visible labels for localization readiness.

The complete multi-mode/settings/history management surface is intentionally richer in the CLI for v1; expanded Textual screen/pilot coverage is retained in the v1.1 roadmap.

### 1.5 Themes and accessibility

Implemented:

- Semantic theme roles: `accent`, `success`, `warning`, `error`, `info`, and `hint`.
- `nebula`, `aurora`, `mono`, and `high-contrast` palettes.
- Saved profile theme preference.
- Saved high-contrast preference.
- Saved reduced-motion preference.
- `--plain` no-color output.
- `--compact` concise output.
- Keyboard-first CLI flow.
- Text labels accompanying status so meaning does not depend only on color.
- Timed interaction restricted to the opt-in timed mode.
- Accessibility documentation and contributor checklist.

### 1.6 Localization-ready architecture

Added an English-first offline message catalog in `src/guessnova/i18n.py`.

Current behavior:

- English (`en`) is the first and currently shipped locale.
- Locale is stored per profile.
- Unknown persisted locale values fall back safely to English.
- CLI onboarding, gameplay status, statistics/history/settings/About messages, and core Textual labels resolve through the catalog.
- Achievement display labels originate from catalog message keys while compatibility mapping is retained.
- Serialized identifiers such as mode names, difficulty names, schema keys, achievement IDs, and replay field names remain stable and are not translated.
- No runtime translation service or network dependency exists.

Documentation: `docs/localization.md`.

---

## 2. Security, privacy, and reliability hardening

### 2.1 Replay parser hardening

`src/guessnova/replay.py` now validates replay input before constructing a `GameSummary`.

Checks include:

- Maximum encoded replay length.
- URL-safe Base64 validation.
- Envelope structure validation.
- Integrity digest length validation.
- Constant-time digest comparison using `hmac.compare_digest`.
- UTF-8/JSON decoding validation.
- Root object validation.
- Exact supported replay version.
- Required-field presence.
- Unknown-field rejection except documented optional fields.
- Known game mode validation.
- Known difficulty validation.
- Target bounds for the difficulty.
- Attempt count bounds.
- Guess count matching attempts.
- Guess values within difficulty range.
- Winning replays ending at the target.
- Losing replays not containing the target.
- Finite, non-negative elapsed time.
- Signed 64-bit portable seed bounds.
- Bounded non-negative explicit-hint metadata.

Backward compatibility:

- Existing replay version 1 payloads without `hints_used` and `hint_penalty` load with zero defaults.
- Negative deterministic seeds within portable signed-64-bit range round-trip correctly.

### 2.2 Local state normalization

`src/guessnova/storage.py`, `profile.py`, `settings.py`, `history.py`, and `leaderboard.py` were strengthened so local/imported JSON is not trusted merely because it can be parsed.

The normalization path now covers:

- Integer schema version validation without accepting booleans as integers.
- Negative/future schema rejection.
- Profiles container type validation.
- Safe profile-name sanitization.
- Non-negative statistics.
- Games-won clamped to games-played.
- Streak values normalized to coherent bounds.
- Achievement ID type/length filtering.
- Known theme validation.
- Known locale validation.
- Strict boolean settings validation.
- History mode/difficulty/type validation.
- Finite non-negative history elapsed time.
- Bounded history retention.
- Leaderboard player/difficulty/mode/attempt/time/timestamp validation.
- Unknown top-level state fields discarded during normalization.
- Reconstructed typed leaderboard/profile structures before persistence.

### 2.3 Import/export hardening

`src/guessnova/import_export.py` now includes:

- Maximum backup file size.
- Maximum rendered export size.
- Temporary-file export.
- Flush/fsync before replacement.
- Atomic replacement of completed backup output.
- Cleanup of temporary file on failure.
- Pre-parse file-size check.
- UTF-8/JSON error normalization.
- Exact GuessNova export marker requirement.
- Integer export-version validation.
- Future-schema rejection.
- Unsupported older-schema rejection at the export-wrapper layer.
- Object payload validation.
- Imported payload normalization again when stored.

### 2.4 Graceful error boundary

The CLI now catches expected operational/data failures at the command-dispatch boundary:

- `OSError`
- `ValueError`

It prints an escaped user-safe error and returns status code `2`, instead of exposing a traceback for expected malformed data or filesystem conditions.

### 2.5 Privacy behavior

The application remains:

- Local-first.
- Account-free.
- Telemetry-free.
- Analytics-free.
- Advertising-free.
- Free of runtime application network requirements.
- Free of committed runtime secrets/API keys.
- Fully usable without funding/donation.

---

## 3. Automated tests added or expanded during the release audit

The audit expanded coverage beyond the earlier 39-test baseline.

New/expanded suites cover:

### `tests/test_engine.py`

- Correct guess and game completion.
- Wrong guesses and smart hints.
- Out-of-range guesses not consuming attempts.
- Attempt exhaustion.
- Deterministic seeds.
- Invalid difficulty.
- Timed timeout through injected clock.
- Explicit range hints.
- Hint usage counter.
- XP penalty counter.
- No-attempt consumption for explicit hints.
- Optional disabled hint penalty.

### `tests/test_achievements.py`

- First-win achievement.
- One-shot achievement.
- Loss streak reset.
- Expert-win achievement.
- Hint penalty reduction of winning XP.
- Minimum XP floor despite unusually large penalty metadata.

### `tests/test_history.py`

- History entry round-trip.
- 200-entry history bound.
- Recent-entry retention.
- Invalid history item rejection.
- Unknown mode rejection.
- Invalid result/type/timing/seed rejection.

### `tests/test_profile.py`

- Profile round-trip including history.
- Profile-name sanitization.
- Legacy profile payload without history.
- Untrusted statistic normalization.
- Coherent win/streak clamping.
- Invalid achievement filtering.

### `tests/test_service.py`

- Result persistence.
- Achievement unlock propagation.
- History persistence.
- Winning leaderboard insertion.
- Losing history retained without leaderboard insertion.

### `tests/test_settings.py`

- Settings round-trip.
- Unknown-key forward compatibility.
- Invalid theme/locale/boolean fallback.
- Locale persistence.
- Onboarding setting persistence through profile serialization.

### `tests/test_cli.py`

- Parser defaults.
- Plain/compact modes.
- No-subcommand help.
- About command.
- Settings persistence.
- Empty history behavior.
- First-run onboarding persistence.
- No-save onboarding non-persistence.
- Malformed replay graceful failure code.
- Missing import file graceful failure code.
- Corrupt local-state graceful failure code.

### `tests/test_replay.py`

- Replay round-trip.
- Negative-seed round-trip.
- Tamper detection.
- Legacy v1 compatibility without hint metadata.
- Malformed encoded strings.
- Oversized replay strings.
- Invalid version.
- Invalid mode/difficulty/target/result/attempts/timing/guesses/seed/hint values.
- Unknown replay-field rejection.
- Attempt/guess-count mismatch.

### `tests/test_import_export.py`

- Backup round-trip.
- Atomic output leaving only completed backup.
- Wrong format rejection.
- Invalid/unsupported version rejection.
- Invalid JSON rejection.
- Oversized file rejection before parsing.

### `tests/test_leaderboard.py`

- Only wins becoming leaderboard entries.
- Attempts/time sorting.
- Serialization round-trip.
- Invalid imported entry rejection.
- Non-finite timing rejection.
- Positive leaderboard-limit requirement.

### `tests/test_i18n.py`

- English default locale.
- Available locale list.
- Named message formatting.
- Unknown-locale English fallback.
- Unknown key rejection.
- Missing format value rejection.

### `tests/test_themes.py`

- Every theme defining all semantic roles.
- Unknown-theme fallback.
- High-contrast theme/settings acceptance.

### Existing suites retained

The earlier tests for daily challenges, hints, security helpers, storage, reverse gameplay, RNG, package/service behavior, and other domain paths remain in the repository.

---

## 4. CI, static analysis, and release automation

### 4.1 CI workflow

`.github/workflows/ci.yml` now enforces:

1. Python 3.13 setup.
2. Development dependency installation.
3. `ruff check .`
4. `ruff format --check .`
5. `mypy src/guessnova` with strict mypy configuration.
6. `pytest --cov=guessnova --cov-report=term-missing --cov-report=xml`
7. `python -m compileall -q src tests scripts`
8. `python scripts/smoke_test.py`
9. Distribution build.
10. Twine artifact validation.

Superseded PR CI runs are cancelled through workflow concurrency configuration.

### 4.2 Strict typing

`pyproject.toml` contains strict mypy configuration for `src/guessnova`.

The release audit proactively narrowed untrusted object types in profile/history/storage/leaderboard code instead of relying on unsafe broad coercion or type ignores.

### 4.3 Security workflow

`.github/workflows/security.yml` includes:

- Python 3.13 setup.
- Project installation.
- `pip-audit` dependency audit.
- Common committed-secret material rejection.
- Scheduled run.
- Push/PR run.
- Concurrency cancellation for superseded PR runs.

### 4.4 CodeQL

`.github/workflows/codeql.yml` performs Python CodeQL analysis for:

- `main` pushes.
- Pull requests.
- Scheduled runs.

Superseded PR analysis is cancelled.

### 4.5 Tagged release workflow

`.github/workflows/release.yml` was strengthened so a semantic tag cannot directly publish artifacts without verification.

The workflow now:

1. Verifies tag version exactly matches `project.version`.
2. Runs Ruff lint.
3. Runs Ruff formatting check.
4. Runs strict mypy.
5. Runs pytest with coverage.
6. Runs bytecode compilation.
7. Runs the end-to-end smoke test.
8. Runs dependency audit.
9. Builds source/wheel artifacts only after verification succeeds.
10. Validates artifacts with Twine.
11. Creates GitHub release assets/notes only from the verified tagged commit.

Published tags should not be rewritten; defective releases should be corrected with a new patch version.

---

## 5. Repository documentation and governance

Confirmed root/open-source material includes:

- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `SUPPORT.md`
- `PRIVACY.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `what_changed.md`
- `CITATION.cff`
- `.gitignore`
- `.editorconfig`
- `.gitattributes`
- `.env.example`
- `MANIFEST.in`
- `Makefile`

GitHub repository material includes:

- `CODEOWNERS`
- Funding configuration.
- Bug-report issue form.
- Feature-request issue form.
- Issue support links.
- Pull-request template/checklist.
- Dependabot configuration.
- CI workflow.
- CodeQL workflow.
- Security audit workflow.
- Tagged release workflow.

Documentation includes both the earlier reference set and the complementary audit guides:

- Architecture.
- Setup.
- Development.
- Testing.
- Release/releasing.
- Troubleshooting.
- Accessibility.
- Performance.
- Game modes.
- Data format.
- Localization.
- Branding.
- GitHub repository operations.
- Architecture Decision Records.
- Contributor quickstart/guides.

`docs/github_repository.md` documents settings that are not reliably represented as source files, including recommended branch protection, required checks, Discussions categories, labels, milestones, releases, and funding behavior.

Repository-level GitHub settings are documented rather than falsely claimed as enabled when the connector does not expose the corresponding administration action.

---

## 6. Branding, support, and project identity

The repository retains:

- GuessNova editable SVG logo.
- Repository banner artwork.
- MIT license.
- Project credit: **Made by the Sanskar**.
- GitHub profile: `https://github.com/sanskarIN`.
- Repository: `https://github.com/sanskarIN/guessnova`.
- Business: `sanskarin@outlook.in`.
- Business: `sanskarin.business@gmail.com`.
- Support: `supportramsandesh@gmail.com`.
- Buy Me a Coffee: `https://buymeacoffee.com/sanskarIN`.
- Visible BMC badge/link in README.

Funding remains optional and does not gate product features.

---

## 7. Commit strategy and history

The repository was developed with many focused Conventional Commits rather than one monolithic update.

### Representative original implementation commits

- `fa767b55` — `docs: add project overview and quickstart`
- `b7c311e5` — `build: configure Python package and dependencies`
- `e0bcaa05` — `chore: add repository hygiene and packaging metadata`
- `e6c65518` — `feat: add core domain models and package entry points`
- `6d3b5a13` — `feat: add deterministic randomness hints and safety helpers`
- `6de182ed` — `feat: implement classic timed and reverse game engines`
- `d6a3ff0d` — `feat: add daily challenges achievements settings and themes`
- `4854b0bd` — `feat: add leaderboard import export and replay support`
- `91732c2d` — `feat: add local profiles and atomic persistence`
- `0770deb2` — `feat: coordinate game results with profiles and leaderboard`
- `4875bce6` — `feat: add rich command line experience`
- `1e9c11c1` — `feat: add Textual terminal user interface`
- `1ac6a8c9` — `test: cover core guessing reverse hints and daily modes`
- `8ce7eaa9` — `test: cover persistence achievements leaderboard and replay`
- `a7274c00` — `test: cover security settings CLI and service coordination`

### Representative release-quality baseline commits

- `4a2e938a` — `chore: add repository code owners`
- `ab091815` — `chore: configure project funding link`
- `86f3efe8` — `chore: add structured bug report template`
- `35c84032` — `chore: add feature request template`
- `0e9ac4f3` — `chore: add pull request quality checklist`
- `643c9e14` — `chore: configure Dependabot updates`
- `5391fd83` — `test: add end-to-end smoke test`
- `eccc0454` — `ci: add test lint smoke and build workflow`
- `c33f0917` — `ci: add CodeQL security analysis`
- `c4b17114` — `ci: add tagged release workflow`
- `5d569a96` — `ci: add dependency and secret security checks`
- `d61105bc` — `docs: record offline first architecture decision`
- `78ff3a42` — `docs: record deterministic engine decision`
- `caf5098a` — `docs: record interface separation decision`
- `1c44d3bc` — `design: add repository branding banner`
- `9a8775d0` — `docs: close v1 implementation checkpoint`

### Release-audit branch

Pull request `#6` contained **69 commits** and changed **44 files** at the final pre-merge PR inspection.

Representative audit commits include work for:

- Bounded session-history model and persistence.
- History/service/profile regression tests.
- Explicit range hints and XP penalties.
- CLI history/settings/About commands.
- Plain/compact terminal controls.
- Contact metadata centralization.
- Strict state/settings/history/leaderboard input validation.
- Replay parser validation and fuzz-style tests.
- Import/export size and atomic-write hardening.
- Semantic Rich themes and high-contrast support.
- English-first message catalog.
- Locale and first-run settings.
- First-run onboarding.
- Textual localization/adaptive controls.
- Strict mypy/format CI gates.
- Workflow concurrency controls.
- Quality-gated tagged releases.
- Localization/release/GitHub-operations documentation.
- Graceful CLI error boundary.

The pull request was merged with normal merge method so these atomic commits were preserved instead of squashed.

### Commit identity

Git commit metadata observed during repository validation confirms the requested Git identity is being used:

- Author/committer name: `Sanskar`
- Author/committer email: `sanskarin@outlook.in`

---

## 8. Verification evidence

### 8.1 Earlier implementation checkpoint — locally passed

The pre-audit checkpoint recorded successful local verification:

```text
PYTHONPATH=src pytest -q
....................................... [100%]
```

Result at that checkpoint: **39 tests passed**.

Also passed at that checkpoint:

```text
PYTHONPATH=src python3 -m compileall -q src tests scripts
PYTHONPATH=src python3 scripts/smoke_test.py
PYTHONPATH=src python3 -m guessnova
```

`pyproject.toml` also parsed successfully with Python `tomllib`.

### 8.2 Remote workflow evidence observed during the audit

Earlier audit-branch revisions produced observable successful GitHub Actions runs before the later strict typing/format and additional product-hardening commits were added.

Observed successful runs included:

- CI run `32210441668` — successful test/build workflow on an earlier audit revision.
- Security run `32210504715` — successful dependency/secret audit on an earlier audit revision.
- CodeQL on the corresponding earlier audit revision — successful.

These successful earlier runs demonstrate that the repository automation itself was functioning. They are **not** being misrepresented as validation of the later final audit head.

### 8.3 Final audit head hosted-run status

The final pre-merge audit head was:

- `b6ee9005ca01402670a070387852399973567809`

GitHub accepted and queued the final workflows:

- CI run `32212856440`
- Security checks run `32212856436`
- CodeQL run `32212856444`

At the last observation before merging, these jobs remained **queued/pending without a reported test failure or job log**. The CI jobs had not been assigned a runner, so there was no final-head Ruff-format/mypy/pytest/build output available to inspect in this session.

This file deliberately does **not** claim those queued final-head jobs passed.

### 8.4 Environment limitations

The implementation container cannot resolve/download external packages from PyPI/GitHub. The local environment has Python 3.13, Rich, and pytest, but does not have all declared release/dev dependencies such as Textual, Ruff, mypy, build, and Twine available offline.

Because the exact final merged tree could not be cloned into that isolated container through normal network access, the complete strict final suite could not be independently rerun locally after the last audit commits.

The repository workflows remain configured to run the complete suite whenever a hosted runner becomes available.

This is a verification-environment limitation, not a known reproduced application defect.

---

## 9. Bugs and issues found/fixed during the audit

The release audit found and fixed concrete robustness gaps rather than only adding documentation.

Examples:

1. Session history was not previously persisted as a bounded first-class profile capability.
2. Explicit narrowed-range hints and optional hint penalties were not fully implemented.
3. Settings/About/history user-facing CLI controls were incomplete.
4. Saved theme/high-contrast preferences did not fully drive semantic Rich presentation.
5. Imported settings accepted values too loosely.
6. Imported profile statistics needed defensive normalization.
7. Imported history needed strict field and finite-time validation.
8. Imported leaderboard rows needed strict player/mode/difficulty/attempt/time validation.
9. State normalization needed to reject malformed schema containers/types and discard unsupported top-level data.
10. Export/import needed explicit size bounds and atomic output behavior.
11. Replay decoding needed strict Base64/envelope/field/type/range/finite-time validation.
12. Replay portable negative-seed compatibility needed explicit signed bounds.
13. CI did not originally enforce strict formatting and mypy.
14. Tagged releases were not originally gated by the complete verification suite/version-tag invariant.
15. User-facing messages needed an externalized English-first localization boundary.
16. First-run onboarding was missing.
17. Expected CLI data/filesystem errors could surface as Python tracebacks instead of clean failures.

Regression tests were added for these paths where practical.

---

## 10. Known limitations / non-blocking future work

No confirmed blocker/critical defect is recorded from the checks that actually completed.

Remaining non-v1-blocking work:

- Final queued GitHub-hosted strict CI/CodeQL/security results should be inspected when runners execute; do not assume success without the resulting logs/status.
- Real terminal screenshots/demo recording should be captured from a signed-off release environment.
- Textual pilot/widget tests can be expanded for focus order, reset, hint interaction, and input submission.
- Manual accessibility evidence can be recorded per release candidate.
- A second fully reviewed locale can be added to prove the localization architecture end-to-end.
- Windows/macOS/Linux packaging matrix can be added if runner availability/budget makes it practical.
- Schema-2 migration fixtures should be added only when a real schema-2 change exists.
- Optional TypeScript/Web/PWA edition remains future scope.
- Repository-level branch protection and Discussions are documented but are GitHub administration settings and were not falsely claimed as enabled by source changes.
- No release tag was created in this audit because the available GitHub connector actions did not expose a direct tag-creation operation and the final strict hosted checks had not completed.

---

## 11. Exact next continuation procedure

If this project is continued in another chat/session:

1. Read this `what_changed.md` first.
2. Inspect the current `main` tree.
3. Inspect the latest commits before changing files.
4. Inspect CI/CodeQL/Security results for the current `main` head and/or the queued final audit runs above.
5. If a strict check reports a failure, fetch the exact failed job logs and fix the reproducible cause with a focused regression/verification commit.
6. Do not undo useful concurrent changes.
7. Do not force-push.
8. Keep changes atomic and meaningful.
9. Update this file with the exact new commands/runs/results.
10. Only create/publish a release tag after the release workflow prerequisites are verifiably green.

---

## 12. Release notes draft

**GuessNova 1.0.0** is a privacy-first, local-first number-guessing game for Python 3.13+ with Rich CLI and Textual TUI interfaces. It includes Classic, Timed, Streak, Reverse, and deterministic Daily Challenge modes; multiple difficulty levels; automatic and explicit smart hints; optional hint penalties; deterministic seeded challenges; replay codes; profiles; XP and achievements; local statistics; bounded session history; a local leaderboard; validated import/export; semantic themes; high-contrast/plain/compact accessibility controls; first-run onboarding; an English-first localization-ready message catalog; atomic and defensively normalized persistence; hardened replay/backup parsers; automated regression and smoke tests; strict CI/type/format/security automation; CodeQL; dependency auditing; quality-gated release automation; open-source governance; branding assets; funding/support information; and complete project documentation.

**Made by the Sanskar**
