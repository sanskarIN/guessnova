# Architecture

GuessNova uses a layered, offline-first Python architecture.

## Layers

### Domain

`domain.py`, `engine.py`, `hints.py`, `rng.py`, and `daily.py` contain deterministic game behavior. They have no dependency on Rich, Textual, filesystem paths, or console input.

### Application services

`service.py` coordinates completed games with profile statistics, achievements, and leaderboard persistence.

### Persistence

`storage.py`, `profile.py`, `settings.py`, `leaderboard.py`, and `import_export.py` own local data structures, schema versioning, migration, and atomic writes.

### Interfaces

`cli.py` is the Rich command-line interface. `tui.py` provides the Textual app experience. Both consume the same game engine.

### Portability and safety

`replay.py` creates portable checksummed game summaries. `security.py` centralizes basic validation helpers.

## Dependency direction

Interfaces -> application services -> domain/persistence. The domain does not import from terminal UI modules.

## State model

The root persisted object contains `schema_version`, `active_profile`, `profiles`, and optional `leaderboard`. Future migrations should be explicit and monotonic.

## Determinism

Normal play uses system randomness. Tests and reproducible challenges can inject a seed. Daily challenges derive a stable integer seed from an ISO date and a versioned namespace.
