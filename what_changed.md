# GuessNova — Complete Work Continuity and v1.1 Merged Checkpoint

## Current milestone

**GuessNova `v1.1.0` implementation is merged into `main`.**

The v1.1 implementation was developed on:

- Branch: `release/v1.1.0-ux-accessibility-20260819`
- Pull request: `#7` — `feat: ship GuessNova 1.1 UX accessibility and portability`
- Base commit: `c20b1dc9737ea215f8b4d5262c36eeea90907c68`
- Final PR head: `f74c76bc7a010a29b14c592ab9a4ca83f1c1496c`
- Merge commit: `b303b764c83dbbca5183ee5b974bd280e7fca0cd`
- Merge method: normal merge, not squash
- PR commits preserved: **56 granular commits**
- Package/runtime/citation version: `1.1.0`
- Requested Git commit email observed in repository commit metadata: `sanskarin@outlook.in`

The normal merge was intentional so the feature/fix/test/docs/build/CI history remains reviewable instead of being collapsed into a single squash commit.

The prior v1.0 release-audit PR was `#6`, merged with:

- `3cc6fec1945c97605506de7d004d7ef4436f48f3` — `feat: complete GuessNova v1.0 release audit`

The v1.0 follow-up checkpoint on `main` was:

- `c20b1dc9737ea215f8b4d5262c36eeea90907c68` — `docs: record final merged v1 release audit and verification state`

This file is the current continuation source of truth after the v1.1 merge.

---

# 1. Current product scope

## 1.1 Core game modes

GuessNova retains the complete v1 gameplay foundation:

- Classic number guessing.
- Timed mode with difficulty-specific time budgets.
- Streak-tagged mode.
- Reverse mode using bounded binary search.
- Deterministic daily challenge mode.
- Easy difficulty.
- Normal difficulty.
- Hard difficulty.
- Expert difficulty.
- Difficulty-specific ranges.
- Difficulty-specific attempt budgets.
- Difficulty-specific timed limits.
- Out-of-range validation without consuming an attempt.
- Deterministic `--seed` runs.
- Deterministic `GUESSNOVA_SEED` environment-variable runs.

## 1.2 Hints

GuessNova includes two hint systems:

- automatic smart temperature/direction/parity feedback after valid wrong guesses;
- explicit narrowed-range hints requested with `hint` or `h`.

Explicit range-hint behavior:

- does not consume a guessing attempt;
- increments a hint counter;
- optionally accumulates an XP penalty;
- supports `--hint-penalty`;
- supports `--no-hint-penalty`;
- remains deterministic relative to the hidden target/difficulty.

Profile smart-hint preference is used by both the Rich CLI and the Textual TUI after the v1.1 TUI fix.

## 1.3 Game summaries and replay codes

Completed game summaries contain:

- mode;
- difficulty;
- target;
- won/lost state;
- attempts;
- elapsed seconds;
- guess sequence;
- optional seed;
- explicit hint count;
- accumulated hint penalty.

Replay codes include:

- version marker;
- compact JSON summary;
- SHA-256-derived integrity digest;
- URL-safe Base64 envelope.

Replay decoding validates:

- maximum encoded size;
- Base64/envelope structure;
- digest length;
- constant-time digest comparison;
- UTF-8/JSON validity;
- root object type;
- supported replay version;
- required fields;
- field allowlist;
- known mode;
- known difficulty;
- target within difficulty range;
- bounded attempt count;
- guess count matching attempts;
- guess values inside the difficulty range;
- winning replay ending on the target;
- losing replay not containing the target;
- finite/non-negative elapsed time;
- signed 64-bit portable seed bounds;
- bounded non-negative hint metadata.

Existing version-1 replay codes that predate optional hint metadata continue to load with zero-value defaults.

---

# 2. Player profiles, progression, and local data

## 2.1 Player progression

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

## 2.2 Local leaderboard

Winning results can become local leaderboard rows containing:

- player name;
- mode;
- difficulty;
- attempt count;
- elapsed seconds;
- creation timestamp.

Rows are normalized before use and sorted through the leaderboard scoring rules.

## 2.3 Session history

History remains bounded to the most recent 200 records per profile.

Each valid history record can contain:

- mode;
- difficulty;
- result;
- attempt count;
- elapsed seconds;
- optional seed;
- played timestamp.

v1.1 moves history querying into reusable domain helpers rather than keeping it only in the UI layer.

