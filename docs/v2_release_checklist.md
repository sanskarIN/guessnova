# GuessNova 2.0 Release Checklist

This is the operational companion to `docs/v2_roadmap.md` and ADR 0006. It intentionally starts as a preparation checklist rather than claiming 2.0 implementation is complete.

## Preparation

- [x] Define compatibility-first 2.0 architecture.
- [x] Define phased 2.0 engineering roadmap.
- [x] Preserve local-first/offline/privacy guarantees as architectural requirements.
- [x] State that compatibility-domain versions advance only for real contract changes.
- [ ] Finish and release the accepted 1.x baseline before cutting 2.0 alpha artifacts.

## Compatibility inventory

- [ ] Record the latest accepted 1.x package version.
- [ ] Record Python state schema and committed migration fixtures.
- [ ] Record backup wrapper and supported legacy wrappers.
- [ ] Record replay format.
- [ ] Record Doctor machine report protocol.
- [ ] Record browser state marker and storage key.
- [ ] Record every deterministic cross-language rule and its golden fixtures.
- [ ] Introduce a portable interchange/challenge protocol version only if its design is accepted.

## Upgrade safety

- [ ] Install the latest accepted 1.x build and create representative profiles, settings, history, leaderboard, and backups.
- [ ] Upgrade that environment to the 2.0 release candidate.
- [ ] Verify accepted 1.x state loads or migrates without silent loss.
- [ ] Verify legacy backups retain their documented import/recovery behavior.
- [ ] Verify unknown future schemas/protocols fail closed with stable diagnostics.
- [ ] Verify failed migrations/imports do not partially mutate persistent state.
- [ ] Verify a pre-write backup exists wherever a 2.0 operation can destructively change Python state.

## Cross-interface behavior

- [ ] Classic parity is documented and tested where parity is promised.
- [ ] Timed parity is documented and tested where parity is promised.
- [ ] Streak parity is documented and tested where parity is promised.
- [ ] Daily parity uses committed Python/JavaScript golden fixtures.
- [ ] Reverse parity covers integer bounds, sequencing, contradictions, completion, and feedback validation.
- [ ] Challenge identity is versioned before it becomes portable/shareable.
- [ ] Browser and Python stores remain separated unless an explicit interchange protocol is used.

## Accessibility

- [ ] CLI plain/compact output remains usable without color.
- [ ] Textual keyboard navigation passes across every pane and Challenge Setup.
- [ ] Browser keyboard navigation passes across all gameplay/settings controls.
- [ ] High-contrast mode has visible structure/focus in Textual.
- [ ] Reduced-motion preferences are respected.
- [ ] Browser system reduced-motion behavior is verified.
- [ ] Manual assistive-technology notes are captured for the release candidate.
- [ ] English and Hindi catalog completeness is green.
- [ ] Any additional locale has native-quality review evidence.

## Reliability and performance

- [ ] Maximum accepted state-size fixtures complete within the documented budget.
- [ ] Large history filtering remains responsive within its budget.
- [ ] Large leaderboard filtering remains responsive within its budget.
- [ ] Browser corrupt/blocked storage falls back safely.
- [ ] Service-worker cache operations remain GuessNova-namespaced.
- [ ] PWA package size/app-shell budget is documented and met.
- [ ] Normal gameplay remains independent of network availability.

## Security and privacy

- [ ] Dependency audit is green.
- [ ] CodeQL Python is green.
- [ ] CodeQL JavaScript/TypeScript is green.
- [ ] Secret-material checks are green.
- [ ] Local web server remains loopback-only by default.
- [ ] Path traversal remains rejected.
- [ ] No account is required for normal gameplay.
- [ ] No telemetry/analytics/advertising is introduced into normal gameplay.
- [ ] No cloud/gameplay backend becomes a runtime dependency of normal gameplay.

## Cross-platform packaging

- [ ] Ubuntu wheel builds, installs, and imports all shipped Python surfaces.
- [ ] Windows wheel builds, installs, and imports all shipped Python surfaces.
- [ ] macOS wheel builds, installs, and imports all shipped Python surfaces.
- [ ] Packaged PWA assets pass the package contract on all three runners.
- [ ] CLI, Textual app, Doctor, and local web entry points execute from the built wheel.
- [ ] Any future native Android/iOS artifact has an independent tested signing/release path before it is advertised.

## Exact-head release gate

- [ ] Ruff lint succeeds.
- [ ] Ruff format check succeeds.
- [ ] Strict mypy succeeds.
- [ ] Python tests and required coverage succeed.
- [ ] Node/browser tests succeed.
- [ ] JavaScript syntax checks succeed.
- [ ] Compile checks succeed.
- [ ] Release metadata checks succeed.
- [ ] Smoke checks succeed.
- [ ] Security workflow succeeds.
- [ ] CodeQL succeeds.
- [ ] Cross-platform built-wheel jobs succeed.
- [ ] Manual accessibility evidence is complete.
- [ ] Truthful signed-off screenshots/demo media are complete.

## Final cut

- [ ] Changelog contains the final 2.0 behavior and compatibility notes.
- [ ] Roadmap reflects what shipped versus what remained gated.
- [ ] `what_changed.md` records exact release evidence and compatibility versions.
- [ ] Tag version equals package version.
- [ ] Tagged workflow rebuilds and validates the release artifacts.
- [ ] Published artifacts are checked after GitHub release creation.
