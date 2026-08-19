# Textual Workspace Reference

Canonical workspace guide: [`tui_workspace.md`](tui_workspace.md).

Challenge setup guide: [`tui_challenges.md`](tui_challenges.md).

Launch:

```bash
guessnova-tui
```

GuessNova 1.5 keeps Play as the initial pane and preserves the keyboard-first Profiles, History, Leaderboard, Settings, and read-only Recovery workspace from v1.4. The shipped TUI now also mounts validated mode/difficulty/seed/date challenge setup inside Play.

## Play challenge setup

Numeric setup supports:

- Classic
- Timed
- Streak
- Daily

Reverse remains on its dedicated interaction path:

```bash
guessnova reverse
```

Seed is enabled for Classic/Timed/Streak. Daily enables only its `YYYY-MM-DD` date field and derives the deterministic seed from the resolved date.

Invalid setup leaves the active game untouched. A successful setup clears the current round, displays a target-free challenge identity, and returns focus to the guess field.

Seeded and Daily configured resets replay from the validated configuration.

## Pane shortcuts

```text
Ctrl+1  Play
Ctrl+2  Profiles
Ctrl+3  History
Ctrl+4  Leaderboard
Ctrl+5  Settings
Ctrl+6  Recovery
Ctrl+R  New round
Ctrl+Q  Quit
```

Plain `R`/`Q` belong only to the focused numeric Play input, preserving reset/quit there. They are not global bindings, so challenge/profile/search/player/path inputs receive ordinary letters normally.

The guess field remains initial focus. Forward Tab from Guess still reaches Submit and Range Hint. Use backward keyboard navigation from Guess to reach challenge setup without changing the established fast-play flow.

## Safety and persistence

- Challenge configuration is validated before the current round is replaced.
- Invalid seed/date input preserves the current round and attempts.
- Challenge status never includes the hidden target.
- Profile deletion requires exact-name confirmation and remains recoverable.
- Changing the active profile resets any unfinished round.
- History and leaderboard views reuse existing validated local data.
- Settings reuse the existing profile settings model.
- High contrast applies immediately; locale changes fully apply on the next TUI launch.
- Recovery diagnostics and backup verification are read-only.
- Repair remains explicit through `guessnova doctor --repair`.
- No account, telemetry, cloud sync, remote leaderboard, or runtime network service is added.

## Compatibility

v1.5 does not change local compatibility identifiers:

```text
state schema = 2
backup wrapper = 2
legacy backup wrapper = 1
replay = 1
Doctor report = 1
```

Automated pilot/helper coverage includes configured challenge parsing, deterministic reset, Daily normalization, invalid-config preservation, target-free status, mode-aware fields, Play-local reset/quit, workspace text-entry isolation, navigation, profile lifecycle, history/leaderboard filters, settings, recovery verification, round isolation, launch-locale stability, and high-contrast behavior.
