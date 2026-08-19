# Game Modes

## Classic

Guess the hidden number before the configured attempt budget is exhausted.

## Timed

Classic rules plus a per-difficulty time budget. The engine accepts an injected clock so timeout behavior can be tested deterministically.

## Streak

Streak-tagged rounds use the same fair guessing engine while profile statistics track consecutive wins and best streak. A failed recorded round resets the current streak.

## Reverse

The player thinks of a number and responds `higher`, `lower`, or `correct`. GuessNova uses bounded binary search and detects inconsistent answers.

## Daily Challenge

A stable SHA-256-derived seed is generated from the challenge date and a versioned namespace. The same date, difficulty, and GuessNova daily namespace reproduce the same target.

## Difficulties

| Level | Range | Attempts | Timed limit |
|---|---:|---:|---:|
| Easy | 1–50 | 10 | 60s |
| Normal | 1–100 | 9 | 45s |
| Hard | 1–500 | 10 | 40s |
| Expert | 1–1000 | 10 | 35s |
