# Accessibility

GuessNova is designed around keyboard-first terminal interaction.

## Current practices

- No mouse is required for CLI gameplay; Textual provides keyboard focus/navigation.
- Outcomes and hints use descriptive text rather than color alone.
- Invalid guesses explain the problem instead of silently failing.
- Timed gameplay is opt-in; classic/daily/reverse play does not require timed input.
- Profile settings include reduced-motion and high-contrast preferences for continued UI development.
- Important information remains textual so it can be read from terminal buffers and logs without interpreting icons.

## Contributor checklist

- Preserve logical input/focus order.
- Keep all actions keyboard accessible.
- Do not encode success/warning/error using color only.
- Keep labels and prompts concise and explicit.
- Test narrow terminals and enlarged font settings.
- Avoid unnecessary animation/fake delays; respect reduced-motion settings when animation exists.
- Maintain usable contrast for custom themes.
- Avoid forcing timed interaction outside timed mode.

## Manual review

Before a release, manually verify CLI and TUI flows using keyboard only, high-contrast settings, a narrow terminal, and increased font scaling. Automated tests supplement but do not replace this review.
