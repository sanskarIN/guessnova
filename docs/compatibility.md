# Compatibility contracts

GuessNova treats persisted formats and cross-interface deterministic rules as explicit compatibility domains. A package version change does not automatically change any data or protocol version, and a data/protocol version changes only when its contract actually changes.

The machine-readable source of truth is [`compatibility.json`](../compatibility.json). CI verifies that file against the runtime constants implemented by the Python and browser code.

## Current preparation baseline

| Domain | Current value | Compatibility rule |
| --- | --- | --- |
| Package/runtime | `1.4.0` | Remains unchanged until a release is intentionally cut. |
| Python requirement | `>=3.13` | Declared by `pyproject.toml`. |
| Python local state schema | `2` | Existing schema migration/rejection rules remain authoritative. |
| Backup wrapper | `2` | Legacy wrapper `1` remains supported as documented. |
| Replay format | `1` | Existing replay validation/rejection rules remain authoritative. |
| Doctor report protocol | `1` | Machine-readable Doctor output remains versioned independently. |
| Browser state marker | `1` | Browser state remains separate from Python schema-2 state. |
| Browser storage key | `guessnova.web.v1` | Legacy unversioned values at this key remain normalized by the browser boundary. |
| Portable interchange | not defined | Browser/Python state interchange is not implied or enabled. |
| Portable challenge descriptor | `1` | Additive deterministic identity contract described below. |

## Portable challenge descriptor v1

Descriptor v1 is an opt-in compatibility contract for deterministic challenge identity. Defining it does **not** silently change the existing CLI or Textual seeded-challenge algorithm. Existing interfaces continue to use their documented behavior until a later integration step deliberately adopts the portable descriptor.

Supported deterministic modes:

- `classic`
- `timed`
- `streak`
- `daily`

`reverse` is intentionally excluded because Reverse mode has no hidden numeric target chosen from a seed/date descriptor.

### Canonical shapes

Seeded Classic/Timed/Streak descriptor:

```json
{
  "version": 1,
  "mode": "classic",
  "difficulty": "normal",
  "seed": 42
}
```

Daily descriptor:

```json
{
  "version": 1,
  "mode": "daily",
  "difficulty": "normal",
  "day": "2026-08-25"
}
```

Descriptors are strict. Unknown fields, missing mode-specific fields, unknown modes/difficulties, unsupported versions, invalid dates, and non-safe-integer seeds are rejected rather than normalized into a different challenge identity.

### Portable seeded target rule

For Classic, Timed, and Streak descriptors, the target is derived from the UTF-8 string:

```text
guessnova-challenge-v1:<mode>:<difficulty>:<seed>
```

The string is hashed with unsigned 32-bit FNV-1a. The result is mapped into the inclusive difficulty range:

```text
minimum + (hash % (maximum - minimum + 1))
```

Seeds must be JavaScript-safe integers in the inclusive range `-9007199254740991` through `9007199254740991` so Python and browser clients represent the identity exactly.

### Daily target rule

Daily descriptors preserve the established cross-language daily-v2 rule:

```text
guessnova-daily-v2:<YYYY-MM-DD>:<difficulty>
```

The same unsigned 32-bit FNV-1a and inclusive-range mapping are used. Dates must be real canonical ISO calendar dates in `YYYY-MM-DD` form.

### Golden vectors

`tests/fixtures/portable_challenges_v1.json` is the shared normative vector set. Python and Node tests consume the exact same file. Any change that makes one runtime disagree with these vectors is a compatibility break and requires an explicit descriptor-version decision rather than silently rewriting v1 behavior.

## Version rejection policy

Readers must reject unknown future versions instead of guessing how to interpret them. This fail-closed rule already applies to the versioned persistence/report domains and is explicit for portable challenge descriptor v1.

A future descriptor v2 may add or revise deterministic identity rules, but v1 vectors and v1 parsing must remain stable for as long as v1 is supported.

## Deliberate separation from portable state interchange

Portable challenge identity and portable user-data interchange are different contracts. Descriptor v1 does not authorize importing browser localStorage as Python state, exporting Python schema-2 data directly into browser storage, or merging profile/history/leaderboard data between surfaces.

`portable_interchange_version` therefore remains `null` until an explicit bounded interchange format, preview-before-mutation behavior, migration/rejection rules, and backup-before-destructive-write guarantees are designed and tested.
