# Game Modes

GuessNova keeps mode rules in the shared domain/engine layer. The Rich CLI and Textual workspace consume those rules rather than maintaining separate target-selection logic.

## Classic

Guess the hidden number within the selected difficulty range and attempt budget. Incorrect in-range guesses provide a smart temperature/direction/parity hint.

In v1.5 Textual Challenge Setup, Classic accepts an optional whole-number seed for deterministic reproduction.

## Timed

Uses the same guessing rules but ends when the difficulty-specific timer is reached. The engine accepts an injected clock so timeout behavior is deterministic in tests.

In v1.5 Textual Challenge Setup, Timed accepts an optional whole-number seed and uses the timer associated with the selected shared difficulty preset.

## Streak

Uses normal guessing rounds tagged as `streak`; persistent profile progression tracks consecutive wins and best streak. A lost round resets the current profile streak.

In v1.5 Textual Challenge Setup, Streak accepts an optional whole-number seed. The mode tag remains part of normal completed-game persistence through `GameService`.

## Reverse

Think of a number and answer `higher`, `lower`, or `correct`. GuessNova narrows the permitted range with binary search and rejects inconsistent response sequences.

Reverse deliberately remains outside ordinary v1.5 numeric Challenge Setup because its interaction contract is different: GuessNova guesses the player's number rather than the player entering guesses against a hidden target.

Use:

```bash
guessnova reverse
```

A future Textual Reverse experience should use a dedicated interaction rather than forcing Reverse through the normal guess input.

## Daily Challenge

Builds a deterministic seed from the selected ISO date plus a versioned namespace. The same date, difficulty, and rules version produce the same challenge target, making comparison fair without a server.

CLI examples:

```bash
guessnova play --mode daily
guessnova play --mode daily --day 2026-08-19
```

In v1.5 Textual Challenge Setup, Daily enables a `YYYY-MM-DD` date field and disables the manual seed field. If the date is blank when Start Challenge is activated, the local current date is resolved and written back into the field.

A configured Daily reset reconstructs from the resolved date.

## Difficulty presets

All interfaces read from the shared `DIFFICULTIES` registry.

- Easy: 1–50, 10 attempts, 60-second timed limit.
- Normal: 1–100, 9 attempts, 45-second timed limit.
- Hard: 1–500, 10 attempts, 40-second timed limit.
- Expert: 1–1000, 10 attempts, 35-second timed limit.

The Textual challenge selector must not maintain a second range/attempt/timer table.

## Deterministic challenges

`--seed` or `GUESSNOVA_SEED` makes non-Daily CLI gameplay reproducible.

The v1.5 TUI similarly accepts an optional integer seed for Classic/Timed/Streak. A successful seeded configuration is stored as validated in-memory challenge metadata. Reset reconstructs from that metadata rather than reading potentially edited widget text.

Daily determinism comes from the resolved ISO date rather than a user-entered seed.

Replay codes serialize completed summary information with a checksum; they are portable summaries, not authentication tokens.

## Challenge Setup safety

Starting a configured TUI round follows validate/build-before-mutate ordering. An invalid seed/date does not replace the active target or consume/reset existing attempts.

Active challenge identity can show mode, difficulty, seed, or resolved Daily date. It deliberately excludes the hidden target.

See [`tui_challenges.md`](tui_challenges.md) for the complete Textual configuration contract.
