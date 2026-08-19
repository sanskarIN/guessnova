# ADR 0005 — Additive Textual Challenge Layer

- Status: Accepted
- Date: 2026-08-19
- Decision owners: GuessNova maintainers

## Context

GuessNova v1.4 already had a mature six-pane Textual workspace in `tui.py` and Textual-independent workspace helpers in `tui_workspace.py`. The helper layer could build seeded, Daily, Timed, and Streak numeric games, but the mounted Play pane did not expose those configuration choices.

Adding challenge controls directly into the large v1.4 `GuessNovaApp` would mix three different concerns:

1. parsing/validating challenge configuration;
2. challenge-specific presentation/widgets;
3. stable workspace/profile/history/settings/recovery orchestration.

That would increase regression risk in already-shipped workspace behavior and make the challenge rules harder to test without Textual.

## Decision

Implement v1.5 challenge setup as an additive layer over the stable v1.4 workspace.

### Reusable configuration boundary

`tui_workspace.py` owns the Textual-independent `ChallengeConfiguration`, `parse_workspace_challenge(...)`, and `build_workspace_game(...)` behavior.

The parser accepts presentation-friendly strings and validates them before a replacement `GuessGame` is installed.

### Presentation boundary

`tui_challenge.py` converts validated configuration or an already-created numeric game into localized, target-free status text.

The presenter must never require access to or display the hidden target merely to identify the active challenge.

### Widget boundary

`tui_challenge_widgets.py` owns the challenge form controls and mode-aware seed/date enablement. It does not own persistence, profile mutation, history recording, leaderboard writes, or game rules.

### Integration boundary

`tui_challenge_app.py` subclasses the stable v1.4 `tui.GuessNovaApp` and mounts challenge controls into Play. The installed `guessnova-tui` entry point targets this additive application.

The subclass delegates all unchanged workspace behavior to the v1.4 application and overrides only challenge-specific mounting, challenge start, configured reset, and related button/input routing.

## Transactional challenge-start rule

A replacement round is installed only after:

1. widget values are read;
2. configuration parses successfully;
3. a replacement game constructs successfully.

Validation failure must preserve the active game object, target, attempts, and result-save state.

This prevents partially applied configuration.

## Reverse-mode rule

Reverse mode is excluded from the numeric challenge setup. Reverse asks GuessNova to find a number the user is thinking of, so it has a different interaction contract from entering guesses against a hidden target.

Reverse remains available through its dedicated interface until a dedicated Textual Reverse experience is designed and tested.

## Deterministic reset rule

When a challenge is created through the form, its validated configuration becomes the reset source.

- Seeded Classic/Timed/Streak reconstruct from mode/difficulty/seed.
- Daily reconstructs from mode/difficulty/resolved date.
- Unseeded numeric challenges retain normal random-reset behavior.

The configuration object stores no hidden target.

## Persistence rule

Challenge form state does not create a new serialized persistence domain.

Completed results continue through `GameService`; profile/settings/history/leaderboard data continue through existing `Storage` boundaries. State schema, backup wrapper, replay format, and Doctor report versions are unchanged by this decision.

## Keyboard/accessibility rule

The v1.4 guess-first interaction remains the primary fast path:

- initial focus stays on Guess;
- forward Tab from Guess remains Submit then Range Hint;
- challenge controls are reachable backward;
- plain `Q/R` remain scoped to `GuessInput`;
- challenge seed/date remain ordinary text-editing fields;
- validation/status is textual, not color-only.

## Localization rule

Every challenge-facing string is part of the same offline English/Hindi catalogs as the rest of the product. No widget-owned hard-coded user-facing error/status string should be introduced when a catalog key is appropriate.

## Consequences

### Positive

- Stable v1.4 workspace code changes minimally.
- Challenge parsing is directly unit-testable without Textual.
- Widget behavior and integration behavior have separate focused pilot suites.
- Invalid configuration cannot partially replace a round.
- Future UI refinements can change presentation without changing deterministic challenge construction.
- Existing persistence/recovery contracts remain untouched.

### Costs

- The shipped Textual app is now an additive subclass rather than the original `tui.GuessNovaApp` directly.
- Package/CI/release checks must verify both the stable workspace import and the shipped challenge app import.
- Maintainers must keep the boundary clear rather than gradually moving unrelated v1.4 workspace logic into the challenge subclass.

## Rejected alternatives

### Rewrite `tui.py`

Rejected because a large rewrite would provide little product benefit while increasing regression risk across Profiles, History, Leaderboard, Settings, and Recovery.

### Persist challenge-form state in schema 3

Rejected because no compatibility/persistence requirement justifies a schema change. The configuration is active UI/application state, not durable user data required across launches.

### Treat Reverse as another numeric selector value

Rejected because it would present an interaction that the numeric guess input cannot correctly execute.

### Duplicate game construction in widgets

Rejected because mode/difficulty/seed/date rules would drift from engine/Daily behavior and become harder to test.

## Verification

The decision is enforced through:

- configuration invariant/parser tests;
- seeded/Daily reconstruction tests;
- target-free presenter tests;
- widget defaults/mode-state tests;
- configured-round pilot tests;
- invalid-config preservation tests;
- deterministic reset tests;
- keyboard/focus regressions;
- localization completeness checks;
- built-wheel stable/shipped Textual import checks;
- smoke coverage through configuration and presentation helpers.

Manual release-candidate accessibility evidence remains required in addition to automated checks.
