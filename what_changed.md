# GuessNova — Cross-Platform Implementation Handoff

## Status

GuessNova `main` now provides a supported interface path across the major desktop, mobile, Chromebook, and browser platform families.

Repository:

```text
https://github.com/sanskarIN/guessnova
```

Current release metadata is intentionally still `1.4.0`; the browser/PWA work remains unreleased until an intentional version/tag decision is made. Python state schema, backup wrapper, replay format, and Doctor report protocol are unchanged.

Previous detailed v1.4 history remains preserved in:

- `docs/continuity/v1_4_pr_checkpoint.md`
- `docs/continuity/v1_3_merged_checkpoint.md`

---

## Supported platform model

### Python desktop interfaces

Official desktop Python path:

- Windows 10/11
- current macOS with Python 3.13+
- modern Linux distributions with Python 3.13+

Available interfaces:

- Rich CLI
- six-pane Textual TUI
- Doctor diagnostics/recovery
- bundled local PWA server

### Browser/PWA interfaces

Responsive PWA path:

- Windows browsers
- macOS browsers
- Linux browsers
- Android
- iOS
- iPadOS
- ChromeOS
- other modern standards-based desktop/mobile browsers

Android/iOS support is deliberately provided by one installable responsive PWA, not by unimplemented native APK/AAB/IPA claims.

Full matrix: `docs/platforms.md`.

---

## Browser/PWA implementation

Bundled assets:

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

Implemented browser features:

- Classic mode
- Timed mode
- Streak mode
- Daily Challenge
- Reverse mode
- Easy / Normal / Hard / Expert difficulties
- smart temperature/direction/parity hints
- explicit range hints
- local games played/won/win-rate statistics
- current/best streak
- bounded recent-round history
- browser-origin local persistence
- responsive phone/tablet/desktop layout
- touch-friendly minimum control sizing
- keyboard focus indicators
- live status output
- light/dark color-scheme adaptation
- reduced-motion support
- install prompting where the browser supports it
- iOS/iPadOS home-screen metadata
- service-worker offline app-shell caching
- no account, telemetry, ads, analytics, cloud sync, or gameplay backend

The browser state intentionally does not silently read/write the Python schema-2 `state.json` store.

---

## Browser state reliability hardening

New module:

```text
src/guessnova/web/browser-state.mjs
```

Browser persistence continues to use:

```text
localStorage key: guessnova.web.v1
browser state marker: 1
history limit: 12
```

The new normalization boundary prevents stale/corrupted localStorage values from being trusted directly by rendering/gameplay code.

Normalization now:

- falls back safely for invalid/non-object JSON;
- discards unknown top-level persisted fields;
- rejects negative/non-integer/non-finite counters;
- bounds counters to a finite safe application limit;
- keeps games-won/streak values internally consistent with games-played;
- bounds history to the configured recent-round limit;
- discards non-object history entries;
- normalizes mode and difficulty identifiers;
- validates stored targets against the selected difficulty range;
- converts invalid completion timestamps to `null`;
- preserves legacy unversioned `guessnova.web.v1` values by normalizing them into the current shape;
- uses `Object.hasOwn()` for difficulty membership so inherited names such as `toString` cannot become fake difficulty identifiers.

`app.js` now parses and serializes through this boundary. If localStorage access itself is blocked by browser privacy settings, gameplay still falls back to in-memory state rather than failing startup.

Deterministic tests are in:

```text
tests/web/test_browser_state.mjs
```

Observed scratch validation for the current normalization logic:

```text
7 tests
7 pass
0 fail
```

This observed scratch run covers the browser-state module with equivalent current difficulty constants; it is not a claim that the complete repository CI suite has passed.

---

## Installability hardening

The PWA manifest supplies real raster icons at:

```text
192x192  src/guessnova/web/icon-192.png
512x512  src/guessnova/web/icon-512.png
```

The HTML uses the 192px raster image for `apple-touch-icon`, while SVG remains available as the normal scalable favicon.

