# GuessNova — Current Engineering Handoff

## Status

GuessNova `main` now has a production-oriented Python terminal stack plus a responsive installable browser/PWA path for the major desktop, mobile, and Chromebook platform families.

Repository:

```text
https://github.com/sanskarIN/guessnova
```

Release metadata intentionally remains `1.4.0`. The browser/PWA and engine-hardening continuation is recorded under `Unreleased`; this work does not create a tag or silently change the Python compatibility formats.

Compatibility metadata at this checkpoint:

```text
package/runtime version  1.4.0
Python state schema       2
backup wrapper            2
legacy backup wrapper     1
replay format             1
Doctor report protocol    1
browser state marker      1
browser localStorage key  guessnova.web.v1
Python requirement        >=3.13
license                   MIT
```

Detailed earlier terminal checkpoints remain in:

- `docs/continuity/v1_4_pr_checkpoint.md`
- `docs/continuity/v1_3_merged_checkpoint.md`

---

## 2026-08-21 continuation — cross-platform engine invariants

This continuation concentrated on correctness shared by the Python engine and browser/PWA engine rather than adding another isolated feature on top of unresolved branch divergence.

### Reverse-mode atomicity defect fixed

A real state-corruption defect existed in both implementations of `ReverseGuesser`.

Before the fix, contradictory `higher`/`lower` feedback mutated `low` or `high` first and only then checked whether the interval had become impossible. The method raised an inconsistency error, but the active object was already left with invalid bounds. A UI could show the error and still hold a poisoned engine instance.

The Python and JavaScript engines now calculate a proposed bound first, validate it against the opposite bound, and mutate only after validation succeeds.

Resulting invariant:

```text
invalid reverse feedback -> exception/error + no search-bound mutation
```

Focused regressions verify the full pre-error tuple/record remains unchanged and that a valid response can still continue the same round afterward.

### Reverse-mode completion boundary fixed

Both Reverse engines previously allowed `respond(...)` to be called after a `correct` response had marked the round finished. `next_guess` already rejected completed rounds, but `respond` did not have the equivalent guard.

Both implementations now reject feedback after completion before touching any state.

Focused regressions verify completed bounds, current guess, and attempt count remain unchanged.

### Python whole-number invariant aligned with the PWA

The browser engine already rejected explicit fractional targets with `Number.isInteger(...)` and treated non-integer guesses as invalid input.

The Python engine previously trusted its type hints at runtime. A caller could construct a game with a target such as `42.5`, which is inside the numeric range but can never be reached by the normal integer user-input path. Python also accepted values such as `42.0` or `True` as guesses because ordinary numeric comparisons permit them.

Python now explicitly requires runtime whole-number semantics for externally supplied targets and guesses:

- explicit targets must be integers and not booleans;
- fractional targets are rejected during construction;
- boolean targets are rejected during construction;
- fractional guesses produce `OUT_OF_RANGE` without consuming an attempt;
- boolean guesses produce `OUT_OF_RANGE` without consuming an attempt.

This closes a cross-platform semantic mismatch and prevents unwinnable fractional-target rounds.

### Granular commits in this continuation

```text
4026c50c6f7d41252b8655a137bb8f33a5b71b29  fix(core): keep reverse bounds atomic on invalid feedback
d894c72797a2b2ad623e2a78804c648cd194d283  test(core): preserve reverse bounds after contradictions
fc1929f61ee646d323736332c2fd3e683cd6441b  fix(web): keep reverse bounds atomic on invalid feedback
1da24f6242c0aa1e6f1c9acd61b0325a005f3ac1  test(web): preserve reverse bounds after contradictions
d2d5123ee648be6f2bf913d2d428519897375841  fix(core): enforce integer target and guess invariants
d1d9ebf146c599d56dc6f7ba799725035cff6416  test(core): reject fractional and boolean guesses
faaeb8a5e61b695bb27d1dec629a50929ae71bee  fix(core): reject reverse feedback after completion
a1e3409c7e0dba52130f1308af91917f2172d314  test(core): reject reverse feedback after completion
68d47e2321e9691cc584b8d19c37b27c3f246625  fix(web): reject reverse feedback after completion
108e557c87e359855ddf0f786ebd85c0ee570e17  test(web): reject reverse feedback after completion
cf4d7456f3dbac7f2a3d3e5120fc624bfe1ecacb  docs(changelog): record cross-platform engine invariant fixes
```

The `CHANGELOG.md` `Unreleased` section now records these behavior and reliability changes without changing the package/runtime version.

---

## Important branch/release reconciliation state

Open PR #11, `feat: add v1.5 Textual challenge workspace`, is not currently safe to merge directly.

Observed comparison at the `cf4d7456...` main checkpoint:

