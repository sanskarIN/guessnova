# Accessibility

GuessNova is designed around keyboard-first terminal interaction and text-first meaning.

## Current practices

- No mouse is required for CLI gameplay; Textual provides keyboard focus/navigation.
- The Textual TUI focuses the numeric guess field on mount, keeps a predictable input → submit → hint tab sequence, and returns focus to input after guesses, hints, and resets.
- TUI reset (`R`) and quit (`Q`) bindings are priority bindings so they remain available while the numeric input is focused.
- Outcomes, hints, warnings, and errors use descriptive text rather than color alone.
- `--plain` disables terminal color for simpler screen-reader/capture output.
- `--compact` replaces rich panels/tables with concise text where supported.
- Saved themes use semantic color roles; `settings --high-contrast` applies the dedicated high-contrast palette to the Rich CLI.
- `settings --reduced-motion` persists the user's reduced-motion preference for presentation features; GuessNova adds no fake-delay animation to core gameplay.
- Invalid guesses explain the problem instead of silently failing.
- Timed gameplay is opt-in; classic/daily/reverse play does not require timed input.
- Automatic smart hints can be disabled per profile or overridden per round.
- Explicit `hint` requests do not consume an attempt and clearly state any configured XP penalty.
- Profile deletion is recoverable and requires typed-name confirmation unless `--yes` is intentionally supplied.
- Important information remains textual so it can be read from terminal buffers without interpreting icons.

Examples:

```bash
guessnova --plain --compact stats
guessnova --plain --compact profiles list
guessnova settings --high-contrast --reduced-motion
guessnova settings --no-smart-hints
guessnova settings --locale hi
```

## Automated accessibility-adjacent coverage

Textual pilot tests verify initial focus, tab order, Enter submission, range-hint behavior, reset behavior, and result persistence. CLI tests exercise plain/compact-compatible commands and parser behavior. These checks prevent regressions in deterministic interaction logic, but they cannot prove screen-reader quality, real terminal scaling, or visual contrast on every environment.

## Contributor checklist

- Preserve logical input/focus order.
- Keep all actions keyboard accessible.
- Do not encode success/warning/error using color only.
- Add new colors through semantic theme roles rather than hard-coded state colors.
- Keep labels and prompts concise and explicit.
- Test narrow terminals and enlarged font settings.
- Avoid unnecessary animation/fake delays; respect reduced-motion settings when animation exists.
- Maintain usable contrast for custom themes.
- Avoid forcing timed interaction outside timed mode.
- Keep a plain/compact path available when adding Rich presentation features.
- Add/update localization keys for new presentation text.
- Keep destructive local-data actions confirmed and recoverable where practical.

## Manual release evidence

Before every release candidate, copy and complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md). The evidence pass covers:

- keyboard-only CLI flows;
- plain/compact output;
- TUI focus, submission, hint, reset, and quit behavior;
- narrow terminals and increased font scaling;
- high contrast and reduced motion;
- English and Hindi rendering;
- release-blocking defect disposition.

Automated tests supplement but do not replace this manual review. Screenshots or demo recordings must come from the exact signed-off release build; see [`media/README.md`](media/README.md).
