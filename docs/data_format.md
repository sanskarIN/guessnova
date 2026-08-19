# Data Format

GuessNova stores local data as JSON through `Storage`. The current state schema is defined by `SCHEMA_VERSION` in `src/guessnova/constants.py` and is currently **2**.

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

## Schema 2

Schema 2 formally makes `deleted_profiles` a canonical top-level state container. GuessNova 1.1 already wrote this field additively while still identifying the state as schema 1, so the schema-1-to-schema-2 migration is intentionally idempotent:

1. schema 0 receives baseline `profiles` and `active_profile`, then advances to schema 1;
2. schema 1 receives `deleted_profiles: {}` only when missing, then advances to schema 2;
3. schema 2 is normalized and persisted as the current format;
4. future schemas are rejected rather than silently downgraded.

Committed migration fixtures live under `tests/fixtures/state/` and cover both a legacy schema-1 save without trash and a schema-1 save that already contains recoverable trash.

## Profile deletion and restore

`guessnova profiles delete NAME` removes the profile from the live profile map and removes matching local leaderboard rows, but stores both inside `deleted_profiles` for recovery. `guessnova profiles restore NAME` restores the profile and retained leaderboard rows. Trash is local, exported with normal backups, validated on load, and bounded.

Creating a new live profile with the same name as a deleted profile is allowed, but restoring the deleted profile fails safely until the live-name collision is resolved.

## Normalization and forward safety

Every load/save passes through state normalization. The normalizer validates or repairs supported data including profile names, statistics, settings, history, leaderboard rows, deleted-profile records, active-profile references, and top-level structure. Unknown top-level fields are dropped. Invalid profiles containers and future schemas are rejected.

Writes use a temporary file in the destination directory, flush and `fsync` it, then atomically replace the state file where supported by the host filesystem.

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

The wrapper's `schema_version` records the embedded payload's actual schema version. For example, the pre-repair backup created by `guessnova-doctor --repair` can be a version-2 backup wrapper containing a schema-1 payload. The wrapper schema metadata and embedded payload schema must match.

### Legacy backup compatibility

GuessNova 1.0/1.1 used backup wrapper version 1 and coupled that wrapper version to the then-current state schema. Version-1 backup wrappers remain importable when their embedded payload schema is supported. The payload is migrated only when it is saved through current `Storage`.

### Backup validation

Import rejects:

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

## Doctor and safe repair

`guessnova-doctor` inspects local state without network access. It reports source/current schema, active profile, profile/history/leaderboard/trash counts, normalization changes, and detected migration/normalization issues.

`guessnova-doctor --repair` requires confirmation (or `--yes`) and refuses state it cannot safely decode/normalize. Before rewriting repairable state it writes an integrity-protected backup of the original payload. Use `--backup-dir PATH` to place that backup elsewhere.

`guessnova-doctor --json` emits machine-readable diagnostic output suitable for scripts.

## Replay codes

Replay codes retain replay version 1. They contain a compact JSON `GameSummary`, replay version, and truncated SHA-256 integrity digest, then use URL-safe Base64 encoding. GuessNova 1.2 does not change replay compatibility or guessing rules.

The replay parser enforces a maximum encoded length, valid URL-safe Base64, envelope/checksum structure, supported version, an allowlist of fields, difficulty/range constraints, attempt/guess consistency, finite non-negative elapsed time, signed 64-bit portable seeds, and bounded hint metadata.

## Localization identifiers

The locale is a presentation preference only. Stable serialized identifiers—mode names, difficulty names, schema keys, achievement IDs, replay field names, backup format markers, and diagnostic JSON keys—are not translated.

## Privacy

Player names, statistics, settings, bounded history, recoverable profile trash, leaderboard data, diagnostics, and repair backups remain local unless the user explicitly exports/shares a file or replay code. GuessNova requires no runtime account, telemetry service, analytics service, or network connection. See `PRIVACY.md`.
