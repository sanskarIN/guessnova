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

## 2026-08-23 continuation — cross-platform release hardening

This continuation started from an already mature repository rather than adding artificial feature count. At the beginning of the pass, the roadmap had no unfinished ordinary engineering checkbox, GitHub exposed no open issues, and the only explicit unchecked roadmap item was the truthful manual release-media capture gate.

The work therefore concentrated on concrete correctness, portability, browser persistence, and offline-cache defects that could still affect real users.

### Reverse-mode whole-number bounds are now enforced everywhere

`ReverseGuesser` previously assumed its type hints/callers would supply integer bounds. That assumption was inconsistent with the whole-number contract already enforced for normal guessing.

Python and JavaScript now both reject fractional/non-integer Reverse bounds before a round starts. Python additionally rejects booleans, which are integer subclasses at runtime.

Resulting invariant:

```text
Reverse search range = two real whole-number bounds with minimum < maximum
```

Dedicated Python and Node regressions cover these invalid-bound cases.

### Reverse-mode feedback sequencing is now a real state machine

A caller could previously request multiple Reverse guesses without responding to the prior proposal. That silently incremented attempt count and replaced the pending guess, weakening replayability and making the engine API easier to misuse.

Both engines now enforce one pending proposal at a time:

```text
next guess -> exactly one feedback response -> next guess
```

A repeated `next_guess()` / `nextGuess()` before feedback raises without changing the pending guess or attempt count.

Successful `higher`/`lower` feedback consumes the pending proposal by clearing the current guess. Contradictory or invalid feedback intentionally leaves the proposal intact so the caller can correct the response and continue the same round.

### Reverse-mode non-text feedback now has a stable domain error

Both engines previously called string operations directly on feedback. Non-text values could therefore leak language/runtime-specific exceptions such as Python `AttributeError` or JavaScript `TypeError` instead of the documented Reverse feedback validation error.

Both implementations now reject non-text feedback with the stable semantic message:

```text
response must be higher, lower, or correct
```

The pending guess, bounds, and attempt count remain unchanged after this validation failure.

### Local browser server gained explicit IPv6 support

The bundled `guessnova web` / `guessnova-web` server previously used the IPv4 `ThreadingHTTPServer` family regardless of the requested bind literal.

The server now:

- keeps IPv4 behavior and the `127.0.0.1` default unchanged;
- selects an IPv6 server family for explicit IPv6 literal binds;
- formats IPv6 browser-launch hosts inside `[...]` as required by URL syntax;
- maps the IPv6 wildcard `::` to the local browser destination `[::1]` for launch display;
- percent-escapes scoped IPv6 zone identifiers when constructing browser URLs;
- retains port validation, path traversal rejection, package-resource read-only serving, and the existing security headers.

Focused tests cover wildcard, loopback, ordinary IPv4, and scoped IPv6 URL formatting without requiring an IPv6-capable CI network interface.

### Browser history normalization now respects difficulty attempt ceilings

Browser-state normalization already bounded raw counters globally, but a stale/corrupt history record could still claim an impossible attempt count such as `999999` for Normal difficulty and have that value rendered into Recent rounds.

History normalization now clamps the retained attempt count to the selected difficulty's actual maximum attempts before the record reaches the UI or is re-serialized.

This remains backward compatible with the existing browser-state marker and `guessnova.web.v1` localStorage key.

### PWA activation no longer deletes unrelated caches

The service worker previously removed every Cache Storage entry whose name was not the current GuessNova cache. On a shared origin, that could remove caches owned by another application.

The service worker now uses an explicit GuessNova cache prefix and only removes obsolete caches in that namespace:

```text
guessnova-web-*
```

The active cache advances to `guessnova-web-v5`, and a committed source-contract regression test ensures activation cannot regress to broad origin-wide cache deletion.

### Release documentation synchronized

`CHANGELOG.md` `Unreleased` now records the Reverse, IPv6, browser-state, and PWA cache-hardening changes without changing package/runtime version or serialized compatibility formats.

`ROADMAP.md` now explicitly records the completed IPv6 server support, namespaced service-worker cleanup, per-difficulty browser attempt bounding, and Python/JavaScript Reverse contract parity. The real screenshot/demo capture remains intentionally unchecked because repository automation cannot manufacture truthful release evidence.

### Granular commits in the 2026-08-23 continuation

```text
c6dcb68b05026b13439d0fe0b5786b9c4aedc75a  fix(core): validate reverse integer bounds
fb7242f26f250aa06ce68e109015ad016607dfd4  test(core): cover reverse bound type validation
d4d963e6ef7197585de8a6acaa14a29e537e858a  fix(web): validate reverse integer bounds
a531925bda0e7ed248cf351f01a967c79e5cb05c  test(web): cover reverse bound type validation
208e92cd4b9b3656aede0a4b6adfbfdab21070a8  fix(core): enforce reverse feedback sequencing
6900db7dc4ed3c5666b60aac41cb7f933756f88e  test(core): cover reverse feedback sequencing
d7a898d92191115da54c447df5337ac41de12ebd  fix(web): enforce reverse feedback sequencing
2a688d3b66dc5ce6b94d97f69d99720f398b504a  test(web): cover reverse feedback sequencing
fa5bc44bb17706ba1b35594263f9243d6242d787  feat(web): support IPv6 literal server binds
848a0fb5950c1f3001e2b4552ca31402c261d942  test(web): cover IPv6 browser host formatting
ac75c4df82d4b3043a422d40ac95106a1b944403  fix(web): bound persisted history attempts
838985a340cc4b6c68c10307f72c4971dde0f1c4  test(web): cover persisted attempt bounds
81606b7a249336480bad26208f3bee97ddb20128  fix(pwa): preserve unrelated origin caches
f7bfc11d8188e343d65afdac7080d77d1130442d  test(pwa): guard cache namespace cleanup
9cd4617a8ba828aeb16857009d8d5b65494ff08a  fix(core): validate reverse feedback type
500d738dc5118232eaf4361c6c4919b619319b36  test(core): cover reverse feedback type validation
6ae016d82fd2ace17b829b2a4077d1ce20f4d3aa  fix(web): validate reverse feedback type
1dec2ff4a304b8f86cf76856377ae487d7fcf7ea  test(web): cover reverse feedback type validation
b9724adea6a212a98cc53ea8d44b6013b247bfa5  fix(web): escape scoped IPv6 browser hosts
ff2c83334bbd6eeda7f758e8506195b10b3cee6d  test(web): cover scoped IPv6 URL escaping
267f246e416b145635158c1a61a0d1f77b7defbe  docs(changelog): record browser and reverse hardening
255d2d471136a75ac6bc89d2aa6319e94112218b  docs(roadmap): record cross-platform hardening completion
```

