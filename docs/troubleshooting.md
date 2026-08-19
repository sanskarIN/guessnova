# Troubleshooting

## `guessnova` or `guessnova-tui` is not found

Activate the project virtual environment and reinstall:

```bash
python -m pip install -e .
```

You can also run the CLI with `python -m guessnova`.

## Python version error

GuessNova requires Python 3.13+. Check:

```bash
python --version
```

## Local data appears corrupted

GuessNova stores versioned JSON under its application-data directory. Back up `state.json` before manual changes. Invalid JSON/newer unsupported schemas should be investigated rather than silently overwritten. Set `GUESSNOVA_HOME` to a temporary directory when testing recovery.

## Import is rejected

Only GuessNova exports with the expected `guessnova-export` wrapper and supported schema version are accepted. Do not remove the format/version fields.

## Replay code is rejected

Replay codes are checksum protected. A changed/truncated code is intentionally rejected. Generate a new code from a completed saved challenge.

## Terminal styling is difficult to read

Try a terminal with modern Unicode/ANSI support and use profile settings/high-contrast theme where available. Core CLI commands remain keyboard-driven and do not require mouse input.

For unresolved problems, see `SUPPORT.md` and include OS, Python version, GuessNova version/commit, command, and non-sensitive error output.
