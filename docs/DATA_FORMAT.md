# Local Data Format

GuessNova stores a JSON state file with schema version `1`.

```json
{
  "active_profile": "Player",
  "leaderboard": [],
  "profiles": {
    "Player": {
      "name": "Player",
      "settings": {
        "high_contrast": false,
        "reduced_motion": false,
        "show_smart_hints": true,
        "sound": false,
        "theme": "nebula"
      },
      "stats": {
        "achievements": [],
        "best_streak": 0,
        "current_streak": 0,
        "games_played": 0,
        "games_won": 0,
        "total_guesses": 0,
        "xp": 0
      }
    }
  },
  "schema_version": 1
}
```

## Atomic writes

State is written to a temporary file in the same directory, flushed and synced, then replaced atomically where supported by the host filesystem.

## Migration policy

Older schemas are migrated forward during load. A file created by a future schema version is rejected instead of being silently downgraded.

## Export format

Exports wrap the complete state with `format: guessnova-export` and a version field. Imports validate both before replacing local state.
