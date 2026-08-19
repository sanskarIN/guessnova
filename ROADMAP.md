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

- [x] Introduce schema 2 only after a concrete schema boundary existed: recoverable profile trash is now a canonical top-level state container.
- [x] Add committed schema-1 migration fixtures with and without pre-existing recoverable trash.
- [x] Preserve schema-0/schema-1 forward migration while rejecting future schemas.
- [x] Separate backup-wrapper versioning from state-schema versioning.
- [x] Add backup-v2 SHA-256 payload integrity and wrapper/payload schema provenance checks.
- [x] Preserve import compatibility for legacy GuessNova version-1 backups.
- [x] Add local `guessnova-doctor` diagnostics with compact/JSON output.
- [x] Add safe repair that writes an integrity-protected pre-repair backup before normalization.
- [x] Add reproducible package build/install/game-CLI/doctor-CLI/smoke verification on Windows, macOS, and Linux CI runners.
- [x] Add Hindi as a complete second shipped locale and enforce catalog-key completeness in tests.
- [x] Reassess property-testing dependency need: no new dependency is added because current defects are covered by deterministic migration, malformed-input, replay, backup-integrity, and state-normalization regression suites; revisit only when a reproducible gap demonstrates material benefit.

## v1.3 — Operator UX and recovery hardening

- [x] Expose Doctor as `guessnova doctor` while retaining `guessnova-doctor` for compatibility.
- [x] Route `python -m guessnova` and the installed `guessnova` script through the same top-level dispatcher.
- [x] Keep Doctor discoverable from root help without duplicating the established game CLI parser.
- [x] Add explicit `--data-dir` diagnostics for support/recovery workflows.
- [x] Add read-only `--verify-backup` inspection without importing or rewriting state.
- [x] Prove a backup payload can pass current state normalization before reporting it as valid.
- [x] Report legacy wrapper status, integrity protection, source schema, normalized schema, normalization changes, and normalized state counts.
- [x] Add Doctor machine report protocol version `1` and stable exit code semantics.
- [x] Add Doctor version reporting tied to the package runtime version.
- [x] Bound local state reads and writes before JSON processing/persistence.
- [x] Validate backup envelopes from one bounded read rather than validating and reporting from separate reads.
- [x] Keep backup capacity larger than accepted state capacity so mandatory pre-repair backup can represent any accepted state.
- [x] Extend smoke, Makefile, normal CI, and tagged-release package matrices through both Doctor entry paths.
- [x] Add canonical and concise Doctor/recovery documentation.

## v1.4 — Full Textual local workspace

- [x] Expand `guessnova-tui` from one gameplay card into Play, Profiles, History, Leaderboard, Settings, and Recovery panes.
- [x] Preserve Play as the initial pane with deterministic initial guess-input focus and existing persisted gameplay behavior.
- [x] Add Ctrl+1…Ctrl+6 direct pane navigation plus global Ctrl+R reset and Ctrl+Q quit.
- [x] Scope plain `Q`/`R` to the numeric Play input so legacy reset/quit remains available there while workspace text fields receive ordinary letters normally.
- [x] Add active-profile summary and achievement visibility in the TUI.
- [x] Add local profile use/create/rename/recoverable-delete/restore actions without duplicating storage semantics.
- [x] Require exact selected-name confirmation before TUI profile deletion.
- [x] Reset unfinished gameplay whenever active-profile ownership changes so a partial round cannot be recorded under another profile.
- [x] Add newest-first bounded History table with result/mode/difficulty/search/date filters and safe invalid-date behavior.
- [x] Add local Leaderboard table with mode/difficulty/player filters while preserving existing rank order.
- [x] Add Settings controls for theme, locale, reduced motion, high contrast, sound, and smart hints using the existing settings model.
- [x] Apply Textual high-contrast borders/focus treatment immediately and keep Switch animation disabled.
- [x] Keep one running TUI linguistically consistent; a changed profile locale is fully applied on the next launch rather than partially relabeling mounted widgets.
- [x] Add read-only local diagnostics and read-only backup verification in the Recovery pane while keeping repair in Doctor.
- [x] Extract Textual-independent workspace helpers for snapshots, profile summaries, deterministic challenge construction, history selection, leaderboard filtering, and settings persistence.
- [x] Add focused helper tests and Textual pilot suites for navigation, lifecycle, filtering, settings, Recovery, round isolation, locale consistency, and high contrast.
- [x] Extend smoke coverage through workspace helpers.
- [x] Verify built-wheel Textual workspace imports on Ubuntu, Windows, and macOS in normal CI and tagged-release matrices.
- [x] Add canonical/concise TUI workspace documentation and expand the manual accessibility evidence gate through all six panes.
- [x] Keep state schema `2`, backup wrapper `2`, replay `1`, and Doctor report `1` because v1.4 does not change those compatibility domains.

