# Textual Workspace

GuessNova 1.4 expands `guessnova-tui` from a single gameplay card into a keyboard-first local workspace. The workspace reuses the same profile, history, leaderboard, settings, backup-inspection, diagnostics, and game-service boundaries as the CLI. It does not introduce a second persistence format or a network-backed account model.

## Launch

```bash
guessnova-tui
```

The application starts on **Play** and focuses the numeric guess field so the existing gameplay flow remains immediate.

## Workspace panes

### Play

The Play pane retains the original Textual gameplay loop:

- whole-number input;
- Submit button;
- explicit range hint button;
- current difficulty range and attempts remaining;
- automatic smart hints when enabled in the active profile;
- result persistence through `GameService`;
- deterministic reset when a seed is present.

`R` starts a new round when normal gameplay focus allows the application binding to handle it. `Ctrl+R` is the global reset binding.

### Profiles

The Profiles pane exposes local profile lifecycle operations without duplicating storage logic:

- inspect the active profile summary;
- view unlocked achievement labels;
- choose and activate a saved profile;
- create a profile;
- rename a selected profile;
- move a selected profile to recoverable trash;
- restore a selected deleted profile;
- refresh local profile/trash state.

Deletion requires the selected profile name to be typed exactly into the name field before the Delete action is accepted. This mirrors the project's recoverability-first behavior instead of turning the TUI into a one-click permanent-delete surface.

Changing the active profile resets any unfinished round. A partially played round is therefore never silently reassigned to another local profile.

The display language stays fixed for the current TUI process. If a newly selected profile uses another locale, its saved locale appears in Settings, but full presentation-language changes take effect on the next TUI launch. This prevents a half-retranslated interface.

### History

The History pane presents up to the newest 100 matching local sessions for the active profile. Filters include:

- win/loss result;
- mode;
- difficulty;
- free-text search;
- start date;
- end date.

Dates use `YYYY-MM-DD`. Invalid date input reports an error without replacing the last valid table contents.

The table displays:

- timestamp;
- mode;
- difficulty;
- result;
- attempts;
- elapsed time.

History selection uses the same bounded `HistoryEntry` data already stored in the active profile.

### Leaderboard

The Leaderboard pane displays the existing ranked local leaderboard and supports filters for:

- mode;
- difficulty;
- case-insensitive player-name substring.

The table displays rank, player, mode, difficulty, attempts, elapsed time, and timestamp. Profile rename/delete/restore behavior remains owned by `Storage`, so workspace refreshes see the same coherent leaderboard state as CLI commands.

### Settings

The Settings pane exposes the active profile's existing local preferences:

- Rich theme identifier;
- locale;
- reduced-motion preference;
- high-contrast preference;
- sound preference;
- automatic smart hints.

Saving uses `Settings.from_dict(...)` and `Storage.save_profile(...)`, preserving the existing onboarding flag.

Smart-hint changes apply to gameplay immediately. High contrast applies to the current Textual screen immediately with stronger borders and focus outlines. The selected locale is persisted but takes full effect on the next TUI launch.

Switch widgets use `animate=False`; GuessNova does not add decorative TUI animation in this workspace.

### Recovery

The Recovery pane is deliberately **read-only**. It displays:

- local data directory;
- state health;
- source and current schema versions;
- live profile count;
- total history count;
- leaderboard count;
- deleted-profile count.

It can also verify a selected GuessNova backup without importing it. Verification reuses the v1.3 `inspect_backup(...)` boundary, including bounded input, wrapper/schema/integrity checks, and proof that the payload can normalize under the current state model.

The TUI does **not** perform repair. Repair remains an explicit operator workflow:

```bash
guessnova doctor --repair
```

This separation keeps the everyday workspace safe while preserving the stronger confirmation and backup-before-write guarantees of Doctor.

## Keyboard navigation

Global pane shortcuts:

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

Plain `Q` and `R` are non-priority application bindings. This matters because Profiles, History, Leaderboard, and Recovery contain text inputs where ordinary letters must remain typable. The priority `Ctrl+Q` and `Ctrl+R` alternatives remain available everywhere.

Each Ctrl+number pane shortcut also moves focus to a useful first control for that pane.

## Accessibility behavior

The workspace preserves these principles:

- keyboard-first operation;
- visible text status, not color-only meaning;
- deterministic initial focus on the guess field;
- non-destructive/read-only Recovery pane;
- recoverable profile deletion;
- no required mouse interaction;
- no required network access;
- no decorative switch animation;
- high-contrast screen class with stronger borders/focus indicators;
- language consistency within one running TUI process.

Automated Textual pilot tests supplement, but do not replace, manual release-candidate accessibility evidence.

## Privacy

Every workspace pane operates on local GuessNova state. The workspace contains no account sign-in, analytics, telemetry, cloud sync, remote leaderboard, or runtime API call.

Backup verification reads only the path the user selects. The Recovery pane never uploads state or backups. Profile names, history, settings, leaderboard entries, and backup metadata may still be personally meaningful local data, so screenshots and support reports should be reviewed before sharing.

## Testing boundaries

Reusable logic lives in `src/guessnova/tui_workspace.py` so it can be tested without rendering a terminal. Textual pilot tests then cover the interactive layer.

Current v1.4 coverage includes:

- workspace snapshots;
- derived profile statistics;
- deterministic challenge construction helpers;
- history filtering/order;
- leaderboard filtering/order;
- settings persistence;
- tab shortcuts;
- text-field handling of ordinary `q`/`r` letters;
- profile create/rename/delete/restore;
- exact delete confirmation;
- history filters and invalid dates;
- leaderboard filters;
- settings save;
- read-only backup verification;
- active-profile round isolation;
- launch-locale stability;
- high-contrast launch/save behavior.

## Compatibility

The v1.4 TUI workspace does not require a state-schema change. It continues using:

- state schema `2`;
- backup wrapper `2`;
- legacy backup wrapper `1`;
- replay format `1`;
- Doctor report protocol `1`.

The workspace is a presentation/application-layer expansion over the existing local formats.
