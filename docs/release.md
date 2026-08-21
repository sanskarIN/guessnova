# Release Process

## Release checklist

1. Start from a clean checkout of the intended release commit on `main`.
2. Use Python 3.13+ and install `.[dev]` plus `build`, `twine`, and `pip-audit`.
3. Run the complete local quality suite:

   ```bash
   ruff check .
   ruff format --check .
   mypy src/guessnova
   pytest --cov=guessnova --cov-report=term-missing
   node --test tests/web/*.mjs
   node --check src/guessnova/web/app.js
   node --check src/guessnova/web/browser-state.mjs
   node --check src/guessnova/web/game-engine.mjs
   node --check src/guessnova/web/sw.js
   python scripts/verify_web_package.py
   python -m compileall -q src tests scripts
   python scripts/verify_release_metadata.py
   python scripts/smoke_test.py
   python -m guessnova --help
   python -m guessnova doctor --help
   python -m guessnova.doctor_cli --help
   python -m guessnova web --help
   python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
   python -c "from guessnova.tui_challenge_app import GuessNovaApp; print(GuessNovaApp.TITLE)"
   pip-audit
   python -m build
   python -m twine check dist/*
   ```

4. Review CI, Security checks, and CodeQL results for the **exact release commit**. Do not treat queued, pending, cancelled-superseded, or older-head results as a pass for the selected release head.
5. Require the CI platform-package matrix to complete on Ubuntu, Windows, and macOS. Each platform must build, validate, install the wheel, start `python -m guessnova --help`, import both the stable Textual workspace and challenge-enabled Textual app from the installed wheel, run Doctor entry-point/version checks, expose both local web entry points, verify the installed PWA package contract, and pass the smoke test.
6. Verify CLI help, seeded play, daily play, explicit hints, reverse mode, settings, advanced history filters/grouping, profile create/use/rename/delete/restore, backup export/import, and Doctor state/backup routes.
7. Verify the six-pane Textual workspace launches with Play active and the numeric guess input focused.
8. Verify Challenge Setup supports Classic, Timed, Streak, and Daily, excludes Reverse from the numeric form, and never exposes the hidden target in status text.
9. Verify a seeded configured challenge reproduces its target after reset, and a Daily configured challenge reproduces its resolved date/seed/target after reset.
10. Verify malformed seed/date input is transactional: the active game object, target, attempts, and completed-result save state are not replaced or partially reset.
11. Verify mode-aware fields: Daily enables date/disables seed; Classic/Timed/Streak enable seed/disable date; a blank Daily date resolves to an explicit date on successful start.
12. Verify Textual pane shortcuts `Ctrl+1` through `Ctrl+6`, global `Ctrl+R`/`Ctrl+Q`, normal character input in workspace/challenge text fields, and backward keyboard access to Challenge Setup without disturbing the established Guess → Submit → Range Hint forward path.
13. Verify Textual Profiles create/use/rename/delete/restore flows, exact-name delete confirmation, achievement summary, and unfinished-round reset when active-profile ownership changes.
14. Verify Textual History result/mode/difficulty/search/date filters, invalid-date behavior, and newest-first bounded display.
15. Verify Textual Leaderboard mode/difficulty/player filters while preserving ranked ordering.
16. Verify Textual Settings persistence for theme/locale/reduced motion/high contrast/sound/smart hints, immediate high-contrast/smart-hint behavior, and next-launch locale semantics.
17. Verify Textual Recovery diagnostics and backup verification remain read-only and do not expose a repair/import action.
18. Verify schema migration from both committed schema-1 fixtures and confirm resulting normalized state is schema 2. Confirm future schema rejection remains intact and no schema-3 fixture/version has been invented without a real boundary.
19. Verify a backup-v2 round trip, legacy wrapper-v1 import, deliberately modified backup failing SHA-256 integrity, and backup preflight rejecting a checksum-valid but structurally unimportable payload.
20. Verify bounded state/backup behavior: oversized state is rejected before decode/normal persistence, oversized backup is rejected before JSON processing, and `MAX_EXPORT_BYTES > MAX_STATE_BYTES` remains true.
21. Verify `guessnova doctor --json`, `guessnova-doctor --json`, explicit `--data-dir`, Doctor report version `1`, stable exit semantics, and a repair flow against isolated schema-1 state. Confirm the repair backup contains the original schema-1 payload and repaired state is schema 2.
22. Confirm JSON repair requires `--yes`, so no interactive prompt can contaminate machine-readable stdout.
23. Verify browser/PWA gameplay for Classic, Timed, Streak, Daily, and Reverse; confirm the portable Daily target agrees with Python for the same date+difficulty and Reverse contradiction/post-completion regressions remain covered.
24. Verify browser state remains origin-local, malformed/oversized persisted state is safely normalized/fallback handled, the service-worker app shell contains the current module set, and no account/telemetry/analytics/cloud requirement has been introduced.
25. Verify the bundled PWA over localhost and, for a release claiming hosted mobile/browser installability, over an HTTPS candidate deployment. Test the intended desktop/mobile browser families without claiming untested devices.
26. Complete a copy of `docs/accessibility_evidence_template.md` against the exact release candidate, including every Textual pane and Challenge Setup. Do not infer manual accessibility results from automated tests.
27. Verify both shipped terminal locales (`en`, `hi`) and confirm no visible catalog key or broken placeholder reaches the user. Relaunch the TUI after changing locale to verify full-language presentation, including challenge controls/status.
28. Update version metadata, `CHANGELOG.md`, `ROADMAP.md`, and `what_changed.md` only when the release version is intentionally selected.
29. Create a semantic tag only after required automated checks and manual gates pass. The tag must exactly match `project.version`; do not infer a tag from a feature-branch name.
30. The release workflow independently verifies that the tag version equals `project.version`, then reruns lint, format, strict mypy, Python tests, Node/browser tests, JavaScript syntax, PWA package verification, compile, release metadata, smoke, dependency audit, and the cross-platform package matrix before it can publish artifacts.
31. After verification succeeds, the workflow builds source/wheel distributions, validates them with Twine, installs the release wheel, verifies the PWA package and challenge-enabled Textual app import, and attaches artifacts to generated GitHub release notes.
32. Verify the published wheel exposes `guessnova`, `guessnova-tui`, `guessnova-doctor`, and `guessnova-web`; confirm `guessnova doctor --help`, `guessnova web --help`, and `guessnova-web --help` work; import both Textual app layers; confirm no local state, caches, credentials, repair backups, or secrets are included.
33. If screenshots/demo media are published, capture them from this exact signed-off tag/commit and record provenance according to `docs/media/README.md`. Never use mock or reconstructed release media.

