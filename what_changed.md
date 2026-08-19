# GuessNova — v1.5 Challenge Workspace Active Handoff

## Current milestone

GuessNova `v1.5.0` is in active development on:

- Repository: `https://github.com/sanskarIN/guessnova`
- Branch: `release/v1.5.0-challenge-workspace-20260819`
- Base `main`: `3b0ae5ba92087e7286b77711d8dfb5df7f132c43`
- Previous shipped source milestone: `v1.4.0`
- Python requirement: `>=3.13`
- License: MIT
- Required Git commit email: `sanskarin@outlook.in`

The complete v1.4 implementation record remains preserved in Git history and in:

- `docs/continuity/v1_4_pr_checkpoint.md`
- `docs/continuity/v1_3_merged_checkpoint.md`

## Why v1.5 exists

The v1.4 workspace already has a tested `build_workspace_game(...)` helper that can construct deterministic configured challenges, but the mounted Play pane still starts only from the preconfigured in-memory game. The next concrete product gap is exposing that proven capability safely inside the Textual workspace.

This milestone must not create a new persistence schema, backup wrapper, replay format, remote service, cloud account, or third locale merely to create activity.

## v1.5 planned product work

1. Add a challenge configuration model suitable for presentation without Textual dependencies.
2. Expose Classic, Timed, Streak, and Daily challenge selection in the mounted Play pane.
3. Expose difficulty selection using the existing difficulty registry.
4. Expose optional deterministic seed input for non-Daily challenges.
5. Expose optional ISO date input for Daily challenges.
6. Keep Reverse mode on its dedicated interaction path rather than pretending it is ordinary numeric guessing.
7. Start a configured round only after validation succeeds.
8. Preserve the current round when configuration validation fails.
9. Make reset repeat the active configured challenge deterministically.
10. Surface the active challenge identity/status without exposing hidden target values.
11. Keep single-letter R/Q ownership restricted to the numeric GuessInput.
12. Preserve profile ownership isolation, local-only storage, read-only Recovery safety, and launch-locale consistency.
13. Add English and Hindi catalog coverage for every new user-facing string.
14. Add helper, pilot/UI, localization, regression, and smoke coverage.
15. Update TUI/workspace/accessibility/testing/release documentation.
16. Bump package/runtime/citation/changelog metadata only after the feature is complete and audited.

## Verification reality at milestone start

The exact v1.4 pull-request head `149fa6ff3dcfbb523386f732feb188a7503991d3` still reports these hosted runs as queued with no conclusion:

- CI `32224689793`
- Security checks `32224689794`
- CodeQL `32224689833`

No pass or failure is claimed for those runs.

The local execution environment still cannot resolve GitHub/package-index hosts, so local dependency-backed execution is not available from this environment. Static review and GitHub-hosted workflows remain the available verification paths unless that limitation changes.

## Compatibility boundaries

Retain unless a real requirement changes them:

- package/runtime/citation version before v1.5 completion: `1.4.0`
- state schema: `2`
- backup wrapper: `2`
- supported legacy backup wrapper: `1`
- replay format: `1`
- Doctor report protocol: `1`

## Next exact tasks

1. Add immutable challenge configuration/presentation helpers and focused tests.
2. Add localized challenge configuration strings in both shipped locales.
3. Wire challenge controls into the Textual Play pane.
4. Add configured-round pilot tests, validation-preservation tests, shortcut tests, and daily/seed determinism tests.
5. Extend smoke coverage.
6. Audit docs, metadata, and workflows.
7. Update this file with exact changed files, verification results, limitations, and recent commits.
