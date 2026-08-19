# GuessNova — Complete Work Continuity through v1.4 Full Textual Workspace

## Current milestone

**GuessNova `v1.4.0` full Textual local-workspace implementation is complete on its release branch and is under pull request review.**

Current release work:

- Repository: `https://github.com/sanskarIN/guessnova`
- Branch: `release/v1.4.0-tui-workspace-20260819`
- Pull request: `#10` — `feat: build GuessNova 1.4 full Textual workspace`
- Base branch: `main`
- Base commit: `c45b163b48353aa307d73ecc6095732803cd5503`
- Pre-handoff branch head: `2afc650a1d453122058963692aeb87f6165e3da2`
- Granular v1.4 commits before this handoff commit: **51**
- This `what_changed.md` update is intentionally the next focused commit and becomes the final PR verification head unless a concrete current-head audit/CI failure requires another fix.
- Package version: `1.4.0`
- Runtime version: `1.4.0`
- Citation version: `1.4.0`
- Local state schema: `2`
- Backup wrapper version: `2`
- Supported legacy backup wrapper: `1`
- Replay format version: `1`
- Doctor machine report protocol: `1`
- Python requirement: `>=3.13`
- License: MIT
- Requested Git commit identity email: `sanskarin@outlook.in`

The v1.4 scope is a **presentation/application-layer expansion**. It intentionally does **not** invent schema 3, backup wrapper 3, replay version 2, Doctor report version 2, a third locale, signing credentials, or a new testing dependency merely to create activity.

The pull request must be merged with a **normal merge**, not squash, so the granular implementation/fix/test/docs/build/CI history remains visible.

---

# 1. Continuity preservation

The complete previous active continuity document was preserved **byte-for-byte** before replacing the live handoff with this v1.4-focused record.

Archived previous checkpoint:

- `docs/continuity/v1_3_merged_checkpoint.md`
- The archive points to the exact former `what_changed.md` blob and contains the full v1.3/v1.2/v1.1/v1.0 continuity record.

Important previous release checkpoints retained in Git history:

- v1.0 audit merge: `3cc6fec1945c97605506de7d004d7ef4436f48f3`
- v1.0 post-audit checkpoint: `c20b1dc9737ea215f8b4d5262c36eeea90907c68`
- v1.1 normal merge: `b303b764c83dbbca5183ee5b974bd280e7fca0cd`
- v1.1 post-merge checkpoint: `9a511102efc3b11bdf68a8ce7f7ca1692874df40`
- v1.2 normal merge: `f17594b16426513850c9a1c118d8fcec225702cd`
- v1.2 post-merge checkpoint: `86ac8754ad07daaa40706c20a8e61fb4024a95e0`
- v1.3 normal merge: `e57cac65b20e6351200ac3ab25a3cf2a07ed9308`
- v1.3 post-merge checkpoint / v1.4 base: `c45b163b48353aa307d73ecc6095732803cd5503`

No previous implementation record was discarded to make this file shorter.

---

# 2. v1.4 product goal

Before v1.4, the Rich CLI had mature local-data workflows while `guessnova-tui` was still primarily one gameplay card.

The real product gap was therefore not another storage schema or another game rule. The gap was an app-like local terminal workspace that exposes the already-proven product capabilities without duplicating persistence or creating network services.

v1.4 turns `guessnova-tui` into a six-pane keyboard-first workspace:

1. **Play**
2. **Profiles**
3. **History**
4. **Leaderboard**
5. **Settings**
6. **Recovery**

The workspace continues to use the same local `Storage`, `GameService`, history, leaderboard, settings, diagnostics, and backup-preflight boundaries as the CLI/Doctor implementation.

---

# 3. Textual workspace architecture

## 3.1 `src/guessnova/tui_workspace.py`

A reusable Textual-independent helper layer was added so domain/application behavior can be tested without rendering widgets.

Current helpers include:

### `WorkspaceSnapshot`

Captures a read-only local workspace view:

