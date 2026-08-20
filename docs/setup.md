# Setup

GuessNova supports two delivery families:

- **Python CLI/TUI** for Windows, macOS, and Linux.
- **Responsive PWA** for Android, iOS/iPadOS, ChromeOS, and modern desktop/mobile browsers.

See [`platforms.md`](platforms.md) for the complete platform matrix.

## Desktop Python requirements

- Python 3.13+
- Git
- Windows 10/11, current macOS, or a modern Linux distribution
- UTF-8 terminal recommended for the richest CLI/TUI presentation

## Windows PowerShell

```powershell
git clone https://github.com/sanskarIN/guessnova.git
cd guessnova
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
guessnova play
guessnova-tui
guessnova doctor --help
guessnova-doctor --help
guessnova web --help
guessnova-web --help
```

## macOS / Linux

```bash
git clone https://github.com/sanskarIN/guessnova.git
cd guessnova
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
guessnova play
guessnova-tui
guessnova doctor --help
guessnova-doctor --help
guessnova web --help
guessnova-web --help
```

## Installed entry points

A normal installation provides:

```text
guessnova          primary CLI dispatcher for gameplay/data, `doctor`, and `web`
guessnova-tui      six-pane Textual local workspace
guessnova-doctor   standalone Doctor compatibility entry point
guessnova-web      standalone local PWA server entry point
```

`python -m guessnova` uses the same top-level dispatcher as the installed `guessnova` script.

## Launch the responsive web/PWA interface locally

After installing the Python package:

```bash
guessnova web
```

or:

```bash
guessnova-web
```

The server defaults to:

```text
http://127.0.0.1:8765/
```

and opens the default browser unless `--no-open` is supplied. Loopback binding is intentional: it does not expose the server to other devices by default.

Options:

```bash
guessnova web --host 127.0.0.1 --port 8765 --no-open
```

For deliberate trusted-LAN development only:

```bash
guessnova web --host 0.0.0.0 --port 8765 --no-open
```

A `0.0.0.0` bind can be reachable from other devices on the network. Do not use the small development server as a public Internet deployment.

## Android, iOS/iPadOS, and ChromeOS

The supported mobile/Chromebook interface is the PWA under:

```text
src/guessnova/web/
```

Deploy that directory to a normal HTTPS static host. The application uses only static HTML/CSS/JavaScript assets, a Web App Manifest, and a service worker; it does not require a GuessNova application backend.

Typical use:

- **Android:** open the HTTPS PWA in a modern browser and use the browser's install/add-to-home-screen action where available.
- **iOS/iPadOS:** open the HTTPS PWA in Safari and use **Add to Home Screen** for an app-like launcher.
- **ChromeOS:** use the browser PWA; the Linux development environment can additionally run the Python CLI/TUI when Python 3.13+ is available.
- **Windows/macOS/Linux browsers:** the same responsive PWA works in addition to the Python interfaces.

Service-worker offline caching and PWA installation require a secure context outside `localhost`, so production/static deployments should use HTTPS.

## PWA storage

The PWA stores lightweight statistics/history and its selected mode/difficulty in browser origin-scoped storage. It does not silently share the Python `state.json` profile/backup model.

Use **Reset local data** inside the PWA or clear the site's browser storage to delete that browser-local progress.

## Textual workspace

Launch:

```bash
guessnova-tui
```

GuessNova starts on Play with the guess input focused. Workspace panes:

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

The workspace provides:

- normal Textual gameplay/hints/result persistence;
- local profile create/use/rename/recoverable-delete/restore;
- active-profile statistics and achievements;
- bounded history filtering;
- local leaderboard filtering;
- local profile settings;
- high-contrast TUI focus/border behavior;
- read-only state diagnostics;
- read-only backup verification.

Changing the active profile resets an unfinished round. This prevents a partially played game from being saved under a different profile.

A locale change is persisted immediately but full TUI relabeling happens on the next launch. This keeps one running interface linguistically consistent.

Recovery repair is intentionally not available as a TUI button. Use Doctor for an explicit repair workflow:

```bash
guessnova doctor --repair
```

See [`tui_workspace.md`](tui_workspace.md) for complete behavior.

## Local Doctor

Recommended state inspection:

```bash
guessnova doctor
guessnova doctor --json
guessnova doctor --data-dir ./alternate-data
```

Compatibility route:

```bash
guessnova-doctor --json
```

Verify a backup before import without writing state:

```bash
guessnova doctor --verify-backup ./guessnova-backup.json
guessnova doctor --json --verify-backup ./guessnova-backup.json
```

The same backup-preflight logic is available read-only from the TUI Recovery pane.

Repairable migration/normalization changes can be applied only after confirmation. GuessNova creates a pre-repair backup before a required rewrite:

```bash
guessnova doctor --repair
guessnova doctor --repair --yes --backup-dir ./repair-backups
```

Do not run `--repair` merely because a state file is old; a normal GuessNova load/save also performs supported forward migration. Doctor is mainly for visibility, scripting, backup preflight, support diagnosis, and explicit normalization/repair workflows.

Doctor refuses oversized, undecodable, non-object, future-schema, or otherwise unnormalizable state. `--json --repair` requires `--yes` so machine output cannot be mixed with an interactive prompt.

See [`doctor.md`](doctor.md) for the full recovery contract.

## Development dependencies

```bash
python -m pip install -e '.[dev]'
ruff check .
ruff format --check .
mypy src/guessnova
pytest
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
python -m guessnova.doctor_cli --help
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
```

Node.js is required only for the browser-engine development/CI checks above, not for users running the bundled PWA.

## Optional environment variables

- `GUESSNOVA_HOME` — override the default local application-data directory for normal Python commands and TUI state.
- `GUESSNOVA_SEED` — default deterministic seed for CLI challenges.

Doctor `--data-dir PATH` can inspect a specific GuessNova data directory without modifying `GUESSNOVA_HOME`.

GuessNova does not require API keys, accounts, telemetry credentials, or a gameplay backend. A remotely hosted PWA naturally downloads its static application assets from the host selected by the deployer.
