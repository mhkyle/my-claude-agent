---
name: compute
description: Conventions and review checklist for Compute program code. Use when reviewing, debugging, or modifying Compute-related code in this repo.
---

Guidance for working with this project's Compute program code.

## Review checklist

- Resource lifecycle: created, bounded, and released (no leaks).
- Error handling: failures surfaced; transient errors retried with backoff.
- Idempotency: safe to retry; no duplicate side effects.
- Limits: quotas, timeouts, and concurrency respected.
- Observability: key operations logged with enough context to debug.

## Change safety

- Call out behaviour changes that affect cost, latency, or correctness.
- Prefer minimal, reversible changes; note rollback steps.

<!-- TODO: fill in language/framework specifics, file locations, and any
     Compute APIs, packages, or invariants this project depends on. -->
