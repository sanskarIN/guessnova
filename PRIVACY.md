# Privacy Policy

GuessNova is designed to work without an account and without sending gameplay data to a server.

## Data stored locally

The application may save profile names, settings, gameplay statistics, achievements, XP, streak values, bounded session history, leaderboard entries, and recoverable deleted-profile records in `state.json` under the local GuessNova data directory.

## Network behavior

The installed Python application does not require network access for gameplay, diagnostics, repair, backup import/export, or local profile management. It contains no telemetry, analytics, advertising, cloud-sync, or remote-account code.

GitHub Actions, repository pages, package registries, or other development/distribution services are separate from the installed GuessNova runtime and have their own policies when a developer chooses to use them.

## Backups

The export command creates a local JSON backup chosen by the user. Backup wrapper v2 records the embedded state schema and SHA-256 payload integrity metadata. Import reads only the selected local file and validates the GuessNova wrapper, supported schema, wrapper/payload schema agreement, and payload integrity before normalized state is persisted.

Legacy GuessNova version-1 backup wrappers remain readable when their embedded state schema is supported.

A backup can include live profiles, leaderboard rows, session history, settings, and recoverable deleted-profile records. Treat exported backups as personal local data if profile names or gameplay history are personally meaningful.

## Local diagnostics

`guessnova-doctor` reads local GuessNova state and reports schema/normalization status plus aggregate counts. It does not upload state, contact a server, or enable telemetry. JSON diagnostic output can include the active local profile name and local counts; scripts that capture or publish that output are outside GuessNova's control.

## Repair backups

`guessnova-doctor --repair` is intentionally conservative. It refuses state it cannot safely decode/normalize. When a repairable state file needs rewriting, GuessNova first creates an integrity-protected backup containing the original payload, then writes normalized state.

Pre-repair backups may contain the same personal local data as ordinary exports. They are not automatically deleted because they are the user's recovery copy. Use `--backup-dir` to choose their location, and delete them manually when no longer needed.

## Profile deletion and recovery

`guessnova profiles delete NAME` is intentionally recoverable. The deleted profile and its associated local leaderboard rows are moved into bounded local profile trash rather than immediately destroyed. Up to the most recent 20 deleted profiles can be retained for undo through `guessnova profiles restore NAME`.

Use `guessnova profiles trash` to see recoverable profile names. Deleting the entire GuessNova local data directory removes both live and recoverable application state from that directory.

## Complete local deletion

Users can delete their local GuessNova data directory at any time to remove saved application data, including profile trash. User-created export files and pre-repair backups are separate files and must also be deleted wherever the user chose to save or copy them.
