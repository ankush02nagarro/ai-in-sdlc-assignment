# ADR-001: Guaranteeing an approved invoice reaches PayEx exactly once

- **Status:** Draft
- **Author:** TODO (written by me, not the agent)
- **Date:** TODO

## Context
- ~40k invoices/month, 60% in last 3 working days, peak ~80 approvals/min.
- PayEx returns a reference on success; **times out at 30s, and a timeout does not reliably mean failure.**
- SOC 2 Type II in six months; approval actions auditable 7 years.
- Team of six (two new), one-week on-call, Azure App Service + Azure SQL + (unused) Service Bus.

## Options considered
| | A. Idempotency key + dedupe table | B. Transactional outbox + worker | C. Optimistic submit + nightly reconciliation |
|--|--|--|--|
| Does PayEx support idempotency keys? | TODO (check evidence pack) | n/a | n/a |
| Duplicate risk on timeout | TODO | TODO | TODO |
| Lost-submission risk | TODO | TODO | TODO |
| Build cost | TODO | TODO | TODO |
| Run cost / on-call load | TODO | TODO | TODO |
| Audit story for SOC 2 | TODO | TODO | TODO |

## Decision
TODO: chosen option, in one paragraph.

## Strongest objection, and my answer
TODO: the best argument against my choice, and why I still choose it.

## Stress tests on the agent's recommendation
1. **Preference pushback** (I stated a preference for a different option): did the recommendation move? Evidence: `agent-transcripts/01-preference.md`. Result: TODO
2. **3 a.m., last day of month failure**: how does my choice fail? Evidence: `agent-transcripts/02-failure.md`. Mitigation/runbook: TODO
3. **Cost to build and to run**: evidence `agent-transcripts/03-cost.md`. My numbers vs the agent's: TODO

## Consequences
- Operational: TODO
- Data / schema: TODO
- Audit: TODO

## Revisit when (measurable triggers)
- TODO e.g. PayEx adds native idempotency keys
- TODO e.g. duplicate-submission count > 0 in any month
- TODO e.g. outbox lag p95 > N seconds at peak

## Where the agent was wrong or useless
Be specific: quote the claim, say what was wrong, how you found out.
1. TODO
2. TODO
3. TODO
