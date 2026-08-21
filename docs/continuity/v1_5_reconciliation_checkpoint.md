# GuessNova v1.5 Challenge Reconciliation Checkpoint

Date: 2026-08-21

This checkpoint records the clean reconstruction of the Textual Challenge Setup feature on top of the current `main` branch. It exists so future work can continue from verified repository facts without relying on the heavily diverged original v1.5 branch.

## Reconciliation branch

```text
reconcile/v1.5.0-challenge-workspace-20260821
```

Pull request:

```text
#13 — feat: reconcile v1.5 challenge setup onto current main
```

The branch was created directly from:

```text
7a745400bda7eccfa163a3acc8da2fd002b741f5
```

That commit already contained the newer browser/PWA, service/storage, security/reliability, and cross-platform engine hardening work from `main`.

The implementation/test head immediately before this checkpoint document was written is:

```text
031feaa14dd9a59899c865fa6ab5e5a0e85fc04f
```

## Why this branch exists

The original v1.5 PR #11 was no longer safe to merge directly. Its release branch had diverged substantially from `main`, with dozens of feature-side commits and more than one hundred newer main-side commits since the common base.

The current strategy is therefore:

1. keep current `main` as the source of truth;
2. selectively port only the useful challenge-specific work;
3. preserve newer PWA/browser, engine, CI, security, storage, and service changes;
4. add regression coverage around the ported behavior;
5. require exact-head CI/security evidence before merge;
6. bump release metadata only when an actual release candidate is intentionally prepared.

## Feature surface reconstructed

The clean branch now includes:

- immutable `ChallengeConfiguration` state;
- Textual-independent challenge parsing;
- deterministic seeded Classic, Timed, and Streak construction;
- deterministic date-bound Daily construction;
- explicit Reverse exclusion from the numeric challenge form;
- target-free challenge identity/status presentation;
- English and Hindi challenge strings;
- keyboard-friendly mode/difficulty/seed/date controls;
- mode-aware seed/date field enablement;
- additive `tui_challenge_app.py` integration over the stable six-pane workspace;
- `guessnova-tui` routing to the challenge-enabled application;
- configured reset semantics;
- transactional challenge replacement;
- smoke coverage;
- Linux/Windows/macOS built-wheel challenge-app import checks in CI and release workflows.

## Reliability improvements beyond the old PR

The reconstructed feature was not copied blindly.

`ChallengeConfiguration` now validates runtime values even when callers bypass the parser or type hints:

- string mode values are normalized through `GameMode`;
- unknown/non-enum-compatible mode values are rejected;
- invalid difficulty runtime values are rejected safely;
- boolean and fractional manual seeds are rejected;
- non-date manual Daily values are rejected.

The parser also converts malformed seed/date field object types into the same user-facing validation errors used for malformed strings instead of leaking raw attribute/type errors.

## Transactional safety invariant

Starting a configured challenge follows this order:

1. read widget values;
2. parse and validate configuration;
3. build the replacement game;
4. only then replace `app.game` and reset result-save state.

If parsing or construction fails, the current game object, target, attempts, and save state remain intact.

Focused tests cover invalid seed and invalid Daily date preservation.

## Reset invariant

Once a challenge is successfully created from the form, its validated configuration becomes the reset source.

- seeded Classic/Timed/Streak recreate the same deterministic target;
- Daily recreates from the resolved date and therefore the same Daily seed/target;
- attempts and transient round feedback are reset;
- the configuration object stores no hidden target.

## Tests ported and expanded

Focused challenge suites now cover:

```text
tests/test_tui_challenge_accessibility.py
tests/test_tui_challenge_app.py
tests/test_tui_challenge_configuration.py
tests/test_tui_challenge_game_status.py
tests/test_tui_challenge_i18n.py
tests/test_tui_challenge_initial_status.py
tests/test_tui_challenge_mode_fields.py
tests/test_tui_challenge_presenter.py
tests/test_tui_challenge_reset.py
tests/test_tui_challenge_safety.py
tests/test_tui_challenge_widgets.py
```

The configuration suite additionally covers malformed manual/runtime values that were not protected by the original stale branch implementation.

## Cross-platform verification configuration

Normal CI continues to run the existing Python and browser/PWA gates and now additionally imports the challenge-enabled Textual app from the built wheel on:

- Ubuntu;
- Windows;
- macOS.

Tagged-release verification has the equivalent installed-wheel challenge-app import checks while retaining the existing browser/PWA package checks.

No Android/iOS native wrapper is introduced by this work. Mobile support remains the installable PWA path.

## Release metadata policy

The package/runtime version intentionally remains:

```text
1.4.0
```

while PR #13 is under verification.

This reconciliation does not change:

```text
Python state schema       2
backup wrapper            2
legacy backup wrapper     1
replay format             1
Doctor report protocol    1
browser state marker      1
```

No tag should be created merely because the feature branch is named for v1.5.

## CI evidence observed before this documentation commit

For exact implementation/test head:

```text
031feaa14dd9a59899c865fa6ab5e5a0e85fc04f
```

GitHub exposed the following PR-triggered workflow state:

```text
CI               pending, no conclusion yet
Security checks  pending, no conclusion yet
CodeQL           queued, no conclusion yet
```

These states are neither pass nor fail. They prove the PR-triggered workflows are wired, but not that the candidate is green.

Because this checkpoint document itself creates a newer head commit, final merge decisions must use CI/security conclusions from the then-current exact PR head rather than the pre-documentation SHA above.

## Merge policy

Do not merge PR #13 until all of the following are true on the same current head:

- normal CI has a successful conclusion;
- security workflow has a successful conclusion;
- CodeQL has a successful conclusion;
- PR reports mergeable/clean against current `main`;
- no new main-side commits require reconciliation;
- release metadata has not been accidentally advanced without an intentional release decision.

Do not merge the old PR #11 over current `main`.

Once PR #13 is verified and becomes the accepted replacement, PR #11 can be closed as superseded with a clear pointer to #13.

## Documentation

Feature design and usage are documented in:

- `docs/tui_challenges.md`
- `docs/adr/0005-additive-textual-challenge-layer.md`

The current repository handoff remains `what_changed.md`; this checkpoint is deliberately narrower and focuses only on the v1.5 challenge reconciliation.
