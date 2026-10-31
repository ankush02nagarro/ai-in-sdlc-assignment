# Items the agent inferred (no direct citation)

Things that appeared in a first-pass agent diagram or narrative but are **not** in the as-built code. Kept here so they do not silently become "facts".

| # | Claim the agent made | Why it is not citable from code | Disposition |
|---|----------------------|----------------------------------|-------------|
| 1 | Azure SQL holds invoices | Only `InMemoryInvoiceRepository` exists; no EF/SqlClient package | Target-state only; marked NOT BUILT |
| 2 | Service Bus publishes `InvoiceApproved` / `invoice.approved` | No Azure.Messaging reference; events appear only in `ops/incidents/INC-2047` | Target-state; note planned rename trap |
| 3 | `PayExClient.SubmitAsync` runs on approve | Present only in INC-2041 deploy-diff under `ops/`, not in `src/` | Target-state + ADR; architecture test forbids Domain→HttpClient |
| 4 | Approve route is `/api/invoices/{id}/approve` | INC-2041 log lines use that path; real route is `/api/approvals/{id}/approve` (C1/S1) | Corrected on as-built sequence |
| 5 | `DecisionResponse` / `CurrentUser` types | Not in Domain or Api; agent invented DTO names from common patterns | Dropped |
| 6 | `ApprovalService` registered as singleton | Patch/diff stories sometimes show singleton; `Program.cs` registers **scoped** (C6) | Corrected |