- active/selected profile;
- live profile names;
- recoverable deleted-profile names;
- leaderboard count;
- local diagnostic report.

### `ProfileSummary`

Derives:

- games played;
- games won;
- win rate;
- average guesses;
- current streak;
- best streak;
- XP;
- achievement count;
- history count.

### `build_workspace_game(...)`

Builds deterministic non-Reverse challenges from TUI-friendly string values.

Supported behavior:

- validates known `GameMode` values;
- validates known difficulties;
- accepts optional integer seed text;
- produces deterministic seeded games;
- accepts ISO `YYYY-MM-DD` daily dates;
- creates reproducible daily games;
- refuses Reverse because Reverse retains its dedicated interaction model;
- returns clear validation errors for invalid seed/date/mode/difficulty input.

This helper is intentionally reusable even though the v1.4 mounted Play pane keeps the established game flow rather than adding a large challenge-configuration form into the same release.

### `select_history(...)`

Returns newest-first bounded active-profile history with filters for:

- mode;
- difficulty;
- win/loss result;
- free-text query;
- since date;
- until date;
- positive limit.

### `select_leaderboard(...)`

Filters the already-ranked local leaderboard by:

- mode;
- difficulty;
- case-insensitive player substring;
- positive limit.

The helper **does not re-rank** filtered data; it preserves `Storage` / leaderboard ordering.

### `save_workspace_settings(...)`

Persists validated settings through `Settings.from_dict(...)` and `Storage.save_profile(...)` while preserving the existing `onboarding_complete` state.

## 3.2 `src/guessnova/tui_widgets.py`

A focused widget layer was added for keyboard responsibilities that should not be global to the whole application.

### `GuessInput`

`GuessInput` subclasses Textual `Input` and owns the legacy Play-only single-letter shortcuts:

- `R` → request a new round;
- `Q` → quit.

A custom `GuessInput.NewRoundRequested` message is posted for reset rather than coupling the input widget to GuessNova game construction.

Why this exists:

- the original one-card TUI could safely make `R/Q` global/priority because its main text field was integer-only;
- v1.4 adds profile names, history search, leaderboard player filter, dates, and backup paths;
- globally stealing `r` or `q` from those fields would make ordinary text entry unusable;
- making app-level single-letter bindings merely non-priority introduced a regression risk that the numeric Input might consume the keys instead of resetting/quitting;
- the final solution scopes `R/Q` to the numeric Play widget and keeps global `Ctrl+R/Ctrl+Q` available everywhere.

This was a concrete static-audit issue found and fixed before final handoff.

## 3.3 `src/guessnova/tui.py`

The main Textual app now owns:

- widget composition;
- pane navigation;
- focus orchestration;
- button/input events;
- table refresh;
- active-profile transition orchestration;
- high-contrast screen state;
- read-only diagnostics rendering;
- read-only backup-preflight rendering.

It does **not** implement a second local database or duplicate storage normalization.

---

# 4. Play pane

The Play pane preserves the original TUI contract:

- starts as the initial pane;
- initial focus lands on `#guess`;
- numeric whole-number input;
- Submit button;
- Range Hint button;
- attempts/range display;
- automatic smart hints when enabled;
- explicit hint requests;
- out-of-range feedback;
- win/loss feedback;
- completed-round persistence through `GameService`;
- exactly-once `_result_saved` guard;
- deterministic seeded reset behavior.

Keyboard behavior:

- focused Play input: plain `R` resets;
- focused Play input: plain `Q` quits;
- anywhere: `Ctrl+R` resets and returns to Play;
- anywhere: `Ctrl+Q` quits.

Completed results refresh:

- profile summary;
- History table/status;
- Leaderboard table/status;
- Recovery diagnostic counts.

---

# 5. Profiles pane

The Profiles pane reuses the existing `Storage` lifecycle APIs.

Supported UI operations:

