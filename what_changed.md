# GuessNova — Work Continuity

## Current milestone

Phase 4/5 release-quality hardening for `v1.0.0` on `main`.

## Completed before this checkpoint

- Python 3.13+ package and console/TUI entry points.
- Core domain models and classic/timed/streak-tagged/reverse/daily gameplay.
- Deterministic RNG, daily seeds, smart hints, replay codes, achievements, settings/themes.
- Local profiles, atomic persistence, leaderboard, validated import/export, security helpers.
- README, MIT license, packaging metadata, initial tests, and several small Conventional Commits.

## Work added in this continuation

- Added editable `assets/guessnova-logo.svg` artwork referenced by README.
- Added `.gitattributes` and `.env.example` repository/environment hygiene.
- Added `CONTRIBUTING.md`, `CHANGELOG.md`, and `ROADMAP.md` where missing.
- Preserved concurrently-added tests and governance files instead of overwriting them.
- Continued with documentation, GitHub automation, CI/security/release checks, and additional verification.

## Important continuity rule

Other work may be landing on `main` from another continuation. Always inspect the latest tree and recent commits before creating/updating a file. Never overwrite a newer useful implementation merely to match an older local draft.

## Verification status

Final commands/workflow results and any discovered fixes will be recorded below before this checkpoint is closed.

## Known limitations

- GitHub connector write actions available in this environment do not expose commit author/committer email fields. Commits created by the connector therefore cannot be forced to use `sanskarin@outlook.in`; the requested email is present in package metadata and should be configured for local Git commits.
- Repository-level settings such as branch protection and enabling Discussions are outside the exposed file/commit actions and must not be falsely claimed as enabled.

## Next exact tasks

1. Complete missing `docs/` pages referenced by README.
2. Add `.github` issue/PR templates, funding config, Dependabot, CI, CodeQL/security, and release workflows.
3. Add/verify `scripts/smoke_test.py` referenced by README.
4. Run/inspect tests and CI; fix every reproducible failure found.
5. Update this file with final commit hashes/messages, workflow results, known limitations, and release notes draft.

## Release notes draft

GuessNova 1.0.0 delivers a privacy-first local number-guessing game with Rich CLI and Textual TUI interfaces, multiple modes, deterministic challenges, smart hints, replay codes, profiles, XP/achievements, local leaderboard, import/export, automated tests, repository automation, and complete project documentation.
