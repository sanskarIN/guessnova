# Release readiness and 2.0 entry

GuessNova currently has a green reconciled v1.5 engineering baseline on `main`, but package metadata remains at `1.4.0` until the intentionally manual release-evidence gates are complete.

This document describes the remaining path without treating unperformed manual work as complete.

## Current automated state

The reconciliation PR that established the v1.5 Challenge Setup and v2 compatibility baseline passed exact-head CI, Security, CodeQL, Python/browser tests, strict mypy, Ruff, smoke verification, and Ubuntu/Windows/macOS built-wheel checks before merge.

Normal CI now also emits a repository-local readiness report:

```bash
python scripts/release_readiness.py --target-version 1.5.0 --json
```

The report intentionally does not infer GitHub Actions status. Exact-head workflow results remain external evidence that must be checked on the candidate commit.

## Remaining v1.5 manual gate

The committed record `docs/release_evidence/v1.5.0.json` remains `pending` until all of the following are actually completed:

- keyboard-only Challenge Setup and workspace navigation review;
- high-contrast review;
- reduced-motion review;
- English catalog/UI review;
- Hindi catalog/UI review;
- truthful release screenshots from the signed-off candidate;
- truthful demo media from the signed-off candidate.

Do not change any check to `true` merely to satisfy automation.

## Tagged-release protection

The release workflow runs:

```bash
python scripts/verify_manual_release_evidence.py --version "$TAG_VERSION"
```

before lint, tests, packaging, or publication. A pending, missing, malformed, or incomplete record fails the tagged release.

Verification and cross-platform package jobs have read-only repository permissions. Only the final publication job receives `contents: write`, and it runs only after verification and all platform-package jobs succeed.

## When the manual evidence is complete

1. Update `docs/release_evidence/v1.5.0.json` with truthful review metadata and evidence references.
2. Advance package/runtime metadata to `1.5.0` in all canonical version locations.
3. Update `CHANGELOG.md`, `ROADMAP.md`, compatibility metadata, release documentation, and `what_changed.md` together.
4. Run exact-head CI, Security, CodeQL, browser tests, dependency audit, smoke checks, and the Ubuntu/Windows/macOS wheel matrices.
5. Tag `v1.5.0` only after every gate is green.

## Entering the next development version

GuessNova 2.0 development remains gated by `docs/v2_roadmap.md`. The compatibility baseline, 2.0 roadmap, and release checklist already exist, so the first development milestone after v1.5 sign-off is `2.0-alpha.1` compatibility-contract freeze.

No package/runtime version, state schema, backup wrapper, replay format, Doctor protocol, or browser-state marker should be bumped simply to begin planning. A compatibility version changes only when a concrete format or semantic boundary requires it.
