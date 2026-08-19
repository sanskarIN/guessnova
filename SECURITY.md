# Security Policy

## Supported versions

Security fixes are applied to the latest stable release line.

## Reporting a vulnerability

Please do not publish a sensitive vulnerability in a public issue. Send a concise report to `sanskarin@outlook.in` with affected version, reproduction conditions, impact, and suggested mitigation if known.

## Security principles

- Local-only data by default.
- No embedded API keys or secrets.
- Atomic writes for application state and completed backup output.
- Explicit state-schema migration with future-schema rejection.
- Independent backup-wrapper versioning with supported-version checks.
- SHA-256 payload integrity validation for backup wrapper v2 using constant-time digest comparison.
- Wrapper/payload schema provenance agreement before backup import.
- Legacy backup compatibility is explicit rather than guessed.
- `guessnova-doctor` diagnostics are read-only unless repair is explicitly requested.
- Repair refuses unreadable/non-object/unsupported state and creates an integrity-protected backup before rewriting repairable state.
- Path boundary helpers for future file operations.
- Bounded numeric and sanitized profile input.
- Integrity checks for replay codes.
- Dependency updates reviewed through automated tooling.

## Integrity is not authentication

Replay and backup SHA-256 integrity checks are designed to detect accidental modification or ordinary tampering. They are not encryption, digital signatures, secret-key authentication, proof of origin, or protection against an attacker who can rewrite both the payload and its unkeyed digest.

Do not put secrets into GuessNova replay codes, state files, backup files, repair backups, fixtures, or issue reports.