## Version/tag invariant

A release tag must be `v` followed by the exact `project.version` in `pyproject.toml`. For example, project version `1.5.0` requires tag `v1.5.0`; project version `1.4.1` requires tag `v1.4.1`. A mismatch intentionally fails the release workflow before artifacts are published.

Package, runtime, citation, and changelog release metadata are also checked by `scripts/verify_release_metadata.py`.

The current reconciliation branch intentionally keeps `project.version = 1.4.0` while challenge work is under pull-request verification. That is not authorization to create another `v1.4.0` tag. Release metadata/tagging must be an explicit later release decision after the feature is accepted and the exact candidate is verified.

## Compatibility domains

Release review treats these independently:

- local state schema: `2`;
- backup wrapper: `2` plus supported legacy wrapper `1`;
- replay format: `1`;
- Doctor JSON report protocol: `1`;
- browser state marker: `1`.

The Challenge Setup reconciliation changes none of these compatibility identifiers. It is an application/presentation-layer addition over existing gameplay/persistence formats. Browser/PWA storage remains a deliberately separate origin-local format rather than being silently merged into Python schema-2 state.

A release change in one domain must not silently redefine another. If an incompatible Doctor JSON contract is ever required, increment the Doctor report version rather than changing existing field semantics under report version 1.

## State/backup/Doctor compatibility gate

A release must not ship unless all of these remain true:

- schema 0 can migrate forward;
- committed schema-1 fixtures migrate to schema 2;
- future state schemas are rejected;
- state reads/writes are bounded;
- backup wrapper v2 records the embedded payload schema;
- wrapper/payload schema mismatch is rejected;
- backup payload tampering is rejected by integrity validation;
- backup validation uses one bounded read;
- legacy backup wrapper v1 remains importable/inspectable when its embedded state schema is supported;
- backup preflight proves current state normalization/importability;
- checksum-valid but unimportable state is rejected;
- backup capacity remains greater than accepted state capacity;
- repair creates a backup before rewriting repairable state;
- unreadable/non-object/oversized/future-schema state is not silently overwritten;
- both Doctor entry paths share the same underlying behavior;
- JSON repair is noninteractive unless `--yes` was explicitly supplied;
- Doctor protocol exit/report version behavior remains covered by tests.

