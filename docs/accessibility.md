# Accessibility

GuessNova is designed around keyboard-first terminal interaction and text-first meaning.

## Current practices

- No mouse is required for CLI gameplay or the Textual workspace.
- The Textual TUI starts on Play, focuses the numeric guess field on mount, and retains the predictable input → submit → hint gameplay sequence.
- Workspace panes are reachable through `Ctrl+1` through `Ctrl+6`: Play, Profiles, History, Leaderboard, Settings, and Recovery.
- Each workspace shortcut moves focus to a useful first control in the selected pane.
- Plain `Q` and `R` are non-priority application bindings so letters remain typable in profile/search/path inputs. `Ctrl+Q` and `Ctrl+R` remain global quit/reset alternatives.
- The TUI returns focus to the guess field after guesses, hints, and explicit round reset.
- Outcomes, hints, warnings, profile actions, filtering status, and recovery status use descriptive text rather than color alone.
- `--plain` disables Rich CLI color for simpler screen-reader/capture output.
- `--compact` replaces Rich CLI panels/tables with concise text where supported.
- Saved Rich themes use semantic color roles; `settings --high-contrast` applies the dedicated high-contrast palette to the Rich CLI.
- The Textual workspace also applies a high-contrast screen class with stronger card/section borders and visible focus outlines when the active profile has high contrast enabled.
- Textual Switch controls use `animate=False`; GuessNova does not add decorative workspace animation.
- `settings --reduced-motion` persists the user's reduced-motion preference for presentation features; GuessNova adds no fake-delay animation to core gameplay.
- Invalid guesses and invalid workspace fields explain the problem instead of silently failing.
- Timed gameplay is opt-in; classic/daily/reverse play does not require timed input.
- Automatic smart hints can be disabled per profile or overridden per round in CLI flows; the TUI immediately observes the saved active-profile smart-hint preference.
- Explicit `hint` requests do not consume an attempt and clearly state any configured XP penalty.
- Profile deletion is recoverable and requires typed-name confirmation unless the CLI `--yes` override is intentionally supplied. The TUI always requires the selected name to be typed exactly before Delete.
- Switching the active profile resets an unfinished TUI round so a partial game cannot be silently reassigned to another profile.
- TUI Recovery is read-only. State repair remains an explicit Doctor action with its stronger confirmation and backup-before-write semantics.
- Important information remains textual so it can be read from terminal buffers without interpreting icons.
- The display language remains consistent during one running TUI process; a changed profile locale is fully applied on the next launch instead of partially relabeling the mounted interface.

Examples:

```bash
guessnova --plain --compact stats
guessnova --plain --compact profiles list
guessnova settings --high-contrast --reduced-motion
guessnova settings --no-smart-hints
guessnova settings --locale hi
guessnova-tui
```

## Textual workspace keyboard map

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

The tab bar and ordinary Tab/Shift+Tab focus navigation remain available in addition to these shortcuts.

## Automated accessibility-adjacent coverage

Textual pilot tests verify:

- initial guess-field focus;
- legacy gameplay tab order;
- Enter submission;
- range-hint behavior;
- reset behavior;
- result persistence;
- Ctrl+number pane navigation;
- ordinary `q`/`r` typing in text fields;
- profile create/rename/delete/restore;
- exact-name deletion confirmation;
- history filtering and invalid-date handling;
- leaderboard filtering;
- settings persistence;
- read-only backup verification;
- active-profile round isolation;
- stable display locale during profile switches;
- high-contrast state on launch and after settings save.

CLI tests exercise plain/compact-compatible commands and parser behavior. These checks prevent regressions in deterministic interaction logic, but they cannot prove screen-reader quality, real terminal scaling, or visual contrast on every environment.

## Contributor checklist

- Preserve logical input/focus order.
- Keep all actions keyboard accessible.
- Do not encode success/warning/error using color only.
- Add new Rich colors through semantic theme roles rather than hard-coded state colors.
- Keep Textual high-contrast selectors focused on structure/focus visibility rather than color-only meaning.
- Keep labels and prompts concise and explicit.
- Test narrow terminals and enlarged font settings.
- Avoid unnecessary animation/fake delays; respect reduced-motion preferences when animation exists.
- Maintain usable contrast for custom themes.
- Avoid forcing timed interaction outside timed mode.
- Keep a plain/compact path available when adding Rich presentation features.
- Add/update localization keys for new presentation text in every shipped locale.
- Keep destructive local-data actions confirmed and recoverable where practical.
- Keep Recovery inspection separate from repair unless a future design preserves explicit confirmation and backup-before-write guarantees.
- Ensure global shortcuts do not steal normal character input from text-editing controls.

## Manual release evidence

Before every release candidate, copy and complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md). The evidence pass should cover:

- keyboard-only CLI flows;
- plain/compact output;
- TUI Play focus, submission, hint, reset, and quit behavior;
- keyboard traversal and shortcut access for all six workspace panes;
- profile lifecycle confirmation/recovery;
- history and leaderboard filtering;
- Settings switches/selects and focus visibility;
- read-only Recovery and backup-verification presentation;
- narrow terminals and increased font scaling;
- high contrast and reduced motion;
- English and Hindi rendering;
- release-blocking defect disposition.

Automated tests supplement but do not replace this manual review. Screenshots or demo recordings must come from the exact signed-off release build; see [`media/README.md`](media/README.md).

See [`tui_workspace.md`](tui_workspace.md) for the complete v1.4 workspace behavior.