```text
main vs release/v1.5.0-challenge-workspace-20260819
status       diverged
feature ahead by  85 commits
feature behind by 108 commits
merge base    3b0ae5ba92087e7286b77711d8dfb5df7f132c43
```

The branch contains useful v1.5 challenge-workspace work, but `main` has accumulated substantial independent browser/PWA, service, storage, CI/security, and engine hardening since the common base. The PR should not be force-merged or treated as a release candidate until its feature layer is deliberately reconciled with current `main` and all overlapping files are reviewed.

High-risk overlap includes workflows, release metadata, changelog/docs, `pyproject.toml`, `tui_workspace.py`, localization, smoke testing, and the active handoff file.

A safe continuation should port/reconcile the challenge feature onto current `main` rather than discarding either side's changes.

---

## Supported interface model

### Python desktop path

Supported Python interfaces on Windows, macOS, and modern Linux:

- Rich CLI
- six-pane Textual TUI
- Doctor diagnostics/recovery
- bundled local PWA server

### Browser/PWA path

Responsive standards-based browser path:

- Windows
- macOS
- Linux
- Android
- iOS
- iPadOS
- ChromeOS

Android/iOS support is provided by the installable PWA. No native APK/AAB/IPA support is claimed because native wrappers have not been implemented and verified.

See `docs/platforms.md` for the platform matrix.

---

## Browser/PWA package surface

Current bundled web files:

```text
src/guessnova/web/
├── app.css
├── app.js
├── browser-state.mjs
├── game-engine.mjs
├── icon.svg
├── icon-192.png
├── icon-512.png
├── index.html
├── manifest.webmanifest
└── sw.js
```

Browser features include:

- Classic, Timed, Streak, Daily, and Reverse modes
- Easy, Normal, Hard, and Expert difficulties
- portable cross-language Daily Challenge targets
- smart direction/temperature/parity hints
- explicit range hints
- local games-played/won/win-rate statistics
- current and best streak
- bounded recent-round history
- browser-origin persistence
- responsive touch/keyboard presentation
- light/dark adaptation
- reduced-motion support
- install prompting where supported
- iOS/iPadOS home-screen metadata
- offline app-shell caching

The browser edition adds no account requirement, telemetry, analytics, advertisements, cloud sync, remote leaderboard, or gameplay backend.

Browser state is deliberately separate from Python schema-2 `state.json`. There is no silent cross-format import/write path.

---

## Browser state reliability boundary

Module:

```text
src/guessnova/web/browser-state.mjs
```

The application does not trust raw `localStorage` content directly. `app.js` parses and serializes browser progress through a defensive normalization layer.

The boundary:

- safely handles missing, invalid, or non-object JSON;
- rejects oversized serialized state before parsing;
- discards unknown persisted top-level fields;
- rejects negative, non-integer, non-finite counters;
- bounds counters to a finite application limit;
- keeps games-won and streak counters internally consistent;
- bounds retained history to 12 entries;
- discards non-object history entries;
- normalizes mode and difficulty identifiers;
- validates stored targets against difficulty ranges;
- converts invalid completion timestamps to `null`;
- uses `Object.hasOwn()` for difficulty membership so prototype names cannot become fake difficulty identifiers;
- preserves legacy unversioned `guessnova.web.v1` state;
- rejects explicitly versioned unknown/future browser-state schemas;
- falls back to in-memory state when browser privacy settings block storage access.

Current browser marker:

```text
BROWSER_STATE_SCHEMA = 1
```

---

## Browser and Python regression coverage relevant to this checkpoint

Python engine coverage now includes:

- completed elapsed-time freezing;
- timeout elapsed-time freezing;
- explicit hint penalty behavior;
- Reverse binary-search convergence;
- invalid Reverse response rejection;
- Reverse response-before-guess rejection;
- Reverse contradictory feedback atomicity;
- Reverse post-completion feedback rejection;
- fractional guess rejection without attempt consumption;
- boolean guess rejection without attempt consumption;
- fractional explicit target rejection;
- boolean explicit target rejection.

Browser engine coverage now includes:

- shared portable Daily vector;
- Python-matching difficulty definitions;
- Classic outcome semantics;
- completed elapsed-time freezing;
- timed timeout duration freezing;
- non-integer explicit target rejection;
- smart-hint thresholds/parity;
- Reverse convergence;
- Reverse contradictory feedback atomicity;
- Reverse post-completion feedback rejection.

Browser-state coverage continues to cover malformed/oversized state, counter bounding, malformed history, legacy unversioned state, prototype-key rejection, and future-schema rejection.

---

## CI and release verification configuration

Normal CI and tagged-release verification are configured to run browser tests with:

