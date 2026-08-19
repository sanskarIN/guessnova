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

Catalog-backed presentation includes onboarding, gameplay status/prompts, reverse mode, statistics/history headings, settings, profile-management messages, About/data-transfer messages, and Textual core labels.

Domain identifiers such as mode names (`classic`, `daily`), difficulty identifiers, command names, environment variables, achievement IDs, schema keys, and replay fields intentionally remain stable machine identifiers. They are not translated because doing so would make saves, commands, exports, and replay codes locale dependent.

Some game-engine generated clue text is intentionally a domain string today rather than a catalog key. Contributors should not silently change serialized/domain semantics just to translate it; a future semantic-hint model should separate clue meaning from display text before those strings are localized.

## Catalog completeness

`catalog_missing_keys(locale)` compares a shipped locale with the English key set. Automated tests require the Hindi catalog to contain every English key, including formatting placeholders.

When adding or changing a message:

1. Add/update the English key.
2. Update every shipped locale in the same change.
3. Preserve required named placeholders such as `{attempts}`, `{profile}`, or `{name}`.
4. Run the localization tests before merging.

## Adding another locale

1. Add a complete catalog mapping with the same keys as `EN_MESSAGES`.
2. Register it in `CATALOGS` using a stable locale identifier such as `fr`.
3. Keep placeholders compatible with the English template.
4. Add tests that compare catalog key sets, resolve representative formatted strings, and verify the locale survives profile serialization.
5. Manually review terminal width, Unicode rendering, punctuation, plural-sensitive messages, and screen-reader output.
6. Record manual evidence using `docs/accessibility_evidence_template.md`.
7. Do not translate serialized enum values, replay field names, schema keys, command names, or configuration/environment variable names without an explicit compatibility design.

## Contributor rules

- New user-facing presentation text belongs in the catalog instead of being duplicated across CLI/TUI code.
- Error strings that form a stable programmatic/API contract should remain separate from translated presentation copy.
- Never interpolate untrusted text into Rich markup without escaping/sanitization.
- A missing catalog key is a development error and intentionally raises `KeyError`; an unknown locale falls back to English.
- Localization remains fully offline: GuessNova uses no translation service, analytics endpoint, or runtime network lookup.
