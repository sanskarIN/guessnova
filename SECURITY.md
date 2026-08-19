# Security Policy

## Supported versions

Security fixes are applied to the latest stable release line.

## Reporting a vulnerability

Please do not publish a sensitive vulnerability in a public issue. Send a concise report to `sanskarin@outlook.in` with affected version, reproduction conditions, impact, and suggested mitigation if known.

## Security principles

- Local-only data by default.
- No embedded API keys or secrets.
- No runtime account, remote leaderboard, telemetry, analytics, cloud-sync, or required application network service.
- Atomic writes for application state and completed backup output.
- Bounded state and backup input reads before UTF-8/JSON processing.
- Bounded normalized state output before final persistence.
- Explicit state-schema migration with future-schema rejection.
- Independent backup-wrapper versioning with supported-version checks.
- Single-read backup validation represented by validated metadata from the same bytes that passed integrity/schema checks.
- SHA-256 payload integrity validation for backup wrapper v2 using constant-time digest comparison.
- Wrapper/payload schema provenance agreement before backup import.
- Legacy backup compatibility is explicit rather than guessed.
- `guessnova doctor --verify-backup` is read-only and proves current state normalizability before reporting a backup as valid.
- TUI Recovery reuses the same read-only diagnostics/backup-preflight boundaries and does not expose repair/import actions.
- `guessnova doctor` and `guessnova-doctor` share the same diagnostic/repair implementation.
- Repair refuses unreadable, non-object, oversized, future-schema, or otherwise unnormalizable state and creates an integrity-protected backup before rewriting repairable state.
- Backup capacity remains larger than accepted state capacity so the mandatory repair backup is representable.
- Doctor JSON output has an explicit report version and avoids interactive prompts during authorized JSON repair.
- TUI profile deletion requires exact selected-name confirmation and moves data to bounded recoverable trash rather than immediate permanent deletion.
- TUI active-profile changes reset unfinished gameplay so a partially played result cannot be silently persisted under another profile identity.
- TUI workspace helpers reuse validated `Storage`, `Settings`, `HistoryEntry`, `LeaderboardEntry`, diagnostics, and backup-inspection boundaries instead of creating parallel parsing/persistence rules.
- v1.5 Challenge Setup validates mode/difficulty/seed/date before replacing the active round.
- Challenge setup only accepts known numeric modes; Reverse remains on its dedicated interaction path.
- Challenge difficulty values come from the shared `DIFFICULTIES` registry rather than a separate unvalidated rule table.
- Daily challenge configuration derives its seed from a validated ISO date instead of accepting a second conflicting manual seed.
- Invalid challenge setup preserves the current game/attempt/result-save state rather than partially mutating application state.
- Active challenge identity deliberately excludes the hidden target.
- Challenge form state remains in-memory and does not create an unnecessary persistence/schema attack surface.
- Play-only single-letter reset/quit commands are scoped to the numeric guess widget; challenge and other workspace text inputs keep ordinary character semantics.
- Path boundary helpers for future file operations.
- Bounded numeric and sanitized profile input.
- Integrity checks for replay codes.
- Dependency updates reviewed through automated tooling.

## Challenge Setup validation boundary

`parse_workspace_challenge(...)` is the validation boundary for presentation-friendly Challenge Setup values.

Before a configured round can replace the active game it must establish:

- a known non-Reverse `GameMode`;
- a difficulty present in `DIFFICULTIES`;
- either no seed or an integer seed for Classic/Timed/Streak;
- a valid ISO date for Daily, with blank date resolved locally;
- no manual Daily seed;
- no Daily date attached to a non-Daily configuration.

`tui_challenge_app.py` constructs the replacement game before assigning it to the app. A validation/construction failure therefore cannot leave a partially replaced round.

The challenge presenter has no reason to display the target. Target non-disclosure is covered by focused regression tests for configured and already-created games.

This validation is application robustness, not a cryptographic boundary. Deterministic seeds are not secrets and should not be treated as authentication credentials.

## TUI Recovery is inspection, not repair

The Textual Recovery pane can display local diagnostic information and verify a selected backup. It intentionally cannot:

- invoke state repair;
- import the verified backup;
- delete state;
- silently rewrite a path selected for verification.

Keeping repair in Doctor prevents the interactive dashboard from bypassing confirmation and pre-repair backup guarantees.

A future TUI repair feature would require a separate security/design review proving that those guarantees remain explicit and testable.

## Text input and shortcut scope

The expanded workspace includes challenge seed/date fields, profile names, searches, dates, player filters, and backup paths. Plain `Q`/`R` therefore belong only to the focused numeric `GuessInput` in Play. They are not application-global bindings, so ordinary workspace text fields can consume normal `q`/`r` characters.

Global `Ctrl+Q`/`Ctrl+R` remain available from every pane. This separation prevents a normal typed character in a text field from unexpectedly triggering a session action while preserving the original Play reset/quit shortcuts.

## Integrity is not authentication

Replay and backup SHA-256 integrity checks are designed to detect accidental modification or ordinary tampering. They are not encryption, digital signatures, secret-key authentication, proof of origin, or protection against an attacker who can rewrite both the payload and its unkeyed digest.

A backup that passes SHA-256 and current normalization is structurally acceptable to GuessNova; this still does not prove who created it.

Likewise, a deterministic challenge seed is reproducibility metadata, not a secret/token/security credential.

## Doctor/TUI support-output safety

Doctor and the Textual workspace perform no runtime network request, but visible output can contain local path information, active/profile names, history/leaderboard information, challenge seeds/dates, schema versions, and aggregate counts.

Treat saved JSON reports, screenshots, screen recordings, terminal logs, and TUI captures as diagnostic/user data and review them before sharing publicly.

Do not put secrets into GuessNova challenge fields, replay codes, state files, backup files, repair backups, Doctor reports, fixtures, issue reports, or terminal captures.

## Future artifact signing

GuessNova does not currently claim cryptographic package-origin signing beyond the repository/release mechanisms actually configured. A signing or trusted-publishing expansion should be added only alongside a concrete package-registry publishing workflow, with protected credentials and documented verification rather than placeholder claims.
