# Stress 3: build/run cost (verbatim agent reply)

**Prompt summary:** Estimate eng-days and on-call load for A/B/C; pick on cost alone; note what cost misses.

**Agent session:** [cost stress](01c24812-f0a7-4ccf-8780-7c3e116c3351)

---

### Rough build (eng-days)
| Option | Days | Notes |
|--------|------|--------|
| **A** Idempotency key + dedupe | **10–14** | Schema/unique index, API middleware, client key plumbing, tests |
| **B** Outbox + worker | **15–20** *(optimistic)* | Outbox txn, poller/worker, retries, basic metrics; lean on App Service + SQL |
| **C** Optimistic + nightly recon | **12–18** | Fire-and-forget path + recon job + mismatch/remediation UI |

Infra at ~40k/mo and peak 80/min is negligible for all three on Azure App Service + SQL.

### Monthly run / on-call
- **A — Low:** Once the unique constraint holds, retries are silent; rare “why was this rejected” tickets.
- **B — Med:** Worker lag, poison rows, and replay need alerts and occasional hands-on.
- **C — High:** Nightly diffs, false positives, and manual rematches become standing ops load (worse under SOC2 evidence pressure).

### Cost-only pick
**Choose A.** Lowest build + lowest ongoing load for this volume and stack.

### What cost misses (correctness)
A can still **lose intent** if the process dies after approval commit and before PayEx (unless you also persist “must send”). **B** is the strongest delivery guarantee. **C** accepts **overnight inconsistency** and rematch risk—cheapest-looking ops debt, not exactly-once.

---

**My note (human):** The agent’s 15–20d for B is optimistic for a team with two new engineers (I budget **25–30d** including load tests and runbooks). Cost-only A is rejected in the ADR because losing intent after Approve breaks SOC 2 auditability of “approved ⇒ submitted.”
