# Feature Specification: Private-policy Strava publishing gate

**Created**: 2026-10-16

**Status**: Implemented

## User scenarios

### P1 — Publish only copy that passes local policy
Given a local private policy and proposed run title/description, the publisher validates required fields, length, configured deny patterns and suffix before any Strava write. Missing/invalid policy, invalid regex, or failed validation blocks publication.

### P1 — Review the exact copy against the exact policy
Before applying a write, an agent reviews the policy and the proposed copy for story quality, factual fit, metrics and private content. A review receipt records positive answers and SHA-256 of policy bytes and proposed title/description. The pre-publish hook rejects missing, negative or stale receipts. A receipt is evidence of an agent review, not an independent proof of its quality.

### P2 — Keep personal configuration local
The public repository includes no real policy, user preference, credentials or activity text. The policy path is supplied locally at runtime. A template documents the schema without populating a real rule.

### P2 — Verify the external write
The publisher rejects non-run activities, writes through the authenticated local Strava adapter and reads the activity back to verify exact title and description.

## Requirements

- FR-001: A single guarded CLI handles title/description PUT requests.
- FR-002: The pre-publish hook always runs locally before network access, including on `--apply`.
- FR-003: `--apply` requires a positive receipt bound to exact policy and copy.
- FR-004: No credentials or personal policy are read from the repository.
- FR-005: Missing policy, review, adapter or readback fails closed.
- FR-006: The implementation is standard-library Python and has offline tests.

## Acceptance checks

1. Invalid title is rejected in preflight without touching Strava.
2. Valid preflight does not make a network call.
3. Missing/stale/negative review blocks `--apply` before adapter import.
4. A changed policy invalidates a prior review.
5. A non-run activity is not mutated; a successful write is read back.
