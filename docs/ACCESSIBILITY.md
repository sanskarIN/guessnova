# Accessibility

This is the concise accessibility reference. The canonical detailed guidance is [`accessibility.md`](accessibility.md).

GuessNova is designed to remain usable without relying on color, animation, sound, or pointer input.

## Current guarantees and practices

- Essential status is expressed with text, not color alone.
- CLI and Textual flows are keyboard-first.
- `--plain` disables color and `--compact` provides reduced presentation where supported.
- Saved high-contrast and reduced-motion preferences are available.
- The TUI initially focuses the guess input and keeps a predictable input → submit → hint focus path.
- Priority `R` reset and `Q` quit bindings remain available while the numeric input has focus.
- Timed interaction is opt-in through timed mode.
- Profile deletion normally requires typed-name confirmation and remains recoverable through bounded local trash.
- English and Hindi are offline presentation locales; stable machine identifiers remain unchanged.

## Release evidence

Automated Textual pilot tests cover focus, submission, hint, reset, and persistence behavior. Every release candidate must also complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md) manually for terminal scaling, contrast, keyboard use, plain/compact output, and locale rendering.

Real screenshots/demo recordings must be captured from the exact signed-off build according to [`media/README.md`](media/README.md); mock media is not acceptable release evidence.
