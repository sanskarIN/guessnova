# Privacy Policy

GuessNova is designed to work without an account and without sending gameplay data to an application backend.

## Data stored locally

The Python application may save profile names, settings, gameplay statistics, achievements, XP, streak values, bounded session history, leaderboard entries, and recoverable deleted-profile records in `state.json` under the local GuessNova data directory.

The Rich CLI, Textual workspace, and Doctor all operate on the same local state model. The Textual workspace does not create a second database or hidden cache of profile/history/leaderboard information.

The browser/PWA interface uses origin-scoped browser storage for lightweight statistics, current/best streak values, recent-round history, and the last selected mode/difficulty. It does not silently read or write the Python `state.json` data directory.

## Network behavior

The installed Python CLI, Textual workspace, and Doctor do not require network access for gameplay, diagnostics, backup verification, repair, backup import/export, or local profile management. They contain no telemetry, analytics, advertising, cloud-sync, remote leaderboard, or remote-account code.

`guessnova web` / `guessnova-web` starts a local static-file server that binds to `127.0.0.1` by default. The bundled PWA can also be deployed to a normal HTTPS static host. When hosted remotely, a browser necessarily requests the application files from that chosen host and the service worker may fetch/cache same-origin application assets. GuessNova still does not send gameplay history, guesses, statistics, profile data, or analytics to an application backend.

A hosting provider, browser vendor, operating-system service, DNS provider, reverse proxy, CDN, or network administrator may independently observe ordinary web-request metadata according to its own policies. That transport metadata is outside GuessNova's local gameplay-storage model.

GitHub Actions, repository pages, package registries, or other development/distribution services are separate from the installed GuessNova runtime and have their own policies when a developer chooses to use them.

## Browser/PWA interface

The PWA is designed for Android, iOS/iPadOS, ChromeOS, and modern desktop/mobile browsers. It can be installed where the browser exposes PWA/home-screen installation support and can use its cached app shell offline after a successful load/install.

Browser-local data can include:

- games played/won;
- current and best streak;
- recent round mode, difficulty, result, attempts, target, and completion timestamp;
- the most recently selected mode and difficulty.

This information is stored under the web origin controlled by the browser. Clearing that site's storage or using **Reset local data** removes GuessNova's browser-local state for that origin. Browser backup/sync features, if enabled by the user or operating system, are controlled by those platforms rather than GuessNova.

The current PWA does not synchronize browser-local state with Python profiles, Doctor, backups, or the Textual workspace.

## Textual workspace

`guessnova-tui` presents local data in six panes: Play, Profiles, History, Leaderboard, Settings, and Recovery.

The workspace may visibly display:

- active/local profile names;
- gameplay statistics and achievements;
- bounded session-history timestamps/results;
- local leaderboard player names/results;
- saved settings;
- local data-directory path;
- schema/count information;
- a user-selected backup path;
- backup structural metadata.

This information remains on the local terminal unless the user or another local tool captures/shares it. Screenshots, screen recordings, terminal transcripts, copied diagnostics, and support reports can therefore contain personally meaningful local information even though GuessNova itself does not transmit it.

Review captures before sharing them publicly.

## TUI Recovery

The Textual Recovery pane is intentionally read-only.

It can:

- run local state diagnostics;
- display aggregate local counts/schema information;
- verify a user-selected backup through the same read-only backup-preflight boundary used by Doctor.

It does not:

- repair state;
- import a verified backup;
- delete state;
- upload state/backups/reports.

Explicit repair remains in Doctor so confirmation and pre-repair backup behavior stay centralized.

## Backups

The export command creates a local JSON backup chosen by the user. Backup wrapper v2 records the embedded state schema and SHA-256 payload integrity metadata. Import reads only the selected local file and validates the GuessNova wrapper, supported schema, wrapper/payload schema agreement, and payload integrity before normalized state is persisted.

Legacy GuessNova version-1 backup wrappers remain readable when their embedded state schema is supported.

A backup can include live profiles, leaderboard rows, session history, settings, and recoverable deleted-profile records. Treat exported backups as personal local data if profile names or gameplay history are personally meaningful.

The browser/PWA's lightweight localStorage state is not automatically included in Python backup files.

## Read-only backup verification

CLI/Doctor route:

```bash
guessnova doctor --verify-backup PATH
```

The TUI Recovery pane exposes the same preflight boundary through a local backup-path field.

Backup preflight reads the selected backup locally, validates wrapper/integrity rules, and passes the embedded state through current normalization in memory. It does not import or rewrite application state.

The resulting report contains structural metadata such as file path, file size, wrapper/schema versions, integrity status, normalization-change status, and normalized counts. It does not print the backup payload itself. The path and counts can still be sensitive in some environments, so review Doctor/TUI output before publishing it.

## Local diagnostics

Recommended route:

```bash
guessnova doctor
```

Compatibility route:

```bash
guessnova-doctor
```

Doctor reads local GuessNova state and reports schema/normalization status plus aggregate counts. It does not upload state, contact an application server, or enable telemetry. JSON diagnostic output can include the active local profile name, selected paths, and local counts; scripts that capture, transmit, or publish that output are outside GuessNova's control.

`--data-dir PATH` selects a local directory explicitly and does not send that path anywhere.

## Repair backups

`guessnova doctor --repair` is intentionally conservative. It refuses state it cannot safely decode/normalize. When a repairable state file needs rewriting, GuessNova first creates an integrity-protected backup containing the original payload, then writes normalized state.

Pre-repair backups may contain the same personal local data as ordinary exports. They are not automatically deleted because they are the user's recovery copy. Use `--backup-dir` to choose their location, and delete them manually when no longer needed.

JSON repair requires `--yes` so an interactive prompt cannot be mixed into machine-readable output. This changes scripting behavior only; it does not send data anywhere.

## Profile deletion and recovery

CLI profile deletion is intentionally recoverable. The Textual Profiles pane uses the same recoverable trash model and additionally requires the selected profile name to be typed exactly before Delete succeeds.

The deleted profile and associated local leaderboard rows are moved into bounded local profile trash rather than immediately destroyed. Up to the most recent 20 deleted profiles can be retained for undo.

Use either:

```bash
guessnova profiles trash
guessnova profiles restore NAME
```

or the TUI Profiles trash/Restore controls to view/undo local deletion.

Deleting the entire GuessNova local data directory removes both live and recoverable Python application state from that directory. It does not clear browser-origin storage; clear the site data separately when using the PWA.

## Settings and locale

The TUI Settings pane edits the same local per-profile settings as the CLI. A locale change is saved locally; the running TUI keeps its launch language until restart so the mounted interface does not become partially translated.

No Python profile setting is synchronized to a server. The PWA currently maintains its own lightweight browser-local mode/difficulty preference rather than sharing the Python profile settings model.

## Complete local deletion

Users can delete their local GuessNova data directory at any time to remove saved Python application data, including profile trash. User-created export files and pre-repair backups are separate files and must also be deleted wherever the user chose to save or copy them.

For the PWA, clear the GuessNova site's browser storage (or use **Reset local data**) for each origin on which it was used. An installed PWA may also need to be uninstalled separately from the browser/operating system.

If Doctor reports, terminal logs, screenshots, browser exports/captures, or screen recordings were deliberately saved elsewhere, those copies are separate files and should also be removed if the user wants to delete them.
