# Data Format

GuessNova stores local data as JSON through `Storage`. The current state schema is defined by `SCHEMA_VERSION` in `src/guessnova/constants.py` and is currently **2**.

State schema, backup-wrapper version, replay version, and Doctor report version are separate compatibility domains. A change in one does not automatically require a version change in the others.

## Local state

Typical shape:

```json
{
  "schema_version": 2,
  "active_profile": "Player",
  "profiles": {
    "Player": {
      "name": "Player",
      "stats": {
        "games_played": 0,
        "games_won": 0,
        "current_streak": 0,
        "best_streak": 0,
        "total_guesses": 0,
        "xp": 0,
        "achievements": []
      },
      "settings": {
        "theme": "nebula",
        "locale": "en",
        "reduced_motion": false,
        "high_contrast": false,
        "sound": false,
        "show_smart_hints": true,
        "onboarding_complete": false
      },
      "history": []
    }
  },
  "leaderboard": [],
  "deleted_profiles": {}
}
```

History is bounded to the most recent 200 entries per profile. Recoverable profile trash is bounded to the most recent 20 deleted profiles. The exact state location is platform dependent and can be overridden with `GUESSNOVA_HOME`.

## State byte boundary

`MAX_STATE_BYTES` limits local state input and output size.

State reads open the file in binary mode and read at most `MAX_STATE_BYTES + 1`. If the extra byte exists, the file is rejected before UTF-8 decoding or JSON parsing.

State writes:

1. normalize the payload;
2. serialize normalized JSON;
3. reject output larger than `MAX_STATE_BYTES`;
4. write a temporary file in the destination directory;
5. flush and `fsync` it;
6. atomically replace `state.json` where supported by the host filesystem.

This is a transport/resource bound, not a new state schema field.

## Schema 2

Schema 2 formally makes `deleted_profiles` a canonical top-level state container. GuessNova 1.1 already wrote this field additively while still identifying the state as schema 1, so the schema-1-to-schema-2 migration is intentionally idempotent:

1. schema 0 receives baseline `profiles` and `active_profile`, then advances to schema 1;
2. schema 1 receives `deleted_profiles: {}` only when missing, then advances to schema 2;
3. schema 2 is normalized and persisted as the current format;
4. future schemas are rejected rather than silently downgraded.

Committed migration fixtures live under `tests/fixtures/state/` and cover both a legacy schema-1 save without trash and a schema-1 save that already contains recoverable trash.

GuessNova 1.3 deliberately keeps state schema 2. No schema-3 migration is created without a concrete incompatible/canonical format boundary.

## Profile deletion and restore

`guessnova profiles delete NAME` removes the profile from the live profile map and removes matching local leaderboard rows, but stores both inside `deleted_profiles` for recovery. `guessnova profiles restore NAME` restores the profile and retained leaderboard rows. Trash is local, exported with normal backups, validated on load, and bounded.

Creating a new live profile with the same name as a deleted profile is allowed, but restoring the deleted profile fails safely until the live-name collision is resolved.

## Normalization and forward safety

Every load/save passes through state normalization. The normalizer validates or repairs supported data including profile names, statistics, settings, history, leaderboard rows, deleted-profile records, active-profile references, and top-level structure. Unknown top-level fields are dropped. Invalid profiles containers and future schemas are rejected.

Doctor and repair use the same bounded state reader and the same normalization function as normal storage rather than maintaining a separate recovery interpretation of the file.

## Backup wrapper v2

The backup wrapper has its **own format version**, independent of the local state schema version. This avoids coupling backup compatibility to every future state migration.

`guessnova export` writes a wrapper like:

```json
{
  "format": "guessnova-export",
  "version": 2,
  "schema_version": 2,
  "integrity": {
    "algorithm": "sha256",
    "payload_sha256": "<64 lowercase hex characters>"
  },
  "payload": {"schema_version": 2}
}
```

The digest is calculated from canonical UTF-8 JSON for the payload using sorted keys and compact separators. Import compares the expected and supplied digest with constant-time comparison.

The wrapper's `schema_version` records the embedded payload's actual schema version. For example, a pre-repair backup created by Doctor can be a version-2 backup wrapper containing a schema-1 payload. The wrapper schema metadata and embedded payload schema must match.

### Bounded single-read validation

