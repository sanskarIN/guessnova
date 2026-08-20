# GuessNova — Cross-Platform Implementation Checkpoint

## Current milestone

GuessNova `main` now contains a supported cross-platform delivery path spanning desktop Python interfaces and a responsive offline-first browser/PWA interface.

Repository:

```text
https://github.com/sanskarIN/guessnova
```

Current package/runtime release metadata remains `1.4.0`. This continuation deliberately does not invent a new release tag or stored-data schema merely because a new presentation surface was added.

Previous detailed v1.4 implementation history remains archived in:

- `docs/continuity/v1_4_pr_checkpoint.md`
- `docs/continuity/v1_3_merged_checkpoint.md`

This file is the active handoff for the cross-platform continuation after that archive.

---

# 1. Supported platform model

GuessNova now has two supported presentation families:

## Python desktop/terminal

Supported on:

- Windows 10/11
- current macOS releases with Python 3.13+
- modern Linux distributions with Python 3.13+

Interfaces:

- Rich CLI
- six-pane Textual TUI
- Doctor diagnostics/recovery CLI
- bundled local PWA server

## Browser/PWA

Supported through modern standards-based browsers on:

- Windows
- macOS
- Linux
- Android
- iOS
- iPadOS
- ChromeOS
- other modern desktop/mobile browser platforms

The mobile strategy intentionally uses one responsive standards-based PWA rather than separate Android/iOS native codebases that would duplicate game rules and maintenance work.

Detailed matrix: `docs/platforms.md`.

---

# 2. New PWA implementation

New bundled web application files:

```text
src/guessnova/web/
├── app.css
├── app.js
├── game-engine.mjs
├── icon.svg
├── index.html
├── manifest.webmanifest
└── sw.js
```

The PWA includes:

- Classic mode
- Timed mode
- Streak mode
- Daily Challenge
- Reverse mode
- Easy/Normal/Hard/Expert difficulties matching Python ranges and attempt/timer values
- smart direction/temperature/parity hints
- explicit range hints
- local played/won/win-rate statistics
- current/best streak tracking
- bounded recent-round history
- origin-scoped local browser persistence
- responsive phone/tablet/laptop/desktop layout
- minimum touch target sizing
- keyboard focus indicators
- live status announcements
- light/dark color-scheme adaptation
- reduced-motion handling
- install prompting where supported
- mobile/iOS web-app metadata
- service-worker offline caching
- no account, telemetry, ads, analytics, cloud sync, or gameplay backend

Browser state intentionally remains sandboxed from the Python `state.json` profile/backup model.

---

# 3. Local PWA server

New source:

```text
src/guessnova/web_server.py
```

Entry paths:

```bash
guessnova web
guessnova-web
```

Defaults:

```text
host: 127.0.0.1
port: 8765
```

Security/reliability properties:

- standard-library HTTP server; no new runtime web-framework dependency
- loopback-only binding by default
- explicit `--host`, `--port`, and `--no-open`
- normalized asset paths
- `..` traversal rejection
- read-only serving from packaged `guessnova/web` resources
- no state mutation/API endpoints
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: no-referrer`
- restrictive same-origin Content Security Policy
- `HEAD` and `GET` asset support

An explicit `--host 0.0.0.0` is documented as trusted-LAN development only. Normal mobile/public deployment should use an HTTPS static host.

---

# 4. Cross-language Daily Challenge parity

The former Python-only deterministic daily mechanism depended on Python's PRNG after producing a SHA-256 seed. That is reproducible inside Python, but it is not a suitable language-independent target rule.

The continuation retains legacy `daily_seed()` for compatibility and adds a portable v2 rule shared by Python and JavaScript:

```text
guessnova-daily-v2:<YYYY-MM-DD>:<difficulty>
```

The string is hashed with unsigned FNV-1a 32-bit and mapped directly into the selected difficulty's inclusive target range.

Fixed parity vector covered by both languages:

```text
Date:       2026-08-19
Difficulty: normal
Hash:       230553734
Target:     35
```

Updated Python files:

- `src/guessnova/rng.py`
- `src/guessnova/daily.py`

Browser implementation:

- `src/guessnova/web/game-engine.mjs`

This makes the same date+difficulty Daily Challenge resolve to the same target in Python and PWA clients.

---

# 5. Python CLI/package integration

Updated:

- `src/guessnova/entrypoint.py`
- `pyproject.toml`

`guessnova` now routes:

```text
doctor -> Doctor CLI
web    -> local PWA server
other  -> existing Rich game CLI
```

New installed script:

```text
guessnova-web = guessnova.web_server:main
```

Packaging metadata now describes both terminal and browser environments and marks the project OS-independent at the Python package metadata level.

The PWA lives inside the selected `src/guessnova` package tree so built-wheel verification can assert that web assets survived packaging.

---

# 6. Automated regression coverage

New Python test:

```text
tests/test_web_server.py
```

Coverage includes:

- safe root asset mapping
- query stripping
- traversal rejection
- required bundled PWA assets
- loopback HTTP serving
- security headers

New Node/browser-engine test:

```text
tests/web/test_game_engine.mjs
```

Coverage includes:

- fixed Python/JavaScript Daily Challenge parity vector
- difficulty configuration parity
- Classic GuessGame result semantics
- smart-hint behavior
- ReverseGuesser convergence

Updated:

```text
tests/test_daily.py
tests/test_entrypoint.py
```

Additional coverage includes portable daily seeds/targets and `guessnova web --help` routing.

During static review, a concrete browser bug was found and fixed: completing a Reverse round disabled its response controls, and a subsequent Reverse round originally inherited those disabled buttons. `startReverse()` now explicitly re-enables all three response controls.

---

# 7. CI expansion

`.github/workflows/ci.yml` now adds Node.js 22 to the main verification job and runs:

```bash
node --test tests/web/*.test.mjs
node --check src/guessnova/web/app.js
node --check src/guessnova/web/game-engine.mjs
node --check src/guessnova/web/sw.js
```

The existing built-wheel matrix remains on:

- Ubuntu
- Windows
- macOS

and now additionally verifies after wheel installation:

```bash
guessnova web --help
guessnova-web --help
```

plus required PWA asset presence inside the installed package.

The pre-existing Python lint, format, strict typing, pytest/coverage, compile, release-metadata, smoke, Doctor, TUI import, security, and CodeQL paths remain configured.

---

# 8. Documentation updated

Added:

- `docs/platforms.md`

Updated:

- `README.md`
- `docs/setup.md`
- `PRIVACY.md`
- `SECURITY.md`
- `what_changed.md`

The documentation now distinguishes:

- Python desktop state from browser origin storage
- application gameplay data from ordinary hosted static-asset requests
- local loopback serving from explicit LAN exposure
- Python CLI/TUI requirements from mobile PWA requirements
- PWA support from claims of native Android/iOS binaries

---

# 9. Granular commit sequence

Cross-platform work was pushed directly to `main` as granular commits rather than one monolithic change.

Implementation/test/docs commits through this checkpoint include:

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
```

This handoff update is the next granular commit after that sequence.

---

# 10. Validation state — no fabricated pass claims

The repository now contains automated checks for the cross-platform work, but this checkpoint does **not** claim those checks passed when their execution result was not observed.

The available execution environment could not clone the repository because external DNS/network access from the local container failed previously with:

```text
fatal: unable to access 'https://github.com/sanskarIN/guessnova.git/':
Could not resolve host: github.com
```

The local environment also did not have all repository development tools installed. Therefore this continuation does not fabricate local executions of:

- Ruff
- Ruff format
- strict mypy
- full pytest suite
- Node browser-engine tests
- built-wheel installation
- browser/device matrix testing

GitHub's combined commit-status connector also returned no status entries for the inspected cross-platform head at that time. That is not equivalent to a passing or failing GitHub Actions result.

What *was* completed in this continuation:

- source-level architecture review
- direct repository file modifications
- static code review of the new PWA/server paths
- fixed-vector cross-language algorithm design
- test definitions for Python and browser logic
- CI definitions for Python/browser/package paths
- packaging-layout review
- documentation consistency audit
- discovery and repair of the Reverse-round restart regression

Before a release tag, the exact candidate commit should receive successful CI/security checks and manual real-browser/device verification.

---

# 11. Release and compatibility boundaries

Unchanged compatibility metadata:

```text
package/runtime version  1.4.0
state schema             2
backup wrapper           2
legacy backup wrapper    1
replay format            1
Doctor report protocol   1
Python requirement       >=3.13
license                  MIT
```

No storage-schema migration is required merely for the new PWA because browser-local state is a separate origin-scoped presentation-store and does not change Python schema-2 persistence.

No native Android APK/AAB or iOS IPA is claimed. Android/iOS/iPadOS support is through the installable standards-based PWA.

---

# 12. Recommended release verification

Before calling a tagged build fully release-verified:

1. require all automated checks to pass on the exact candidate SHA;
2. run Python package installation on Windows, macOS, and Linux;
3. run CLI, TUI, Doctor, `guessnova web`, and `guessnova-web` entry checks;
4. confirm built-wheel PWA assets are present;
5. run Node browser-engine tests and syntax checks;
6. test the hosted PWA on current Android Chrome/Chromium;
7. test the hosted PWA on current iPhone Safari and Add to Home Screen;
8. test the hosted PWA on iPad Safari;
9. test the PWA on ChromeOS;
10. test current Chrome/Edge/Firefox/Safari desktop browsers where available;
11. verify first-load and offline cached-load behavior;
12. verify install/uninstall and browser-storage reset behavior;
13. verify touch, keyboard, light/dark scheme, reduced motion, and responsive breakpoints;
14. verify the same Daily Challenge date+difficulty target between Python and browser;
15. complete existing manual accessibility evidence on the exact release candidate;
16. capture real screenshots/media only from the verified candidate.

Do not fabricate device screenshots, accessibility evidence, or CI conclusions.

---

# 13. Current continuation priorities

If work continues from this checkpoint:

1. inspect the latest `main` SHA first;
2. inspect exact GitHub Actions conclusions once available;
3. fix only reproducible failures with focused regression coverage;
4. consider a future release version only when preparing a real release candidate;
5. keep the portable daily-v2 test vector synchronized across Python and JavaScript;
6. keep mobile/browser data isolated unless a carefully designed explicit import/export bridge is introduced;
7. do not expose the local Python web server publicly by default;
8. do not claim native Android/iOS packages unless those artifacts are actually implemented and verified;
9. preserve privacy-first/no-account/no-telemetry guarantees;
10. preserve granular commit history.

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

GuessNova remains usable without donation, account creation, telemetry, analytics, cloud sync, or a gameplay backend.
