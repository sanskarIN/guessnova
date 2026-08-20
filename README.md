# GuessNova

<p align="center">
  <img src="assets/banner.svg" alt="GuessNova — number guessing, supernova style" width="820" />
</p>

<p align="center">
  <a href="https://github.com/sanskarIN/guessnova/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/sanskarIN/guessnova/ci.yml?branch=main&label=CI"></a>
  <a href="https://github.com/sanskarIN/guessnova/actions/workflows/codeql.yml"><img alt="CodeQL" src="https://img.shields.io/github/actions/workflow/status/sanskarIN/guessnova/codeql.yml?branch=main&label=CodeQL"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://www.python.org/"><img alt="Python 3.13+" src="https://img.shields.io/badge/python-3.13%2B-3776AB.svg"></a>
  <a href="https://buymeacoffee.com/sanskarIN"><img alt="Buy Me a Coffee" src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20GuessNova-FFDD00?logo=buymeacoffee&logoColor=000000"></a>
</p>

> **Made by the Sanskar**

**GuessNova** is a production-minded, privacy-first number guessing game for Python terminals and standards-based browsers. It turns a familiar game into a polished local product with multiple modes, cross-platform daily challenges, replay codes, smart and explicit hints, recoverable profiles, rich session history, achievements, XP, statistics, a leaderboard, integrity-protected backup/restore, read-only backup verification, local diagnostics/repair, bilingual terminal presentation, first-run onboarding, semantic themes, a full six-pane Textual workspace, a Rich CLI, and an offline-first responsive PWA for phones, tablets, Chromebooks, and desktop browsers.

## Demo

Real release captures belong in `docs/media/` and must come from a signed-off build. Until then, the CLI flow looks like:

```text
GuessNova · Classic · Normal · 1–100
Guess [9 left] › 50
Too low.
Hint: warm; try higher. The target is odd.
Guess [8 left] › hint
Range hint: the target is between 62 and 82. Using it costs 10 XP from a winning reward.
```

## Features

- **Classic** — focused number guessing with difficulty-based ranges and attempt budgets.
- **Timed** — solve before the difficulty-specific timer expires.
- **Streak** — play streak-tagged rounds and build persistent profile streaks.
- **Reverse** — think of a number and let GuessNova find it with binary search.
- **Daily Challenge** — portable v2 daily targets are reproducible across the Python and browser clients for the same date and difficulty.
- **Smart hints** — temperature, direction, and parity feedback after guesses.
- **Explicit range hints** — type `hint` for a narrowed range clue, with optional XP penalty via `--hint-penalty` / `--no-hint-penalty`.
- **Profiles** — local stats, average guesses, streaks, XP, settings, achievements, and bounded session history.
- **Safe profile lifecycle** — list, create, activate, rename, delete, inspect recoverable trash, and restore profiles without permanent one-command deletion.
- **Advanced history** — filter by mode, difficulty, result, date range, free-text search, and group by day/mode/difficulty/result.
- **First-run onboarding** — concise keyboard/privacy/settings guidance with no sign-in or network requirement.
- **Replay codes** — checksum-protected, strictly validated portable summaries for completed challenges.
- **Local leaderboard** — ranked winning results stored on your device; profile rename/delete/restore keeps related local data coherent.
- **Schema-2 persistence** — explicit migration from older saves with committed migration fixtures and future-schema rejection.
- **Integrity-protected backups** — backup wrapper v2 separates backup-format versioning from state schema and verifies SHA-256 payload integrity while retaining legacy backup compatibility.
- **Backup preflight** — `guessnova doctor --verify-backup PATH` validates wrapper integrity, schema metadata, and current importability without writing state.
- **Local doctor** — `guessnova doctor` inspects schema/profile/history/leaderboard/trash health and can safely normalize repairable state after creating a pre-repair backup; `guessnova-doctor` remains a compatible standalone entry point.
- **Bounded persistence I/O** — state and backup readers reject oversized input before unbounded JSON processing, and state saves are size checked before atomic replacement.
- **Scriptable diagnostics** — Doctor JSON report protocol v1 plus stable exit codes for healthy/valid, cancelled, and attention/error states.
- **Deterministic test mode** — use `--seed` or `GUESSNOVA_SEED` for reproducibility.
- **Accessible terminal modes** — `--plain` disables color and `--compact` prefers concise text over panels/tables.
- **Six-pane Textual workspace** — Play, Profiles, History, Leaderboard, Settings, and read-only Recovery in one keyboard-first local interface.
- **TUI profile safety** — create/use/rename/delete/restore locally, require exact-name delete confirmation, and reset unfinished rounds when profile ownership changes.
- **TUI data views** — newest-first bounded history filters plus ranked local leaderboard filters without creating a second storage model.
- **TUI settings and recovery** — active-profile settings, immediate high-contrast/smart-hint behavior, read-only diagnostics, and read-only backup verification.
- **Offline-first PWA** — responsive browser gameplay with Classic, Timed, Streak, Daily, and Reverse modes, local statistics/history, service-worker caching, and install support where the browser provides it.
- **Adaptive accessibility** — touch-friendly controls, keyboard focus indicators, live status announcements, responsive layouts, automatic light/dark color schemes, and reduced-motion support in the PWA.
- **Themes and contrast** — saved semantic Rich themes plus dedicated CLI and Textual high-contrast behavior.
- **English + Hindi** — complete offline `en` and `hi` terminal message catalogs with English fallback and per-profile locale settings.
- **Privacy-first** — no accounts, ads, analytics, telemetry, cloud sync, remote leaderboard, or application network calls.

