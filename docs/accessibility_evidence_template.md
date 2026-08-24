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

## Textual TUI — Play

- [ ] Initial focus lands on the guess input.
- [ ] Tab order starts guess input → submit → range hint.
- [ ] Enter submits a guess from the input.
- [ ] Range Hint returns focus to the input and does not consume an attempt.
- [ ] `R` resets the round from normal gameplay focus.
- [ ] `Ctrl+R` resets the round globally and returns to Play.
- [ ] `Q` exits when normal gameplay focus allows the application binding.
- [ ] `Ctrl+Q` exits globally.
- [ ] Winning/losing feedback remains understandable from text alone.
- [ ] A completed TUI round persists exactly one result.

Evidence / notes:

## Textual TUI — Challenge Setup

- [ ] Challenge Setup is reachable with keyboard-only navigation from Play, including backward navigation from the initial guess field.
- [ ] Forward Tab from the initial guess field still follows Guess → Submit → Range Hint before cycling elsewhere.
- [ ] Mode and difficulty selects are keyboard operable.
- [ ] Classic, Timed, and Streak enable the seed field and disable the Daily date field.
- [ ] Daily enables the date field and disables the manual seed field.
- [ ] Reverse is not offered in the numeric Challenge Setup and remains available through its dedicated interaction.
- [ ] Seed/date fields accept ordinary `q` and `r` characters without triggering quit/reset.
- [ ] Start Challenge is keyboard operable and returns focus to the numeric guess field after success.
- [ ] A blank Daily date resolves to an explicit date after a successful start.
- [ ] Invalid seed input reports understandable text, focuses the seed field, and leaves the active round/attempts intact.
- [ ] Invalid Daily date input reports understandable text, focuses the date field, and leaves the active round/attempts intact.
- [ ] Active challenge status identifies mode/difficulty/seed-or-date without revealing the hidden target.
- [ ] `Ctrl+R` on a seeded configured challenge reproduces the validated deterministic challenge while resetting transient round state.
- [ ] `Ctrl+R` on a configured Daily challenge preserves the resolved Daily identity while resetting transient round state.
- [ ] Challenge status/errors remain understandable without relying on color alone.

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
- [ ] Narrow terminal layout remains navigable across all six panes and Challenge Setup.
- [ ] Challenge mode/difficulty/seed/date controls remain reachable at narrow width and enlarged terminal font sizes.
- [ ] High-contrast CLI setting remains readable.
- [ ] High-contrast TUI focus/borders remain readable, including Challenge Setup controls.
- [ ] Reduced-motion preference does not trigger unnecessary animation or fake delays.
- [ ] Data tables remain horizontally/vertically navigable where terminal size requires it.

Evidence / notes:

## Localization

- [ ] English CLI labels/prompts render correctly.
- [ ] Hindi CLI labels/prompts render correctly after `guessnova settings --locale hi`.
- [ ] English TUI workspace labels/status render correctly.
- [ ] Hindi TUI workspace labels/status render correctly after relaunch with a Hindi profile.
- [ ] English Challenge Setup labels/help/status/errors render correctly.
- [ ] Hindi Challenge Setup labels/help/status/errors render correctly after relaunch with a Hindi profile.
- [ ] Seed/date/mode/difficulty formatted values remain present and understandable in both locales.
- [ ] Placeholders and formatted values remain present in both locales.
- [ ] No untranslated catalog key name is exposed to users.
- [ ] Switching to a differently localized profile does not leave the current mounted TUI partially translated.

Evidence / notes:

## Privacy and local-data review

- [ ] No workspace or Challenge Setup action unexpectedly requires network access.
- [ ] Challenge status never exposes the hidden target.
- [ ] Recovery backup verification does not import or modify the selected backup/state.
- [ ] Screenshots/support captures are reviewed for profile names, history, paths, challenge metadata, and other local data before sharing.

Evidence / notes:

## Defects and disposition

| Issue | Severity | Reproducible | Fixed in candidate | Follow-up |
| --- | --- | --- | --- | --- |
| | | | | |

## Sign-off

- [ ] No release-blocking accessibility defect remains open.
- [ ] Any accepted non-blocking limitation is documented in `what_changed.md` and the relevant issue.
- [ ] Screenshots/demo media, when published, were captured from this exact signed-off commit or tag.
