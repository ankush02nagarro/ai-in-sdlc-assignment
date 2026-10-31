# Stress 2: 3 a.m., last day of month (verbatim agent reply)

**Prompt summary:** Chosen design is outbox + worker + invoice-id key + nightly reconcile. Ask for one concrete failure of *this* design and a runbook. Do not re-POST blindly.

**Agent session:** [3am failure](1f544864-e97c-403e-a456-c246511e6fcd)

---

## Failure mode (this design)

**Stale “pending” after a late PayEx success (timeout ≠ failure).**

At 03:00 UTC month-end, the worker claims a huge outbox backlog. It POSTs invoice `INV-88421` to PayEx with that id as the idempotency/reference key, then hits the **30s timeout** and leaves the outbox row `pending` (or resets for retry). PayEx actually **accepted and booked the payment** after the client gave up. Under load, retries, lease churn, or a second worker reclaim can keep treating the row as unpaid work. If PayEx’s idempotency is weak under replay storms, or ops “helps” by forcing a resend, you get **double payment / duplicate settlement** for the same approved invoice—while the DB still shows Approved + unacked outbox.

Nightly reconciliation is the backstop, but it does **not** run until after the peak window; damage can accumulate overnight.

## Runbook

**Detect**
- Spike of outbox rows stuck `pending`/`in_flight` past lease + timeout for Approved invoices.
- PayEx responses/logs: duplicate reference, already-paid, or successful settle for ids still `pending` locally.
- Cash/settlement mismatch vs approved unpaid count before the nightly job.

**Mitigate**
1. Pause or throttle the PayEx worker for the affected queue/shard.
2. For each stuck invoice id: **query PayEx by invoice id first**; mark outbox `succeeded` if already paid; only enqueue a new POST if PayEx confirms **not** present.
3. Drain with reduced concurrency; keep one writer per invoice id (lease/lock).
4. Let nightly reconciliation catch residuals; escalate finance for any confirmed duplicates.

**Do not**
- Re-POST blindly after timeout, restart, or “stuck pending.”
- Delete/reset outbox rows to “retry clean” without a PayEx lookup.
- Treat 30s timeout as definitive failure or as success without confirmation.
