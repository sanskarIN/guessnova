# Accessibility Release Evidence Template

Use one copy of this checklist for every release candidate. Record observed behavior, terminal/OS, date, tester, and any linked issue. Do not mark an item complete from code inspection alone when the item requires manual interaction.

## Release candidate

- Version / tag candidate:
- Commit SHA:
- Date:
- Tester:
- Operating system:
- Terminal and version:
- Terminal font / scale:
- Locale tested:

## Keyboard-only CLI

- [ ] `guessnova play` can be completed without a mouse.
- [ ] `hint`, quit, invalid input, and replay output remain understandable without color.
- [ ] `guessnova reverse` is fully keyboard operable.
- [ ] `guessnova profiles` create/list/use/rename/delete/restore flows are keyboard operable.
- [ ] Profile deletion requires explicit confirmation unless `--yes` is intentionally supplied.
- [ ] `guessnova history` filters and grouping remain readable in keyboard-only use.
- [ ] `guessnova doctor` state/backup output remains understandable without relying on color.

Evidence / notes:

## Plain and compact output

- [ ] `guessnova --plain --compact stats` is readable.
- [ ] `guessnova --plain --compact history` is readable.
- [ ] `guessnova --plain --compact profiles list` is readable.
- [ ] No important state is communicated by color alone.

Evidence / notes:

## Textual TUI — Play baseline

- [ ] Initial focus lands on the guess input.
- [ ] Forward Tab order starts guess input → submit → range hint.
- [ ] Enter submits a guess from the input.
- [ ] Range Hint returns focus to the input and does not consume an attempt.
- [ ] `R` resets the round from the focused numeric GuessInput.
- [ ] `Ctrl+R` resets the round globally and returns to Play.
- [ ] `Q` exits from the focused numeric GuessInput.
- [ ] `Ctrl+Q` exits globally.
- [ ] Winning/losing feedback remains understandable from text alone.
- [ ] A completed TUI round persists exactly one result.

Evidence / notes:

## Textual TUI — v1.5 Challenge Setup

- [ ] Challenge Setup is visible without hiding the normal Play controls.
- [ ] Mode/difficulty meaning is understandable from visible text.
- [ ] Classic can be selected by keyboard.
- [ ] Timed can be selected by keyboard.
- [ ] Streak can be selected by keyboard.
- [ ] Daily can be selected by keyboard.
- [ ] Reverse is not presented as an ordinary numeric challenge option.
- [ ] Easy/normal/hard/expert difficulty can be selected by keyboard.
- [ ] Classic/Timed/Streak enable the optional seed field and disable the Daily date field.
- [ ] Daily disables the seed field and enables the date field.
- [ ] Shift+Tab from Guess reaches Start Challenge and allows continued backward navigation through configuration controls.
- [ ] Enter from the enabled seed field can start a non-Daily challenge.
- [ ] Enter from the enabled Daily date field can start a Daily challenge.
- [ ] A valid seeded challenge clears the previous round and returns focus to Guess.
- [ ] A valid Daily date is normalized/displayed as `YYYY-MM-DD` and returns focus to Guess.
- [ ] Blank Daily date resolves to an explicit current local date after successful start.
- [ ] Invalid seed reports a text error, focuses seed, and leaves the active round/attempt count intact.
- [ ] Invalid Daily date reports a text error, focuses date, and leaves the active round/attempt count intact.
- [ ] The active challenge line identifies mode and difficulty.
- [ ] Seeded challenge identity reports the seed without reporting the hidden target.
- [ ] Configured Daily identity reports the date without reporting the hidden target.
- [ ] Unseeded challenge identity is understandable without exposing the target.
- [ ] `Ctrl+R` on a configured seeded challenge reproduces the same deterministic target.
- [ ] `Ctrl+R` on a configured Daily challenge reproduces the same resolved-date challenge.
- [ ] Plain `q`/`r` typed in challenge text fields are field input rather than global quit/reset actions.
- [ ] Challenge errors/status are understandable without color.

Evidence / notes:

## Textual TUI — workspace navigation

- [ ] `Ctrl+1` opens Play and focuses the guess input.
- [ ] `Ctrl+2` opens Profiles and focuses the profile-name field.
- [ ] `Ctrl+3` opens History and focuses the history-search field.
- [ ] `Ctrl+4` opens Leaderboard and focuses the player-filter field.
- [ ] `Ctrl+5` opens Settings and focuses the first settings control.
- [ ] `Ctrl+6` opens Recovery and focuses the backup-path field.
- [ ] Tab/Shift+Tab remain usable in every pane.
- [ ] Ordinary `q` and `r` characters can be typed inside workspace text inputs without quitting/resetting.
- [ ] Focus indicators remain visible in normal and high-contrast modes.

Evidence / notes:

## Textual TUI — Profiles

