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

Legacy version-0 payloads receive baseline `profiles`/`active_profile` fields and are upgraded in memory to schema 1. The additive `history` profile field is optional when reading, so existing schema-1 saves without it remain valid. Files with a schema newer than the application supports are rejected to avoid destructive downgrade writes.

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

Replay codes contain a compact JSON `GameSummary`, replay version, and truncated SHA-256 integrity digest, then use URL-safe Base64 encoding. Summaries include mode, difficulty, target, win status, attempts, elapsed time, guesses, optional seed, explicit-hint count, and accumulated XP hint penalty. Older version-1 replay payloads that do not contain the new optional hint fields still load through dataclass defaults.

A replay code is integrity protected, not encrypted or authenticated, and must not contain secrets.

## Privacy

Player names, statistics, settings, bounded history, and leaderboard data remain local unless the user explicitly exports/shares a file or replay code. See `PRIVACY.md`.
