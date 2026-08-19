# Localization

GuessNova keeps presentation messages behind the offline catalog API in `src/guessnova/i18n.py`.

## Shipped locales

- `en` — English, default and fallback locale.
- `hi` — Hindi, complete second shipped catalog used to verify the localization architecture end to end.

`Settings.locale` is persisted per player profile. Use:

```bash
guessnova settings --locale en
guessnova settings --locale hi
```

The next CLI/TUI invocation that uses that profile loads the saved locale. Unknown or malformed persisted locale values safely fall back to English.

## Current localized presentation

Catalog-backed presentation includes:

- onboarding;
- gameplay status/prompts;
- reverse mode;
- statistics/history headings;
- leaderboard headings;
- settings;
- profile-management messages;
- About/data-transfer messages;
- Textual Play labels;
- Textual workspace tab labels;
- Textual profile actions and safety messages;
- Textual history filters/status;
- Textual settings labels/status;
- Textual Recovery diagnostics/backup-verification status.

The Hindi catalog is required to contain every English key. v1.4 adds representative formatting tests for profile-summary and backup-verification messages in both locales.

## TUI locale behavior

The Textual workspace chooses its display locale when the application starts. The mounted controls then remain in that locale for the lifetime of the process.

If the user activates a profile with a different saved locale:

1. the selected profile becomes active immediately;
2. its Settings pane shows the saved locale value;
3. gameplay preferences such as smart hints apply immediately;
4. the already-mounted interface keeps its launch locale;
5. the newly selected locale is fully applied on the next TUI launch.

This avoids a mixed-language interface where only dynamically refreshed labels change while static tab/button labels remain in the old language.

## Stable machine identifiers

Domain identifiers such as mode names (`classic`, `daily`), difficulty identifiers, command names, environment variables, achievement IDs, schema keys, Doctor JSON keys, backup markers, and replay fields intentionally remain stable machine identifiers. They are not translated because doing so would make saves, commands, exports, diagnostics, and replay codes locale dependent.

Some game-engine generated clue/error text is intentionally a domain string today rather than a catalog key. Contributors should not silently change serialized/domain semantics just to translate it; a future semantic-hint/error model should separate meaning from display text before those strings become localized presentation.

## Catalog completeness

`catalog_missing_keys(locale)` compares a shipped locale with the English key set. Automated tests require the Hindi catalog to contain every English key, including formatting placeholders.

When adding or changing a message:

1. Add/update the English key.
2. Update every shipped locale in the same change.
3. Preserve required named placeholders such as `{attempts}`, `{profile}`, `{name}`, `{source}`, or `{integrity}`.
4. Add representative formatting coverage for multi-value messages where practical.
5. Run the localization tests before merging.

## Adding another locale

1. Add a complete catalog mapping with the same keys as `EN_MESSAGES`.
2. Register it in `CATALOGS` using a stable locale identifier such as `fr`.
3. Keep placeholders compatible with the English template.
4. Add tests that compare catalog key sets, resolve representative formatted strings, and verify the locale survives profile serialization.
5. Add Textual workspace formatting/pilot coverage for representative tab/action/status paths.
6. Manually review terminal width, Unicode rendering, punctuation, plural-sensitive messages, focus labels, and screen-reader output.
7. Record manual evidence using `docs/accessibility_evidence_template.md`.
8. Do not translate serialized enum values, replay field names, schema keys, command names, or configuration/environment variable names without an explicit compatibility design.

## Contributor rules

- New user-facing presentation text belongs in the catalog instead of being duplicated across CLI/TUI code when it is normal presentation copy.
- Error strings that form a stable domain/programmatic contract should remain separate from translated presentation copy until a semantic presentation boundary is introduced.
- Never interpolate untrusted text into Rich markup without escaping/sanitization.
- A missing catalog key is a development error and intentionally raises `KeyError`; an unknown locale falls back to English.
- Keep one running TUI process linguistically consistent; avoid partial live relabeling unless every mounted presentation element can be updated atomically.
- Localization remains fully offline: GuessNova uses no translation service, analytics endpoint, or runtime network lookup.

See [`tui_workspace.md`](tui_workspace.md) for the v1.4 workspace behavior.