- view active-profile statistics summary;
- view unlocked achievement labels;
- choose a saved profile;
- activate a profile;
- create a profile;
- rename a selected profile;
- refresh profile/trash state;
- delete a selected profile into recoverable trash;
- restore a selected deleted profile.

## 5.1 Exact-name deletion confirmation

The TUI does not expose a one-click destructive delete.

Before Delete succeeds:

1. a saved profile must be selected;
2. the profile-name field must contain the selected profile name **exactly**;
3. only then does the TUI call the existing recoverable `Storage.delete_profile(...)` path.

The profile and matching local leaderboard rows therefore use the existing bounded recoverable-trash model.

## 5.2 Active-profile round ownership

A real interaction-risk was addressed during v1.4 review:

- a player could begin a round under profile A;
- switch to profile B;
- then finish the same in-memory round;
- without an ownership rule, the result could be persisted under B even though part of the round occurred under A.

Final behavior:

- activating another profile resets unfinished gameplay;
- creating and activating a new profile resets unfinished gameplay;
- restoring and activating a deleted profile resets unfinished gameplay;
- deleting the active profile and falling back to the canonical active profile resets unfinished gameplay;
- renaming the active profile does not reset because identity continuity is intentionally preserved by `Storage.rename_profile(...)`.

This is covered by Textual pilot regression tests.

---

# 6. History pane

The History pane presents up to the newest 100 matching local sessions for the active profile.

Filters:

- result: All / Win / Loss;
- mode;
- difficulty;
- free-text search;
- since date;
- until date.

Date format:

```text
YYYY-MM-DD
```

Invalid-date behavior:

- reports a clear error;
- does not destroy the last valid table contents.

Columns:

- timestamp;
- mode;
- difficulty;
- result;
- attempts;
- elapsed time.

The TUI uses existing validated `HistoryEntry` values and does not create a second history store.

---

# 7. Leaderboard pane

The Leaderboard pane exposes the existing ranked local winning-result data.

Filters:

- mode;
- difficulty;
- case-insensitive player-name substring.

Columns:

- rank;
- player;
- mode;
- difficulty;
- attempts;
- elapsed time;
- timestamp.

Profile rename/delete/restore coherence remains owned by `Storage`; the TUI simply refreshes the validated local leaderboard.

---

# 8. Settings pane

The Settings pane edits the active profile's established settings model:

- theme;
- locale;
- reduced motion;
- high contrast;
- sound preference;
- automatic smart hints.

Settings persistence continues through `Settings.from_dict(...)` plus `Storage.save_profile(...)`.

## 8.1 Immediate behavior

- smart-hint preference updates the current TUI gameplay behavior immediately;
- high-contrast preference updates the mounted Textual screen immediately.

## 8.2 High contrast

The TUI applies a `high-contrast` screen class with stronger:

- card/section borders;
- focus outlines for Buttons;
- focus outlines for Inputs;
- focus outlines for Selects;
- focus outlines for Switches.

Status meaning is still textual; high contrast is not used as the only information channel.

## 8.3 Reduced motion

Textual Switch controls use:

```text
animate=False
```

The workspace adds no fake delays or decorative motion.

## 8.4 Locale consistency

A second real interaction concern was addressed:

- mounted Textual tab/button labels are created during composition;
- changing only dynamically refreshed labels after a profile switch would produce a mixed-language UI.

Final v1.4 behavior:

- the TUI selects its display locale when launched;
- switching profiles loads the selected profile's settings values;
- saved smart-hint/high-contrast preferences can apply immediately;
- the mounted display locale remains stable for the process lifetime;
- the newly selected locale takes full effect on the next TUI launch.

This avoids partial relabeling and is covered by a pilot regression.

---

# 9. Recovery pane

The Recovery pane is intentionally **read-only**.

It displays:

- state health;
- data directory;
- source schema;
- current schema;
- live profile count;
- history count;
- leaderboard count;
- deleted-profile count.

It also accepts a selected local backup path for read-only verification.

