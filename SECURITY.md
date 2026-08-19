# Security Policy

## Supported versions

Security fixes are applied to the latest stable release line.

## Reporting a vulnerability

Please do not publish a sensitive vulnerability in a public issue. Send a concise report to `sanskarin@outlook.in` with affected version, reproduction conditions, impact, and suggested mitigation if known.

## Security principles

- Local-only data by default.
- No embedded API keys or secrets.
- Atomic writes for application state.
- Versioned import/export validation.
- Path boundary helpers for future file operations.
- Bounded numeric and sanitized profile input.
- Integrity checks for replay codes.
- Dependency updates reviewed through automated tooling.
