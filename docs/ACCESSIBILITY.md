# Accessibility

GuessNova is designed to remain usable without relying on color, animation, sound, or pointer input.

## Principles

- Every essential status has text, not color alone.
- CLI commands and TUI flows are keyboard-first.
- No sound is required; the default sound setting is off.
- Settings include reduced-motion and high-contrast preferences for interface evolution.
- Numeric range, attempts remaining, outcomes, and hints are written in plain language.
- Error messages explain the valid action rather than only reporting failure.

## Terminal recommendations

Use a terminal with a readable monospace font and sufficient contrast. The CLI remains understandable if ANSI colors are disabled by the environment.

## Contributions

Accessibility regressions are treated as defects. Changes to UI copy or interaction should be tested without depending solely on visual styling.
