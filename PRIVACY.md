# Privacy Policy

GuessNova is designed to work without an account and without sending gameplay data to a server.

## Data stored locally

The application may save profile names, settings, gameplay statistics, achievements, XP, streak values, bounded session history, leaderboard entries, and recoverable deleted-profile records in `state.json` under the local GuessNova data directory.

The Rich CLI, Textual workspace, and Doctor all operate on the same local state model. The Textual workspace does not create a second database or hidden cache of profile/history/leaderboard information.

## Network behavior

The installed Python application does not require network access for gameplay, the Textual workspace, diagnostics, backup verification, repair, backup import/export, or local profile management. It contains no telemetry, analytics, advertising, cloud-sync, remote leaderboard, or remote-account code.

GitHub Actions, repository pages, package registries, or other development/distribution services are separate from the installed GuessNova runtime and have their own policies when a developer chooses to use them.

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

Doctor reads local GuessNova state and reports schema/normalization status plus aggregate counts. It does not upload state, contact a server, or enable telemetry. JSON diagnostic output can include the active local profile name, selected paths, and local counts; scripts that capture, transmit, or publish that output are outside GuessNova's control.

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

Deleting the entire GuessNova local data directory removes both live and recoverable application state from that directory.

## Settings and locale

The TUI Settings pane edits the same local per-profile settings as the CLI. A locale change is saved locally; the running TUI keeps its launch language until restart so the mounted interface does not become partially translated.

No setting is synchronized to a server.

## Complete local deletion

Users can delete their local GuessNova data directory at any time to remove saved application data, including profile trash. User-created export files and pre-repair backups are separate files and must also be deleted wherever the user chose to save or copy them.

If Doctor reports, terminal logs, screenshots, or screen recordings were deliberately saved elsewhere, those copies are separate files and should also be removed if the user wants to delete them.