`filter_history(...)` supports:

- mode;
- difficulty;
- result (`win`/`loss`);
- free-text query;
- start date;
- end date.

Free-text matching includes:

- timestamp;
- mode;
- difficulty;
- result;
- attempts;
- seed.

`group_history(...)` supports:

- day;
- mode;
- difficulty;
- result.

## 2.4 Advanced history CLI

Current examples:

```bash
guessnova history --limit 20
guessnova history --result win --difficulty hard
guessnova history --since 2026-08-01 --until 2026-08-31
guessnova history --search daily --group-by mode
guessnova --plain --compact history --group-by result
```

History and leaderboard limits now require positive integers.

---

# 3. v1.1 profile lifecycle and undoable deletion

## 3.1 Profile commands

Added:

```bash
guessnova profiles list
guessnova profiles create NAME
guessnova profiles use NAME
guessnova profiles rename CURRENT NEW
guessnova profiles delete NAME
guessnova profiles trash
guessnova profiles restore NAME
```

Options:

```text
profiles create NAME --no-activate
profiles delete NAME --yes
profiles restore NAME --no-activate
```

## 3.2 Storage APIs

Added:

- `list_profile_names()`;
- `active_profile_name()`;
- `create_profile()`;
- `set_active_profile()`;
- `rename_profile()`;
- `delete_profile()`;
- `list_deleted_profile_names()`;
- `restore_profile()`.

## 3.3 Profile invariants

Implemented safeguards:

- duplicate live names are rejected;
- switching to a missing profile is rejected;
- rename to a different existing live name is rejected;
- profile rename updates matching local leaderboard player names;
- deleting the active profile chooses another remaining live profile when possible;
- imported/orphaned active-profile names are normalized to an existing live profile when live profiles exist;
- restore is rejected on live-name collision;
- restore is rejected for missing trash records.

## 3.4 Recoverable local profile trash

New bound:

```text
MAX_DELETED_PROFILES = 20
```

Normalized state now contains additive `deleted_profiles` data.

A retained deleted-profile record contains:

- deletion timestamp;
- normalized profile payload;
- normalized leaderboard rows that belonged to the deleted profile.

Deletion behavior:

1. remove the profile from the live profile map;
2. remove its leaderboard rows from the live leaderboard;
3. save the profile and removed rows into recoverable trash;
4. bound trash to the newest 20 records;
5. update the active profile if necessary.

Restore behavior:

1. reject a live-name collision;
2. load the normalized trash profile;
3. return it to the live profile map;
4. restore retained leaderboard rows through normal leaderboard insertion rules;
5. optionally make the restored profile active;
6. remove the recovered trash entry.

## 3.5 Delete confirmation

`guessnova profiles delete NAME` normally requires typing the exact normalized profile name.

`--yes` intentionally bypasses typed confirmation for explicit scripted/non-interactive workflows.

The operation is recoverable, not secure erasure.

`PRIVACY.md` now distinguishes:

- recoverable profile deletion;
- deleting the entire GuessNova application-data directory;
- separately deleting user-created backup/export copies.

---

# 4. Localization

## 4.1 Shipped locales

GuessNova now ships two complete offline catalogs:

- `en` — English, default and fallback;
- `hi` — Hindi.

## 4.2 Locale settings

Locale is persisted per profile.

Examples:

```bash
guessnova settings --locale en
guessnova settings --locale hi
```

Unknown/malformed persisted locale values fall back safely to English.

## 4.3 Catalog completeness

Added:

- `available_locales()`;
- `catalog_missing_keys(locale)`.

Tests require the Hindi catalog to contain every English catalog key.

Representative named placeholders are tested in both locales.

## 4.4 Stable machine identifiers

The following intentionally remain untranslated compatibility identifiers:

- CLI command names;
- environment variables;
- mode IDs;
- difficulty IDs;
- schema keys;
- achievement IDs;
- replay field names.

This keeps saves, commands, exports, and replay codes independent of presentation locale.

## 4.5 Current localization boundary

Catalog-backed presentation includes onboarding, gameplay status/prompts, reverse messages, statistics/history headings, settings, profile-management messages, About/data-transfer messages, and core Textual labels.

Some engine-generated semantic hint prose remains a domain string. The localization documentation explicitly requires separating hint meaning from display text before translating those strings instead of changing serialized/domain semantics merely for presentation.

---