```bash
node --test tests/web/*.mjs
```

and syntax-check:

```bash
node --check src/guessnova/web/app.js
node --check src/guessnova/web/browser-state.mjs
node --check src/guessnova/web/game-engine.mjs
node --check src/guessnova/web/sw.js
```

The existing Python gates remain configured for Ruff, formatting, strict mypy, pytest/coverage, compileall, release metadata, smoke testing, dependency auditing, and package verification.

Ubuntu, Windows, and macOS package matrices continue to build/install the wheel and verify installed commands and required PWA assets.

---

## CI evidence at this exact continuation

For main checkpoint `cf4d7456f3dbac7f2a3d3e5120fc624bfe1ecacb`:

- GitHub combined-status lookup exposed an empty status list;
- the available commit workflow-run lookup exposed no pull-request-triggered runs;
- an empty result is **not** treated as a pass or failure.

The execution container still cannot resolve `github.com`, so a full local clone and repository-wide local test run could not be performed from that environment.

Do not claim a full repository pass from this continuation until an actual CI conclusion or complete local run is observed.

---

## Local browser server

Server module:

```text
src/guessnova/web_server.py
```

Entry points:

```bash
guessnova web
guessnova-web
```

Default bind:

```text
127.0.0.1:8765
```

Important properties:

- standard-library server, no web-framework runtime dependency;
- loopback-only by default;
- explicit `--host`, `--port`, and `--no-open` controls;
- traversal rejection and path normalization;
- read-only serving of package resources;
- no gameplay/state mutation HTTP API;
- GET/HEAD support;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: no-referrer`;
- restrictive same-origin Content Security Policy.

`0.0.0.0` remains an explicit trusted-LAN development choice, not the normal default. Public/mobile deployment should use HTTPS static hosting.

---

## Daily Challenge parity

Portable rule:

```text
guessnova-daily-v2:<YYYY-MM-DD>:<difficulty>
```

Python and JavaScript both use unsigned FNV-1a 32-bit and map the result into the selected inclusive difficulty range.

Fixed cross-language vector:

```text
Date:       2026-08-19
Difficulty: normal
Hash:       230553734
Target:     35
```

Legacy Python `daily_seed()` remains available for compatibility.

---

## Validation truthfulness

Verified directly during the work:

- repository metadata and current main head through the GitHub connector;
- current open PR state and main/feature divergence;
- Python and JavaScript engine source before modification;
- the Reverse mutation-before-validation defect in both engines;
- the Python fractional/boolean target/guess runtime mismatch;
- committed source/test changes and exact commit SHAs;
- changelog update;
- exact-head combined-status/workflow-run lookups.

Not claimed:

- a complete local Ruff/mypy/pytest/Node repository pass;
- a successful GitHub Actions conclusion when no conclusion was exposed;
- real-device Android/iOS/iPadOS/ChromeOS evidence;
- release-candidate accessibility evidence;
- signed release artifacts;
- PR #11 mergeability after reconciliation, because reconciliation has not yet been completed.

---

## Next engineering priorities

1. Reconcile the useful v1.5 Challenge Setup work from PR #11 onto current `main` without losing the 108 main-side commits since the common base.
2. Resolve overlapping TUI/workflow/docs/release metadata deliberately; do not overwrite current PWA/security/service changes with the stale branch versions.
3. Run or observe complete Python + Node quality gates on the exact reconciled head.
4. Require CI/security checks to pass on that exact candidate SHA before tagging.
5. Install the wheel on Windows, macOS, and Linux and verify CLI, TUI, Doctor, `guessnova web`, and `guessnova-web`.
6. Verify the complete PWA module/asset set in the installed wheel.
7. Host the PWA over HTTPS for Android/iOS/iPadOS/ChromeOS and current desktop-browser validation.
8. Complete keyboard/touch/responsive/light-dark/reduced-motion checks and manual accessibility evidence on the exact candidate.
9. Compare Python/browser Daily Challenge targets for the same date+difficulty.
10. Capture screenshots/demo media only from a verified candidate.

Do not fabricate CI, device, accessibility, provenance, or screenshot evidence.

---

## Project identity

- Project: **GuessNova**
- Repository: `https://github.com/sanskarIN/guessnova`
- GitHub profile: `https://github.com/sanskarIN`
- License: MIT
- Credit: **Made by the Sanskar**
- Business: `sanskarin@outlook.in`
- Business: `sanskarin.business@gmail.com`
- Support: `supportramsandesh@gmail.com`
- Buy Me a Coffee: `https://buymeacoffee.com/sanskarIN`

GuessNova remains usable without donation, account creation, telemetry, analytics, cloud sync, remote leaderboard, or a gameplay backend.
