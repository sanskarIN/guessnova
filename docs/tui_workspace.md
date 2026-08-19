# Textual Workspace

GuessNova 1.5 extends the v1.4 keyboard-first local workspace with validated challenge setup inside Play. The workspace continues to reuse the same profile, history, leaderboard, settings, backup-inspection, diagnostics, game-service, and game-engine boundaries as the CLI. It does not introduce a second persistence format or a network-backed account model.

For the focused challenge-configuration reference, see [`tui_challenges.md`](tui_challenges.md).

## Launch

```bash
guessnova-tui
```

The application starts on **Play** and focuses the numeric guess field so the established gameplay flow remains immediate.

## Workspace panes

### Play

The Play pane retains the Textual gameplay loop:

- whole-number input;
- Submit button;
- explicit range hint button;
- current difficulty range and attempts remaining;
- automatic smart hints when enabled in the active profile;
- result persistence through `GameService`;
- deterministic reset when a seed/date-backed configuration is present.

GuessNova 1.5 also mounts a **Challenge Setup** block in Play with:

- mode selection;
- difficulty selection;
- optional deterministic seed for Classic/Timed/Streak;
- Daily `YYYY-MM-DD` date selection;
- mode-aware enablement so only the relevant seed/date input is active;
- a Start Challenge action;
- localized help, validation errors, and active challenge identity.

The numeric setup supports Classic, Timed, Streak, and Daily. Reverse remains separate because its interaction model is GuessNova guessing a number the player has chosen:

```bash
guessnova reverse
```

Challenge setup validates and builds the replacement game before changing the current in-memory round. Invalid seed/date configuration therefore preserves the current game, target, attempts, and result-save state.

After successful configuration, GuessNova normalizes the accepted fields, updates the range/attempt display, clears old feedback/guess input, shows a target-free active identity, and returns focus to the numeric guess field.

Configured reset behavior:

- seeded Classic/Timed/Streak reconstruct the same deterministic challenge;
- Daily reconstructs from the resolved date;
- unseeded challenges retain normal random-reset semantics.

The numeric Play input remains a dedicated `GuessInput` widget. While that field is focused, `R` requests a new round and `Q` quits. `Ctrl+R` and `Ctrl+Q` are the global equivalents available from every pane.

Plain `Q/R` are not application-global, so the new challenge seed/date inputs can receive ordinary text for validation without triggering reset/quit.

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

Changing the active profile resets any unfinished round. A partially played round is therefore never silently reassigned to another local profile. If the round came from v1.5 challenge setup, the validated challenge configuration can remain active while attempt state is reset.

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

It can also verify a selected GuessNova backup without importing it. Verification reuses the `inspect_backup(...)` boundary, including bounded input, wrapper/schema/integrity checks, and proof that the payload can normalize under the current state model.

The TUI does **not** perform repair. Repair remains an explicit operator workflow:

```bash
guessnova doctor --repair
```

This separation keeps the everyday workspace safe while preserving the stronger confirmation and backup-before-write guarantees of Doctor.

## Keyboard navigation

Global pane and application shortcuts:

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

Plain `Q` and `R` are **Play-local bindings owned by the numeric guess input**, not global application bindings. Challenge, Profiles, History, Leaderboard, and Recovery text fields therefore receive ordinary `q`/`r` characters normally. The Ctrl variants remain available everywhere.

The v1.5 challenge block is inserted before the original title/guess controls in focus order, while the app still explicitly focuses Guess on launch. Consequently:

- initial focus remains Guess;
- forward Tab remains Guess → Submit → Range Hint;
- Shift+Tab from Guess reaches Start Challenge, then the challenge inputs/selectors backward;
- no mouse interaction is required for configuration.

Each Ctrl+number pane shortcut also moves focus to a useful first control for that pane.

## Accessibility behavior

The workspace preserves these principles:

- keyboard-first operation;
- visible text status, not color-only meaning;
- deterministic initial focus on the guess field;
- Play-local `Q`/`R` without stealing letters from other text inputs;
- visible challenge mode/difficulty labeling;
- mode-aware disabling of irrelevant seed/date fields;
- text validation errors that preserve the existing round;
- target-free active challenge identity;
- non-destructive/read-only Recovery pane;
- recoverable profile deletion;
- no required mouse interaction;
- no required network access;
- no decorative switch animation;
- high-contrast screen class with stronger borders/focus indicators;
- language consistency within one running TUI process.

Automated Textual pilot tests supplement, but do not replace, manual release-candidate accessibility evidence.

## Privacy

Every workspace pane and challenge control operates on local GuessNova state. The workspace contains no account sign-in, analytics, telemetry, cloud sync, remote leaderboard, or runtime API call.

Challenge configuration is in-memory presentation/application state. Mode, difficulty, seed, and resolved Daily date are not added to the state schema merely because they appear in the form. Completed games continue to persist only through existing history/profile/leaderboard boundaries.

Backup verification reads only the path the user selects. The Recovery pane never uploads state or backups. Profile names, history, settings, leaderboard entries, seeds/dates visible on screen, and backup metadata may still be personally meaningful local data, so screenshots and support reports should be reviewed before sharing.

## Testing boundaries

Reusable logic lives in `src/guessnova/tui_workspace.py` so challenge parsing/configuration, history selection, leaderboard filtering, profile summaries, and settings persistence can be tested without rendering a terminal.

Additional v1.5 source boundaries are:

- `src/guessnova/tui_challenge.py` — localized target-free challenge presentation;
- `src/guessnova/tui_challenge_widgets.py` — challenge form widgets and mode-aware field state;
- `src/guessnova/tui_challenge_app.py` — additive integration over the stable v1.4 workspace.

Current coverage includes:

- workspace snapshots;
- derived profile statistics;
- deterministic challenge construction helpers;
- immutable challenge configuration invariants;
- seeded and Daily parser normalization;
- invalid seed/date validation;
- target-free active challenge status;
- mode-aware challenge fields;
- seeded configured-round startup;
- Daily configured-round startup;
- invalid-config current-round preservation;
- configured deterministic reset;
- initial active challenge identity;
- challenge setup keyboard reachability;
- history filtering/order;
- leaderboard filtering/order;
- settings persistence;
- tab shortcuts;
- Play-local `R` reset and `Q` quit;
- text-field handling of ordinary `q`/`r` letters outside the numeric GuessInput;
- profile create/rename/delete/restore;
- exact delete confirmation;
- history filters and invalid dates;
- leaderboard filters;
- settings save;
- read-only backup verification;
- active-profile round isolation;
- launch-locale stability;
- high-contrast launch/save behavior;
- smoke coverage through challenge parser/configuration/presentation helpers.

Normal CI and tagged-release package matrices build and install wheels on Linux, Windows, and macOS and import both the stable workspace and the shipped challenge-enabled application layer.

## Compatibility

The v1.5 challenge workspace does not require a serialized-format change. It continues using:

- state schema `2`;
- backup wrapper `2`;
- legacy backup wrapper `1`;
- replay format `1`;
- Doctor report protocol `1`.

v1.5 is a presentation/application-layer expansion over the existing local formats.