## Supported platforms

GuessNova now provides a supported interface across the major desktop, mobile, Chromebook, and browser platform families:

| Platform | Python CLI/TUI | Web/PWA |
| --- | --- | --- |
| Windows 10/11 | ✅ | ✅ |
| macOS | ✅ | ✅ |
| Modern Linux | ✅ | ✅ |
| Android | — | ✅ |
| iOS/iPadOS | — | ✅ |
| ChromeOS | optional Linux environment | ✅ |
| Modern desktop/mobile browsers | — | ✅ |

Python 3.13+ is required for the CLI/TUI/Doctor/local web server. Mobile support is provided through the responsive standards-based PWA rather than separate Android and iOS codebases. See [`docs/platforms.md`](docs/platforms.md) for the detailed support matrix, installation guidance, security notes, and cross-platform daily-challenge rules.

A Unicode/ANSI-capable terminal provides the richest terminal presentation, but `--plain` remains available for reduced Rich formatting. CI builds and installs the package on Windows, macOS, and Linux runners, verifies the bundled PWA after wheel installation, and runs dedicated browser-engine/syntax checks with Node.js.

## Tech stack

- **Python 3.13+** for domain/application code, desktop interfaces, diagnostics, persistence, and the local PWA server.
- **Rich** for accessible terminal presentation.
- **Textual** for the six-pane local workspace and deterministic pilot testing.
- **HTML/CSS/JavaScript** for the dependency-light responsive PWA.
- **Service Worker + Web App Manifest** for offline caching and installable browser behavior.
- **JSON** for versioned local persistence, backup wrappers, and replay payloads.
- **Browser localStorage** for lightweight origin-scoped PWA statistics/history.
- **SHA-256** from Python's standard library for backup/replay integrity checks.
- **pytest / pytest-cov** for Python automated tests and **Node.js test runner** for browser-engine parity checks.
- **Ruff**, **mypy**, **pip-audit**, **CodeQL**, and **GitHub Actions** for repository quality and security automation.

## Quick start

```bash
git clone https://github.com/sanskarIN/guessnova.git
cd guessnova
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
guessnova play
guessnova-tui
guessnova web
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
guessnova play
guessnova-tui
guessnova web
```

The standalone browser entry point is also available:

```bash
guessnova-web
```

Both web commands bind to `127.0.0.1:8765` by default and open the responsive local PWA. See [`docs/setup.md`](docs/setup.md) and [`docs/platforms.md`](docs/platforms.md) for full setup and deployment details.

### Browser/PWA deployment

The static web application is bundled under:

```text
src/guessnova/web/
```

It can be deployed to any normal HTTPS static host. HTTPS is recommended for production because service workers and installability require a secure context outside `localhost`. Android, iOS/iPadOS, ChromeOS, and browser-first desktops can use this hosted PWA without requiring Python on the client device.

For intentional LAN development only:

```bash
guessnova web --host 0.0.0.0 --port 8765 --no-open
```

Binding to `0.0.0.0` exposes the development server to reachable network interfaces, so use it only on trusted networks.

## Play and manage local data

```bash
guessnova play
guessnova play --difficulty hard
guessnova play --mode timed --difficulty expert
guessnova play --mode daily
guessnova play --mode daily --day 2026-08-19
guessnova play --seed 20260819 --no-save
guessnova reverse
guessnova stats
guessnova leaderboard
```

### History

```bash
guessnova history --limit 20
guessnova history --result win --difficulty hard
guessnova history --since 2026-08-01 --until 2026-08-31
guessnova history --search daily --group-by mode
guessnova --plain --compact history --group-by result
```

