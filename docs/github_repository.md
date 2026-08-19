# GitHub Repository Operations

This page documents repository settings that are not source-controlled by normal files and therefore must be configured in GitHub's repository settings by an administrator.

## Recommended default-branch protection

For `main`:

- Require a pull request before merging for non-emergency changes.
- Require the `CI` test/build jobs, `CodeQL`, and `Security checks` to succeed.
- Require branches to be up to date before merge when practical.
- Block force pushes and branch deletion.
- Require conversation resolution before merge.
- Keep administrator bypass limited to genuine recovery work.
- Prefer linear history only if the chosen merge policy is consistent with it; GuessNova release work currently preserves focused commits with normal merge commits rather than squash-only history.

Do not enable a required check until the corresponding workflow has completed successfully at least once, otherwise maintainers can accidentally make `main` unmergeable.

Source documentation is not evidence that protection is actually enabled. Check repository branch metadata/settings before claiming `main` is protected.

## Current workflow expectations

Pull requests should be evaluated at their exact current head. Superseded runs may be cancelled by concurrency and must not be treated as failures; queued/pending runs must not be recorded as passes.

The CI package matrix is expected to verify built artifacts on Ubuntu, Windows, and macOS, including:

```text
python -m guessnova --help
guessnova doctor --help
guessnova-doctor --help
guessnova-doctor --version
```

plus the end-to-end smoke test.

CodeQL and Security checks remain separate workflows.

## Discussions

GitHub Discussions is optional. If enabled, recommended categories are:

- Announcements — maintainer release/news posts.
- Q&A — setup and gameplay questions.
- Ideas — exploratory feature proposals before an issue is warranted.
- Show and tell — screenshots, themes, challenge results, and integrations.

Security vulnerabilities must use the private route in `SECURITY.md`, not Discussions.

## Labels

Suggested labels:

- `bug`
- `enhancement`
- `documentation`
- `testing`
- `accessibility`
- `security`
- `performance`
- `recovery`
- `compatibility`
- `good first issue`
- `help wanted`
- `dependencies`
- `release`
- `needs reproduction`

Labels should describe work, not people, and should not be created only to inflate repository activity.

## Milestones

Use milestones only when they communicate a real release/maintenance target, for example `v1.1`, `v1.2`, `v1.3`, or a security patch. Keep `ROADMAP.md` as the public product direction and use milestones for actionable issue/PR tracking.

Do not create schema-version milestones solely to force implementation of a nonexistent migration. Compatibility work should follow an actual product/data-format boundary.

## Releases

The source-controlled release workflow builds Python artifacts for semantic version tags. Before tagging, follow `docs/release.md`, verify all required checks for the exact release commit, update `CHANGELOG.md`, and confirm the tagged commit is the intended release candidate.

Release-candidate manual accessibility evidence and authentic screenshot/demo provenance remain separate from automated CI.

Artifact signing/trusted publishing should be enabled only when a concrete package-registry publishing workflow exists; repository docs should not claim a signing mechanism that has not actually been configured.

## Funding

`.github/FUNDING.yml` points to the public Buy Me a Coffee profile where GitHub supports a custom funding URL. Funding must remain optional and must not alter product capabilities.
