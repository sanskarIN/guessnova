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

## Unreleased — Cross-platform browser/PWA edition

- [x] Add an installable responsive PWA for modern desktop and mobile browsers, including Android, iOS/iPadOS, ChromeOS, Windows, macOS, and Linux browser paths.
- [x] Add Classic, Timed, Streak, Daily, and Reverse browser modes across Easy, Normal, Hard, and Expert difficulties.
- [x] Preserve deterministic Daily Challenge parity between Python and JavaScript through the portable daily-v2 FNV-1a rule.
- [x] Add a standard-library local web server exposed through both `guessnova web` and `guessnova-web`.
- [x] Keep the normal server loopback-only by default and reject path traversal while serving package resources read-only.
- [x] Support explicit IPv6 server binds, URL-safe browser-launch formatting including scoped IPv6 zone identifiers, and deterministic `.js`/`.mjs` MIME types across host operating systems.
- [x] Add responsive, keyboard-accessible, touch-friendly browser presentation with reduced-motion and color-scheme support.
- [x] Add PWA manifest metadata, real 192px/512px raster install icons, iOS home-screen metadata, and offline app-shell caching.
- [x] Keep service-worker cache cleanup and reads namespaced to GuessNova, and await install/activation lifecycle work so unrelated shared-origin caches remain untouched.
- [x] Keep browser gameplay private and local-only with no account, telemetry, analytics, ads, cloud sync, or gameplay backend.
- [x] Keep browser storage explicitly separate from the Python schema-2 local state rather than silently coupling incompatible stores.
- [x] Normalize malformed/stale browser storage before rendering, discard unknown fields, bound counters/history and per-difficulty attempt counts, and retain backward readability for unversioned `guessnova.web.v1` state.
- [x] Keep Reverse-mode whole-number bounds, response sequencing, contradiction recovery, completion guards, and feedback validation aligned between Python and JavaScript engines.
- [x] Cover browser engine and browser-state behavior with deterministic Node tests.
- [x] Run committed browser tests in both normal CI and tagged-release verification.
- [x] Verify browser module syntax and required PWA assets in built wheels across Ubuntu, Windows, and macOS package matrices.

## v1.5 release candidate — Challenge Setup integration

- [x] Reconcile Challenge Setup directly onto the latest hardened `main` instead of merging stale v1.5 branches.
- [x] Add immutable validated Challenge Setup for Classic, Timed, Streak, and Daily modes.
- [x] Keep invalid seed/date validation non-destructive so an active round is not replaced or reset on input failure.
- [x] Keep active challenge presentation target-free and deterministic configured resets reproducible.
- [x] Route the installed Textual entry point to the additive challenge-enabled workspace without replacing existing storage/recovery boundaries.
- [x] Add focused challenge configuration, presenter, widget, accessibility, localization, reset, initial-state, and safety regressions.
- [x] Extend smoke and cross-platform built-wheel checks through the challenge-enabled application.
- [x] Modernize GitHub Actions checkout, Python setup, Node setup, CodeQL, and release-publication toolchain paths.
- [x] Add and enforce a machine-readable compatibility baseline before 2.0 development.
- [x] Define the compatibility-first 2.0 roadmap and release checklist under `docs/v2_roadmap.md` and `docs/v2_release_checklist.md`.
- [x] Require exact-head CI, Security, and CodeQL success for the final release-candidate head.
- [x] Add a machine-readable manual-evidence manifest and block tagged publication while it is pending or incomplete.
- [x] Scope tagged-release repository write permission to the final publication job only.
- [ ] Complete manual Challenge Setup accessibility evidence.
- [ ] Complete truthful signed-off screenshots/demo media.
- [ ] Advance package/runtime metadata to `1.5.0` only after the release gates above are accepted.

## Next-version preparation — portable challenge compatibility

- [x] Publish a strict opt-in portable challenge descriptor version `1` without silently changing the current CLI/Textual seeded-challenge behavior.
- [x] Mirror descriptor validation and deterministic target derivation in Python and browser JavaScript.
- [x] Commit one shared golden-vector fixture consumed by both Python and Node tests for seeded and Daily challenge identity.
- [x] Publish descriptor version `1` in `compatibility.json` and verify the Python/browser version constants agree in CI and release checks.
- [x] Require the browser descriptor module in built-wheel PWA package verification and JavaScript syntax gates.
- [x] Document the descriptor contract, safe seed range, canonical Daily date format, and separation from future state interchange.
- [ ] Audit stable future-version rejection behavior across every remaining versioned compatibility reader before declaring the 2.0 compatibility freeze complete.
- [ ] Integrate portable descriptor identity into normal challenge share/copy flows only after the accepted 1.x release gates are complete.
- [ ] Design portable browser/Python user-data interchange separately; challenge identity alone must never imply state-format compatibility.

## Gated future candidates

These are intentionally not release checkboxes until their prerequisite exists:

- Schema 3 migration fixtures — only after a concrete schema-3 design introduces a real compatibility boundary.
- A third shipped locale — only after native-quality review and the same catalog-completeness guarantees as English/Hindi.
- Artifact signing/provenance beyond current GitHub release traceability — only if a real package-registry publishing workflow is introduced.
- Property-based testing dependency — only if a reproducible defect demonstrates a material coverage gap not addressed by deterministic regression suites.
- Live in-process full relocalization of every mounted Textual widget — only if implemented atomically so the interface cannot become partially translated.
- TUI repair/write actions — only if they preserve explicit confirmation, pre-repair backup guarantees, and a clear separation from read-only inspection.
- Native Android/iOS wrappers — only if they add real platform value beyond the installable PWA and preserve the same offline/privacy guarantees; no APK/AAB/IPA support should be claimed before such artifacts exist and are tested.
- Browser/Python state interchange — only after an explicit versioned interchange format is designed, migrated, validated, and tested; browser state must not be silently treated as Python schema-2 state.

## Release-media gate

The only intentionally manual v1.1 carry-over is real screenshot/demo capture. Repository automation cannot truthfully substitute a mock image for a real terminal capture. The exact capture/provenance procedure is documented in `docs/media/README.md`.
