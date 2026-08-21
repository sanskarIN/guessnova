# Textual Workspace

GuessNova's Textual interface is a keyboard-first local workspace. The stable six-pane workspace reuses the same profile, history, leaderboard, settings, backup-inspection, diagnostics, and game-service boundaries as the CLI. The current challenge-enabled application adds validated Play configuration as an additive layer rather than introducing a second persistence format or a network-backed account model.

## Launch

```bash
guessnova-tui
```

The installed entry point launches the challenge-enabled application layered over the stable workspace. It still starts on **Play** and focuses the numeric guess field so the established gameplay fast path remains immediate.

## Workspace panes

### Play

The Play pane provides:

- whole-number input;
- Submit button;
- explicit range hint button;
- current difficulty range and attempts remaining;
- automatic smart hints when enabled in the active profile;
- result persistence through `GameService`;
- deterministic reset when a validated seed or Daily configuration is present;
- validated Challenge Setup controls for Classic, Timed, Streak, and Daily.

Challenge Setup accepts mode/difficulty plus an optional whole-number seed for Classic/Timed/Streak or a `YYYY-MM-DD` Daily date. Reverse is deliberately not represented as an ordinary numeric-target configuration because its interaction model is different; use:

```bash
guessnova reverse
```

Challenge configuration is transactional: GuessNova validates the form and constructs the replacement game before replacing the active round. Invalid seed/date input therefore leaves the existing game and attempts intact. Seeded configured resets reconstruct from mode/difficulty/seed, while configured Daily resets reconstruct from the resolved date. Challenge status never needs to reveal the hidden target.

The numeric Play input is a dedicated `GuessInput` widget. While that field is focused, `R` requests a new round and `Q` quits, preserving the original single-card keyboard behavior. `Ctrl+R` and `Ctrl+Q` are the global equivalents available from every pane. Challenge seed/date fields are ordinary text inputs, so plain `q`/`r` remain normal text there.

Detailed Challenge Setup behavior is documented in [`tui_challenges.md`](tui_challenges.md).

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

Changing the active profile resets any unfinished round. A partially played round is therefore never silently reassigned to another local profile. If a validated configured challenge is active, reset uses that configuration while clearing the unfinished attempt state.

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

It can also verify a selected GuessNova backup without importing it. Verification reuses the established `inspect_backup(...)` boundary, including bounded input, wrapper/schema/integrity checks, and proof that the payload can normalize under the current state model.

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

Plain `Q` and `R` are **Play-local bindings owned by the numeric guess input**, not global application bindings. Profiles, History, Leaderboard, Recovery, and Challenge Setup text fields therefore receive ordinary `q`/`r` characters normally. The Ctrl variants remain available everywhere.

Each Ctrl+number pane shortcut also moves focus to a useful first control for that pane. Initial focus remains on Guess. The established forward-Tab path begins Guess → Submit → Range Hint; Challenge Setup remains keyboard reachable, including with backward navigation.

## Accessibility behavior

The workspace preserves these principles:

- keyboard-first operation;
- visible text status, not color-only meaning;
- deterministic initial focus on the guess field;
- Play-local `Q`/`R` without stealing letters from other text inputs;
- keyboard-reachable Challenge Setup without breaking the established forward gameplay path;
- textual challenge validation/status that never relies only on color;
- non-destructive invalid challenge configuration;
- non-destructive/read-only Recovery pane;
- recoverable profile deletion;
- no required mouse interaction;
- no required network access;
- no decorative switch animation;
- high-contrast screen class with stronger borders/focus indicators;
- language consistency within one running TUI process.

Automated Textual pilot tests supplement, but do not replace, manual release-candidate accessibility evidence. The release evidence template contains a dedicated Challenge Setup section.

## Privacy

Every workspace pane and Challenge Setup operation uses local GuessNova state/in-memory game configuration. The workspace contains no account sign-in, analytics, telemetry, cloud sync, remote leaderboard, or runtime API call.

Challenge configuration contains mode/difficulty/seed/date metadata only; it does not persist or expose the hidden target. Backup verification reads only the path the user selects. The Recovery pane never uploads state or backups. Profile names, history, settings, leaderboard entries, paths, and challenge metadata may still be personally meaningful local data, so screenshots and support reports should be reviewed before sharing.

## Testing boundaries

Reusable logic lives in `src/guessnova/tui_workspace.py` so it can be tested without rendering a terminal. Challenge presentation/widgets/integration are split into dedicated modules, and Textual pilot tests cover the interactive layer.

Stable workspace coverage includes:

- workspace snapshots;
- derived profile statistics;
- basic deterministic challenge construction helpers;
- history filtering/order;
- leaderboard filtering/order;
- settings persistence;
- tab shortcuts;
- Play-local `R` reset and `Q` quit;
- text-field handling of ordinary `q`/`r` letters outside Play;
- profile create/rename/delete/restore;
- exact delete confirmation;
- history filters and invalid dates;
- leaderboard filters;
- settings save;
- read-only backup verification;
- active-profile round isolation;
- launch-locale stability;
- high-contrast launch/save behavior.

Challenge-specific coverage adds:

- `ChallengeConfiguration` runtime invariants and parser normalization;
- deterministic seeded/Daily construction;
- target-free challenge status;
- English/Hindi challenge presentation;
- widget defaults and Reverse exclusion;
- mode-aware seed/date enablement;
- seeded and Daily start flows;
- invalid-config active-round preservation;
- deterministic configured reset;
- initial challenge identity;
- guess-first and backward keyboard navigation;
- plain `Q/R` text-entry safety in challenge fields.

See [`testing.md`](testing.md) for the complete suite inventory.

## Architecture

The installed TUI deliberately uses an additive layer:

```text
tui_challenge_app.py
        |
tui.py  (stable six-pane workspace)
        |
GameService / Storage / diagnostics / backup inspection
```

Supporting challenge modules are:

```text
tui_workspace.py          validated Textual-independent ChallengeConfiguration/parser
tui_challenge.py          localized target-free challenge status
tui_challenge_widgets.py  mode/difficulty/seed/date controls
tui_challenge_app.py      challenge-specific mount/start/reset integration
```

The design decision and rejected alternatives are recorded in [`adr/0005-additive-textual-challenge-layer.md`](adr/0005-additive-textual-challenge-layer.md).

## Compatibility

Challenge Setup does not require a state-schema change. The current interface continues using:

- state schema `2`;
- backup wrapper `2`;
- legacy backup wrapper `1`;
- replay format `1`;
- Doctor report protocol `1`.

Challenge configuration is in-memory application/UI state and does not create a new persistence format merely to support the form.
