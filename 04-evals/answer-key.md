# Answer key used for scoring (my labels, written before any run)

`ops/evals/README.md` deliberately does not say which cases are defective. These labels are mine, written
from reading each diff against the real code before I ran anything. A run counts as **caught** only if it names
the defect in the "Must name" column. Anything else near the right line is **missed**. On a clean case, a
**false alarm** means asserting a defect. Style notes and "consider adding a test" are not false alarms.

| Case | Label | Must name (to count as caught) | Notes / how confident I am in the label |
|------|-------|--------------------------------|------------------------------------------|
| 01 bulk-approve | defective | `request.Ids` is nullable and iterated without a check (NRE, so 500), **or** a failure part-way through the loop leaves earlier invoices approved with no error mapping (no `Handle`, partial batch) | High. Either defect counts. |
| 02 search | defective | SQL injection: `customer`/`status` interpolated into SQL | High |
| 03 discount rounding | defective | Discount is truncated (`ToZero`) before subtracting, so the discounted total rounds **up**: the customer is over-charged up to 0.01 vs the old `AwayFromZero` total (e.g. 1.00 at 0.6%: old 0.99, new 1.00) | Medium-high. Subtle money change with no test. |
| 04 rename | clean | (n/a) Pure rename `_repository` to `_invoices` | High |
| 05 delete | defective | No `[RequireRole("Admin")]`: any signed-in user can delete (AGENTS.md: destructive actions are Admin only) | High. "Ignores not-found / returns 204" alone is not enough. |
| 06 tests | clean | (n/a) Tests only. A duplicate of the existing whitespace-reason test is not a defect | High |
| 07 log payload | defective | Logs the whole invoice **and the session object** at Information (PII / session data in logs) | High |
| 08 dictionary | defective | `ConcurrentDictionary` replaced by `Dictionary` with no lock in a **singleton** repository, so concurrent requests race (check-then-add, corrupt dictionary) | High |
| 09 README + logging | clean | (n/a) Docs plus a logging-level tweak that matches the current `appsettings.json` | Medium. The README "sign out to reset data" claim cannot be checked from the diff alone. Calling it *possibly inaccurate* is a doc note. Asserting a code defect is a false alarm. |
| 10 catch-all | defective | `catch (Exception)` returns **200 "completed"**, so every unexpected failure is reported to the client as success | High |
| 11 PayEx retry (mine) | defective | Retrying a non-idempotent payment POST after a timeout, with no idempotency key, causes duplicate payment | High |
| 12 trim reason (mine, clean) | clean | (n/a) `Trim()` is after the `IsNullOrWhiteSpace` guard | High |

Totals: 8 defective (01, 02, 03, 05, 07, 08, 10, 11) and 4 clean (04, 06, 09, 12).
