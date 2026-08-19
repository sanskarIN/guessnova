# Support

For help using GuessNova, open a GitHub issue when the question and diagnostic information can be discussed publicly.

Before reporting local-state problems, run:

```bash
guessnova-doctor
guessnova-doctor --json
```

The doctor is local-only and can identify schema migration/normalization requirements without changing state. If a repair is appropriate, `guessnova-doctor --repair` creates a pre-repair backup before writing normalized state.

## What to include in a public issue

Prefer non-sensitive details:

- operating system;
- Python version;
- GuessNova version/commit;
- command that failed;
- exit code;
- concise error message;
- whether `guessnova-doctor` reports healthy/attention/unreadable state;
- schema version numbers when relevant.

Review diagnostic JSON before sharing it. It can contain the active local profile name and local aggregate counts. Do **not** publicly upload `state.json`, exported backups, pre-repair backups, replay codes containing personally meaningful data, credentials, private terminal history, or other files you have not reviewed.

For support that should not be public, contact `supportramsandesh@gmail.com`.

Business contact:

- `sanskarin@outlook.in`
- `sanskarin.business@gmail.com`

Project home: `https://github.com/sanskarIN/guessnova`

Support development: `https://buymeacoffee.com/sanskarIN`

**Made by the Sanskar**