# 5. Textual TUI work in v1.1

## 5.1 Dependency injection and local persistence

`GuessNovaApp` now accepts optional injected:

- profile name;
- `GuessGame`;
- `Storage`.

This enables deterministic pilot tests and temporary local state.

Completed TUI changes:

- loads active profile locale;
- loads saved smart-hint preference;
- localized core labels;
- explicit Range Hint button;
- initial focus on the numeric input;
- predictable focus path;
- refocus after empty input, guesses, errors, and hints;
- persisted completed results through `GameService`;
- exactly-once save guard per completed round;
- priority `R` reset binding;
- priority `Q` quit binding;
- adaptive main-card width;
- reset preserves difficulty;
- reset preserves mode;
- reset preserves deterministic seed;
- reset clears the finished-result save guard.

## 5.2 TUI regression tests

`tests/test_tui.py` covers:

- initial focus on guess input;
- Tab from input to submit;
- Tab from submit to hint;
- Enter submission;
- deterministic winning state;
- persisted games-played/games-won;
- explicit hint count;
- no attempt consumption for range hints;
- focus returning to input after hint;
- reset clearing attempts;
- reset producing an unfinished round;
- reset refocusing input;
- loading saved smart-hint preference;
- deterministic seeded reset preserving the same seed/target.

Pilot scenarios use `asyncio.run(...)` and Textual `run_test()` without adding `pytest-asyncio`.

---

# 6. Accessibility and manual evidence

## 6.1 Current accessibility-oriented behavior

- Keyboard-first CLI.
- Keyboard-first TUI interaction.
- Descriptive text rather than color-only meaning.
- `--plain` no-color mode.
- `--compact` reduced presentation mode.
- High-contrast saved preference.
- Reduced-motion saved preference.
- Timed interaction only in opt-in timed mode.
- Predictable TUI focus sequence.
- Priority TUI reset/quit bindings.
- Recoverable/described profile deletion.
- Offline English/Hindi presentation.

## 6.2 Release evidence template

Created:

- `docs/accessibility_evidence_template.md`.

It requires release-candidate evidence for:

- version/tag/commit;
- OS and terminal;
- font/scale;
- locale;
- keyboard-only CLI;
- keyboard-only reverse mode;
- profile management;
- deletion confirmation;
- history filtering;
- plain/compact output;
- no-color meaning;
- TUI focus order;
- Enter submission;
- hint interaction;
- reset/quit;
- result persistence;
- narrow terminal;
- increased font scale;
- high contrast;
- reduced motion;
- English rendering;
- Hindi rendering;
- defects and release sign-off.

Automated tests supplement this checklist; they do not falsely replace real terminal/screen-reader/scaling/contrast observations.

---

# 7. Release media authenticity

Created:

- `docs/media/README.md`.

Rules:

- no fabricated terminal screenshot may be labeled as a real release capture;
- no reconstructed/mock recording may be labeled as the release demo;
- media must come from the exact signed-off release build;
- exact source commit/tag must be recorded;
- deterministic gameplay should be used where practical;
- capture environment must not expose credentials, private terminal history, unrelated paths, tokens, or personal data.

Real screenshots/demo media remain a manual release-candidate capture task. The repository intentionally does not contain fabricated media merely to mark the roadmap checkbox complete.

---

# 8. Persistence, import/export, and privacy

## 8.1 State format

State remains schema version `1` because v1.1 additions are additive and have safe defaults.

Current normalized top-level state includes:

- `schema_version`;
- `active_profile`;
- `profiles`;
- `leaderboard`;
- `deleted_profiles`.

## 8.2 Additive compatibility

Existing schema-1 state remains readable when it lacks:

- history;
- locale;
- onboarding state;
- deleted-profile trash.

No schema-2 migration was fabricated because no incompatible schema-2 design exists yet.

## 8.3 State normalization

Normalization covers:

- integer schema version without treating booleans as integers;
- negative/future schema rejection;
- profiles-container type;
- profile-name sanitization;
- non-negative statistics;
- coherent games-won/streak bounds;
- achievement ID filtering;
- known theme;
- known locale;
- strict booleans;
- history mode/difficulty/result/value validation;
- finite history timing;
- bounded history;
- leaderboard validation;
- bounded/normalized profile trash;
- orphaned active-profile repair;
- dropping unknown top-level state fields.

## 8.4 Atomic state and backup writes

State writes use:

