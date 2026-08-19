# GuessNova Doctor — Concise Reference

Canonical guide: [`doctor.md`](doctor.md).

Use either entry path:

```bash
guessnova doctor
guessnova-doctor
```

Common commands:

```bash
guessnova doctor --json
guessnova doctor --data-dir ./data
guessnova doctor --repair
guessnova doctor --repair --yes --backup-dir ./backups
guessnova doctor --verify-backup ./guessnova-backup.json
guessnova doctor --json --verify-backup ./guessnova-backup.json
```

Doctor is local-only and does not require network access.

## Guarantees

- State and backup input reads are byte bounded.
- State normalization is performed before a repair write.
- Repair refuses undecodable, oversized, future-schema, or otherwise unnormalizable state.
- A repair backup is created before any required rewrite.
- Backup verification checks wrapper compatibility, v2 integrity, schema metadata, and payload importability.
- Legacy backup-v1 files remain supported when their state schema is supported.
- Backup verification is read-only.

## JSON protocol

Current `report_version`: `1`.

Kinds:

- `state`
- `backup`
- `error`

Exit codes:

- `0` success / healthy / valid;
- `1` repair cancelled;
- `2` attention or validation failure.

For scripting, use `--json`. A JSON repair requires `--yes` so an interactive prompt can never corrupt machine-readable output.

A backup SHA-256 digest is an integrity check, not authentication, encryption, signing, or proof of origin.
