# Textual Challenge Setup

GuessNova 1.5 adds validated challenge configuration directly to the shipped `guessnova-tui` Play experience while preserving the v1.4 six-pane local workspace.

The feature is intentionally an application/presentation-layer addition. It does not add a new save schema, backup wrapper, replay format, account system, remote leaderboard, or network service.

## Launch

```bash
guessnova-tui
```

The application still starts on **Play** with focus on the numeric guess field. The challenge controls are mounted ahead of that field in document order, so the established `Guess → Submit → Range Hint` forward-Tab flow remains unchanged.

Use `Shift+Tab` from the guess field to move backward into the challenge controls.

## Supported challenge modes

The mounted numeric challenge form supports:

- `classic`
- `timed`
- `streak`
- `daily`

`reverse` is deliberately excluded. Reverse mode uses a different interaction model where GuessNova guesses the player's number, so it remains on its dedicated CLI path instead of being presented as ordinary numeric target guessing.

```bash
guessnova reverse
```

## Difficulty choices

The form reads directly from the shared `DIFFICULTIES` registry. Current choices are:

| Difficulty | Range | Attempts | Timed limit |
| --- | ---: | ---: | ---: |
| `easy` | 1–50 | 10 | 60 seconds |
| `normal` | 1–100 | 9 | 45 seconds |
| `hard` | 1–500 | 10 | 40 seconds |
| `expert` | 1–1000 | 10 | 35 seconds |

The TUI does not maintain a second copy of these rules.

## Seed field

The optional seed field is enabled for:

- Classic
- Timed
- Streak

A seed must be a whole number. When present, it is passed through the same `GuessGame` deterministic random source used by the CLI and tests.

Example seed:

```text
20260819
```

Starting the same mode/difficulty/seed combination produces the same target under the same rules version.

Leaving the seed blank creates a normal unseeded round. Resetting an unseeded round may therefore choose a new target, matching existing GuessNova reset behavior.

## Daily date field

The date field is enabled only for Daily mode.

Accepted format:

```text
YYYY-MM-DD
```

Example:

```text
2026-08-19
```

If the Daily date is blank, the challenge parser resolves the local current date when **Start Challenge** is activated. The resolved date is written back into the field so the active Daily identity is explicit rather than remaining an ambiguous blank.

Daily challenges derive their seed from the resolved date. The manual seed field is disabled for Daily mode and is cleared after a Daily challenge is successfully started.

## Mode-aware fields

The challenge form keeps irrelevant fields disabled:

- Daily → date enabled, seed disabled.
- Classic/Timed/Streak → seed enabled, date disabled.

Changing mode updates these states immediately.

Values in an irrelevant field are never treated as configuration for the selected mode. After a successful start, the form normalizes itself to the accepted configuration.

## Starting a configured challenge

The start operation is transactional at the application-state level:

1. Read mode, difficulty, seed, and date controls.
2. Parse and validate the configuration.
3. Construct the replacement game.
4. Only after both validation and construction succeed, replace the active in-memory round.
5. Clear guess/feedback state.
6. Update the range/attempt display.
7. Show the active challenge identity.
8. Return focus to the numeric guess field.

This order matters. An invalid configuration does not partially replace the current round.

## Validation failures

Examples of rejected input include:

- unknown mode;
- unknown difficulty;
- Reverse mode passed through the numeric challenge parser;
- non-integer seed text;
- malformed Daily date.

Malformed Daily date example:

```text
19-08-2026
```

Expected format:

```text
2026-08-19
```

When validation fails:

- the existing `GuessGame` remains active;
- existing attempts remain intact;
- the existing target remains intact;
- completed-result save state remains intact;
- the error is rendered in the challenge status area;
- focus moves to the relevant seed or date field.

No invalid challenge configuration is persisted.

## Active challenge status

The Play pane displays a target-free identity line.

Seeded example:

```text
Active: timed · hard · seed 20260819
```

Daily example after configuration:

```text
Active: daily · normal · date 2026-08-19
```

Unseeded example:

```text
Active: classic · normal · random seed
```

The hidden target is never included in this identity line.

When the app starts with an already-created Daily `GuessGame` whose original date is unavailable to the presentation layer, the status may identify the existing deterministic seed instead. Once a Daily challenge is created through the form, the resolved date is used.