- temporary file in the destination directory;
- JSON rendering;
- flush;
- `fsync`;
- replacement;
- cleanup of leftover temp path on failure.

Import/export includes:

- GuessNova wrapper marker;
- version check;
- future-version rejection;
- object payload validation;
- maximum backup sizes;
- atomic output;
- imported-state normalization before final persistence.

## 8.5 Runtime privacy

GuessNova remains:

- account-free;
- telemetry-free;
- analytics-free;
- advertising-free;
- free of required runtime network calls;
- usable without donation/funding;
- free of required secrets/API keys.

---

# 9. CI, security, portability, and release engineering

## 9.1 Strict CI test job

`.github/workflows/ci.yml` requires:

1. Python 3.13.
2. `.[dev]` installation.
3. `ruff check .`.
4. `ruff format --check .`.
5. strict `mypy src/guessnova`.
6. pytest with coverage.
7. `compileall` over source/tests/scripts.
8. release metadata verification.
9. end-to-end smoke test.

Superseded PR runs are cancelled through concurrency settings.

## 9.2 Cross-platform package matrix

CI additionally uses:

- Ubuntu latest;
- Windows latest;
- macOS latest.

Each platform:

1. installs Python 3.13;
2. installs build/Twine tooling;
3. builds distributions;
4. validates distributions;
5. installs the generated wheel;
6. launches `python -m guessnova --help`;
7. runs the end-to-end smoke test.

Bash is explicitly used for distribution wildcard commands so Windows runner shell expansion does not make those steps unreliable.

## 9.3 Security workflow

Security workflow retains:

- dependency audit using `pip-audit`;
- common committed secret-material rejection;
- push/PR triggers;
- scheduled runs;
- concurrency handling.

## 9.4 CodeQL

Python CodeQL remains configured for:

- `main` pushes;
- pull requests;
- scheduled analysis.

## 9.5 Tagged release workflow

The tag workflow now blocks publishing behind both:

- strict verification job;
- Ubuntu/Windows/macOS package matrix.

Strict release verification includes:

- exact tag/project-version match;
- Ruff lint;
- Ruff formatting;
- strict mypy;
- pytest coverage;
- compileall;
- release metadata synchronization;
- smoke test;
- dependency audit.

Only then may `build-release` create and validate final distributions and attach them to GitHub release notes.

---

# 10. Release metadata synchronization

Created:

- `scripts/verify_release_metadata.py`.

It verifies that:

- `pyproject.toml` has a valid project version;
- `guessnova.__version__` matches it;
- `CITATION.cff` matches it;
- `CHANGELOG.md` has a heading for it.

Current version values are synchronized at:

```text
1.1.0
```

The verifier runs in normal CI, `make check`, and tag-release verification.

A `src/guessnova/py.typed` marker is included so downstream type checkers can recognize the package's inline typing information.

---

# 11. v1.1 end-to-end smoke coverage

`scripts/smoke_test.py` now checks:

- deterministic winning game;
- profile progression;
- first-win achievement;
- leaderboard insertion;
- filtered winning history;
- replay round trip;
- profile rename;
- active-profile rename behavior;
- leaderboard rename behavior;
- profile deletion to trash;
- trash listing;
- profile restoration;
- leaderboard restoration;
- Hindi catalog completeness;
- representative Hindi formatting;
- backup/export;
- backup/import;
- reverse binary search.

This smoke script is reused by CI and package/release jobs.

---

# 12. Tests added/expanded in v1.1

## 12.1 History

Coverage includes:

- serialization round trip;
- 200-record bound;
- recent-record retention;
- malformed-record rejection;
- result filter;
- difficulty filter;
- since-date filter;
- until-date filter;
- case-insensitive search;
- seed search;
- invalid date handling;
- day grouping;
- mode grouping;
- difficulty grouping;
- result grouping;
- unsupported grouping rejection.

## 12.2 Profile lifecycle

Coverage includes:

- create;
- list;
- active switch;
- duplicate rejection;
- missing-switch rejection;
- rename;
- active rename;
- leaderboard rename;
- rename collision;
- delete;
- leaderboard removal;
- trash bound;
- restore;
- XP restoration;
- leaderboard restoration;
- restore collision;
- missing trash rejection.

## 12.3 State normalization

Coverage includes:

- schema-0 migration;
- future-schema rejection;
- invalid JSON;
- invalid profile container;
- untrusted profile/stat normalization;
- leaderboard normalization;
- deleted-profile record normalization;
- malformed trash rejection;
- active profile selection after delete;
- orphaned active-profile repair.

## 12.4 CLI

Coverage includes:

- advanced history arguments;
- parsed ISO date filters;
- grouping values;
- positive limits;
- profile create/rename/delete/restore integration;
- saved-session filtering/grouping;
- zero-limit parser rejection.

## 12.5 Localization

Coverage includes:

- English default;
- English/Hindi available locale list;
- Hindi formatted messages;
- complete Hindi key set;
- unknown-locale fallback;
- unsupported catalog validation;
- unknown key rejection;
- missing placeholder rejection;
- Hindi settings round trip;
- Hindi profile round trip.

## 12.6 Textual

Coverage includes:

- initial focus;
- Tab order;
- Enter submission;
- result persistence;
- hint interaction;
- hint attempt preservation;
- focus restoration;
- reset;
- smart-hint setting loading;
- seeded reset determinism.

Existing v1 suites for engine, achievements, replay, import/export, leaderboard, profile, service, settings, themes, security helpers, RNG, daily challenge, and other domain paths remain in the repository.

---

# 13. Documentation and repository quality

## 13.1 Updated/created documentation

- `README.md` — v1.1 commands/features/localization/profile/history/TUI/portability.
- `CHANGELOG.md` — v1.1 release changes.
- `ROADMAP.md` — current completion and manual-media gate.
- `PRIVACY.md` — recoverable deletion/backup behavior.
- `CONTRIBUTING.md` — strict quality/localization/TUI/accessibility rules.
- `what_changed.md` — this complete continuation checkpoint.
- `docs/data_format.md` — canonical detailed state/replay/export format.
- `docs/DATA_FORMAT.md` — synchronized concise data reference.
- `docs/localization.md` — English/Hindi architecture and contributor rules.
- `docs/testing.md` — complete testing strategy.
- `docs/TESTING.md` — synchronized concise testing reference.
- `docs/accessibility.md` — current accessibility behavior.
- `docs/ACCESSIBILITY.md` — synchronized concise accessibility reference.
- `docs/accessibility_evidence_template.md` — manual release checklist.
- `docs/release.md` — complete release process.
- `docs/RELEASING.md` — synchronized concise releasing reference.
- `docs/media/README.md` — authentic release-media rules.

## 13.2 Repository/governance material retained

- MIT `LICENSE`.
- `CODE_OF_CONDUCT.md`.
- `SECURITY.md`.
- `SUPPORT.md`.
- `CITATION.cff`.
- `.editorconfig`.
- `.gitattributes`.
- `.gitignore`.
- `.env.example`.
- `MANIFEST.in`.
- `Makefile`.
- `CODEOWNERS`.
- Funding config.
- Issue forms.
- Pull-request template.
- Dependabot config.
- CI workflow.
- Security workflow.
- CodeQL workflow.
- Release workflow.
- SVG logo/banner assets.

## 13.3 Pull-request checklist

The PR template now asks contributors to verify:

- Ruff lint;
- Ruff format;
- strict mypy;
- pytest;
- compileall;
- release metadata;
- smoke test;
- privacy;
- compatibility;
- recoverable destructive actions;
- localization;
- stable serialized identifiers;
- color-independent meaning;
- keyboard focus/bindings;
- temporary/deterministic test state;
- changelog/work-continuity updates;
- accessibility/media release impact.

---

# 14. Source distribution/package metadata

`MANIFEST.in` explicitly includes:

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
- work-continuity document;
- SVG assets;
- Markdown documentation tree.

Current metadata:

- project version: `1.1.0`;
- runtime version: `1.1.0`;
- citation version: `1.1.0`;
- Python requirement: `>=3.13`;
- license: MIT;
- author email in package metadata: `sanskarin@outlook.in`.

---

# 15. Complete v1.1 PR commit map

The merged PR retained 56 focused commits.

## 15.1 History/profile/localization/TUI implementation

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

## 15.2 Accessibility/docs/release preparation

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

## 15.3 Packaging/CI/metadata work

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

## 15.4 Final audit/fix/documentation commits

