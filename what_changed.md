# GuessNova — Current Engineering Handoff

## Status

GuessNova `main` now has a production-oriented Python terminal stack plus a responsive installable browser/PWA path for the major desktop, mobile, and Chromebook platform families.

Repository:

```text
https://github.com/sanskarIN/guessnova
```

Release metadata intentionally remains `1.4.0`. The browser/PWA continuation is recorded under `Unreleased`; this work does not create a tag or silently change the Python compatibility formats.

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

New module:

```text
src/guessnova/web/browser-state.mjs
```

The application no longer trusts raw `localStorage` content directly. `app.js` parses and serializes browser progress through a defensive normalization layer.

The boundary now:

- safely handles missing, invalid, or non-object JSON;
- discards unknown persisted top-level fields;
- rejects negative, non-integer, non-finite counters;
- bounds counters to a finite application limit;
- keeps games-won and streak counters internally consistent;
- bounds retained history to 12 entries;
- discards non-object history entries;
- normalizes mode and difficulty identifiers;
- validates stored targets against difficulty ranges;
- converts invalid completion timestamps to `null`;
- uses `Object.hasOwn()` for difficulty membership so prototype names such as `toString` cannot become fake difficulty identifiers;
- preserves legacy unversioned `guessnova.web.v1` state;
- rejects explicitly versioned unknown/future browser-state schemas instead of interpreting them as the current format;
- falls back to in-memory state when browser privacy settings block storage access.

Current browser marker:

```text
BROWSER_STATE_SCHEMA = 1
```

An unversioned legacy browser object is accepted and normalized. If a persisted object explicitly contains a schema other than integer `1`, it falls back to safe defaults.

---

## Browser regression tests

Browser engine tests:

```text
tests/web/test_game_engine.mjs
```

Browser-state tests:

```text
tests/web/test_browser_state.mjs
```

The state suite now covers:

- isolated/versioned default objects;
- malformed persisted-value recovery;
- counter bounding and consistency;
- malformed/oversized history normalization;
- invalid target/timestamp handling;
- legacy unversioned state readability;
- corrupt JSON recovery;
- normalized serialization round-trip;
- prototype/inherited-key difficulty rejection;
- future/unknown browser schema rejection.

Observed scratch execution for the current state-normalization regression set:

```text
8 tests
8 pass
0 fail
```

This is an observed targeted Node scratch run for the browser-state logic. It is not represented as a full repository CI pass.

---

## CI defect fixed

A real browser-test gate defect was found in both normal CI and tagged-release verification.

The workflows used:

```bash
node --test tests/web/*.test.mjs
```

but the committed engine test is named:

```text
tests/web/test_game_engine.mjs
```

The browser test command is now:

```bash
node --test tests/web/*.mjs
```

Normal CI and release verification now also syntax-check:

```bash
node --check src/guessnova/web/app.js
node --check src/guessnova/web/browser-state.mjs
node --check src/guessnova/web/game-engine.mjs
node --check src/guessnova/web/sw.js
```

The existing Python gates remain configured for Ruff, formatting, strict mypy, pytest/coverage, compileall, release metadata, and smoke testing.

---

## Cross-platform package verification

Ubuntu, Windows, and macOS package matrices continue to build/install the wheel and verify the primary installed commands.

The PWA wheel check now explicitly requires:

```text
index.html
app.js
browser-state.mjs
game-engine.mjs
sw.js
manifest.webmanifest
icon-192.png
icon-512.png
```

This prevents a wheel from appearing valid while omitting a JavaScript module needed by the browser client.

---

## Offline installability

The PWA includes real raster install icons:

```text
192x192  src/guessnova/web/icon-192.png
512x512  src/guessnova/web/icon-512.png
```

The service worker caches the browser-state module together with the rest of the application shell. Current cache namespace:

```text
guessnova-web-v3
```

The namespace was advanced so existing installations can transition to the state-normalized application shell.

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

## Documentation alignment

This continuation aligned:

- `ROADMAP.md`
- `CHANGELOG.md`
- `what_changed.md`
- existing platform/setup/privacy/security documentation from the cross-platform implementation