Backup verification reuses `inspect_backup(...)`, which already includes:

- bounded file input;
- supported wrapper-version checks;
- schema validation;
- wrapper/payload schema agreement;
- SHA-256 integrity check for wrapper v2;
- legacy wrapper-v1 handling;
- current state normalization/importability proof;
- normalized structural metadata.

The pane does **not**:

- invoke `repair(...)`;
- import the backup;
- overwrite state;
- delete state;
- upload the backup/report.

Repair remains centralized in:

```bash
guessnova doctor --repair
```

This preserves Doctor's explicit confirmation and backup-before-write guarantees.

---

# 10. Keyboard and focus model

Global application shortcuts:

```text
Ctrl+1  Play
Ctrl+2  Profiles
Ctrl+3  History
Ctrl+4  Leaderboard
Ctrl+5  Settings
Ctrl+6  Recovery
Ctrl+R  New round
Ctrl+Q  Quit
```

Pane shortcut focus targets:

- Play → guess input;
- Profiles → profile-name input;
- History → history-search input;
- Leaderboard → player-filter input;
- Settings → theme Select;
- Recovery → backup-path input.

Play-local single-letter commands:

- `R` → new round;
- `Q` → quit.

Other text fields receive ordinary `r` and `q` characters normally.

The final binding/message approach follows Textual's supported widget binding/custom message model rather than monkeypatching framework internals.

---

# 11. Localization

The existing offline `en` and `hi` catalogs were expanded for the complete normal workspace presentation.

New catalog-backed areas include:

- pane labels;
- profile controls/status;
- profile deletion guidance;
- history controls/status;
- settings labels/status;
- Recovery labels/status;
- backup verification status.

The existing completeness contract remains:

```text
catalog_missing_keys("hi") == set()
```

Representative formatted v1.4 messages are tested in both English and Hindi, including:

- profile summary;
- backup-verification status.

Stable machine identifiers remain untranslated:

- mode IDs;
- difficulty IDs;
- schema keys;
- backup markers;
- replay fields;
- Doctor JSON keys/kinds;
- commands/environment variables;
- achievement IDs.

---

# 12. v1.4 test architecture

## 12.1 `tests/test_tui_workspace.py`

Covers reusable non-Textual logic:

- seeded challenge construction;
- deterministic target reproduction;
- daily-date challenge reproduction;
- invalid seed rejection;
- invalid daily-date rejection;
- dedicated-Reverse separation;
- workspace snapshots;
- profile statistics derivation;
- newest-first History filtering;
- Leaderboard filtering while preserving rank order;
- settings persistence;
- onboarding-setting preservation.

## 12.2 `tests/test_tui.py`

Retains and expands core Play regressions:

- deterministic initial focus;
- guess → submit → hint tab order;
- Enter submission;
- winning-result persistence;
- hint attempt behavior;
- Play-local plain `R` reset;
- Play-local plain `Q` quit;
- saved smart-hint preference;
- deterministic seeded reset.

## 12.3 `tests/test_tui_workspace_app.py`

Covers:

- direct pane shortcuts;
- profile text fields accepting ordinary `q/r`;
- profile create;
- profile rename;
- incorrect delete confirmation refusing deletion;
- exact-name deletion;
- recoverable trash;
- restore.

## 12.4 `tests/test_tui_workspace_data.py`

Covers:

- History filter combinations;
- invalid-date behavior;
- History Clear;
- Settings persistence;
- smart-hint update;
- Recovery backup verification;
- Recovery verification not importing/mutating application state.

## 12.5 `tests/test_tui_workspace_leaderboard.py`

Covers:

- Leaderboard pane navigation;
- initial ranked rows;
- mode/difficulty/player filtering;
- Clear restoring full view.

## 12.6 `tests/test_tui_workspace_accessibility.py`

Covers:

