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
        "reduced_motion": false,
        "high_contrast": false,
        "sound": false,
        "show_smart_hints": true
      }
    }
  },
  "leaderboard": []
}
```

The exact file location is platform dependent and can be overridden with `GUESSNOVA_HOME`.

## Migration

Legacy version-0 payloads receive baseline `profiles`/`active_profile` fields and are upgraded in memory to schema 1. Files with a schema newer than the application supports are rejected to avoid destructive downgrade writes.

## Export wrapper

`guessnova export` writes:

```json
{
  "format": "guessnova-export",
  "version": 1,
  "payload": {"...": "local state"}
}
```

Imports require the marker, a supported version, and an object payload.

## Replay codes

Replay codes contain a compact JSON `GameSummary`, replay version, and truncated SHA-256 integrity digest, then use URL-safe Base64 encoding. A replay code is not encrypted and must not contain secrets.

## Privacy

Player names, statistics, settings, and leaderboard data remain local unless the user explicitly exports/shares a file or replay code. See `PRIVACY.md`.
