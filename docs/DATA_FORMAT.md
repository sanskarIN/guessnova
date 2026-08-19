# Local Data Format

This is the concise data-format reference. The canonical detailed specification is [`data_format.md`](data_format.md).

GuessNova stores a normalized JSON state file with schema version `2`. Current state contains:

- `active_profile` — the current local profile name.
- `profiles` — live profile records with stats, settings, bounded history, locale, and onboarding preference.
- `leaderboard` — validated local winning-result rows.
- `deleted_profiles` — up to 20 recoverable deleted profiles plus retained leaderboard rows.
- `schema_version` — currently `2`.

## Migration

Schema 0 advances through schema 1. Schema 1 then advances to schema 2 by making `deleted_profiles` a canonical top-level field while preserving an existing trash container when present. Migration fixtures are committed under `tests/fixtures/state/`. Future schemas are rejected instead of silently downgraded.

## Atomic writes

State is normalized, written to a temporary file in the same directory, flushed and synced, then replaced atomically where supported by the host filesystem.

## Profile trash

`guessnova profiles delete NAME` moves a live profile and its local leaderboard entries into bounded recoverable trash. `guessnova profiles restore NAME` restores them unless a live profile with that name already exists. Deleting the entire application-data directory removes both live and recoverable state from that directory.

## Backup format

Backup wrapper version `2` is independent from state schema version. It records:

- `format: guessnova-export`;
- backup wrapper `version: 2`;
- the embedded payload's `schema_version`;
- SHA-256 payload integrity metadata;
- the complete local state payload.

Imports verify wrapper/payload schema consistency and payload integrity. Legacy version-1 GuessNova backups remain readable when their embedded state schema is supported.

## Diagnostics and repair

`guessnova-doctor` inspects local state without sending it anywhere. `guessnova-doctor --repair` creates an integrity-protected pre-repair backup before writing normalized state. Unreadable/non-object state is not overwritten automatically.

Replay-code validation is separate from state/export validation; see [`data_format.md`](data_format.md) for replay limits and compatibility details.