- unfinished gameplay before profile switch;
- active-profile switch resetting the round;
- remaining on the Profiles pane after switch;
- launch-locale stability after selecting a differently localized profile;
- selected profile's saved locale visible in Settings;
- high contrast loaded at startup;
- high contrast applied immediately after settings save;
- high-contrast persistence.

## 12.7 `tests/test_i18n.py`

Adds representative workspace formatting checks while retaining full Hindi-key completeness.

---

# 13. Smoke coverage

`scripts/smoke_test.py` retains previous end-to-end engine/profile/replay/backup/Doctor/repair/reverse checks and now additionally covers workspace-helper behavior:

- workspace snapshot;
- active-profile name;
- live/deleted profile lists;
- leaderboard count;
- healthy diagnostics;
- active-profile winning History selection;
- local Leaderboard player filter;
- deterministic seeded workspace challenge;
- repeated seeded target equality;
- deterministic daily-date workspace challenge;
- repeated daily seed/target equality;
- workspace settings persistence;
- Hindi locale persistence;
- high-contrast persistence;
- smart-hint disable persistence.

The smoke flow remains noninteractive; Textual pilot tests cover mounted-widget behavior.

---

# 14. CI and package verification

## 14.1 Strict CI job

Retained gates:

- Python 3.13;
- development extras;
- Ruff lint;
- Ruff format check;
- strict mypy;
- pytest + coverage;
- compileall;
- release metadata verification;
- smoke test.

## 14.2 Cross-platform package matrix

Ubuntu, Windows, and macOS built-wheel jobs now verify:

```bash
python -m guessnova --help
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
guessnova doctor --help
guessnova-doctor --help
guessnova-doctor --version
python scripts/smoke_test.py
```

The explicit Textual import ensures the built wheel contains/imports the expanded workspace on all supported desktop OS families.

## 14.3 Tagged-release matrix

The tagged-release package matrix applies the same Textual workspace import check before final publication is eligible to proceed.

The strict release job still includes:

- tag/package version equality;
- Ruff;
- strict mypy;
- pytest;
- compile;
- release metadata;
- smoke;
- dependency audit.

---

# 15. Version and compatibility metadata

Synchronized release metadata:

```text
pyproject.toml              1.4.0
src/guessnova/__init__.py   1.4.0
CITATION.cff                1.4.0
CHANGELOG.md                [1.4.0] - 2026-08-19
```

Unchanged compatibility identifiers:

```text
state schema                 2
backup wrapper               2
legacy backup wrapper        1
replay format                 1
Doctor report protocol        1
```

Reason no schema change exists:

- no canonical stored-state field/model boundary changed;
- Profiles, History, Leaderboard, Settings, diagnostics, and backups reuse existing storage formats;
- v1.4 is an application/presentation expansion.

---

# 16. Documentation completed for v1.4

Added:

- `docs/tui_workspace.md` — canonical workspace guide;
- `docs/TUI_WORKSPACE.md` — concise workspace reference;
- `docs/continuity/v1_3_merged_checkpoint.md` — byte-for-byte archive of the former active continuity record.

Updated:

- `README.md`;
- `CHANGELOG.md`;
- `ROADMAP.md`;
- `CITATION.cff`;
- `PRIVACY.md`;
- `SECURITY.md`;
- `SUPPORT.md`;
- `CONTRIBUTING.md`;
- `.github/pull_request_template.md`;
- `.github/workflows/ci.yml`;
- `.github/workflows/release.yml`;
- `docs/accessibility.md`;
- `docs/accessibility_evidence_template.md`;
- `docs/architecture.md`;
- `docs/development.md`;
- `docs/localization.md`;
- `docs/release.md`;
- `docs/RELEASING.md`;
- `docs/setup.md`;
- `docs/testing.md`;
- `docs/TESTING.md`;
- `what_changed.md`.

The manual accessibility template now requires actual evidence for every workspace pane rather than allowing v1.4 to reuse the old single-card TUI checklist.

---

# 17. Important implementation decisions

## 17.1 No parallel storage model

