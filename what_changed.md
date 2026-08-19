# GuessNova — v1.5 Challenge Workspace Active Handoff

## Current milestone

GuessNova `v1.5.0` implementation is prepared on:

- Repository: `https://github.com/sanskarIN/guessnova`
- Branch: `release/v1.5.0-challenge-workspace-20260819`
- Pull request: `https://github.com/sanskarIN/guessnova/pull/11`
- PR base: `main`
- Base `main` SHA: `3b0ae5ba92087e7286b77711d8dfb5df7f132c43`
- Previous source milestone: `v1.4.0`
- Prepared package/runtime/citation version: `1.5.0`
- Python requirement: `>=3.13`
- License: MIT
- Required Git commit email: `sanskarin@outlook.in`

The v1.4 implementation record remains preserved in Git history and continuity documentation. This file records the active v1.5 work rather than duplicating the previous milestone in full.

## Milestone purpose

The v1.4 workspace already had deterministic challenge construction helpers, but the mounted Play pane could not configure those challenges. v1.5 closes that concrete gap without changing the local state schema, backup wrapper, replay format, Doctor protocol, account model, or network behavior.

## Product implementation completed on this branch

### Challenge configuration model

`src/guessnova/tui_workspace.py` now provides an immutable `ChallengeConfiguration` and `parse_workspace_challenge(...)` boundary.

The configuration layer:

- accepts stable mode/difficulty identifiers;
- rejects Reverse from ordinary numeric challenge setup;
- validates difficulty through the shared `DIFFICULTIES` registry;
- parses optional whole-number seeds for Classic/Timed/Streak;
- parses Daily dates as ISO `YYYY-MM-DD`;
- resolves a blank Daily date to the local current date;
- prevents a Daily configuration from carrying a manual seed;
- prevents non-Daily configurations from carrying a Daily date;
- reconstructs deterministic seeded/Daily games without storing a hidden target.

`build_workspace_game(...)` delegates through this validated model instead of duplicating construction rules.

### Challenge presentation

New `src/guessnova/tui_challenge.py` provides localized target-free challenge identity helpers.

Identity can report:

- mode;
- difficulty;
- deterministic seed;
- resolved Daily date;
- unseeded/random state.

The hidden target is deliberately excluded from the challenge identity contract.

### Challenge form

New `src/guessnova/tui_challenge_widgets.py` provides the mounted Challenge Setup widget with:

- Classic/Timed/Streak/Daily mode selection;
- shared difficulty selection;
- optional seed input;
- Daily date input;
- Start Challenge action;
- localized help/status;
- visible mode/difficulty context;
- mode-aware field state.

Daily disables seed and enables date. Classic/Timed/Streak enable seed and disable date. Reverse is not shown in this numeric setup.

### Challenge-enabled Textual application

New `src/guessnova/tui_challenge_app.py` subclasses the stable v1.4 workspace rather than rewriting it.

The installed `guessnova-tui` entry point now routes to this challenge-enabled layer.

A configured challenge start follows parse/build-before-mutate ordering:

1. read form values;
2. parse/validate configuration;
3. construct the replacement game;
4. only then replace the active round;
5. normalize accepted seed/date fields;
6. update range/attempt display;
7. clear stale guess/feedback state;
8. show target-free identity;
9. return focus to Guess.

Invalid configuration leaves the current `GuessGame`, target, attempts, and result-save state intact and focuses the relevant field.

### Deterministic configured reset

For a challenge created through the form:

- seeded Classic/Timed/Streak reset from mode/difficulty/seed;
- Daily resets from mode/difficulty/resolved date;
- deterministic configuration therefore reproduces the same seeded target;
- unseeded challenges retain normal random reset semantics.

The validated configuration is the reset source rather than mutable widget text.

### Keyboard/accessibility behavior

The v1.4 fast-play interaction remains intact:

- initial focus is Guess;
- forward Tab remains Guess → Submit → Range Hint;
- Challenge Setup is reachable backward from Guess;
- successful challenge start returns focus to Guess;
- invalid seed focuses Seed;
- invalid Daily date focuses Date;
- plain `Q/R` remain scoped to the numeric `GuessInput`;
- challenge/profile/search/path fields receive ordinary characters;
- global `Ctrl+Q`/`Ctrl+R` remain available.

### Localization

`src/guessnova/i18n.py` contains complete English and Hindi Challenge Setup strings for:

- title;
- mode/difficulty context;
- seed/date placeholders;
- Start action;
- help;
- active identity;
- seed/date/random details;
- localized validation wrapper.

Hindi catalog completeness remains enforced against the English key set.

### Persistence/privacy compatibility

v1.5 Challenge Setup is in-memory application/presentation state.

It does **not** add:

- state schema 3;
- backup wrapper 3;
- replay format 2;
- Doctor report 2;
- cloud account state;
- telemetry;
- remote leaderboard;
- application network calls.

Completed rounds still persist through `GameService` and existing `Storage` behavior.

## Automated coverage added

New focused challenge test files:

