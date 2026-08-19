# GuessNova — v1.4 Merged Full Textual Workspace Checkpoint

## Current milestone

**GuessNova `v1.4.0` full Textual local-workspace implementation is merged into `main`.**

Merged release work:

- Repository: `https://github.com/sanskarIN/guessnova`
- Branch: `release/v1.4.0-tui-workspace-20260819`
- Pull request: `#10` — `feat: ship GuessNova 1.4 full Textual workspace`
- Base commit: `c45b163b48353aa307d73ecc6095732803cd5503`
- Final PR head: `149fa6ff3dcfbb523386f732feb188a7503991d3`
- v1.4 PR commits preserved: **52 granular commits**
- Merge method: **normal merge**, not squash
- Merge commit: `b118bdb8903230e1cddc3865b1cfbd3e7b038132`
- Merge commit author: `Sanskar <sanskarin@outlook.in>`
- GitHub merge verification: **valid signed merge commit**
- Post-merge continuity archive commit before this file update: `80ce8eec78d3832dccc443545b09078f534cd083`
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

The v1.4 merge preserves the full implementation/fix/test/docs/build/CI history. It intentionally does **not** invent schema 3, backup wrapper 3, replay version 2, Doctor report version 2, a third locale, package-signing claims, or a new property-testing dependency without a concrete prerequisite.

---

# 1. Continuity archives

Detailed pre-merge implementation history is preserved in-repository rather than being deleted from the active handoff.

## v1.4 complete PR checkpoint

- `docs/continuity/v1_4_pr_checkpoint.md`
- Exact former v1.4 pre-merge `what_changed.md` blob: `440abbc2ac4fd3a0dfdf32897e4dc1aa541f2446`
- Archive commit: `80ce8eec78d3832dccc443545b09078f534cd083`

That archive contains the full v1.4 source-level architecture, every pane, helper/widget design, tests, smoke/CI changes, documentation map, static-audit findings, local execution limitation, manual gates, and continuation instructions.

## v1.3 and older complete checkpoint

- `docs/continuity/v1_3_merged_checkpoint.md`
- Former v1.3 active continuity blob: `014cba52fbe736f33380ce3d8ede5161001eef63`

That archive preserves the detailed v1.3/v1.2/v1.1/v1.0 history.

Important prior milestones:

- v1.0 audit merge: `3cc6fec1945c97605506de7d004d7ef4436f48f3`
- v1.1 merge: `b303b764c83dbbca5183ee5b974bd280e7fca0cd`
- v1.2 merge: `f17594b16426513850c9a1c118d8fcec225702cd`
- v1.3 merge: `e57cac65b20e6351200ac3ab25a3cf2a07ed9308`
- v1.3 post-merge / v1.4 base: `c45b163b48353aa307d73ecc6095732803cd5503`

---

# 2. v1.4 shipped implementation

`guessnova-tui` is no longer only a single gameplay card. It is now a six-pane keyboard-first local workspace:

1. Play
2. Profiles
3. History
4. Leaderboard
5. Settings
6. Recovery

The workspace reuses the existing local product boundaries rather than introducing a second storage/database/network layer.

## Play

Retains:

- deterministic initial guess-input focus;
- numeric guessing;
- Submit and Range Hint controls;
- automatic smart hints;
- explicit range hints;
- attempts/range state;
- result persistence through `GameService`;
- exactly-once completed-round guard;
- deterministic seeded reset behavior.

Final shortcut model:

- focused numeric `GuessInput`: plain `R` = new round;
- focused numeric `GuessInput`: plain `Q` = quit;
- anywhere: `Ctrl+R` = reset and return to Play;
- anywhere: `Ctrl+Q` = quit.

Plain `R/Q` are intentionally **not** application-global, so ordinary profile/search/player/path text inputs can type `r` and `q` normally.

## Profiles

Adds TUI flows for:

- active profile summary;
- unlocked achievement labels;
- profile selection/use;
- create;
- rename;
- recoverable delete;
- recoverable-trash visibility;
- restore;
- refresh.

Delete requires the selected profile name to be typed exactly before the action succeeds.

Active-profile ownership changes reset any unfinished game before later persistence so a partially played round cannot silently move between profiles.

## History

Adds newest-first bounded table/filter UX for:

- result;
- mode;
- difficulty;
- free-text search;
- since date;
- until date.

Invalid ISO-date input reports an error without erasing the last valid table data.

## Leaderboard

Adds local ranked table/filter UX for:

- mode;
- difficulty;
- case-insensitive player substring.

Filtering preserves the existing validated leaderboard rank order.

## Settings

Adds TUI controls for existing per-profile settings:

- theme;
- locale;
- reduced motion;
- high contrast;
- sound preference;
- automatic smart hints.

