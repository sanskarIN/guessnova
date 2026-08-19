# GuessNova Roadmap

The roadmap prioritizes coherent quality improvements over feature count. Core offline gameplay remains fully usable without accounts, network access, or donations.

## v1.0 — Production terminal foundation

- [x] Core guessing engine and deterministic challenge support.
- [x] Classic, timed, streak-tagged, reverse, and daily modes.
- [x] Rich CLI and adaptive Textual TUI.
- [x] Automatic smart hints plus explicit narrowed-range hints and optional XP penalties.
- [x] Profiles, XP, achievements, local leaderboard, replay codes, import/export, and bounded session history.
- [x] Persistent theme, locale, smart-hint, reduced-motion, high-contrast, and sound preferences.
- [x] First-run onboarding, About information, plain output, and compact output.
- [x] Local atomic persistence, defensive imported-state normalization, and privacy-first defaults.
- [x] English-first externalized message catalog with locale-ready settings.
- [x] Replay parser hardening and deterministic malformed-input/fuzz-style coverage.
- [x] Strict lint, formatting, mypy, test, compile, smoke, build, dependency/security, CodeQL, and release automation baseline.
- [x] Complete contributor/security/privacy/support/release/architecture/accessibility/performance/localization documentation baseline.

## v1.1 — UX and accessibility refinement

- [ ] Add real terminal screenshots and a short demo recording captured from signed-off release builds.
- [ ] Expand Textual widget/pilot tests for focus order, input submission, reset, and hint interactions.
- [ ] Add a documented manual accessibility evidence checklist for each release candidate.
- [ ] Add richer history search/grouping if real user history demonstrates a need beyond mode/difficulty filters.
- [ ] Consider profile-management commands for listing, renaming, and deleting local profiles with safe confirmation/undo semantics.

## v1.2 — Reliability and portability

- [ ] Add more migration fixtures when schema 2 is introduced; do not invent migrations before a schema change exists.
- [ ] Add reproducible packaging verification on Windows, macOS, and Linux runners if repository budget/runner availability supports a matrix.
- [ ] Add a second fully reviewed locale to prove the localization architecture end to end.
- [ ] Evaluate property-testing libraries only if they provide better parser/state coverage than the deterministic malformed-input suites.

## Future optional edition

A TypeScript/PWA edition may be explored only if it preserves deterministic rules, offline usability, keyboard accessibility, stable challenge/replay semantics, and privacy-first behavior. It is not required for the Python terminal release.