### Profiles and undoable deletion

```bash
guessnova profiles list
guessnova profiles create Nova
guessnova profiles use Nova
guessnova profiles rename Nova Explorer
guessnova profiles delete Explorer
guessnova profiles trash
guessnova profiles restore Explorer
```

Profile deletion normally asks you to type the profile name before moving it to recoverable local trash. `--yes` is available for intentional scripted deletion. Recoverable trash is bounded to the most recent 20 deleted profiles.

### Settings and localization

```bash
guessnova settings
guessnova settings --theme mono --reduced-motion --no-smart-hints
guessnova settings --high-contrast
guessnova settings --locale en
guessnova settings --locale hi
guessnova --plain --compact about
```

### Backup, diagnostics, and recovery

```bash
guessnova export ./guessnova-backup.json
guessnova doctor --verify-backup ./guessnova-backup.json
guessnova doctor --json --verify-backup ./guessnova-backup.json
guessnova import ./guessnova-backup.json

guessnova doctor
guessnova doctor --compact
guessnova doctor --json
guessnova doctor --data-dir ./alternate-data
guessnova doctor --repair
guessnova doctor --repair --yes --backup-dir ./guessnova-repair-backups

# Compatibility entry point
guessnova-doctor --help
```

A normal Doctor state run and `--verify-backup` are read-only. Repair requires confirmation unless `--yes` is provided, refuses unreadable/oversized/future-schema/un-normalizable state, and writes an integrity-protected backup before normalization when a rewrite is needed. `--json` emits one versioned JSON document; `--json --repair` requires `--yes` so an interactive prompt cannot corrupt machine-readable output.

Doctor exit codes are stable: `0` success/healthy/valid, `1` repair cancelled, and `2` attention or validation failure. See [`docs/doctor.md`](docs/doctor.md).

### Textual workspace

```bash
guessnova-tui
```

Workspace keyboard map:

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

The TUI uses the same local `Storage`, `GameService`, diagnostics, and backup-preflight logic as CLI/Doctor workflows. Profile deletion remains recoverable and requires exact-name confirmation. Changing the active profile resets an unfinished round so the result cannot be silently reassigned. The Recovery pane can inspect state and verify a backup but does not repair or import it.

Locale settings are persisted per profile; the mounted TUI keeps one display language for its current process and fully applies a changed locale on the next launch. Smart-hint and high-contrast settings apply immediately.

See [`docs/tui_workspace.md`](docs/tui_workspace.md).

For deterministic non-daily CLI play you may also set:

```bash
GUESSNOVA_SEED=20260819 guessnova play --no-save
```

## Data, privacy, and security

GuessNova's Python interfaces store data only in a local application-data directory; set `GUESSNOVA_HOME` to choose a custom location. Saves use schema-2 normalized JSON and atomic replacement. Local state reads/writes are bounded; backup reads are separately bounded. Backup wrapper v2 records the embedded source schema and verifies a canonical SHA-256 payload digest before import. Legacy version-1 GuessNova backups remain readable when their state schema is supported. Doctor/TUI backup verification additionally proves the embedded state can pass current normalization before reporting the backup as valid. Recoverable profile trash is bounded, and replay text is length-bounded, checksum checked, field-allowlisted, and range validated before use.

The PWA uses only origin-scoped browser storage for local game statistics and recent history. It does not create an account or silently bridge browser data into the Python data directory. Neither interface requires an API key, telemetry endpoint, cloud service, remote leaderboard, or application network connection for gameplay.

Read [`PRIVACY.md`](PRIVACY.md), [`SECURITY.md`](SECURITY.md), [`docs/data_format.md`](docs/data_format.md), [`docs/doctor.md`](docs/doctor.md), [`docs/platforms.md`](docs/platforms.md), and [`docs/tui_workspace.md`](docs/tui_workspace.md).

## Development and testing

```bash
python -m pip install -e '.[dev]'
ruff check .
ruff format --check .
mypy src/guessnova
pytest --cov=guessnova --cov-report=term-missing
node --test tests/web/*.test.mjs
node --check src/guessnova/web/app.js
node --check src/guessnova/web/game-engine.mjs
node --check src/guessnova/web/sw.js
python -m compileall -q src tests scripts
python scripts/verify_release_metadata.py
python scripts/smoke_test.py
python -m guessnova --help
python -m guessnova doctor --help
python -m guessnova web --help
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
python -m build
```