The TUI does not introduce SQLite, another JSON document, cloud sync, or a separate cache of user state.

## 17.2 Recovery is read-only

The app-like TUI cannot silently bypass Doctor's stronger repair safety model.

## 17.3 Single-letter shortcuts are widget scoped

The Play numeric field owns `R/Q`; text-editing fields remain text-editing fields.

## 17.4 Profile ownership is explicit

An unfinished game is reset before active-profile ownership changes.

## 17.5 Mounted locale is stable

A full locale change is deferred to the next TUI launch instead of creating a partially translated interface.

## 17.6 No property-testing dependency added

The new failure classes are directly covered with deterministic helper tests and Textual pilot tests. A new property-testing dependency is still gated on a demonstrated coverage gap.

## 17.7 No artifact-signing claim invented

Signing/provenance expansion remains gated until a real package-registry publishing workflow exists.

---

# 18. Static audit findings fixed during v1.4

Concrete issues/risks identified and addressed before final handoff:

1. **Profile ownership drift risk** — an unfinished round could otherwise cross an active-profile switch. Active ownership changes now reset the round.
2. **Partial live-localization risk** — profile switches with different locales could otherwise refresh some text but not mounted tab/button labels. One running TUI now keeps its launch locale; next launch fully applies the selected profile locale.
3. **Global single-letter shortcut conflict** — profile/search/path fields need normal `q/r` text entry. Single-letter commands are no longer application-global.
4. **Non-priority Play shortcut regression risk** — merely making app `R/Q` non-priority could let the numeric Input consume those keys instead of reset/quit. `GuessInput` now owns Play-local `R/Q` and communicates reset with a custom message.
5. **Workspace verification depth** — helper behavior is covered independently from widget behavior, and package matrices explicitly import the built-wheel Textual module.
6. **Manual accessibility gate staleness** — release evidence now covers all six panes, focus, filtering, destructive confirmation, Recovery, locale, high contrast, and normal text entry.

The custom widget binding/message implementation was checked against current official Textual documentation for widget-local `BINDINGS`, `post_message(...)`, and namespaced message handlers.

---

# 19. Local execution limitation

The available execution/container environment for this continuation cannot resolve GitHub or package-index hosts.

Observed failures include:

```text
fatal: unable to access 'https://github.com/sanskarIN/guessnova.git/':
Could not resolve host: github.com
```

and package installation attempts failing on DNS/name resolution.

Therefore this handoff does **not** invent claims that the following were executed locally:

- Ruff;
- strict mypy;
- pytest;
- built-wheel import;
- local Textual pilot execution;
- dependency installation.

Repository-side safeguards added/retained include:

- focused deterministic tests;
- Textual pilot suites;
- smoke extensions;
- strict CI;
- three-OS package matrix;
- built-wheel Textual import;
- CodeQL;
- Security checks;
- static file-by-file audit.

---

# 20. Hosted workflow state before this final handoff commit

The repository continues to show GitHub-hosted runner saturation similar to v1.1-v1.3.

The pre-handoff head immediately before this `what_changed.md` update did not produce an actionable failed conclusion while audited. Runs on successive v1.4 heads were repeatedly queued/pending, and superseded runs can be cancelled by workflow concurrency.

This file does **not** call queued/pending/cancelled-superseded runs successful.

## Exact-final-head rule

This handoff commit creates a new PR head.

Only workflow status for that exact final head counts for merge-time verification.

After this commit:

1. fetch PR #10 metadata and exact final head SHA;
2. fetch CI / CodeQL / Security runs for that exact SHA;
3. if a concrete failure exists, inspect the exact failed job/step/log;
4. fix the smallest reproducible issue;
5. add/adjust regression coverage;
6. update this handoff again only when necessary;
7. if runs remain queued/pending with no actionable failure, record that exact state honestly during the post-merge checkpoint rather than claiming a pass.

---

# 21. Manual release-candidate gates

Do **not** create a `v1.4.0` tag solely because the source PR merges.

