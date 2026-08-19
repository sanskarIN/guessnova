# Security Policy

## Supported versions

Security fixes are applied to the latest stable release line.

## Reporting a vulnerability

Please do not publish a sensitive vulnerability in a public issue. Send a concise report to `sanskarin@outlook.in` with affected version, reproduction conditions, impact, and suggested mitigation if known.

## Security principles

- Local-only data by default.
- No embedded API keys or secrets.
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
- `guessnova doctor` and `guessnova-doctor` share the same diagnostic/repair implementation.
- Repair refuses unreadable, non-object, oversized, future-schema, or otherwise unnormalizable state and creates an integrity-protected backup before rewriting repairable state.
- Backup capacity remains larger than accepted state capacity so the mandatory repair backup is representable.
- Doctor JSON output has an explicit report version and avoids interactive prompts during authorized JSON repair.
- Path boundary helpers for future file operations.
- Bounded numeric and sanitized profile input.
- Integrity checks for replay codes.
- Dependency updates reviewed through automated tooling.

## Integrity is not authentication

Replay and backup SHA-256 integrity checks are designed to detect accidental modification or ordinary tampering. They are not encryption, digital signatures, secret-key authentication, proof of origin, or protection against an attacker who can rewrite both the payload and its unkeyed digest.

A backup that passes SHA-256 and current normalization is structurally acceptable to GuessNova; this still does not prove who created it.

## Doctor and support-output safety

Doctor performs no runtime network request, but its output can contain local path information, the active profile name, schema versions, and aggregate counts. Treat saved JSON reports as diagnostic data and review them before sharing publicly.

Do not put secrets into GuessNova replay codes, state files, backup files, repair backups, Doctor reports, fixtures, issue reports, or terminal captures.

## Future artifact signing

GuessNova does not currently claim cryptographic package-origin signing beyond the repository/release mechanisms actually configured. A signing or trusted-publishing expansion should be added only alongside a concrete package-registry publishing workflow, with protected credentials and documented verification rather than placeholder claims.
