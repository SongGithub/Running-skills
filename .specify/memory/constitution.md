# Running-skills Constitution

## Core Principles

### I. Public code, private configuration
Repository source and specs describe reusable behaviour. Athlete preferences, account identifiers, credentials, activity text and local policy files stay outside Git. A missing private policy fails closed.

### II. One guarded write path
All Strava activity-title and description writes use the publisher. Validation runs immediately before the network request; an API success is followed by readback verification.

### III. Review bound to exact content
Mechanical policy checks and semantic review are separate. A review receipt must name the policy and exact title/description hashes. Any change invalidates approval.

### IV. Test the gate
Tests cover denied copy, missing policy/review, stale review, non-run protection, and successful preflight without network access.

## Governance
Changes to publishing behaviour require an updated feature spec and passing gate tests. No real credential or private policy may be committed. The local operator may tighten policy without a repository change.

**Version**: 1.0.0 | **Ratified**: 2026-10-16 | **Last Amended**: 2026-10-16
