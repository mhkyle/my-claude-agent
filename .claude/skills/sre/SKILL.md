---
name: sre
description: Cloud SRE guidance — incident response, SLOs, observability, and runbooks. Use for operational questions, incident triage, reliability reviews, or alerting/monitoring design.
---

You are applying Site Reliability Engineering practices. Apply the relevant
sections; do not dump the whole checklist.

## Triage (during an incident)

1. Establish impact and blast radius; state severity.
2. Mitigate first (rollback / failover / feature-flag), then investigate.
3. Communicate: what's broken, since when, who's on it, next update time.
4. Keep a timestamped timeline of actions and findings.

## SLOs

- Define SLIs (latency, error rate, saturation, availability).
- Set targets with an error budget; alarm on burn rate, not raw thresholds.

## Observability

- Prefer structured logs, metrics, and traces with correlation IDs.
- Dashboards should answer: is it healthy? if not, where? and what changed?

## Runbook template

- Symptom → likely causes → diagnostic commands → mitigation → follow-up.

<!-- TODO: replace with your service's concrete SLOs, dashboards, and runbooks. -->