- `tests/test_tui_challenge_configuration.py`
- `tests/test_tui_challenge_i18n.py`
- `tests/test_tui_challenge_presenter.py`
- `tests/test_tui_challenge_widgets.py`
- `tests/test_tui_challenge_mode_fields.py`
- `tests/test_tui_challenge_app.py`
- `tests/test_tui_challenge_safety.py`
- `tests/test_tui_challenge_reset.py`
- `tests/test_tui_challenge_game_status.py`
- `tests/test_tui_challenge_initial_status.py`
- `tests/test_tui_challenge_accessibility.py`

Coverage includes:

- configuration invariants;
- seeded/Daily reconstruction;
- malformed mode/difficulty/seed/date input;
- Reverse separation;
- English/Hindi challenge formatting/completeness;
- target-free status;
- widget defaults;
- mode-aware field state;
- seeded Timed startup;
- Daily startup/normalization;
- invalid-seed current-round preservation;
- invalid-date current-round preservation;
- deterministic configured reset;
- initial challenge identity;
- guess-first focus;
- backward keyboard reachability;
- ordinary `q`/`r` challenge-field input.

`scripts/smoke_test.py` also exercises challenge parsing, deterministic reconstruction, and localized challenge presentation.

## Build/CI/release updates

- `pyproject.toml` routes `guessnova-tui` through `guessnova.tui_challenge_app:run`.
- `Makefile` verifies both the stable workspace and shipped challenge app imports.
- Normal CI built-wheel package checks import both Textual application layers on Linux/Windows/macOS.
- Tagged-release package checks import both Textual application layers on Linux/Windows/macOS.
- Package/runtime/citation metadata is prepared at `1.5.0`.
- `CHANGELOG.md` includes the `1.5.0` release section.

### Final dependency/toolchain maintenance pass

The final continuation audit found current Dependabot updates that were still absent from the v1.5 branch. They were incorporated without changing product/runtime compatibility identifiers:

- development coverage compatibility widened from `pytest-cov>=6.2,<7` to `pytest-cov>=6.2,<8`, allowing the current 7.x line;
- `actions/checkout` updated from v4 to v7 across CI, CodeQL, Security, and Release workflows;
- `actions/setup-python` updated from v5 to v7 across CI, Security, and Release workflows;
- `github/codeql-action` updated from v3 to v4 for init/analyze;
- `softprops/action-gh-release` updated from v2 to v3.

Focused maintenance commits:

- `1ed5b25` — `build(deps-dev): allow pytest-cov 7`
- `dfd42b7` — `ci(deps): update checkout action to v7`
- `a7ccef0` — `ci(deps): update setup-python action to v7`
- `034dedd` — `ci(deps): update CodeQL checkout to v7`
- `fe3f9eb` — `ci(deps): update CodeQL action to v4`
- `bec4026` — `ci(deps): update security checkout to v7`
- `5379fb9` — `ci(deps): update security setup-python to v7`
- `013f9e2` — `ci(deps): update release checkout to v7`
- `18f82fe` — `ci(deps): update release setup-python to v7`
- `56848e7` — `ci(deps): update release action to v3`

These changes mirror the repository's open Dependabot updates instead of inventing unrelated release churn. The Dependabot PRs target `main`, so they are intentionally not closed from this release branch; GitHub/Dependabot can reconcile them after the v1.5 branch is merged.

### Final Phase-6 documentation integrity gate

The master final-audit requirements include documentation-link checking. The repository had comprehensive documentation but no executable local-link verification tool. This was a genuine missing release-quality gate and was closed in this continuation.

Added `scripts/check_docs_links.py`:

- dependency-free and Python-standard-library only;
- recursively scans repository Markdown;
- ignores generated/tool directories;
- ignores fenced and inline code examples;
- validates inline Markdown links/images;
- validates reference-style link definitions;
- validates HTML `href`/`src` targets embedded in Markdown;
- URL-decodes local paths;
- accepts repository-root-relative local paths;
- requires local files/directories to exist;
- rejects targets that escape the repository root;
- deliberately does not fetch external URLs or validate fragment-only GitHub anchor slugs, keeping the gate deterministic and offline.

Added `tests/test_docs_links.py` with focused regression coverage for:

- valid local/external/fragment/image links;
- missing local targets;
- reference links;
- embedded HTML targets;
- fenced/inline code-example exclusion;
- repository-root escape rejection.

Integrated the checker into:

- `make docs-links`;
- `make check`;
- normal CI quality verification;
- tagged-release verification.

Documentation was updated in both concise and canonical testing references and in the definition-of-done audit.

Focused documentation-integrity commits:

- `ca6042a` — `feat(tooling): add offline documentation link checker`
- `5c2b63d` — `test(tooling): cover documentation link checker`
- `b4a7ed7` — `build: add documentation links to make check`
- `441ec58` — `ci: verify documentation links`
- `9695b49` — `ci: gate releases on documentation links`
- `8c61cf0` — `docs: document offline link verification`
- `ce4c28f` — `docs: add canonical documentation link testing guide`
- `a60b2f1` — `docs: mark documentation link gate implemented`

