# Release evidence

GuessNova release automation verifies code, packaging, compatibility metadata, security checks, and cross-platform installation. Some release gates are intentionally manual and must never be represented as complete by automation.

This directory stores machine-readable sign-off records for those manual gates.

## Rules

- Do not set a manual check to `true` until that check was actually performed against the intended release candidate.
- Do not invent reviewer names, dates, screenshots, demo media, or accessibility results.
- Keep screenshot/demo references as repository-relative paths or durable release-evidence identifiers.
- The tagged-release workflow validates the evidence record before it performs release publication.
- Automated CI success does not substitute for manual accessibility or release-media review.
- A pending evidence record is expected during development and must not be treated as a failure in normal CI.

## Required checks

A release evidence record must explicitly sign off:

1. keyboard-only Challenge Setup and core workspace navigation;
2. high-contrast presentation;
3. reduced-motion behavior;
4. English UI/catalog review;
5. Hindi UI/catalog review;
6. screenshots captured from the signed-off release candidate;
7. demo media captured from the signed-off release candidate.

The record also requires a reviewer, an ISO-8601 review timestamp, and at least one evidence reference for screenshots and demo media.

## v1.5.0

`v1.5.0.json` is intentionally committed in the `pending` state. It should remain pending until the manual work is actually complete. `scripts/verify_manual_release_evidence.py` is the canonical validator used by tagged-release automation.
