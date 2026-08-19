# GuessNova Definition-of-Done Audit

This document maps the repository against the GuessNova master development requirements. It exists to distinguish **implemented source/repository capability** from **release evidence that still requires a successful runner or manual review**.

Do not convert an evidence gap into a feature rewrite. Do not mark an evidence item complete without actual evidence.

## Status legend

- `[x]` implemented or repository-configured and supported by committed code/tests/docs.
- `[ ]` evidence or work still required.
- `N/A` not applicable to this local Python terminal product.

## Product identity

- [x] Public open-source GuessNova repository.
- [x] MIT license.
- [x] Python 3.13+ primary implementation.
- [x] Windows/macOS/Linux package workflow coverage.
- [x] `Made by the Sanskar` visible in README/About/branding surfaces.
- [x] GitHub, business, support, and Buy Me a Coffee metadata documented.
- [x] Git commit author email policy documented as `sanskarin@outlook.in`.

## Core game capability

- [x] Multiple named difficulty levels.
- [x] Difficulty-specific ranges.
- [x] Difficulty-specific attempt limits.
- [x] Classic mode.
- [x] Timed mode.
- [x] Streak-tagged gameplay integrated with persistent streak statistics.
- [x] Reverse guessing with dedicated `ReverseGuesser` interaction.
- [x] Date-seeded Daily challenge.
- [x] Higher/lower feedback.
- [x] Temperature/direction/parity smart hints.
- [x] Explicit narrowed-range hint.
- [x] Optional hint XP penalty.
- [x] Seeded deterministic challenges.
- [x] Deterministic replay encoding/decoding.
- [x] Local leaderboard.
- [x] Import/export/backup flows.
- [x] XP and achievements.
- [x] Profile statistics and session history.

## v1.5 Textual challenge capability

- [x] Play-pane challenge setup.
- [x] Classic/Timed/Streak/Daily selection.
- [x] Shared difficulty registry selection.
- [x] Optional integer seed for non-Daily numeric modes.
- [x] Daily ISO date configuration.
- [x] Blank Daily date resolves to the local current date.
- [x] Reverse excluded from the ordinary numeric challenge form.
- [x] Validation occurs before replacing the active round.
- [x] Invalid setup preserves current target/attempt state.
- [x] Mode-aware enablement of seed/date fields.
- [x] Target-free active challenge status.
- [x] Deterministic seeded reset.
- [x] Deterministic Daily reset.
- [x] Initial Guess focus preserved.
- [x] Guess → Submit → Hint forward-Tab flow preserved.
- [x] Challenge setup reachable through keyboard navigation.
- [x] Plain Q/R remain local to GuessInput rather than global.
- [x] English/Hindi challenge strings kept key-complete.

## Profiles, statistics, and local data

- [x] Multiple local profiles.
- [x] Active profile selection.
- [x] Profile create/rename.
- [x] Recoverable profile deletion.
- [x] Profile restore.
- [x] Bounded recoverable trash.
- [x] Profile ownership isolation for unfinished rounds.
- [x] Games played/won.
- [x] Win rate.
- [x] Average winning guesses.
- [x] Current/best streak.
- [x] XP.
- [x] Achievement collection.
- [x] Bounded history.
- [x] History filtering/search/grouping in CLI.
- [x] History filtering in TUI.
- [x] Leaderboard filtering in TUI.

## UX and accessibility

- [x] First-run onboarding.
- [x] Rich CLI.
- [x] Plain output option.
- [x] Compact output option.
- [x] Semantic terminal themes.
- [x] High-contrast preference.
- [x] Reduced-motion preference.
- [x] Automatic smart-hint preference.
- [x] Keyboard-first Textual workspace.
- [x] Visible focus treatment.
- [x] Text status rather than color-only result meaning.
- [x] Read-only Recovery in everyday TUI.
- [x] Exact-name confirmation for TUI profile deletion.
- [x] English/Hindi externalized catalogs.
- [x] Running TUI keeps one coherent launch locale.
- [ ] Manual accessibility evidence for the exact v1.5 release candidate must be completed using `docs/accessibility_evidence_template.md`.

## Privacy and security

- [x] No required account/sign-in.
- [x] No analytics or telemetry.
- [x] No cloud sync.
- [x] No remote leaderboard.
- [x] No runtime application API dependency.
- [x] Local state normalization and schema validation.
- [x] Bounded state reads.
- [x] Bounded state writes.
- [x] Atomic state replacement.
- [x] Bounded backup reads.
- [x] Backup v2 SHA-256 payload integrity.
- [x] Legacy backup compatibility where supported.
- [x] Read-only backup preflight.
- [x] Doctor state diagnostics.
- [x] Doctor safe repair with pre-repair backup.
- [x] Future-schema rejection.
- [x] Replay length/checksum/field/range validation.
- [x] Security policy and responsible-disclosure guidance.
- [x] Dependency/security workflow.
- [x] CodeQL workflow.
- [x] Secret-material checks in repository automation.

## Persistence and compatibility

