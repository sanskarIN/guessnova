# ADR 0004: Separate backup format and state schema versions

- Status: Accepted
- Date: 2026-08-19

## Context

GuessNova 1.0/1.1 used one integer for both the local state schema and the exported backup wrapper. That coupling meant a future state migration could make an older wrapper appear unsupported even when its payload remained safely migratable.

GuessNova 1.2 also introduces a real schema-2 boundary: recoverable profile trash becomes a canonical top-level state field with committed schema-1 migration fixtures.

## Decision

Use independent version domains:

- `SCHEMA_VERSION` identifies the local state payload schema.
- `EXPORT_VERSION` identifies the backup wrapper/envelope format.
- Backup wrapper v2 explicitly records the embedded payload schema.
- Wrapper/payload schema metadata must match.
- Backup v2 carries SHA-256 payload integrity metadata.
- Legacy backup wrapper v1 remains readable when its embedded state schema is supported.
- Future wrapper or state versions are rejected rather than guessed/downgraded.

## Consequences

Benefits:

- state migrations no longer require arbitrary backup-wrapper version changes;
- old backups can remain readable across compatible migrations;
- repair backups truthfully record their source schema;
- corruption/tampering is detected before persistence;
- compatibility rules are independently testable.

Costs:

- two version values must be maintained and documented;
- import code must retain a small legacy-v1 path;
- SHA-256 integrity is corruption detection only, not authentication or encryption.

## Non-goals

This decision does not add cloud backup, account sync, encryption, digital signatures, telemetry, or runtime network access.
