# Support

For help using GuessNova, open a GitHub issue when the question and diagnostic information can be discussed publicly.

## TUI workspace problems

For a `guessnova-tui` problem, first record the non-sensitive basics:

- operating system;
- terminal and terminal size;
- Python version;
- GuessNova version/commit;
- active pane (Play, Profiles, History, Leaderboard, Settings, or Recovery);
- keyboard/mouse action that triggered the problem;
- whether the issue reproduces with a temporary `GUESSNOVA_HOME`;
- whether high contrast or Hindi locale is enabled.

Do not publish screenshots or recordings before reviewing them. The Textual workspace can visibly contain profile names, history, leaderboard names, local paths, settings, and backup-path metadata.

The canonical workspace guide is `docs/tui_workspace.md`.

## Local-state problems

Before reporting a local-state problem, run the recommended read-only Doctor route:

```bash
guessnova doctor
guessnova doctor --json
```

For a specific local data directory:

```bash
guessnova doctor --json --data-dir ./data
```

The standalone compatibility route remains available:

```bash
guessnova-doctor --json
```

Doctor is local-only and can identify schema migration/normalization requirements without changing state. If a supported repair is appropriate, `guessnova doctor --repair` creates a pre-repair backup before writing normalized state.

The Textual Recovery pane can also refresh the same read-only diagnostic information, but repair remains intentionally outside the TUI.

## Backup problems

Before reporting a backup problem, preflight it without importing:

```bash
guessnova doctor --json --verify-backup ./guessnova-backup.json
```

The TUI Recovery pane can perform the same read-only backup verification on a selected path.

Backup preflight validates supported wrapper/integrity/schema rules and current state normalizability. A structurally valid result is not proof of who created the backup.

## Profile workspace problems

TUI profile deletion requires the selected profile name to be typed exactly and then moves the profile into recoverable trash.

If a profile appears missing after deletion, check:

```bash
guessnova profiles trash
```

or the TUI Profiles trash select before assuming the data was permanently deleted.

Changing the active profile resets an unfinished TUI round by design so a partially played result cannot be saved under a different profile.

## What to include in a public issue

Prefer non-sensitive details:

- operating system;
- Python version;
- GuessNova version/commit;
- command or TUI pane/action that failed;
- exit code when a CLI/Doctor command is involved;
- Doctor `report_version`;
- Doctor result `kind`;
- concise error/issue message;
- healthy/attention/unreadable status where relevant;
- source/current schema numbers when relevant;
- backup wrapper/source/normalized schema versions when relevant;
- whether the issue reproduces with isolated local state;
- for TUI focus issues, the pane and control that had focus before/after the action.

Review diagnostic JSON and terminal/TUI captures before sharing them. Doctor/TUI output can contain profile names, selected local paths, local history/leaderboard data, and aggregate counts.

Do **not** publicly upload `state.json`, exported backups, pre-repair backups, private Doctor reports, credentials, private terminal history, or other files you have not reviewed.

## Doctor exit codes

- `0` — success / healthy state / valid backup / successful or no-op repair.
- `1` — interactive repair cancelled.
- `2` — attention required or handled validation/filesystem error.

For scripted repair, `--json --repair` requires `--yes` so stdout remains one machine-readable JSON document.

## Private support

For support that should not be public, contact `supportramsandesh@gmail.com`.

Business contact:

- `sanskarin@outlook.in`
- `sanskarin.business@gmail.com`

Project home: `https://github.com/sanskarIN/guessnova`

Support development: `https://buymeacoffee.com/sanskarIN`

Full recovery guide: `docs/doctor.md`

Full Textual workspace guide: `docs/tui_workspace.md`

**Made by the Sanskar**