Smart-hint and high-contrast changes apply immediately. Locale is persisted immediately but the already-mounted TUI keeps its launch language until restart, preventing a partially translated interface.

Textual Switch controls use `animate=False`.

## Recovery

The TUI Recovery pane is intentionally read-only.

It can:

- display local state health;
- display data directory;
- display source/current schema;
- display profile/history/leaderboard/trash counts;
- refresh diagnostics;
- verify a selected backup using existing `inspect_backup(...)` preflight.

It cannot:

- call repair;
- import the selected backup;
- overwrite state;
- delete state;
- upload data.

Repair remains explicit through:

```bash
guessnova doctor --repair
```

---

# 3. v1.4 architecture

New/expanded source boundaries:

- `src/guessnova/tui_workspace.py` — Textual-independent workspace helpers.
- `src/guessnova/tui_widgets.py` — focused widget behavior, especially Play-only `GuessInput` shortcuts.
- `src/guessnova/tui.py` — pane composition, focus, widget events, refresh/orchestration.

`tui_workspace.py` includes reusable helpers for:

- deterministic seeded/daily challenge construction;
- workspace snapshots;
- profile statistics;
- newest-first history filtering;
- rank-preserving leaderboard filtering;
- validated settings persistence.

The v1.4 mounted TUI continues using:

- `Storage` for profile/settings/history/leaderboard state;
- `GameService` for completed results;
- `diagnose(...)` for state diagnostics;
- `inspect_backup(...)` for read-only backup verification.

No parallel database, cloud sync, remote leaderboard, or hidden persistence model was introduced.

---

# 4. v1.4 regression coverage added

Focused test surfaces now include:

- `tests/test_tui_workspace.py`
- `tests/test_tui_workspace_app.py`
- `tests/test_tui_workspace_data.py`
- `tests/test_tui_workspace_leaderboard.py`
- `tests/test_tui_workspace_accessibility.py`
- expanded `tests/test_tui.py`
- expanded `tests/test_i18n.py`

Coverage added for:

- deterministic workspace challenge construction;
- reproducible daily date;
- invalid seed/date and Reverse separation;
- workspace snapshots;
- profile statistics;
- history filtering/order;
- leaderboard filtering/order;
- settings persistence;
- pane shortcuts;
- normal `q/r` input outside Play;
- Play-local `R` reset;
- Play-local `Q` quit;
- profile create/use/rename/delete/restore;
- exact-name delete confirmation;
- active-profile round isolation;
- invalid History dates;
- leaderboard filters;
- settings persistence;
- launch-locale consistency;
- high contrast at launch/after save;
- read-only backup verification.

`scripts/smoke_test.py` also exercises the reusable workspace helper layer in addition to retained gameplay/profile/replay/backup/Doctor/repair/reverse checks.

---

# 5. Cross-platform package/release gates

Normal CI and tagged-release package matrices now install the built wheel on:

- Ubuntu;
- Windows;
- macOS.

Each package path includes explicit Textual-workspace import verification:

```bash
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
```

and retains game/Doctor/smoke verification.

Strict CI/release gates remain configured for:

- Ruff lint;
- Ruff format check;
- strict mypy;
- pytest/coverage;
- compileall;
- release metadata verification;
- smoke test;
- dependency audit on release/security paths;
- CodeQL and Security workflows.

---

# 6. Exact final-head hosted verification state at merge

Final PR head:

```text
149fa6ff3dcfbb523386f732feb188a7503991d3
```

Immediately before and after the normal merge, GitHub reported:

- CI run `32224689793`: `queued`, conclusion `null`.
- Security checks run `32224689794`: `queued`, conclusion `null`.
- CodeQL run `32224689833`: `queued`, conclusion `null`.

CI job-level status for run `32224689793`:

- job `95981909116` — `test (3.13)`: `queued`, conclusion `null`.
- job `95981909209` — `package (ubuntu-latest)`: `queued`, conclusion `null`.
- job `95981909299` — `package (macos-latest)`: `queued`, conclusion `null`.
- job `95981909370` — `package (windows-latest)`: `queued`, conclusion `null`.

**These checks are not recorded as passed.**

No exact-final-head workflow produced an actionable failure conclusion before the merge. The repository continued the GitHub-hosted runner saturation pattern seen in prior release work.

If these runs later execute and expose a reproducible failure, the next continuation must inspect the exact failed job/step/log and apply a focused fix/regression on a new branch/PR.

---

# 7. Local execution limitation

The available execution/container environment could not resolve GitHub or package-index hosts.

Observed clone failure:

```text
fatal: unable to access 'https://github.com/sanskarIN/guessnova.git/':
Could not resolve host: github.com
```

Package installation attempts also failed on DNS/name resolution.

Therefore this checkpoint does **not** claim local execution of:

