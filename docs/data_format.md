# Data Format

GuessNova stores local data as JSON through `Storage`. The current schema version is defined in `src/guessnova/constants.py`.

## Local state

Typical shape:

```json
{
  "schema_version": 1,
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
      "history": [
        {
          "mode": "classic",
          "difficulty": "normal",
          "won": true,
          "attempts": 4,
          "elapsed_seconds": 12.5,
          "seed": 20260819,
          "played_at": "2026-08-19T03:00:00+00:00"
        }
      ]
    }
  },
  "leaderboard": []
}
```

History is bounded to the most recent 200 entries per profile so local state cannot grow indefinitely. The exact file location is platform dependent and can be overridden with `GUESSNOVA_HOME`.

## Migration and forward safety

Legacy version-0 payloads receive baseline `profiles`/`active_profile` fields and are upgraded in memory to schema 1. Additive profile fields such as `history`, `locale`, and `onboarding_complete` have safe defaults, so existing schema-1 saves that predate them continue to load. Files with a schema newer than the application supports are rejected to avoid destructive downgrade writes.

Every load/save passes through state normalization: unknown top-level fields are discarded, malformed profile/stat/settings/history values are ignored or reduced to safe defaults, leaderboard entries are reconstructed through their typed adapter, and an invalid profiles container is rejected. Writes use a temporary file, flush/fsync it, and atomically replace the state file.

## Export wrapper

`guessnova export` writes:

```json
{
  "format": "guessnova-export",
  "version": 1,
  "payload": {"...": "local state"}
}
```

Imports require the marker, a supported version, and an object payload. Imported payloads are normalized again when saved; an export wrapper is not treated as trusted merely because it has the correct marker.

## Replay codes

Replay codes contain a compact JSON `GameSummary`, replay version, and truncated SHA-256 integrity digest, then use URL-safe Base64 encoding. Summaries include mode, difficulty, target, win status, attempts, elapsed time, guesses, optional seed, explicit-hint count, and accumulated XP hint penalty.

The replay parser enforces a maximum encoded length, valid URL-safe Base64, envelope/checksum structure, supported version, an allowlist of fields, difficulty/range constraints, attempt/guess consistency, finite non-negative elapsed time, signed 64-bit portable seeds, and bounded hint metadata. Older version-1 replay payloads that omit the later optional hint fields continue to load with zero-value defaults.

A replay code is integrity protected against accidental corruption; the checksum is not a secret-key signature, encryption, authentication, or proof that a challenge came from a trusted person. Replay codes must not contain secrets.

## Localization identifiers

The locale is a presentation preference only. Stable serialized identifiers—mode names, difficulty names, schema keys, achievement IDs, and replay field names—are not translated. See `docs/localization.md`.

## Privacy

Player names, statistics, settings, bounded history, and leaderboard data remain local unless the user explicitly exports/shares a file or replay code. See `PRIVACY.md`.
