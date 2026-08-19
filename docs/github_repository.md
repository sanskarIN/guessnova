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
- Prefer linear history only if the chosen merge policy is consistent with it.

Do not enable a required check until the corresponding workflow has completed successfully at least once, otherwise maintainers can accidentally make `main` unmergeable.

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
- `good first issue`
- `help wanted`
- `dependencies`
- `release`
- `needs reproduction`

Labels should describe work, not people, and should not be created only to inflate repository activity.

## Milestones

Use milestones only when they communicate a real release/maintenance target, for example `v1.1`, `v1.2`, or a security patch. Keep `ROADMAP.md` as the public product direction and use milestones for actionable issue/PR tracking.

## Releases

The source-controlled release workflow builds Python artifacts for semantic version tags. Before tagging, follow `docs/release.md`, verify all required checks, update `CHANGELOG.md`, and confirm the tagged commit is the intended release candidate.

## Funding

`.github/FUNDING.yml` points to the public Buy Me a Coffee profile where GitHub supports a custom funding URL. Funding must remain optional and must not alter product capabilities.
