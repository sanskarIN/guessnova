# Textual Workspace Reference

Canonical guide: [`tui_workspace.md`](tui_workspace.md).

Launch:

```bash
guessnova-tui
```

GuessNova 1.4 keeps Play as the initial pane and adds a keyboard-first local workspace for Profiles, History, Leaderboard, Settings, and read-only Recovery.

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

Plain `R`/`Q` belong only to the focused numeric Play input, preserving the original reset/quit flow there. They are not global bindings, so profile/search/player/path inputs can type ordinary `r`/`q` characters normally.

## Safety and persistence

- Profile deletion requires exact-name confirmation and remains recoverable.
- Changing the active profile resets any unfinished round.
- History and leaderboard views reuse existing validated local data.
- Settings reuse the existing profile settings model.
- High contrast applies immediately; locale changes fully apply on the next TUI launch.
- Recovery diagnostics and backup verification are read-only.
- Repair remains explicit through `guessnova doctor --repair`.
- No account, telemetry, cloud sync, remote leaderboard, or runtime network service is added.

## Compatibility

v1.4 does not change the local compatibility identifiers:

```text
state schema = 2
backup wrapper = 2
legacy backup wrapper = 1
replay = 1
Doctor report = 1
```

Automated pilot tests cover Play-local reset/quit, workspace text-entry isolation, navigation, profile lifecycle, history/leaderboard filters, settings, recovery verification, round isolation, launch-locale stability, and high-contrast behavior.