- [x] Explicit state schema.
- [x] Schema migration tests/fixtures.
- [x] Schema 0/1 → current migration support.
- [x] State schema currently `2`.
- [x] Backup wrapper currently `2`.
- [x] Legacy backup wrapper `1` supported.
- [x] Replay format currently `1`.
- [x] Doctor machine-report protocol currently `1`.
- [x] v1.5 challenge UI requires no serialized-format change.

## Architecture and code quality

- [x] Modular-monolith architecture.
- [x] Domain engine free of Textual/Rich/filesystem dependencies.
- [x] Explicit `Storage` boundary.
- [x] Explicit `GameService` boundary.
- [x] Textual-independent workspace helpers.
- [x] v1.5 challenge parser/configuration separated from widgets.
- [x] v1.5 localized challenge presentation separated from widgets.
- [x] v1.5 challenge widget layer separated from integration layer.
- [x] Strict mypy configured.
- [x] Ruff lint configured.
- [x] Ruff format check configured.
- [x] pytest configured.
- [x] No microservice/network layer added for an offline terminal game.

## Automated testing surfaces

- [x] Domain engine tests.
- [x] Replay parser malformed-input coverage.
- [x] Backup integrity/importability tests.
- [x] State normalization/migration tests.
- [x] Profile lifecycle tests.
- [x] Doctor diagnostics/repair tests.
- [x] Textual pilot tests.
- [x] TUI profile/history/leaderboard/settings/recovery tests.
- [x] v1.5 challenge configuration tests.
- [x] v1.5 challenge widget tests.
- [x] v1.5 configured-round integration tests.
- [x] v1.5 invalid-config preservation regressions.
- [x] v1.5 deterministic-reset regressions.
- [x] v1.5 keyboard regressions.
- [x] v1.5 localization completeness tests.
- [x] Smoke test covers critical local product paths.
- [x] Compile step configured.
- [x] Release metadata verifier configured.

## CI/package/release automation

- [x] Linux primary quality job.
- [x] Linux built-wheel package job.
- [x] Windows built-wheel package job.
- [x] macOS built-wheel package job.
- [x] Twine distribution validation.
- [x] Installed game CLI verification.
- [x] Installed stable Textual workspace import verification.
- [x] Installed v1.5 challenge Textual app import verification.
- [x] Installed Doctor route verification.
- [x] Installed standalone Doctor route verification.
- [x] Smoke test in package matrices.
- [x] Tagged release quality gate.
- [x] Tagged release artifact build.
- [ ] Obtain successful final-head CI conclusions for the v1.5 release candidate.
- [ ] Obtain successful final-head Security checks conclusion for the v1.5 release candidate.
- [ ] Obtain successful final-head CodeQL conclusion for the v1.5 release candidate.

Configured workflows are not equivalent to passed workflows. The unchecked items above require actual GitHub runner evidence.

## Documentation and repository quality

- [x] README.
- [x] LICENSE.
- [x] CONTRIBUTING.
- [x] CODE_OF_CONDUCT.
- [x] SECURITY.
- [x] SUPPORT.
- [x] PRIVACY.
- [x] CHANGELOG.
- [x] ROADMAP.
- [x] `what_changed.md` continuity process.
- [x] Setup/development/testing/release/troubleshooting/accessibility/performance docs.
- [x] Architecture documentation and ADRs.
- [x] Issue templates.
- [x] Pull-request template.
- [x] Dependency-update configuration.
- [x] Funding configuration.
- [x] GitHub repository operations/branch-protection guidance.
- [x] Real-media provenance procedure.
- [ ] Capture real release screenshots/demo from the exact signed-off build after automated/manual release evidence is complete.

## Performance

- [x] Persistence collections are bounded where growth matters.
- [x] TUI History/Leaderboard presentation is bounded.
- [x] No runtime network latency dependency.
- [x] Performance documentation exists.
- [x] No speculative caching/index/database layer added without a measured need.

## Not applicable / intentionally not added

- `N/A` Database indexes: persistence is bounded local JSON rather than a database.
- `N/A` Web cookie/session/CORS/CSP/CSRF controls: no web service is shipped.
- `N/A` Mobile touch targets/splash behavior: current primary product is terminal-based.
- `N/A` Server loading/skeleton network states: no remote runtime data source exists.
- `N/A` Cloud authentication/authorization: no cloud account model exists.
- `N/A` Database transaction framework: state writes use local atomic replacement and guarded multi-step storage operations.

## Optional future candidates, not current definition-of-done blockers

These should be pursued only with a coherent product reason and complete tests/docs:

- atomic full in-process relocalization of all mounted Textual widgets;
- a dedicated Textual Reverse interaction instead of CLI-only Reverse;
- an optional offline TypeScript/PWA edition preserving deterministic challenge rules and privacy/accessibility guarantees;
- a third locale after native-quality review;
- package-registry trusted publishing/signing if a real registry workflow is introduced;
- property-based testing dependency if a reproducible defect demonstrates a coverage gap.

## Release-evidence rule

GuessNova must not be called fully release-verified while any required final-head automated/manual evidence item above is unchecked.

Repository implementation can be complete while release evidence is pending. Record the distinction precisely in `what_changed.md` and release notes.
