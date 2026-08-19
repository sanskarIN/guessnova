# GuessNova Doctor

GuessNova Doctor is a local-only diagnostics and recovery interface for inspecting application state and validating backup files without requiring an account, API key, telemetry service, or network connection.

Two equivalent entry paths are shipped:

```bash
guessnova doctor --help
guessnova-doctor --help
```

The standalone `guessnova-doctor` command remains available for backward compatibility. The primary `guessnova doctor` route is the recommended discoverable form for new documentation and support workflows.

## State diagnostics

Inspect the default local data directory:

```bash
guessnova doctor
```

Inspect a specific data directory without changing `GUESSNOVA_HOME`:

```bash
guessnova doctor --data-dir ./example-data
```

Machine-readable output:

```bash
guessnova doctor --json
guessnova doctor --json --data-dir ./example-data
```

Compact human-readable output:

```bash
guessnova --compact doctor
guessnova-doctor --compact
```

Color-free output:

```bash
guessnova --plain doctor
guessnova-doctor --plain
```

State diagnostics report whether the file exists, whether it can be safely decoded and normalized, source/current schema versions, active profile, profile/history/leaderboard/trash counts, whether normalization would change stored data, and any issues requiring attention.

## Bounded input safety

Local state reads are capped by `MAX_STATE_BYTES`. Backup reads are independently capped by `MAX_EXPORT_BYTES`.

The readers consume at most the configured bound plus one byte before rejecting oversized input. This prevents a malformed or unexpectedly large local JSON file from being loaded without a size guard.

Normal state saves are also size checked after normalization and before the atomic replacement write.

## Safe repair

A repair is explicit:

```bash
guessnova doctor --repair
```

Interactive repair requires typing `REPAIR` exactly. For deliberate non-interactive use:

```bash
guessnova doctor --repair --yes
```

Choose where the pre-repair backup is written:

```bash
guessnova doctor --repair --yes --backup-dir ./recovery-backups
```

Repair behavior is deliberately conservative:

1. Diagnose the current state.
2. Refuse invalid UTF-8/JSON, non-object state, unsupported future schemas, oversized state, or any state that cannot be safely normalized.
3. Re-read the source through the same bounded state reader.
4. Normalize the state in memory.
5. If no rewrite is needed, return without creating a redundant backup.
6. If a rewrite is needed, create a GuessNova backup of the original payload first.
7. Only after the backup succeeds, atomically write normalized state.

A repair backup uses the current backup wrapper and records the source state schema version. It is integrity protected when written with backup wrapper version 2.

Repair is normalization and migration, not forensic reconstruction. Doctor does not guess missing data, decrypt files, bypass future-schema safety, or silently replace undecodable state.

## Backup verification

Validate a backup without importing it:

```bash
guessnova doctor --verify-backup ./guessnova-backup.json
guessnova doctor --json --verify-backup ./guessnova-backup.json
```

Verification checks:

- GuessNova wrapper marker;
- supported backup-wrapper version;
- bounded file size;
- UTF-8 and JSON validity;
- object payload;
- supported source schema;
- wrapper/payload schema agreement for backup v2;
- SHA-256 payload integrity for backup v2;
- current state normalization/importability;
- normalized schema version;
- normalized profile/leaderboard/deleted-profile counts.

A checksum-valid envelope is **not** reported as a valid restorable backup if its payload cannot pass current state normalization.

Legacy wrapper-v1 backups remain inspectable/importable when their state schema is supported. They are reported with `legacy_wrapper=true` and `integrity_protected=false` because legacy wrappers did not contain the v2 integrity field.

`--verify-backup` is read-only and cannot be combined with `--repair`, `--yes`, `--backup-dir`, or `--data-dir`.

## Machine JSON protocol

Doctor JSON documents contain:

```json
{
  "report_version": 1,
  "kind": "state"
}
```

The current `report_version` is `1`.

Possible `kind` values:

- `state` — local-state diagnostic result;
- `backup` — validated backup inspection result;
- `error` — command/validation failure represented as JSON.

State results include `healthy`. Backup results include `valid`. Error results include `healthy: false` plus an `error` message.

Additive fields may be introduced within a report version when they do not change existing field meaning. A future incompatible machine-contract change must increment the report version rather than silently redefining existing fields.

`--json --repair` requires `--yes`; Doctor will not print an interactive prompt into machine-readable output.

## Exit codes

Doctor uses stable exit semantics:

- `0` — healthy state, valid backup, or successful/no-op repair;
- `1` — interactive repair was cancelled;
- `2` — attention required, validation error, unsafe repair request, unreadable state, or invalid backup.

These values are defined in `src/guessnova/doctor_protocol.py` and shared by both entry paths.

## Privacy

Doctor operates only on paths selected by local GuessNova configuration or explicit command arguments. It performs no runtime network request and sends no diagnostic data anywhere.

JSON/text reports contain structural state information such as counts and profile name. Treat output as local diagnostic data if profile names are personally meaningful. Backup inspection does not print the backup payload itself.

## Integrity versus authenticity

Backup v2 SHA-256 detects accidental or unauthorized content changes relative to the digest stored inside the same file. It is not a digital signature, secret-key MAC, encryption mechanism, publisher identity proof, or authenticity guarantee.

Do not describe a valid backup checksum as proof that a file came from a trusted person.

## Support workflow

For a state problem, prefer this order:

1. Run `guessnova doctor --json` and keep the output locally.
2. If the state is readable but normalization is required, create an ordinary export if possible.
3. Run repair only when the report indicates a supported migration/normalization path.
4. Preserve the generated pre-repair backup until the repaired state is confirmed.
5. For a backup problem, run `guessnova doctor --json --verify-backup PATH` before importing it.
6. Share only non-sensitive diagnostic details when opening a public issue.

See also:

- [`data_format.md`](data_format.md)
- [`troubleshooting.md`](troubleshooting.md)
- [`testing.md`](testing.md)
- [`release.md`](release.md)
- [`../PRIVACY.md`](../PRIVACY.md)
- [`../SECURITY.md`](../SECURITY.md)
