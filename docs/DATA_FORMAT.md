# Local Data Format

This is the concise data-format reference. The canonical detailed specification is [`data_format.md`](data_format.md).

GuessNova stores a normalized JSON state file with schema version `1`. Current state can contain:

- `active_profile` — the current local profile name.
- `profiles` — live profile records with stats, settings, bounded history, locale, and onboarding preference.
- `leaderboard` — validated local winning-result rows.
- `deleted_profiles` — up to 20 recoverable deleted profiles plus their retained leaderboard rows.
- `schema_version` — currently `1`.

## Atomic writes

State is normalized, written to a temporary file in the same directory, flushed and synced, then replaced atomically where supported by the host filesystem.

## Additive compatibility

Fields introduced after the initial schema-1 release—including history, locale, onboarding state, and recoverable profile trash—have safe defaults and do not require a fabricated schema migration. A file created by a future schema version is rejected instead of silently downgraded.

## Profile trash

`guessnova profiles delete NAME` moves a live profile and its local leaderboard entries into bounded recoverable trash. `guessnova profiles restore NAME` restores them unless a live profile with that name already exists. Deleting the entire application-data directory removes both live and recoverable state from that directory.

## Export format

Exports wrap the complete state with `format: guessnova-export` and a version field. Imports validate the wrapper, then normalized state validation runs again before persistence.

Replay-code validation is separate from state/export validation; see [`data_format.md`](data_format.md) for replay limits and compatibility details.