Backup files are read through a single bounded binary read of at most `MAX_EXPORT_BYTES + 1` before decoding. The validated envelope is represented internally by `ValidatedExport`, which carries:

- path;
- byte size from that validated read;
- backup-wrapper version;
- embedded source schema version;
- integrity-protection status/algorithm;
- the validated payload from that same read.

Backup inspection consumes this validated object instead of validating one read and then re-reading the path for metadata.

`MAX_EXPORT_BYTES` is intentionally larger than `MAX_STATE_BYTES` so any accepted state that requires repair can be represented inside its mandatory pre-repair backup wrapper.

### Legacy backup compatibility

GuessNova 1.0/1.1 used backup wrapper version 1 and coupled that wrapper version to the then-current state schema. Version-1 backup wrappers remain importable and inspectable when their embedded payload schema is supported. The payload is migrated only when normalized/persisted through current storage.

Legacy wrappers are reported by Doctor as not integrity protected because the v1 wrapper did not include backup-v2 SHA-256 metadata.

### Backup validation

Envelope validation rejects:

- an invalid GuessNova format marker;
- invalid/non-integer wrapper versions;
- unsupported old wrapper versions;
- future wrapper versions;
- invalid/future schema versions;
- wrapper/payload schema metadata mismatches;
- missing or unsupported integrity metadata in wrapper v2;
- invalid integrity digest length/type;
- payload tampering that changes the digest;
- invalid JSON or non-object payloads;
- oversized files.

Backup integrity protects against accidental modification/corruption. SHA-256 here is not a secret-key signature, encryption, origin authentication, or proof that a backup came from a trusted person.

## Backup preflight/importability

`guessnova doctor --verify-backup PATH` is read-only. After envelope validation, it passes the embedded state through current `normalize_state(...)` in memory. A checksum-valid envelope is not reported as a valid restorable backup if the payload cannot be normalized by the current application.

The backup report includes:

- source backup-wrapper version;
- source state schema version;
- normalized/current state schema version;
- legacy-wrapper status;
- integrity-protection status/algorithm;
- whether normalization changes the payload;
- normalized profile count;
- normalized leaderboard count;
- normalized deleted-profile count;
- validated file size.

No state write occurs during backup verification.

## Doctor and safe repair

Recommended entry point:

```bash
guessnova doctor
```

Compatibility entry point:

```bash
guessnova-doctor
```

Doctor reports source/current schema, active profile, profile/history/leaderboard/trash counts, normalization changes, and detected migration/normalization issues.

`guessnova doctor --repair` requires confirmation (or `--yes`) and refuses state it cannot safely decode/normalize. Before rewriting repairable state it writes an integrity-protected backup of the original payload. Use `--backup-dir PATH` to place that backup elsewhere.

`--data-dir PATH` targets a specific local GuessNova data directory without changing the process environment.

See [`doctor.md`](doctor.md) for complete behavior and recovery guidance.

## Doctor JSON protocol

Doctor machine output has a separate report version. Current report version is `1`.

State example:

```json
{
  "report_version": 1,
  "kind": "state",
  "healthy": true,
  "state_exists": true,
  "readable": true,
  "source_schema_version": 2,
  "current_schema_version": 2,
  "normalization_changed": false,
  "issues": []
}
```

Backup documents use `kind: "backup"` and error documents use `kind: "error"`. Stable serialized keys are not localized.

## Replay codes

Replay codes retain replay version 1. They contain a compact JSON `GameSummary`, replay version, and truncated SHA-256 integrity digest, then use URL-safe Base64 encoding. GuessNova 1.3 does not change replay compatibility or guessing rules.

The replay parser enforces a maximum encoded length, valid URL-safe Base64, envelope/checksum structure, supported version, an allowlist of fields, difficulty/range constraints, attempt/guess consistency, finite non-negative elapsed time, signed 64-bit portable seeds, and bounded hint metadata.

## Localization identifiers

The locale is a presentation preference only. Stable serialized identifiers—mode names, difficulty names, schema keys, achievement IDs, replay field names, backup format markers, Doctor report kinds, and diagnostic JSON keys—are not translated.

## Privacy

Player names, statistics, settings, bounded history, recoverable profile trash, leaderboard data, diagnostics, and repair backups remain local unless the user explicitly exports/shares a file, report, or replay code. GuessNova requires no runtime account, telemetry service, analytics service, or network connection. See `PRIVACY.md`.