- Ruff;
- strict mypy;
- pytest;
- Textual pilot suites;
- built-wheel import;
- dependency audit.

The repository contains the corresponding tests/workflows, but no local pass is fabricated.

---

# 8. Static audit issues fixed before merge

Concrete v1.4 interaction/design risks found and fixed during review:

1. **Profile ownership drift** — unfinished gameplay now resets when active-profile ownership changes.
2. **Partial live localization** — mounted TUI keeps its launch language; selected profile locale fully applies next launch.
3. **Text-input shortcut conflict** — plain `Q/R` are not global across workspace text fields.
4. **Play reset/quit regression risk** — dedicated `GuessInput` owns plain `R/Q` so Play preserves legacy keys while other inputs remain normal text editors.
5. **Workspace testing separation** — non-widget behavior moved to independently testable helpers instead of being buried entirely in a large Textual class.
6. **Built-wheel visibility** — package matrices explicitly import the Textual workspace on all three desktop OS families.
7. **Stale manual evidence gate** — accessibility evidence now covers all six panes and their keyboard/safety flows.

The widget-local binding/custom-message approach was checked against current official Textual documentation during the v1.4 audit.

---

# 9. Documentation completed

Added:

- `docs/tui_workspace.md`
- `docs/TUI_WORKSPACE.md`
- `docs/continuity/v1_4_pr_checkpoint.md`
- `docs/continuity/v1_3_merged_checkpoint.md`

Updated during v1.4:

- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `CITATION.cff`
- `PRIVACY.md`
- `SECURITY.md`
- `SUPPORT.md`
- `CONTRIBUTING.md`
- `.github/pull_request_template.md`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `docs/accessibility.md`
- `docs/accessibility_evidence_template.md`
- `docs/architecture.md`
- `docs/development.md`
- `docs/localization.md`
- `docs/release.md`
- `docs/RELEASING.md`
- `docs/setup.md`
- `docs/testing.md`
- `docs/TESTING.md`
- `what_changed.md`

---

# 10. Release metadata / compatibility domains

Current release metadata:

```text
project version       1.4.0
runtime version       1.4.0
citation version      1.4.0
state schema          2
backup wrapper        2
legacy backup         1
replay format         1
Doctor report         1
```

v1.4 does not require stored-format migration because it changes the application/TUI layer over existing validated local formats.

---

# 11. Manual release gates still required

The source merge does **not** automatically authorize a `v1.4.0` tag.

Before a real v1.4 release tag:

1. select the exact release candidate commit;
2. require successful automated checks for that exact commit;
3. verify package/runtime/citation/changelog metadata;
4. verify schema migration/future-schema rejection;
5. verify backup-v2/legacy/tamper/importability behavior;
6. verify Doctor JSON/exit/repair behavior;
7. install/verify the built wheel;
8. manually exercise Play, Profiles, History, Leaderboard, Settings, Recovery;
9. verify Play-local `R/Q` and global Ctrl equivalents;
10. verify normal `q/r` input outside Play;
11. verify profile deletion/restore and unfinished-round isolation;
12. verify History/Leaderboard filters;
13. verify high contrast/reduced motion;
14. verify English and Hindi after relaunch;
15. complete `docs/accessibility_evidence_template.md` on the exact candidate;
16. capture real screenshots/demo only from that signed-off build;
17. record media provenance;
18. create an immutable tag only after gates pass.

Do not fabricate accessibility evidence or release media.

---

# 12. Repository settings reality

After the v1.4 merge, GitHub branch metadata for `main` still reports:

```text
protected: false
branch protection enabled: false
required status checks enforcement: off
```

Repository documentation recommends branch protection, but it is not currently enabled. Do not claim otherwise unless repository metadata later confirms a settings change.

---

# 13. Next continuation priorities

If work continues:

1. inspect current `main` before branching;
2. recheck the exact v1.4 PR-head workflow conclusions before claiming they passed/failed;
3. if a concrete v1.4 failure appears, make the smallest focused patch release/fix branch and add a regression;
4. do not create schema 3 unless a real stored-format boundary appears;
5. do not add a third locale without complete/native-quality review;
6. do not add TUI repair writes unless Doctor confirmation and backup-before-write guarantees are preserved;
7. do not add property-testing dependency without a demonstrated coverage gap;
8. do not claim package signing/trusted publishing without a real registry workflow;
9. keep local-only/privacy/accessibility/determinism guarantees;
10. keep using `sanskarin@outlook.in` for Git commits;
11. preserve granular history with normal merges unless explicitly instructed otherwise;
12. update this live handoff after meaningful continuation work.

Potential future product directions remain gated, including atomic full in-process TUI relocalization, richer challenge configuration inside the mounted TUI, and an optional offline TypeScript/PWA edition that preserves compatibility/privacy/determinism/accessibility constraints.

---

# 14. Project identity

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
