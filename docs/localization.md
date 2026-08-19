# Localization

GuessNova ships English first while keeping presentation messages behind a small catalog API in `src/guessnova/i18n.py`.

## Current behavior

- `en` is the default and currently shipped locale.
- `Settings.locale` is persisted per player profile.
- `guessnova settings --locale en` selects the current locale.
- Rich CLI onboarding, gameplay status, statistics/history headings, settings, About, data-transfer messages, and Textual core labels resolve through the catalog.
- Domain identifiers such as mode names (`classic`, `daily`) and serialized keys remain stable English identifiers so saves/replay codes do not change when display languages are added.
- Unknown persisted locales safely fall back to English.

## Adding a locale

1. Add a complete catalog mapping with the same keys as `EN_MESSAGES`.
2. Register it in `CATALOGS` using a stable locale identifier such as `hi` or `fr`.
3. Keep placeholders identical to the English template; for example `{attempts}` must remain available when a translated template uses it.
4. Add tests that compare catalog key sets, resolve representative formatted strings, and verify the locale survives profile serialization.
5. Manually review terminal width, Unicode rendering, punctuation, plural-sensitive messages, and screen-reader output.
6. Do not translate serialized enum values, replay field names, schema keys, command names, or configuration/environment variable names without an explicit compatibility design.

## Contributor rules

- New user-facing presentation text should be added to the catalog instead of duplicated across CLI/TUI code.
- Error strings that form a stable programmatic/API contract should remain separate from translated presentation copy.
- Never interpolate untrusted text into Rich markup without considering markup escaping/sanitization.
- A missing catalog key is a development error and intentionally raises `KeyError`; an unknown locale falls back to English.

This architecture keeps localization optional and offline: no translation service, analytics endpoint, or network lookup is used at runtime.