The repository CI runs linting, formatting, strict typing, Python tests, browser-engine tests, JavaScript syntax validation, migration fixtures, backup-integrity/importability regressions, bounded state-I/O regressions, Doctor/repair protocol regressions, reusable TUI-workspace helper tests, focused Textual pilot suites, coverage reporting, bytecode compilation, release-metadata verification, smoke testing, cross-platform package build/install/Twine validation, built-wheel Textual-workspace import, Doctor entry-path checks, PWA asset/entry-point checks, dependency auditing, secret-material checks, and CodeQL analysis. Replay/import boundaries retain deterministic malformed-input/fuzz-style regression coverage. See [`docs/development.md`](docs/development.md) and [`docs/testing.md`](docs/testing.md).

## Architecture

GuessNova is a modular monolith with a UI-independent Python game core plus a small standards-based browser engine that mirrors portable game rules and carries fixed parity tests:

```text
                           Top-level command dispatcher
                         /            |              \
                Rich game CLI     Doctor CLI     Local PWA server
                         \            |              /
                            application services
                           /                    \
                      domain/core          local adapters
                  (Python game engine)  (storage/replay/backup/diagnostics)
                         |
                  Textual workspace

Browser / mobile / ChromeOS
          |
   responsive PWA
          |
 portable JS game engine
          |
 parity vectors (difficulty + daily-v2 rules)
```

The dispatcher routes command families without duplicating Python recovery/storage logic. The Python core engine has no Rich/Textual or filesystem dependency, making seeded gameplay deterministic and directly testable. `tui_workspace.py` keeps workspace query/configuration logic independent from Textual widgets, while `tui.py` owns composition/focus/events. State migration, backup integrity, diagnostics, and repair remain local adapter/application concerns rather than game-rule concerns.

The PWA intentionally remains sandboxed from Python persistence and implements lightweight browser-local statistics/history. Cross-platform rules that must agree across languages—difficulty definitions and daily-v2 target vectors—are covered by both Python and Node tests. See [`docs/architecture.md`](docs/architecture.md), [`docs/platforms.md`](docs/platforms.md), [`docs/localization.md`](docs/localization.md), and [`docs/adr/`](docs/adr/).

## Build and release

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Semantic tags are handled by a quality-gated GitHub release workflow. The tag must match the package version, and release artifacts are blocked until strict verification and Windows/macOS/Linux package checks succeed. Built wheels must expose the game CLI, import the Textual workspace, expose the `guessnova doctor` route, retain the standalone Doctor compatibility entry point, expose both web entry paths, and contain the bundled PWA assets. Release candidates additionally require documented manual accessibility evidence covering all six TUI panes. Real screenshot/demo media must be captured from the exact signed-off build rather than fabricated by automation.

See [`docs/release.md`](docs/release.md), [`docs/accessibility_evidence_template.md`](docs/accessibility_evidence_template.md), [`docs/media/README.md`](docs/media/README.md), and [`CHANGELOG.md`](CHANGELOG.md).

## Documentation

- [Setup](docs/setup.md)
- [Cross-platform support](docs/platforms.md)
- [Development](docs/development.md)
- [Architecture](docs/architecture.md)
- [Game modes](docs/game_modes.md)
- [Textual workspace](docs/tui_workspace.md)
- [Data format](docs/data_format.md)
- [Doctor diagnostics and recovery](docs/doctor.md)
- [v1.2 reliability plan](docs/v1_2_reliability_plan.md)
- [Localization](docs/localization.md)
- [Accessibility](docs/accessibility.md)
- [Accessibility evidence template](docs/accessibility_evidence_template.md)
- [Testing](docs/testing.md)
- [Performance](docs/performance.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Release process](docs/release.md)
- [Release media](docs/media/README.md)
- [GitHub repository operations](docs/github_repository.md)
- [Architecture decisions](docs/adr/)
- [Branding](docs/BRANDING.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Work continuity](what_changed.md)

## Contributing

Issues and pull requests are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) first. Security vulnerabilities should follow the private reporting guidance in [`SECURITY.md`](SECURITY.md) rather than being published as exploit details in a normal issue.

## License

GuessNova is open source under the [MIT License](LICENSE).

## Contact and support

- Business: **sanskarin@outlook.in**
- Business: **sanskarin.business@gmail.com**
- Support: **supportramsandesh@gmail.com**
- GitHub: **https://github.com/sanskarIN**
- Repository: **https://github.com/sanskarIN/guessnova**

## Support the project

<a href="https://buymeacoffee.com/sanskarIN"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-@sanskarIN-FFDD00?logo=buymeacoffee&logoColor=000000" alt="Buy Me a Coffee @sanskarIN"></a>

Support is optional; every GuessNova feature remains fully usable without donating.

**Made by the Sanskar**