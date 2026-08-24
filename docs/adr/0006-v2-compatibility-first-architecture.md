# ADR 0006: Compatibility-first architecture for GuessNova 2.0

- Status: Accepted for 2.0 preparation
- Date: 2026-08-24

## Context

GuessNova now has multiple mature local interfaces: Rich CLI, a Textual workspace, Doctor diagnostics/recovery, and an installable browser/PWA edition. These surfaces intentionally do not all share the same persistence format.

The Python application currently owns its versioned local state and backup contracts. The browser owns a separate localStorage contract. Deterministic gameplay rules are shared conceptually but implemented in Python and JavaScript.

A major-version transition creates a temptation to merge these concerns into one large state format or to add native/cloud layers simply because the version number is larger. That would weaken the existing offline/privacy guarantees and increase migration risk.

## Decision

GuessNova 2.0 will use explicit compatibility boundaries instead of one implicit universal state model.

### 1. Local stores remain interface-owned

Python local state and browser localStorage remain separate persistence domains unless a versioned interchange format is deliberately introduced.

### 2. Portability is a separate protocol

Cross-interface portability, if implemented, uses a dedicated versioned interchange document. It is not Python schema state and it is not raw browser localStorage.

The interchange protocol must define:

- protocol version;
- provenance/source surface;
- bounded field sizes and record counts;
- supported portable fields;
- normalization behavior;
- unknown/future-version rejection;
- import preview semantics;
- mutation/backup guarantees.

### 3. Deterministic rules get golden cross-language fixtures

Rules intended to produce identical results across Python and JavaScript must have committed fixtures consumed by both implementations. A rule is not considered portable merely because the implementations look similar.

### 4. Compatibility versions advance only for real boundaries

Package major version does not automatically force state schema, backup wrapper, replay format, Doctor protocol, or browser-state marker changes. Each domain advances only when its own contract changes.

### 5. Offline/privacy guarantees are architectural constraints

Normal gameplay must remain usable without an account, analytics, telemetry, advertising, cloud sync, or a gameplay backend. Optional future network features must not become a dependency of local gameplay.

### 6. Native wrappers are product work, not a checkbox

Android/iOS native wrappers are allowed only when they provide real platform value and have build, test, accessibility, privacy, signing, and release verification. Until then, mobile support is the installable PWA path.

## Consequences

Positive consequences:

- smaller migration blast radius;
- clearer rollback and recovery behavior;
- compatibility changes are testable independently;
- Python/browser implementations can evolve without silently corrupting each other's stores;
- a 2.0 release can improve architecture without inventing unnecessary schema churn.

Costs:

- multiple compatibility domains remain visible in documentation;
- any future interchange protocol requires explicit mapping code and fixtures;
- deterministic parity needs cross-language golden tests instead of informal duplication.

## Rejected alternatives

### Treat browser localStorage as Python state

Rejected because the schemas have different ownership, validation, and lifecycle semantics.

### Bump every format to version 2/3 for the major release

Rejected because version numbers should represent real compatibility boundaries, not marketing alignment.

### Make cloud accounts the canonical state owner

Rejected because it would violate the current local-first/offline product contract and create a mandatory backend dependency.

## Verification

The 2.0 roadmap and release checklist must reference this ADR. Any proposed compatibility-domain change should include fixtures, migration/rejection tests, and documentation before it can be marked release-ready.
