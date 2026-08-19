# Troubleshooting

## Command not found

Activate the same virtual environment where GuessNova was installed, then run `python -m guessnova` as a fallback.

## Colors or symbols look incorrect

Use a modern terminal with UTF-8 enabled. Core messages remain readable even without styling.

## I want a clean profile

Set `GUESSNOVA_HOME` to a new empty directory for an isolated run, or remove the existing local GuessNova data directory after backing it up.

## Import fails

Verify that the file was created by `guessnova export` and was not manually truncated or changed to a future unsupported schema version.

## Reproducible bug report

Use `--seed <number>` and `--no-save`, record the difficulty/mode, and include the seed and observed behavior in the issue.
