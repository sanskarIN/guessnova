# Local Data Format

This is the concise data-format reference. The canonical detailed specification is [`data_format.md`](data_format.md).

GuessNova stores a normalized JSON state file with schema version `2`. Current state contains:

- `active_profile` — the current local profile name.
- `profiles` — live profile records with stats, settings, bounded history, locale, and onboarding preference.
- `leaderboard` — validated local winning-result rows.
- `deleted_profiles` — up to 20 recoverable deleted profiles plus retained leaderboard rows.
- `schema_version` — currently `2`.

State schema, backup-wrapper version, replay version, and Doctor report version are separate compatibility domains.

## Migration

Schema 0 advances through schema 1. Schema 1 then advances to schema 2 by making `deleted_profiles` a canonical top-level field while preserving an existing trash container when present. Migration fixtures are committed under `tests/fixtures/state/`. Future schemas are rejected instead of silently downgraded.

GuessNova 1.3 keeps state schema 2; schema 3 is not invented without a concrete compatibility boundary.

## Bounded atomic state I/O

State reads are capped by `MAX_STATE_BYTES` and read at most the limit plus one byte before UTF-8/JSON decoding. State saves normalize and serialize first, reject oversized output, then use a temporary file, flush/`fsync`, and atomic replacement where supported.

## Profile trash

`guessnova profiles delete NAME` moves a live profile and its local leaderboard entries into bounded recoverable trash. `guessnova profiles restore NAME` restores them unless a live profile with that name already exists. Deleting the entire application-data directory removes both live and recoverable state from that directory.

## Backup format

Backup wrapper version `2` is independent from state schema version. It records:

- `format: guessnova-export`;
- backup wrapper `version: 2`;
- the embedded payload's `schema_version`;
- SHA-256 payload integrity metadata;
- the complete local state payload.

Backup validation uses one bounded read represented internally as `ValidatedExport`. Imports verify wrapper/payload schema consistency and payload integrity. Legacy version-1 GuessNova backups remain readable when their embedded state schema is supported.

`MAX_EXPORT_BYTES` is intentionally greater than `MAX_STATE_BYTES`, preserving the invariant that any accepted repairable state can fit inside the required pre-repair backup wrapper.

## Backup preflight

```bash
guessnova doctor --verify-backup PATH
```

This is read-only. It validates the backup envelope and then proves the embedded state can pass current `normalize_state(...)` before reporting the backup as valid. Reports include source/normalized schema versions, legacy/integrity status, normalization-change status, normalized state counts, and validated file size.

A checksum-valid but structurally unimportable payload is rejected.

## Diagnostics and repair

Recommended route:

```bash
guessnova doctor
```

Compatibility route:

```bash
guessnova-doctor
```

Doctor can inspect an explicit `--data-dir`, emit compact/JSON output, verify backups without importing them, and repair supported state after creating a pre-repair backup. Unreadable, oversized, future-schema, non-object, or otherwise unnormalizable state is not overwritten automatically.

Doctor JSON report version is currently `1`; document kinds are `state`, `backup`, and `error`. Exit codes are `0` success/healthy/valid, `1` cancelled repair, and `2` attention/validation failure.

See [`doctor.md`](doctor.md) for the full contract.

Replay-code validation is separate from state/export/Doctor validation; see [`data_format.md`](data_format.md) for replay limits and compatibility details.
