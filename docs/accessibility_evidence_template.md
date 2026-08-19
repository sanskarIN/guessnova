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

Evidence / notes:

## Plain and compact output

- [ ] `guessnova --plain --compact stats` is readable.
- [ ] `guessnova --plain --compact history` is readable.
- [ ] `guessnova --plain --compact profiles list` is readable.
- [ ] No important state is communicated by color alone.

Evidence / notes:

## Textual TUI

- [ ] Initial focus lands on the guess input.
- [ ] Tab order is guess input → submit → range hint.
- [ ] Enter submits a guess from the input.
- [ ] Range Hint returns focus to the input and does not consume an attempt.
- [ ] `R` resets the round and returns focus to the input.
- [ ] `Q` exits the application.
- [ ] Winning/losing feedback remains understandable from text alone.
- [ ] A completed TUI round persists exactly one result.

Evidence / notes:

## Display and scaling

Test at a normal width and a narrow terminal.

- [ ] 100% terminal font scale is usable.
- [ ] Increased font scale remains usable without hiding required controls.
- [ ] Narrow terminal layout remains navigable.
- [ ] High-contrast CLI setting remains readable.
- [ ] Reduced-motion preference does not trigger unnecessary animation or fake delays.

Evidence / notes:

## Localization

- [ ] English CLI labels/prompts render correctly.
- [ ] Hindi CLI labels/prompts render correctly after `guessnova settings --locale hi`.
- [ ] Placeholders and formatted values remain present in both locales.
- [ ] No untranslated key name is exposed to users.

Evidence / notes:

## Defects and disposition

| Issue | Severity | Reproducible | Fixed in candidate | Follow-up |
| --- | --- | --- | --- | --- |
| | | | | |

## Sign-off

- [ ] No release-blocking accessibility defect remains open.
- [ ] Any accepted non-blocking limitation is documented in `what_changed.md` and the relevant issue.
- [ ] Screenshots/demo media, when published, were captured from this exact signed-off commit or tag.
