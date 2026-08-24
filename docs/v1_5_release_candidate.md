# GuessNova v1.5 Release Candidate Checklist

This checklist tracks the clean v1.5 Challenge Setup reconciliation built from the hardened `main` line on 2026-08-24.

## Scope already prepared on the reconciliation branch

- [x] Base the work on the latest hardened `main` instead of merging a stale release branch.
- [x] Port the immutable validated challenge configuration layer.
- [x] Port the challenge-enabled Textual application and widgets.
- [x] Preserve current Python engine, Reverse-mode, PWA, IPv6, browser-state, and service-worker hardening from `main`.
- [x] Route the installed `guessnova-tui` entry point to the challenge-enabled workspace.
- [x] Restore focused configuration, presenter, widget, accessibility, reset, localization, initial-state, and safety regression tests.
- [x] Extend the end-to-end smoke test through deterministic challenge parsing/reconstruction/presentation.
- [x] Restore the Challenge Setup guide and architecture decision record.
- [x] Extend the manual accessibility evidence template through Challenge Setup.
- [x] Modernize CI/release/security workflows from `actions/checkout@v4` to `@v7` and `actions/setup-python@v5` to `@v7`.
- [x] Modernize GitHub release publication from `softprops/action-gh-release@v2` to `@v3`.
- [x] Verify both the stable workspace import and challenge-enabled app import in cross-platform built-wheel jobs.
- [x] Bound the Ruff development formatter line to the repository's established formatter contract instead of accepting arbitrary formatter-major behavior changes.

## Automated acceptance gates

These are evidence gates and remain unchecked until GitHub reports success on the exact current branch head.

- [ ] CI test job succeeds: Ruff lint and format, strict mypy, Python tests/coverage, Node/PWA tests, JavaScript syntax, compile, metadata, and smoke.
- [ ] Ubuntu built-wheel package verification succeeds.
- [ ] Windows built-wheel package verification succeeds.
- [ ] macOS built-wheel package verification succeeds.
- [ ] Security dependency audit and secret-material checks succeed.
- [ ] CodeQL Python analysis succeeds.
- [ ] CodeQL JavaScript/TypeScript analysis succeeds.

## Behavioral acceptance gates

- [ ] Invalid seed input leaves the active round unchanged.
- [ ] Invalid Daily date leaves the active round unchanged.
- [ ] Seeded Classic/Timed/Streak configurations rebuild deterministically.
- [ ] Daily configuration rebuilds deterministically for the selected date.
- [ ] Challenge status never reveals the target before legitimate completion.
- [ ] Reset reconstructs the configured deterministic challenge rather than silently switching identity.
- [ ] Reverse remains on its existing dedicated interaction path.
- [ ] Existing profile/history/leaderboard/settings/recovery workspace behavior remains intact.
- [ ] Existing browser/PWA behavior remains intact.

## Compatibility acceptance gates

v1.5 Challenge Setup does not require compatibility-domain migrations.

- [x] Python state schema remains `2`.
- [x] Backup wrapper remains `2` with legacy wrapper `1` support.
- [x] Replay format remains `1`.
- [x] Doctor machine report protocol remains `1`.
- [x] Browser state marker remains `1`.
- [x] Browser localStorage key remains `guessnova.web.v1`.
- [ ] Package/runtime version changes to `1.5.0` only after exact-head automated and manual release gates are accepted.

## Manual release gates

- [ ] Complete keyboard-only Challenge Setup verification.
- [ ] Complete high-contrast Challenge Setup verification.
- [ ] Complete reduced-motion verification where motion is present.
- [ ] Complete English/Hindi presentation review for Challenge Setup.
- [ ] Capture truthful terminal/Textual screenshots from the signed-off build.
- [ ] Capture the short signed-off demo recording following `docs/media/README.md`.

## Release cut

Only after all required gates above are complete:

1. Update package/runtime metadata to `1.5.0`.
2. Synchronize `CHANGELOG.md`, `ROADMAP.md`, release documentation, and `what_changed.md`.
3. Re-run exact-head CI, Security, and CodeQL after the version/documentation cut.
4. Create tag `v1.5.0` only from the accepted commit.
5. Require tagged-release verification to rebuild and validate artifacts rather than trusting branch-local artifacts.
6. Verify the generated GitHub release artifacts and release notes.

## Relationship to older branches

The earlier v1.5 branches remain historical inputs only. The clean release path must preserve the hardened `main` history and should supersede the older challenge PRs after this reconciliation PR is established.

## v2.0 handoff

After v1.5 is accepted, use `docs/v2_roadmap.md` and `docs/adr/0006-v2-compatibility-first-architecture.md` as the entry gate for the 2.0 line. A major package version does not automatically require state-schema, backup-wrapper, replay, Doctor-protocol, or browser-state version changes.