### Repository work queue after this pass

GitHub issue/PR search at this checkpoint reports no open issues and no open pull requests. The previous handoff's warning about open PR #11 is therefore historical, not a current merge task.

The remaining explicit roadmap item is manual release evidence:

```text
real terminal screenshots + short demo recording from a signed-off release build
```

Other ideas under **Gated future candidates** are intentionally not treated as unfinished release work until their stated prerequisites exist. This prevents fake schema migrations, unnecessary dependencies, or unsupported native-mobile claims from being added only to increase feature count.

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

The `CHANGELOG.md` `Unreleased` section records these behavior and reliability changes without changing the package/runtime version.

---

## Historical branch/release reconciliation note

At the 2026-08-21 checkpoint, PR #11 (`feat: add v1.5 Textual challenge workspace`) was open and heavily diverged from then-current `main`. That warning was correct for that historical checkpoint.

At the 2026-08-23 checkpoint, GitHub issue/PR search reports no open pull requests. Therefore PR #11 is no longer listed as a current engineering blocker or next action. The old divergence information remains recoverable from Git history and this handoff's previous revisions if repository archaeology is required.

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
- clamps stored history attempts to each difficulty's real attempt ceiling;
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
- Reverse whole-number bound validation;
- Reverse one-feedback-per-proposal sequencing;
- Reverse non-text feedback validation without state loss;
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
- Reverse post-completion feedback rejection;
- Reverse whole-number bound validation;
- Reverse one-feedback-per-proposal sequencing;
- Reverse non-text feedback validation without state loss.

Browser-state coverage includes malformed/oversized state, counter bounding, per-difficulty history attempt bounding, malformed history, legacy unversioned state, prototype-key rejection, and future-schema rejection.

Service-worker coverage includes app-shell module presence, navigation-only offline fallback, cache-storage failure isolation, same-origin GET-only interception, and GuessNova-only cache namespace cleanup.

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

## Validation evidence at the 2026-08-23 continuation

Verified directly through the GitHub connector:

- current repository metadata and `main` contents;
- no open GitHub issues at the beginning of the pass;
- no open pull requests at the end of the pass;
- the current roadmap and its one manual release-media checkbox;
- Python and JavaScript engine source before each modification;
- local web-server implementation and tests;
- browser-state normalization implementation and tests;
- PWA service-worker implementation and tests;
- every source/test/docs commit listed in the current continuation.

A combined-status lookup performed during the continuation exposed no commit statuses for the queried head. The available GitHub fetch surface also does not permit listing Actions runs through the generic repository fetch endpoint. An empty/unavailable status result is **not** treated as a pass or a failure.

The execution environment used for this continuation does not provide a local checked-out repository with dependencies, and its direct network clone path is unavailable. Therefore this handoff does not claim a complete local Ruff/mypy/pytest/Node execution.

Do not claim a full repository pass until an actual exact-head CI conclusion or complete exact-head local run is observed.

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
- IPv4 and explicit IPv6 literal bind support;
- bracketed IPv6 browser URL formatting with scoped-zone escaping;
- traversal rejection and path normalization;
- read-only serving of package resources;
- no gameplay/state mutation HTTP API;
- GET/HEAD support;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: no-referrer`;
- restrictive same-origin Content Security Policy.

`0.0.0.0` / `::` remain explicit trusted-LAN development choices, not the normal default. Public/mobile deployment should use HTTPS static hosting.

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

Not claimed without independent evidence:

- a complete exact-head local Ruff/mypy/pytest/Node repository pass;
- a successful GitHub Actions conclusion when no conclusion is exposed;
- real-device Android/iOS/iPadOS/ChromeOS evidence;
- release-candidate accessibility evidence;
- signed release artifacts;
- real terminal screenshots/demo media before they are captured from a signed-off build.

---

## Next engineering priorities

1. Run or observe the complete Python + Node quality gates on the exact current head.
2. Require CI/security checks to pass on that exact candidate SHA before tagging a release.
3. Install the built wheel on Windows, macOS, and Linux and verify CLI, TUI, Doctor, `guessnova web`, and `guessnova-web` from the installed artifact.
4. Verify the complete PWA module/asset set in the installed wheel and host the PWA over HTTPS for browser/mobile release validation.
5. Complete keyboard/touch/responsive/light-dark/reduced-motion checks and the manual accessibility evidence template on the exact candidate.
6. Compare Python/browser Daily Challenge targets for the same date+difficulty as a release-candidate parity check.
7. Capture real screenshots and demo media only from the verified candidate, following `docs/media/README.md` provenance rules.
8. Consider any item under **Gated future candidates** only when its prerequisite actually exists; do not manufacture schema/version/native-platform work to make the roadmap look busier.

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
