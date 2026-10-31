# ADR-001: Guaranteeing an approved invoice reaches PayEx exactly once

- **Status:** Accepted
- **Author:** Ankush (written by me; agent used only for the three stress transcripts)
- **Date:** 2026-10-31

## Context
- ~40k invoices/month, 60% in last 3 working days, peak ~80 approvals/min.
- PayEx returns a reference on success; **times out at 30s, and a timeout does not reliably mean failure.**
- SOC 2 Type II in six months; approval actions auditable 7 years.
- Team of six (two new), one-week on-call, Azure App Service + Azure SQL + (unused) Service Bus.
- Today’s code has **no** PayEx and **no** SQL (`InMemoryInvoiceRepository` only). This ADR is for the upcoming integration. INC-2041 shows what happens if PayEx is called synchronously on approve.

## Options considered
| | A. Idempotency key + dedupe table | B. Transactional outbox + worker | C. Optimistic submit + nightly reconciliation |
|--|--|--|--|
| Does PayEx support idempotency keys? | Assume yes via invoice id / reference (confirm with vendor before build); if no, A alone is insufficient | Same assumption for worker POSTs | Same; nightly job still needs a safe lookup key |
| Duplicate risk on timeout | Medium if caller retries without key; **low** if key enforced | **Low** if worker always sends invoice id and never blind-retries without PayEx GET | **High** — timeout treated as miss → resubmit or overnight “fix” creates doubles |
| Lost-submission risk | **High** if approve commits then process dies before POST | **Low** — outbox row in same txn as Approved | Medium — lost until nightly; finance gap overnight |
| Build cost | 10–14 eng-days (agent); plausible | 15–20 (agent, optimistic); **I budget 25–30** with two new engineers | 12–18 build, but high ops tax |
| Run cost / on-call load | Low | Medium (lag, poison messages) | High (nightly diffs, rematches) |
| Audit story for SOC 2 | Weak if “Approved” ≠ “must submit” persisted | Strong: Approved + outbox intent + PayEx reference | Weak overnight; rematch evidence is messy |

## Decision
**B primary, with A’s key discipline and C as a backstop:** on Approve, write invoice `Approved` and an outbox row in one Azure SQL transaction; a submission worker drains the outbox and POSTs to PayEx using the **invoice id as the idempotency/reference key**; a **nightly reconciliation** job compares Approved-without-PayEx-reference vs PayEx and alerts — it does not blind-resubmit. Approve stays fast and auditable; PayEx latency stays off the request path (the INC-2041 lesson).

## Strongest objection, and my answer
**Objection:** A is cheaper and “good enough” if PayEx supports keys; B is over-engineering for a six-person team.  
**Answer:** A does not persist *intent to submit*. A crash between Approve and POST leaves an Approved invoice that never reaches PayEx with no row to retry — unacceptable under SOC 2 and month-end cash. The incremental cost of outbox on SQL we are already adopting is smaller than one duplicate-payment incident. Keys alone do not create work to drain.

## Stress tests on the agent's recommendation
1. **Preference pushback** (I preferred C): recommendation **did not move** — stayed on B. Evidence: `agent-transcripts/01-preference.md`. Result: agent correctly treated sprint savings on C as false; I agree.
2. **3 a.m., last day of month failure**: stale outbox `pending` after a late PayEx success under 30s timeout → duplicate risk if ops re-POSTs. Evidence: `agent-transcripts/02-failure.md`. Mitigation/runbook: throttle worker; **GET PayEx by invoice id before any retry**; never reset outbox “clean” without lookup.
3. **Cost to build and to run**: agent picked **A on cost alone** (10–14d, low ops) and called B 15–20d medium ops. Evidence: `agent-transcripts/03-cost.md`. My numbers: B **25–30d**; I reject cost-only A because of lost-intent. Agent did correctly note that cost misses correctness.

## Consequences
- **Operational:** new worker service/function, outbox lag SLOs, poison-message runbook, month-end throttle playbook.
- **Data / schema:** Azure SQL invoices table + outbox (or outbox columns) + unique PayEx reference; Domain stays free of HttpClient (architecture test).
- **Audit:** every Approve has intent row; PayEx reference attached when settled; 7-year retention on decision + submission trail.

## Revisit when (measurable triggers)
- PayEx documents that invoice-id idempotency is **not** supported or is scoped differently than we assumed.
- Duplicate-submission count **> 0** in any calendar month (finance or PayEx report).
- Outbox lag p95 **> 60s** at peak for two consecutive month-ends.
- Worker error rate **> 1%** of outbox drains for a week.

## Where the agent was wrong or useless
1. **Cost agent recommended A on cost alone** while admitting A can lose intent — that is not an exactly-once design. Quoting cost without weighting lost Approved invoices is useless for this ADR; I discarded the cost-only pick.
2. **Agent assumed PayEx idempotency on invoice id without vendor evidence.** Useful as a *design assumption* to flag; useless as a fact. We must confirm before build (revisit trigger #1).
3. **Early architecture chats treated ops PayEx/SQL as already present** (see `01-architecture/corrections.md`). Useless for “as-built”; I confined PayEx to this ADR + target diagram.
