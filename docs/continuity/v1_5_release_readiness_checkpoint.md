# GuessNova v1.5 release-readiness checkpoint

Date: 2026-08-24

## Merged baseline

PR #14 (`feat: reconcile v1.5 challenge setup and prepare v2 architecture`) merged into `main` as commit `9e3c24db7653b500aacb31b68a59739f586e8059` after its final exact head passed CI, Security, CodeQL, Python/browser tests, Ruff, strict mypy, smoke checks, and Ubuntu/Windows/macOS built-wheel verification.

The merge completes the engineering reconciliation. It does not complete the intentionally manual release-evidence gate and does not create a v1.5 tag.

## Follow-up release-safety branch

Branch: `release/v1.5-readiness-v2-entry-20260824`

This branch adds:

- `docs/release_evidence/README.md` defining the truthful manual-evidence contract;
- pending `docs/release_evidence/v1.5.0.json` sign-off metadata;
- `scripts/verify_manual_release_evidence.py` with strict validation and regression tests;
- `scripts/release_readiness.py` for repository-local status reporting without pretending to know external CI state;
- normal-CI readiness reporting for target version `1.5.0`;
- tagged-release fail-fast enforcement of approved manual evidence;
- read-only default permissions in the tagged-release workflow;
- `contents: write` scoped only to the final release-publication job;
- per-tag release concurrency to prevent duplicate publication jobs racing;
- `docs/release_readiness.md` with the v1.5-to-v2 handoff procedure;
- an explicit 2.0 entry-gate status section in `docs/v2_roadmap.md`.

## Compatibility state

No compatibility domain is bumped by this preparation work:

```text
package/runtime version  1.4.0
Python state schema       2
backup wrapper            2
legacy backup wrapper     1
replay format             1
Doctor report protocol    1
browser state marker      1
browser localStorage key  guessnova.web.v1
portable interchange      not defined
challenge descriptor      not defined
```

## Remaining v1.5 gate

The following work is intentionally not automated or fabricated:

- keyboard-only Challenge Setup/workspace review;
- high-contrast and reduced-motion review;
- English and Hindi UI/catalog review;
- signed-off screenshots from the intended release candidate;
- signed-off demo media from the intended release candidate.

Until those checks are actually performed, `docs/release_evidence/v1.5.0.json` must remain `pending` and package metadata must remain `1.4.0`.

## Next version entry

After truthful v1.5 evidence is approved:

1. advance all canonical package/runtime metadata to `1.5.0`;
2. rerun exact-head CI, Security, CodeQL, dependency audit, smoke, browser, and cross-platform built-wheel gates;
3. tag/release `v1.5.0` only if those gates pass;
4. then enter `2.0-alpha.1` under `docs/v2_roadmap.md`.

The next major line starts with compatibility-contract freeze, not an artificial schema or protocol bump.
