# Privacy Policy

GuessNova is designed to work without an account and without sending gameplay data to a server.

## Data stored locally

The application may save profile names, settings, gameplay statistics, achievements, XP, streak values, bounded session history, leaderboard entries, and recoverable deleted-profile records in `state.json` under the local GuessNova data directory.

## Network behavior

The Python application itself does not require network access for gameplay and contains no telemetry, analytics, advertising, or remote-account code.

GitHub Actions, repository pages, package registries, or other development/distribution services are separate from the installed GuessNova runtime and have their own policies when a developer chooses to use them.

## Backups

The export command creates a local JSON backup chosen by the user. Import reads only the selected local file and validates the GuessNova export wrapper and schema version before normalized state is persisted.

A backup can include live profiles, leaderboard rows, session history, settings, and recoverable deleted-profile records. Treat exported backups as personal local data if profile names or gameplay history are personally meaningful.

## Profile deletion and recovery

`guessnova profiles delete NAME` is intentionally recoverable. The deleted profile and its associated local leaderboard rows are moved into bounded local profile trash rather than immediately destroyed. Up to the most recent 20 deleted profiles can be retained for undo through `guessnova profiles restore NAME`.

Use `guessnova profiles trash` to see recoverable profile names. Deleting the entire GuessNova local data directory removes both live and recoverable application state from that directory.

## Complete local deletion

Users can delete their local GuessNova data directory at any time to remove saved application data, including profile trash. User-created export files are separate files and must also be deleted wherever the user chose to save or copy them.