The service worker caches both raster icons, all primary JavaScript modules including `browser-state.mjs`, and uses cache namespace:

```text
guessnova-web-v3
```

The namespace advanced so existing installations can transition to the state-normalized app shell.

A temporary text-only placeholder commit was created earlier when a normal text-file action was first used for a `.png` path. That was caught immediately. A follow-up Git object/blob/tree commit replaced it with actual PNG bytes and added the 512px image. Repository fetch verification confirmed both current paths are binary PNG content.

The corrective commit is:

```text
ec4877716ce3c5a6b3aecafe28b776039fd13dc1  fix(web): replace placeholder with real PWA raster icons
```

Do not treat the earlier placeholder commit as the current file state.

---

## Local PWA server

Module:

```text
src/guessnova/web_server.py
```

Entry points:

```bash
guessnova web
guessnova-web
```

Defaults:

```text
127.0.0.1:8765
```

Properties:

- Python standard-library server; no runtime web-framework dependency
- loopback-only binding by default
- `--host`, `--port`, `--no-open`
- path normalization
- traversal rejection
- read-only package-resource serving
- no gameplay/state mutation HTTP API
- `GET` / `HEAD`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: no-referrer`
- restrictive same-origin Content Security Policy

`--host 0.0.0.0` is documented only for deliberate trusted-LAN development. Normal phone/tablet/public deployment should use an HTTPS static host.

---

## Cross-language Daily Challenge parity

Legacy `daily_seed()` remains available for compatibility.

Portable daily-v2 rule:

```text
guessnova-daily-v2:<YYYY-MM-DD>:<difficulty>
```

Python and JavaScript both use unsigned FNV-1a 32-bit and map the result directly into the selected difficulty's inclusive range.

Fixed parity vector:

```text
Date:       2026-08-19
Difficulty: normal
Hash:       230553734
Target:     35
```

Updated Python files:

- `src/guessnova/rng.py`
- `src/guessnova/daily.py`

Browser file:

- `src/guessnova/web/game-engine.mjs`

Tests in both languages protect the vector.

---

## CLI and package integration

Updated:

- `src/guessnova/entrypoint.py`
- `pyproject.toml`

Dispatcher behavior:

```text
doctor -> Doctor CLI
web    -> bundled local PWA server
other  -> existing Rich gameplay/data CLI
```

Installed script:

```text
guessnova-web = guessnova.web_server:main
```

The Python package metadata reflects terminal + web environments and OS-independent packaging.

PWA assets live inside `src/guessnova` so wheel installation can be checked for asset preservation.

---

## Tests added/updated

### Python

```text
tests/test_web_server.py
```

Covers:

- root asset mapping
- query stripping
- traversal rejection
- required PWA asset presence, including `browser-state.mjs`
- required 192px/512px raster icon presence
- local HTTP serving
- server security headers

Updated:

```text
tests/test_daily.py
tests/test_entrypoint.py
```

Covers portable daily parity and web-command routing.

### Browser engine

```text
tests/web/test_game_engine.mjs
```

Covers:

- Daily Challenge parity vector
- difficulty configuration parity
- GuessGame outcome behavior
- smart-hint semantics
- ReverseGuesser convergence

### Browser state

```text
tests/web/test_browser_state.mjs
```

Covers:

- isolated/versioned default browser state
- malformed persisted-value recovery
- internally consistent bounded counters
- malformed/oversized history normalization
- invalid target/timestamp normalization
- legacy unversioned state readability
- corrupt JSON recovery
- normalized serialization round-trip
- rejection of inherited/prototype-key difficulty identifiers

### Static-review bug fixed earlier

A completed Reverse round disabled the three response controls, and a newly started Reverse round initially inherited those disabled controls.

Fixed in:

```text
61a0d058b268e1c73f5133645101940d5a8b46c0  fix(web): re-enable reverse controls on new rounds
```

`startReverse()` explicitly re-enables Lower / Correct / Higher.

---

## CI and release gates

A browser-test glob defect was found during this continuation.

The workflows previously used:

```bash
node --test tests/web/*.test.mjs
```

but the committed engine test is named:

```text
tests/web/test_game_engine.mjs
```

The test glob is now correctly:

```bash
node --test tests/web/*.mjs
```

Normal CI now runs:

```bash
node --test tests/web/*.mjs
node --check src/guessnova/web/app.js
node --check src/guessnova/web/browser-state.mjs
node --check src/guessnova/web/game-engine.mjs
node --check src/guessnova/web/sw.js
```

The existing Python checks remain configured:

- Ruff lint
- Ruff format check
- strict mypy
- pytest + coverage
- compileall
- release-metadata verification
- smoke tests

Built-wheel matrices remain on:

- Ubuntu
- Windows
- macOS

and verify:

```bash
guessnova web --help
guessnova-web --help
```

plus required bundled modules/assets including:

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

Tagged `.github/workflows/release.yml` includes the same browser tests, JavaScript syntax checks, installed-wheel PWA entry-point checks, and PWA asset verification. A release tag therefore cannot intentionally rely only on the Python surface while ignoring the browser client.

---

## Documentation updated

Added previously:

- `docs/platforms.md`

Updated across the cross-platform continuation:

- `README.md`
- `docs/setup.md`
- `PRIVACY.md`
- `SECURITY.md`
- `ROADMAP.md`
- `CHANGELOG.md`
- `what_changed.md`

Documentation now clearly separates:

- desktop Python requirements from mobile/browser requirements
- Python `state.json` from browser-origin storage
- local loopback hosting from deliberate LAN exposure
- gameplay-data privacy from ordinary static-asset HTTP requests on a remote host
- PWA support from native mobile binary claims
- shipped PWA work from still-gated native wrapper/interchange candidates

---

## Important cross-platform commits

The continuation was intentionally granular. Earlier key commits include:

```text
0d702a7959abdfed518b366304e3cf14dbfb028f  feat(web): add local PWA server
d602874490cd443cc9aecb7c17afdd16749fdad9  feat(web): add portable browser game engine
7c307993dbde4f24514fed1a864a23453241bf98  feat(web): add responsive PWA shell
20edfc225899eab1f7ba6e08f77c2b8538e13b39  feat(web): add adaptive mobile desktop styling
4833dfe8d937b191cffec2934d213fe6f8959247  feat(web): implement offline browser gameplay
c00583e3395bd83f139be6938f6f05645d98ba57  feat(web): add installable PWA manifest
1f9d6683ef1b070c877bddfc40413b292fd47c47  feat(web): add offline service worker
6edfc5f43332bdb135fd327fb87756328af230cb  feat(web): add scalable app icon
1312f345191704dd5cc9ff06fbd558a0eab4269c  feat(core): add cross-language daily challenge hash
2afd1200d60b979a703251dcf7a21293db23d821  feat(core): use portable daily targets across platforms
356a9e47803de83cf0fffa22f28093316e4cff14  test(core): cover portable daily challenge parity
f07eb5bc3dffebac10d973f27271510370f76df3  feat(cli): route guessnova web command
efdc270747d1bc2a0e409380756c2d8d4b29f134  build: expose cross-platform web entry point
1945850a6535a696bec40cac0091139c6782c34d  test(web): cover bundled PWA server
0c54377d95fd1f0b521832d94c1f2241e8363af4  test(web): cover portable browser engine
5a709b8fe8be9c478e0d5573be828c934efa1c0d  test(cli): cover web command routing
deb9b97e7b96995ce7e3b76de3fa586f168cee54  ci: validate Python and PWA cross-platform surfaces
a098b9afba06f170c0de2e9e80f4ec75cf7cf795  docs: document full cross-platform support matrix
b86984b1fb648db953c45c4df48f27d253f958c5  docs: publish cross-platform support and PWA usage
61a0d058b268e1c73f5133645101940d5a8b46c0  fix(web): re-enable reverse controls on new rounds
74b50e294f59f865f29313c141fcbe034d81065a  style(web): harden local server formatting
5ea450e119f188fd257575acc609e77d1b84530a  feat(web): improve iOS and mobile PWA metadata
42dbd0f15445a9924c96a4272a7d0455d782b6ca  docs(privacy): cover browser and PWA data behavior
360fc7f5682a51ad176e9bdab45be89a66f039fd  docs(security): define PWA and local server boundaries
0cc60cb9e09c3e8d9a36e169365f86a4190ca4be  docs(setup): add desktop mobile and PWA setup
66035db20ab2b8c158970aa6dc1ed32407d4dda9  docs: record cross-platform implementation checkpoint
663013f47d611d0eb3f7d73f481363be59c7cd5b  feat(web): add 192px PWA raster icon (temporary text placeholder; superseded)
ec4877716ce3c5a6b3aecafe28b776039fd13dc1  fix(web): replace placeholder with real PWA raster icons
dfac717dcbf83a394f284fa9c1ce64195411a33f  fix(web): satisfy PWA raster icon requirements
0b1f3bbe983050a4259d5e89b9df90a23715a3f7  fix(web): use raster iOS home screen icon
f8e2a9b10134d2ee9bd627454d8ad549063d0da9  fix(web): cache installable PWA raster icons
73fc58ba37fdf227889d251ffbd8bff378006bdc  test(web): require raster PWA install icons
9a83505865df72ea2cf814cb1fbd2390e945351d  ci: verify installable PWA icon assets in wheels
dfa210ad06d7d77c9e93259059015307d9fd8eaa  ci(release): gate releases on PWA browser checks
```

Reliability/quality continuation commits include:

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
```

---

## Validation state

Do not infer unobserved passes.

Verified directly during the cross-platform work:

- repository file modifications and commit history
- portable FNV-1a daily-v2 fixed vector calculation
- current 192px icon path is a real PNG blob
- current 512px icon path is a real PNG blob
- source/static review of PWA/server paths
- Reverse restart regression discovery and repair
- browser state normalization logic and prototype-key hardening
- local scratch Node execution of the current browser-state regression set: 7/7 pass
- documentation consistency review

Not claimed:

- a complete local Ruff/mypy/pytest/Node full-suite pass;
- successful GitHub Actions conclusions when no conclusion was exposed by the available status connector;
- real Android/iOS/ChromeOS device evidence;
- release-candidate accessibility evidence;
- signed release artifacts.

The available local execution environment cannot clone GitHub because external DNS/network resolution is unavailable. The GitHub combined-status connector returned an empty status set when inspected; an empty set is not equivalent to pass or fail.

Release-candidate verification still requires actual CI conclusions and real browser/device checks on the exact candidate SHA.

---

## Compatibility metadata

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

The PWA does not require a Python state-schema migration because its browser-local storage is a separate presentation store.

---

## Release-candidate checklist

Before tagging a release candidate:

1. require CI/security checks to pass on the exact candidate SHA;
2. install the wheel on Windows, macOS, and Linux;
3. verify CLI, TUI, Doctor, `guessnova web`, and `guessnova-web`;
4. verify the complete PWA asset/module set is present in the wheel;
5. run `node --test tests/web/*.mjs` and all configured JavaScript syntax checks;
6. host the PWA over HTTPS;
7. test current Android Chromium installation/offline behavior;
8. test iPhone Safari Add to Home Screen/offline behavior;
9. test iPad Safari;
10. test ChromeOS;
11. test available current desktop Chrome/Edge/Firefox/Safari;
12. verify corrupt/stale browser storage falls back or normalizes without breaking startup;
13. verify touch, keyboard, responsive breakpoints, light/dark mode, and reduced motion;
14. compare a Daily Challenge target between Python and browser for the same date+difficulty;
15. complete the existing manual accessibility evidence on the candidate;
16. capture real screenshots/media only from that verified candidate.

Do not fabricate CI results, device evidence, accessibility evidence, or screenshots.

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
