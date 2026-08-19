# GuessNova Roadmap

The roadmap prioritizes coherent quality improvements over feature count. Core offline gameplay remains fully usable without accounts, network access, or donations.

## v1.0 — Production terminal foundation

- [x] Core guessing engine and deterministic challenge support.
- [x] Classic, timed, streak-tagged, reverse, and daily modes.
- [x] Rich CLI and Textual TUI.
- [x] Profiles, XP, achievements, local leaderboard, replay codes, import/export.
- [x] Local atomic persistence and privacy-first defaults.
- [x] Test, documentation, CI, security, and release baseline.

## v1.1 — UX and accessibility refinement

- [ ] Persistent settings commands/screens for theme, hints, reduced motion, and high contrast.
- [ ] Richer session-history browsing and filtering.
- [ ] More explicit hint controls and optional hint penalties.
- [ ] Real terminal screenshots and demo recording from release builds.
- [ ] Expanded Textual widget/pilot tests and manual accessibility checklist evidence.

## v1.2 — Reliability and portability

- [ ] Additional property/fuzz testing for replay/import parsers.
- [ ] More migration fixtures for long-lived local saves.
- [ ] Reproducible packaging verification on Windows, macOS, and Linux.
- [ ] Internationalization loader with English externalized as the first locale.

## Future optional edition

A TypeScript/PWA edition may be explored only if it preserves deterministic rules, offline usability, keyboard accessibility, and privacy-first behavior. It is not required for the Python terminal release.