The roadmap no longer describes the already-shipped PWA source as merely a future optional edition. Native wrappers and browser/Python state interchange remain gated future candidates until they have a real design, compatibility boundary, and tests.

---

## Granular reliability/quality commits in this continuation

```text
8db75504017ebab17d3b95d7441d408c4a48234c  fix(ci): run the committed browser test suite
6a247b8c942099ec46dcbb126d1717fb9b1cd49d  fix(release): execute browser tests before publishing
a2728eb5a2f9b1594c2e13b83297215dbd1df0e1  feat(web): add defensive browser state normalization
02b40bcd3d8b3b2525d12cb336ba8caf90a40fa3  test(web): cover corrupt browser state recovery
e3a8fc290cf5e37730a6bf35180cefd80defa338  fix(web): normalize persisted state before rendering
9f38e3a796afffe7e4a019d91026dbbe73e755af  fix(web): cache browser state module for offline PWA
806d429909eebee29c94a0c23035068f9374208d  test(web): require browser state module in package assets
d32d5e7fc1f307245af24c1ae6b815a460c0dc61  ci(web): verify state module syntax and wheel inclusion
1ab994de1e9f2674a68b40f9d0eae41a393a5d82  ci(release): validate browser state module in artifacts
dee40c6fddad7634b54beca2e421e99672282cc8  docs(roadmap): promote shipped PWA from future candidate
67404c4af29183e20142330461209c6c822ad33f  docs(changelog): record PWA reliability and CI hardening
594a6fc934fa4ad1adcf974fed389da662584f42  fix(web): reject inherited difficulty keys
8fab003a95b4975a981dbb3725dd86f4ecbe8e11  test(web): reject prototype-key difficulty values
0f790e0dd94428098e73b3109c3f9868d27c6d09  docs: refresh cross-platform reliability handoff
8e2f2559dfa59293e8c59d5b41f6cb258fa185f7  fix(web): reject unknown browser state schemas
1d39582a2abfa84e96d2bb4ae5e50eefec46abf6  test(web): cover future browser schema rejection
```

Earlier cross-platform/PWA implementation commits remain in Git history; this section intentionally records the reliability continuation rather than duplicating the entire repository history.

---

## Validation truthfulness

Verified directly during the work:

- repository files and commit history through the GitHub connector;
- the CI/release glob mismatch and its correction;
- source/static review of the PWA/server/state boundaries;
- real PNG install icon paths from the earlier cross-platform work;
- browser-state normalization behavior;
- prototype-key hardening;
- explicit future-schema rejection;
- targeted browser-state scratch tests: 8/8 pass.

Not claimed:

- a complete local Ruff/mypy/pytest/Node repository pass;
- a successful GitHub Actions conclusion when no conclusion was exposed by the available status data;
- real-device Android/iOS/iPadOS/ChromeOS evidence;
- release-candidate accessibility evidence;
- signed release artifacts.

The available container could not clone GitHub because external DNS resolution was unavailable. An inspected GitHub combined-status result was empty; an empty status set is not equivalent to a pass or failure.

---

## Release-candidate checklist

Before tagging the browser/PWA continuation:

1. require CI/security checks to pass on the exact candidate SHA;
2. install the wheel on Windows, macOS, and Linux;
3. verify CLI, TUI, Doctor, `guessnova web`, and `guessnova-web`;
4. verify the complete PWA module/asset set in the installed wheel;
5. run `node --test tests/web/*.mjs` and configured JavaScript syntax checks;
6. test corrupt/stale browser storage and unknown schema handling;
7. host the PWA over HTTPS for mobile/browser validation;
8. test Android Chromium install/offline behavior;
9. test iPhone and iPad Safari Add to Home Screen/offline behavior;
10. test ChromeOS;
11. test available current desktop Chrome/Edge/Firefox/Safari;
12. verify keyboard, touch, responsive breakpoints, light/dark mode, and reduced motion;
13. compare Python/browser Daily Challenge targets for the same date+difficulty;
14. complete manual accessibility evidence on the exact candidate;
15. capture screenshots/demo media only from that verified candidate.

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