## Reset behavior

`R` in the focused numeric guess field and global `Ctrl+R` retain the existing reset behavior.

For a challenge created through the configuration form:

- seeded Classic/Timed/Streak reset from the stored validated configuration;
- Daily reset from the stored resolved date;
- deterministic configuration therefore reproduces the same seed and target;
- attempts, hints, completion state, guess input, and feedback are reset for the new round.

The configuration object contains only mode/difficulty/seed/date metadata. It does not contain or expose the hidden target.

## Profile ownership

The v1.4 active-profile isolation rule remains in force.

If profile ownership changes while a configured round is unfinished, GuessNova resets the round before later persistence. A partially played challenge cannot be silently recorded under another profile.

The selected challenge configuration can remain active across the profile transition, but the in-progress attempt state does not.

Completed results continue through the shared `GameService` path and therefore use the same profile/history/leaderboard/achievement behavior as other gameplay.

## Keyboard behavior

Global shortcuts remain:

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

Plain `R` and `Q` remain scoped to `GuessInput`, the numeric Play field.

This is important because challenge seed/date controls are ordinary Textual `Input` widgets. Plain letters typed into those fields are treated as field input rather than application-level reset/quit commands. Invalid text can therefore be shown and validated safely instead of unexpectedly terminating or resetting the app.

## Localization

Every new user-facing challenge string is present in both shipped catalogs:

- English (`en`)
- Hindi (`hi`)

The existing catalog-completeness test continues to require Hindi to contain every English message key.

The current-process locale rule is unchanged: saving a different locale persists it to the profile, while the already-mounted TUI keeps one coherent launch language until restart.

## Accessibility

The challenge form preserves the established workspace principles:

- guess field remains initial focus;
- forward Tab from Guess still reaches Submit and Range Hint;
- challenge configuration is reachable with backward keyboard navigation;
- visible text identifies mode/difficulty/seed/date state;
- errors are text, not color-only signals;
- irrelevant fields are disabled rather than visually pretending to be active;
- no mouse interaction is required;
- no animation is required;
- no network access is required.

Manual release-candidate evidence should include the challenge controls in addition to the six v1.4 panes.

## Architecture

The feature is split into small boundaries:

- `src/guessnova/tui_workspace.py`
  - `ChallengeConfiguration`
  - `parse_workspace_challenge(...)`
  - `build_workspace_game(...)`
- `src/guessnova/tui_challenge.py`
  - localized target-free status presentation
- `src/guessnova/tui_challenge_widgets.py`
  - mode/difficulty/seed/date controls and mode-aware enablement
- `src/guessnova/tui_challenge_app.py`
  - additive integration with the stable v1.4 `GuessNovaApp`
- `src/guessnova/tui.py`
  - stable six-pane workspace and core gameplay behavior

The installed `guessnova-tui` script points to the challenge-enabled application layer.

This layering lets v1.5 add behavior without duplicating the mature profile/history/leaderboard/settings/recovery implementation.

## Automated coverage

Focused coverage includes:

- challenge parser validation;
- immutable configuration invariants;
- deterministic seeded reconstruction;
- deterministic Daily reconstruction;
- target-free challenge status;
- English/Hindi message formatting;
- widget defaults;
- Reverse exclusion from numeric setup;
- mode-aware seed/date field enablement;
- seeded configured-round startup;
- Daily normalization;
- invalid-seed round preservation;
- invalid-date round preservation;
- deterministic configured reset;
- initial challenge identity;
- guess-first focus order;
- plain `Q/R` behavior in challenge text fields;
- backward keyboard access to challenge controls;
- smoke coverage through parser/configuration/presentation helpers.

Normal CI and tagged-release package matrices also import the shipped challenge-enabled Textual application from installed wheels on Linux, Windows, and macOS.

## Compatibility

v1.5 challenge configuration changes no serialized compatibility domain:

- state schema remains `2`;
- backup wrapper remains `2`;
- legacy backup wrapper remains `1`;
- replay format remains `1`;
- Doctor machine-report protocol remains `1`.

Challenge configuration is in-memory UI/application state. It is not added to the local persistence schema merely to support the form.