The release workflow has not been tagged or published from this branch. A tag must not be created until exact-head automated and manual release gates pass.

## Documentation completed/updated

Added during v1.5:

- `docs/tui_challenges.md`
- `docs/completion_audit.md`
- `docs/adr/0005-additive-textual-challenge-layer.md`

Updated during the milestone/final audit:

- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `PRIVACY.md`
- `SECURITY.md`
- `SUPPORT.md`
- `docs/TUI_WORKSPACE.md`
- `docs/tui_workspace.md`
- `docs/ARCHITECTURE.md`
- `docs/architecture.md`
- `docs/TESTING.md`
- `docs/testing.md`
- `docs/RELEASING.md`
- `docs/release.md`
- `docs/setup.md`
- `docs/development.md`
- `docs/troubleshooting.md`
- `docs/localization.md`
- `docs/accessibility.md`
- `docs/accessibility_evidence_template.md`
- `docs/game_modes.md`
- `docs/performance.md`
- `docs/completion_audit.md`
- `what_changed.md` (this final handoff)

The documentation explicitly separates implementation completion from release evidence.

## Pull request checkpoint

PR #11 is open and mergeable at the GitHub repository level.

Immediately before this final handoff commit, PR #11 reported:

- head: `a60b2f170aa11b00c10dee6ec639a5674fba2642`
- commits: `79`
- changed files: `54`
- additions: `3474`
- deletions: `643`
- base: `main` at `3b0ae5ba92087e7286b77711d8dfb5df7f132c43`

This handoff update becomes the 80th focused branch commit after the v1.4 base and is intended to be the **final branch mutation before hosted verification**. Do not edit documentation merely to record later workflow status because doing so would create a new unverified head.

The history intentionally uses many small Conventional Commits instead of one monolithic or squashed feature commit.

## Compatibility boundaries

Current prepared v1.5 values:

- package/runtime/citation version: `1.5.0`
- state schema: `2`
- backup wrapper: `2`
- supported legacy backup wrapper: `1`
- replay format: `1`
- Doctor report protocol: `1`

No compatibility identifier above should change merely to create activity.

## Verification reality

### Local execution environment

The available continuation environment cannot resolve GitHub/package-index hosts for a normal local clone/dependency installation. Therefore this continuation does **not** claim a local Ruff, format, mypy, pytest, build, Twine, pip-audit, dependency-backed smoke, or full-repository documentation-link pass.

Static review and committed deterministic regression coverage have been performed through the GitHub repository interface. Dependency/toolchain edits were checked against the repository's current Dependabot-generated patches before being applied. The documentation-link checker is itself dependency-free, but the complete repository checkout required to execute it is not locally available in this continuation environment.

### Hosted verification

PR #11 triggers three exact-head workflow families:

- CI;
- Security checks;
- CodeQL.

The intermediate head `985e5e80ef9f75dffa5250a46f7e20ef9dc0023d` successfully triggered new CI/Security/CodeQL runs, all queued when inspected. That evidence is now superseded because the documentation integrity gate required additional source/workflow/documentation commits.

Only workflow conclusions attached to the final handoff SHA count as automated release-candidate evidence. A queued, pending, absent, cancelled, or superseded run is not a pass.

Required evidence before release verification can be claimed:

- final-head CI success, including Ruff, format, mypy, pytest, compile, release metadata, documentation-link verification, and smoke test;
- final-head Linux built-wheel package success;
- final-head Windows built-wheel package success;
- final-head macOS built-wheel package success;
- final-head Security checks success;
- final-head CodeQL success;
- manual accessibility evidence on the exact release candidate using `docs/accessibility_evidence_template.md`;
- real screenshots/demo only from the exact signed-off build if release media is published.

## Definition-of-done status

See `docs/completion_audit.md` for the requirement-by-requirement audit.

The final repository audit now includes the previously missing documentation-link gate. No open ordinary GitHub issues were found, and repository code search found no matches for `TODO`, `FIXME`, `XXX`, `NotImplemented`, or placeholder `pass` in the searchable repository state. No additional concrete product defect was identified through the available repository interface after closing the dependency/toolchain and documentation-integrity gaps.

Remaining release blockers are evidence gates rather than invented feature work:

1. run/fix exact final-head PR workflows;
2. complete manual v1.5 accessibility evidence;
3. capture real release media only after sign-off if desired;
4. tag/release only after all required gates are satisfied.

Optional candidates listed in `docs/completion_audit.md` remain optional and are not definition-of-done blockers. They should not be added merely to inflate feature or commit count.

## Next exact actions

1. Freeze this branch head.
2. Inspect final-head CI/Security/CodeQL conclusions.
3. If the documentation-link gate finds an existing broken local target, fix the affected documentation with a focused commit and rerun exact-head verification.
4. If any other concrete workflow failure occurs, inspect the failed step, fix it with a focused commit plus regression where practical, then repeat exact-head verification.
5. Merge PR #11 with the normal merge method only after required automated gates pass and no release-blocking code defect remains. Preserve granular history; do not squash.
6. Do not tag `v1.5.0` until manual accessibility evidence is also complete.