Before an actual release tag:

1. select an exact release commit;
2. observe successful required automated checks for that exact commit;
3. verify package/runtime/citation/changelog all remain `1.4.0`;
4. verify schema-1 fixtures still migrate to schema 2;
5. verify future-schema rejection;
6. verify backup-v2 round trip;
7. verify legacy wrapper-v1 compatibility;
8. verify tampered backup rejection;
9. verify checksum-valid but unimportable backup rejection;
10. verify state/backup size bounds;
11. verify Doctor report protocol/exit semantics;
12. verify safe backup-before-write repair;
13. install/build-wheel on supported release path;
14. verify Textual workspace import from the built wheel;
15. manually exercise Play, Profiles, History, Leaderboard, Settings, Recovery;
16. verify Play-local plain `R/Q` and global Ctrl equivalents;
17. verify normal `q/r` text input outside Play;
18. verify profile deletion confirmation/restore;
19. verify unfinished-round profile isolation;
20. verify History/Leaderboard filters;
21. verify high contrast and reduced motion;
22. verify English workspace;
23. verify Hindi workspace after relaunch;
24. complete `docs/accessibility_evidence_template.md` on the exact candidate;
25. capture desired screenshots/demo only from that exact signed-off build;
26. record release-media provenance;
27. tag immutably only after gates pass.

Automated tests are not substituted for manual accessibility evidence.

Real screenshots/demo are not fabricated.

---

# 22. Repository settings state

At the v1.4 base checkpoint, `main` repository metadata still reported:

```text
protected: false
branch protection enabled: false
required status checks enforcement: off
```

Source documentation recommends branch protection, but source code cannot truthfully claim the GitHub repository setting is enabled when repository metadata says otherwise.

If branch protection is later enabled manually/repository-side, record the actual verified configuration rather than assuming it from documentation.

---

# 23. Gated future work after v1.4

Not v1.4 blockers:

- real signed-off release screenshots/demo;
- completed manual accessibility evidence for an exact release candidate;
- schema 3 only after a concrete stored-format boundary exists;
- a third locale only after complete/native-quality review;
- full atomic in-process Textual relocalization only if every mounted presentation element can update coherently;
- TUI repair/write actions only if explicit confirmation and pre-repair backup guarantees are preserved;
- property-based testing only when a demonstrated defect justifies the dependency;
- artifact signing/trusted publishing only with a real registry workflow;
- optional TypeScript/PWA edition only if offline/privacy/determinism/accessibility/compatibility guarantees are preserved.

---

# 24. Project identity

- Project: **GuessNova**
- Repository: `https://github.com/sanskarIN/guessnova`
- GitHub profile: `https://github.com/sanskarIN`
- License: MIT
- Credit: **Made by the Sanskar**
- Business: `sanskarin@outlook.in`
- Business: `sanskarin.business@gmail.com`
- Support: `supportramsandesh@gmail.com`
- Buy Me a Coffee: `https://buymeacoffee.com/sanskarIN`

GuessNova remains fully usable without donation, account creation, telemetry, analytics, cloud sync, remote leaderboard, or required runtime network access.

---

# 25. Continuation instructions after v1.4

If work continues after this checkpoint:

1. inspect `main` first; do not assume no concurrent changes;
2. read this `what_changed.md`;
3. use `docs/continuity/v1_3_merged_checkpoint.md` when older v1.3/v1.2/v1.1/v1.0 detail is needed;
4. recheck exact v1.4 final-head workflow conclusions before claiming success;
5. inspect concrete failed logs rather than guessing at CI defects;
6. avoid schema/version churn without a real compatibility need;
7. preserve local-only/privacy/accessibility guarantees;
8. keep recovery writes explicit and backup-before-write;
9. continue focused conventional commits using `sanskarin@outlook.in`;
10. preserve granular history with normal merges unless explicitly instructed otherwise;
11. update `what_changed.md` after meaningful continuation work.