- `bbd14834` — `docs: record complete GuessNova 1.1 continuation checkpoint`
- `3764de3c` — `fix: honor TUI hint preference and deterministic reset`
- `cbededf3` — `test: cover TUI saved hint preference and seeded reset`
- `3913b40e` — `style: format advanced history regression tests`
- `a7216b74` — `fix: normalize orphaned active profile references`
- `ce50d515` — `test: cover orphaned active profile normalization`
- `0434395e` — `docs: align contribution guide with 1.1 quality gates`
- `f74c76bc` — `docs: strengthen pull request validation checklist`

The PR merge commit is:

- `b303b764c83dbbca5183ee5b974bd280e7fca0cd` — `feat: ship GuessNova 1.1 UX accessibility and portability`

This current `what_changed.md` update is a post-merge main-branch checkpoint and is intentionally separate from the 56 preserved PR commits.

---

# 16. Exact workflow status at PR merge

The final PR head was:

```text
f74c76bc7a010a29b14c592ab9a4ca83f1c1496c
```

Immediately before/after merge, the connector reported these pull-request workflow states for that exact head:

- CI run `32215436765`: `queued`, no conclusion.
- CodeQL run `32215436694`: `queued`, no conclusion.
- Security checks run `32215436661`: `pending`, no conclusion.

The earlier runs that showed `cancelled` conclusions were superseded by later branch commits under the configured concurrency behavior; they were not test failures.

No final-head workflow returned a failure conclusion before the merge.

This file **does not claim the queued/pending final-head workflows passed**. The merge was completed because the user requested the complete repository work in the current interaction and the GitHub-hosted runners remained queued rather than producing actionable failure logs.

The v1.1 code was subjected to a file-by-file static review in addition to the added tests/workflows, including targeted fixes for:

- history renderer list-invariance typing;
- profile command formatting;
- Windows distribution-glob shell behavior;
- TUI priority reset/quit bindings;
- TUI smart-hint setting usage;
- deterministic reset seed preservation;
- orphaned active-profile normalization;
- stale privacy/release/testing/accessibility/data-format docs;
- metadata drift prevention.

If those GitHub runs later execute and expose a reproducible failure, the next continuation should inspect the exact failed job/step, add a focused regression fix, and preserve the same granular commit discipline.

---

# 17. Manual release-candidate gates not falsely automated

Two categories intentionally still require real release-candidate evidence.

## 17.1 Manual accessibility evidence

The source checklist is complete, but a person must complete its observation fields against an exact candidate build/terminal.

File:

- `docs/accessibility_evidence_template.md`

## 17.2 Real screenshots/demo media

Capture instructions and provenance rules are complete, but no fabricated screenshot/demo was added.

File:

- `docs/media/README.md`

A real capture must come from a signed-off commit/tag and record that provenance.

These are release-candidate evidence tasks, not missing application source code.

---

# 18. Tag/release rule

Do **not** create or move `v1.1.0` merely because the implementation is merged.

Before tagging:

1. observe successful required checks for the release candidate;
2. complete manual accessibility evidence;
3. capture any desired real release media from the signed-off build;
4. confirm `pyproject.toml`, runtime version, citation version, and changelog still match `1.1.0`;
5. create immutable `v1.1.0` only from the selected release commit.

The release workflow independently re-runs strict verification and the three-platform package matrix before it can publish artifacts.

Published tags should not be rewritten. A post-release defect should become a new patch version.

---

# 19. Remaining optional future work

Not blockers for the merged Python terminal v1.1 implementation:

- manual release-candidate accessibility evidence;
- authentic signed-off terminal screenshots/demo recording;
- schema-2 migration fixtures only when a real incompatible schema-2 design exists;
- property-testing dependency evaluation only if future parser/state defects justify it;
- additional offline locales;
- semantic localization of engine-generated hint meaning after separating semantics from display prose;
- richer multi-screen Textual profile/history/settings UI;
- optional TypeScript/Web/PWA edition only if privacy, deterministic rules, stable challenge/replay semantics, offline usability, and keyboard accessibility remain intact.

---

# 20. Project identity

- Project: **GuessNova**
- Repository: `https://github.com/sanskarIN/guessnova`
- GitHub profile: `https://github.com/sanskarIN`
- License: MIT
- Credit: **Made by the Sanskar**
- Business email: `sanskarin@outlook.in`
- Business email: `sanskarin.business@gmail.com`
- Support email: `supportramsandesh@gmail.com`
- Buy Me a Coffee: `https://buymeacoffee.com/sanskarIN`

Every core GuessNova feature remains usable without donating.