- [ ] Saved profiles can be selected and activated without a mouse.
- [ ] A profile can be created from the keyboard.
- [ ] A selected profile can be renamed from the keyboard.
- [ ] Delete refuses a mismatched confirmation name.
- [ ] Delete succeeds only after the selected profile name is typed exactly.
- [ ] Deleted profiles appear in recoverable trash.
- [ ] A deleted profile can be restored from the keyboard.
- [ ] Profile summary and achievement text remain readable without color.
- [ ] Switching the active profile resets an unfinished round instead of reassigning it.
- [ ] If challenge setup was active, profile switching resets attempt state before later persistence.

Evidence / notes:

## Textual TUI — History

- [ ] Result filter is keyboard operable.
- [ ] Mode filter is keyboard operable.
- [ ] Difficulty filter is keyboard operable.
- [ ] Free-text search is keyboard operable.
- [ ] Since/until date fields are keyboard operable.
- [ ] Apply and Clear are keyboard operable.
- [ ] Invalid date input reports an understandable error and does not destroy the last valid table contents.
- [ ] The history table remains readable at normal and enlarged terminal font sizes.

Evidence / notes:

## Textual TUI — Leaderboard

- [ ] Mode/difficulty selects are keyboard operable.
- [ ] Player-name filtering accepts normal text input.
- [ ] Apply and Clear are keyboard operable.
- [ ] Rank/player/mode/difficulty/attempt/time/timestamp columns remain understandable.
- [ ] Profile rename/delete/restore changes are reflected after workspace refresh.

Evidence / notes:

## Textual TUI — Settings

- [ ] Theme select is keyboard operable.
- [ ] Locale select is keyboard operable.
- [ ] Reduced-motion switch is keyboard operable.
- [ ] High-contrast switch is keyboard operable.
- [ ] Sound-preference switch is keyboard operable.
- [ ] Smart-hints switch is keyboard operable.
- [ ] Save persists the expected active-profile settings.
- [ ] Smart-hint changes affect later gameplay in the current process.
- [ ] Enabling high contrast visibly strengthens focus/border presentation.
- [ ] Locale changes are clearly communicated as taking full effect on the next TUI launch.
- [ ] Switch controls do not use decorative animation.

Evidence / notes:

## Textual TUI — Recovery

- [ ] Local state health text is understandable without color.
- [ ] Data-directory and schema/count information are readable.
- [ ] Refresh Diagnostics is keyboard operable.
- [ ] Backup path accepts normal text input.
- [ ] Verify Backup is keyboard operable.
- [ ] A valid backup reports wrapper/schema/integrity information without importing it.
- [ ] An invalid backup reports an understandable error.
- [ ] Recovery contains no accidental repair/write action.
- [ ] Repair remains clearly directed to the explicit Doctor workflow when needed.

Evidence / notes:

## Display and scaling

Test at a normal width and a narrow terminal.

- [ ] 100% terminal font scale is usable.
- [ ] Increased font scale remains usable without hiding required controls.
- [ ] Narrow terminal layout remains navigable across all six panes.
- [ ] Challenge Setup remains navigable at narrow width and increased font scale.
- [ ] High-contrast CLI setting remains readable.
- [ ] High-contrast TUI focus/borders remain readable.
- [ ] Reduced-motion preference does not trigger unnecessary animation or fake delays.
- [ ] Data tables remain horizontally/vertically navigable where terminal size requires it.

Evidence / notes:

## Localization

- [ ] English CLI labels/prompts render correctly.
- [ ] Hindi CLI labels/prompts render correctly after `guessnova settings --locale hi`.
- [ ] English TUI workspace labels/status render correctly.
- [ ] Hindi TUI workspace labels/status render correctly after relaunch with a Hindi profile.
- [ ] English Challenge Setup labels/help/errors/status render correctly.
- [ ] Hindi Challenge Setup labels/help/errors/status render correctly.
- [ ] Placeholders and formatted values remain present in both locales.
- [ ] No untranslated catalog key name is exposed to users.
- [ ] Switching to a differently localized profile does not leave the current mounted TUI partially translated.

Evidence / notes:

## Privacy and local-data review

- [ ] No workspace/challenge action unexpectedly requires network access.
- [ ] Challenge status does not expose the hidden target.
- [ ] Recovery backup verification does not import or modify the selected backup/state.
- [ ] Screenshots/support captures are reviewed for profile names, history, paths, seeds/dates, and other local data before sharing.

Evidence / notes:

## Defects and disposition

| Issue | Severity | Reproducible | Fixed in candidate | Follow-up |
| --- | --- | --- | --- | --- |
| | | | | |

## Sign-off

- [ ] No release-blocking accessibility defect remains open.
- [ ] Any accepted non-blocking limitation is documented in `what_changed.md` and the relevant issue.
- [ ] Screenshots/demo media, when published, were captured from this exact signed-off commit or tag.
