# GuessNova 2.0 Engineering Roadmap

This document prepares the 2.0 line without pretending that unreleased work already exists. GuessNova remains local-first, deterministic where promised, offline-capable, and privacy-preserving throughout the transition.

## Entry gate

Versioned 2.0 development artifacts start only after the current 1.x release candidate is reconciled onto current `main`, exact-head CI/Security/CodeQL are green, and the manual release-evidence gates are complete.

Compatibility analysis and additive preparation may land before that gate only when it leaves the current shipped interface behavior and package/runtime version unchanged. No 2.0 alpha artifact may be cut from that preparation alone.

The 2.0 preparation branch must not silently change package/runtime version, Python state schema, backup wrapper, replay format, Doctor protocol, or browser-state marker.

## Product goals

GuessNova 2.0 should make the existing terminal, Textual, and browser/PWA experiences feel like one coherent product while preserving the advantages of each surface.

Primary goals:

- deterministic challenge identity that can be represented consistently across supported interfaces;
- explicit compatibility contracts instead of implicit cross-format assumptions;
- stronger install/update/recovery ergonomics;
- first-class accessibility evidence and localization quality gates;
- reproducible developer and release tooling;
- no mandatory account, telemetry, analytics, advertising, cloud sync, or gameplay backend;
- no native-mobile claims unless real native artifacts are implemented, tested, and signed off.

## 2.0-alpha.1 — compatibility contract freeze

- [x] Inventory every persisted or externally visible compatibility domain in `compatibility.json` and `docs/compatibility.md`.
- [x] Publish a machine-readable compatibility matrix for package version, Python state schema, backup wrapper, replay format, Doctor report protocol, browser state marker, and future interchange/challenge formats.
- [x] Keep state schema `2` unless a concrete state-model change requires schema `3`.
- [x] Keep backup wrapper `2` unless a concrete envelope/integrity change requires a new wrapper.
- [x] Keep replay format `1` unless replay semantics actually change.
- [x] Define portable challenge descriptor `1` for opt-in deterministic challenge identity without changing existing TUI/CLI seeded behavior.
- [x] Add shared Python/JavaScript golden fixtures for portable seeded and Daily deterministic target rules.
- [ ] Reject unknown future compatibility versions with stable errors across every inventoried domain. Descriptor-v1 future-version rejection is complete; the full-domain audit remains.

## 2.0-alpha.2 — cross-interface challenge parity

- [ ] Promote validated Challenge Setup from release-candidate work into the normal Textual workspace contract.
- [ ] Ensure Classic, Timed, Streak, Daily, and Reverse semantics remain aligned between Python and browser engines.
- [ ] Define whether Reverse receives a portable challenge descriptor; do not force it into a target-based format.
- [ ] Add interface-parity tests for difficulty bounds, attempts, deterministic seeds, Daily dates, invalid input, completion, and reset behavior.
- [ ] Keep challenge presentation target-free until a round legitimately reveals the target.
- [ ] Add deterministic copy/share challenge identifiers only after the descriptor format is versioned and validated.

## 2.0-alpha.3 — explicit data portability

- [ ] Design a versioned interchange format separate from Python local state and browser localStorage.
- [ ] Document which profile, settings, history, achievement, leaderboard, and challenge fields are portable.
- [ ] Require bounded parsing, normalization, and provenance metadata.
- [ ] Add import preview before mutation.
- [ ] Require an integrity-protected backup before destructive/importing writes to Python state.
- [ ] Never treat browser state as Python schema-2 state directly.
- [ ] Add round-trip and downgrade/future-version rejection fixtures.

## 2.0-beta.1 — install, update, and recovery experience

- [ ] Add a single documented installation matrix for terminal/TUI/PWA surfaces.
- [ ] Add a read-only environment capability report to Doctor for terminal, Textual, and local web/PWA support.
- [ ] Add structured troubleshooting hints while keeping Doctor machine output versioned.
- [ ] Evaluate safe opt-in repair actions for the Textual Recovery pane; keep writes out unless confirmation and backup-before-write guarantees are preserved.
- [ ] Add release-artifact provenance verification if package-registry publishing is introduced.
- [ ] Keep all repair/import operations atomic from the user's perspective.

## 2.0-beta.2 — accessibility and localization quality

- [ ] Make keyboard-only acceptance tests part of every interactive surface's release gate.
- [ ] Preserve reduced-motion and high-contrast behavior in Textual and browser surfaces.
- [ ] Add screen-reader/manual semantic checks to the release evidence template.
- [ ] Keep English and Hindi catalog completeness enforced in CI.
- [ ] Add a third locale only after native-quality review and full catalog-completeness coverage.
- [ ] Implement live Textual relocalization only if every mounted widget can change atomically.

## 2.0-beta.3 — reliability and performance budgets

- [ ] Define startup, state-load, history-filter, package-size, and PWA app-shell budgets.
- [ ] Add deterministic stress fixtures for maximum accepted local-state sizes.
- [ ] Add browser storage corruption/failure stress tests.
- [ ] Add long-history and leaderboard performance regressions.
- [ ] Keep the normal gameplay path dependency-light and offline-capable.
- [ ] Introduce property-based testing only if a reproducible coverage gap justifies the dependency.

## 2.0-rc.1 — release hardening

- [ ] Freeze compatibility versions and migration fixtures.
- [ ] Run exact-head Ruff, mypy, Python tests/coverage, Node tests, JavaScript syntax, smoke, dependency audit, Security, and CodeQL.
- [ ] Build and install wheels on Ubuntu, Windows, and macOS.
- [ ] Verify installed CLI, challenge-enabled Textual app, Doctor, local web server, and packaged PWA assets.
- [ ] Complete manual accessibility evidence.
- [ ] Capture truthful release screenshots and demo media from the signed-off build.
- [ ] Verify upgrade from the latest 1.x release without data loss.

## 2.0 release definition of done

A 2.0 tag is allowed only when:

1. Every compatibility-domain change has a version, migration/rejection rule, fixtures, and documentation.
2. All automated gates are green on the exact tagged commit.
3. Cross-platform built-wheel verification is green.
4. Manual accessibility and release-media evidence is complete.
5. Privacy/offline guarantees are still true and documented.
6. No native Android/iOS artifact is claimed unless it has its own tested release path.
7. `CHANGELOG.md`, `ROADMAP.md`, release docs, and `what_changed.md` agree on shipped behavior.

## Explicit non-goals until gated

The following are not automatically part of 2.0:

- accounts or mandatory cloud sync;
- remote telemetry or analytics;
- advertising SDKs;
- an online gameplay backend;
- schema 3 without a real schema boundary;
- native APK/AAB/IPA wrappers without platform-specific value and test coverage;
- silent browser/Python state interchange;
- dependencies added only to increase feature count.

## Versioning policy during preparation

Preparation commits remain on the current package version until a release branch is intentionally cut. Alpha/beta/RC version bumps should happen only when those artifacts are intended to be built and tested as versioned releases.