Backup SHA-256 integrity is corruption/change detection, not authentication, encryption, origin proof, or digital signing.

## Textual workspace and Challenge Setup release gate

A release containing Challenge Setup must retain these invariants:

- Play remains the initial pane and initial numeric-input focus is deterministic;
- Challenge Setup is additive over the stable six-pane workspace rather than a replacement persistence/UI model;
- completed rounds persist exactly once through `GameService`;
- active-profile ownership changes reset unfinished gameplay;
- profile deletion requires exact-name confirmation and remains recoverable;
- History and Leaderboard use validated existing local state rather than a parallel database;
- Settings save through the existing profile settings model;
- high contrast remains visible without making color the only status channel;
- Switch controls do not introduce decorative animation;
- one running TUI remains linguistically consistent;
- Recovery diagnostics and backup verification are read-only;
- repair remains centralized in Doctor;
- ChallengeConfiguration/parser validation occurs before active-game replacement;
- invalid challenge input preserves the active round;
- configured seeded/Daily reset reconstructs from validated metadata without storing/exposing the hidden target;
- Reverse remains outside the numeric Challenge Setup until a dedicated Textual interaction is designed/tested;
- built wheels import both `guessnova.tui.GuessNovaApp` and `guessnova.tui_challenge_app.GuessNovaApp` on Linux, Windows, and macOS;
- Textual pilot tests use temporary local state and deterministic games.

## Browser/PWA release gate

A release containing the browser client must retain these invariants:

- `tests/web/*.mjs` runs the complete committed Node test set;
- `app.js`, `browser-state.mjs`, `game-engine.mjs`, and `sw.js` pass syntax validation;
- `scripts/verify_web_package.py` succeeds for source and installed-wheel contexts required by CI/release workflows;
- portable Daily vectors agree between Python and JavaScript;
- browser Reverse contradictions do not corrupt bounds and completed rounds reject further feedback;
- browser state normalization protects against malformed/oversized persisted values and future schemas;
- browser storage remains separate from Python state unless a reviewed migration/interchange design explicitly changes that boundary;
- the service-worker cache includes the current required modules/assets;
- gameplay does not require accounts, telemetry, analytics, advertising, cloud sync, or a remote leaderboard;
- localhost serving remains loopback-only by default, while production/mobile hosting uses HTTPS.

## Reproducibility

Use the tagged commit as the sole release source. Do not build a release from a dirty local working tree or upload hand-modified artifacts. The GitHub workflow rebuilds distributions from checkout so artifacts are traceable to the tag.

Cross-platform CI verifies packaging behavior on the three supported desktop OS families, but generated GitHub release artifacts still come from the release workflow's clean checkout. Platform checks validate portability; they do not create three different product versions.

## Accessibility evidence

A release candidate is not considered manually signed off until the evidence checklist has been completed on the candidate commit. For a candidate containing Challenge Setup, evidence includes Play, Challenge Setup, Profiles, History, Leaderboard, Settings, Recovery, shortcut/focus behavior, narrow terminals, increased scaling, high contrast, reduced motion, and English/Hindi presentation.

Browser/mobile accessibility evidence should be captured separately when a release claim depends on those interfaces. Automated tests and standards-based implementation are not substitutes for real-device/browser/manual evidence.

Any release-blocking accessibility issue should receive a reproducible issue/test where practical before tagging.

## Release media

Real terminal/browser screenshots and demo recordings are manual release artifacts, not generated placeholders. Store them under `docs/media/` only after capture from the signed-off build. Include the exact tag/commit in the filename or companion metadata.

## Rollback

Do not rewrite or move published tags. If a release has a defect, prepare a new patch version with a regression test, update the changelog, rerun the complete quality suite, and publish a new immutable tag.

A rollback must not rewrite a user's newer state schema with older software. If state compatibility is uncertain, preserve the state directory, run read-only Doctor diagnostics/preflight where supported, and use export/repair backups rather than attempting a downgrade write.

## Secrets and future artifact signing

GuessNova itself requires no secrets. Artifact signing/trusted-publishing expansion is intentionally gated until a real package-registry publishing workflow exists. If that workflow is introduced later, use GitHub environment protection, trusted publishing where available, and repository/environment secrets; never place publishing tokens or signing credentials in source files, workflow YAML, `.env.example`, documentation, fixtures, or generated release archives.
