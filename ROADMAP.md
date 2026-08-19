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

- [ ] Add real terminal screenshots and a short demo recording captured from a signed-off release build. Capture/provenance rules are complete under `docs/media/`; real media must not be fabricated before sign-off.
- [x] Expand Textual pilot tests for focus order, input submission, reset, hint interactions, and persisted results.
- [x] Add a documented manual accessibility evidence checklist for each release candidate.
- [x] Add richer history result/date/text filtering and grouping by day, mode, difficulty, or result.
- [x] Add profile-management commands for listing, creating, activating, renaming, deleting, viewing recoverable trash, and restoring profiles.
- [x] Make profile deletion recoverable with bounded local trash and retained leaderboard restoration data.
- [x] Persist TUI completed rounds through the same local application service used by the CLI.

## v1.2 — Reliability and portability

- [ ] Add schema-2 migration fixtures when schema 2 is introduced; do not invent a migration before a real schema change exists.
- [x] Add reproducible package build/install/CLI/smoke verification on Windows, macOS, and Linux CI runners.
- [x] Add Hindi as a complete second shipped locale and enforce catalog-key completeness in tests.
- [ ] Evaluate a property-testing dependency only if future parser/state defects demonstrate materially better coverage than the deterministic malformed-input suites already present.

## Release-media gate

The only intentionally incomplete v1.1 item is real screenshot/demo capture. It is a manual release-candidate activity because repository automation cannot truthfully substitute a mock image for a real terminal capture. The exact procedure and provenance requirements are documented in `docs/media/README.md`.

## Future optional edition

A TypeScript/PWA edition may be explored only if it preserves deterministic rules, offline usability, keyboard accessibility, stable challenge/replay semantics, and privacy-first behavior. It is not required for the Python terminal release.