## v1.5 — In-Play challenge workspace

- [x] Add validated challenge setup inside the shipped Textual Play experience without replacing the v1.4 workspace.
- [x] Expose Classic, Timed, Streak, and Daily numeric challenge selection.
- [x] Keep Reverse on its dedicated interaction path rather than presenting it as ordinary target guessing.
- [x] Reuse the shared difficulty registry for TUI challenge choices.
- [x] Add optional deterministic integer seed configuration for Classic/Timed/Streak.
- [x] Add Daily ISO-date configuration with blank date resolving to the local current date.
- [x] Add immutable `ChallengeConfiguration` and reusable parser/reconstruction helpers outside Textual.
- [x] Validate configuration and construct the replacement game before mutating the active round.
- [x] Preserve the current round, attempts, and result-save state after invalid seed/date input.
- [x] Disable irrelevant seed/date fields when the selected mode changes.
- [x] Normalize accepted seed/date values after a successful challenge start.
- [x] Show target-free active challenge identity for configured and pre-existing numeric games.
- [x] Make seeded and Daily configured resets reconstruct from validated configuration.
- [x] Preserve guess-first startup and Guess → Submit → Hint forward-Tab navigation.
- [x] Keep plain `Q/R` ownership scoped to numeric `GuessInput`; challenge text fields remain ordinary inputs.
- [x] Add English/Hindi challenge strings with catalog completeness retained.
- [x] Add focused configuration/presentation/widget/integration/safety/reset/keyboard/localization tests.
- [x] Extend smoke coverage through challenge parser/configuration/presentation helpers.
- [x] Route the installed `guessnova-tui` script to the challenge-enabled application layer.
- [x] Verify both the stable workspace and shipped challenge app are imported from built wheels in Linux/Windows/macOS CI and release package matrices.
- [x] Add dedicated challenge documentation and a definition-of-done audit.
- [x] Keep state schema `2`, backup wrapper `2`, replay `1`, and Doctor report `1` because challenge configuration is in-memory UI/application state.
- [ ] Complete final-head v1.5 CI, Security checks, and CodeQL evidence.
- [ ] Complete the manual v1.5 accessibility evidence checklist on the exact release candidate.

## Gated future candidates

These are intentionally not release checkboxes until their prerequisite exists:

- Schema 3 migration fixtures — only after a concrete schema-3 design introduces a real compatibility boundary.
- A third shipped locale — only after native-quality review and the same catalog-completeness guarantees as English/Hindi.
- Artifact signing/provenance beyond current GitHub release traceability — only if a real package-registry publishing workflow is introduced.
- Property-based testing dependency — only if a reproducible defect demonstrates a material coverage gap not addressed by deterministic regression suites.
- Live in-process full relocalization of every mounted Textual widget — only if implemented atomically so the interface cannot become partially translated.
- TUI repair/write actions — only if they preserve explicit confirmation, pre-repair backup guarantees, and a clear separation from read-only inspection.

## Release-media gate

The only intentionally manual v1.1 carry-over is real screenshot/demo capture. Repository automation cannot truthfully substitute a mock image for a real terminal capture. The exact capture/provenance procedure is documented in `docs/media/README.md`.

## Future optional edition

A TypeScript/PWA edition may be explored only if it preserves deterministic rules, offline usability, keyboard accessibility, stable challenge/replay semantics, and privacy-first behavior. It is not required for the Python terminal release.
