# Game Modes

## Classic

Guess the hidden number within the selected difficulty range and attempt budget. Incorrect in-range guesses provide a smart temperature/direction/parity hint.

## Timed

Uses the same guessing rules but ends when the difficulty-specific timer is reached. The engine accepts an injected clock so timeout behavior is deterministic in tests.

## Streak

Uses normal guessing rounds tagged as `streak`; persistent profile progression tracks consecutive wins and best streak. A lost round resets the current profile streak.

## Reverse

Think of a number and answer `higher`, `lower`, or `correct`. GuessNova narrows the permitted range with binary search and rejects inconsistent response sequences.

## Daily Challenge

Builds a deterministic seed from the selected ISO date plus a versioned namespace. The same date, difficulty, and rules version produce the same challenge target, making comparison fair without a server.

## Difficulty presets

- Easy: 1–50, 10 attempts, 60-second timed limit.
- Normal: 1–100, 9 attempts, 45-second timed limit.
- Hard: 1–500, 10 attempts, 40-second timed limit.
- Expert: 1–1000, 10 attempts, 35-second timed limit.

## Deterministic challenges

`--seed` or `GUESSNOVA_SEED` makes non-daily gameplay reproducible. Replay codes serialize completed summary information with a checksum; they are portable summaries, not authentication tokens.
