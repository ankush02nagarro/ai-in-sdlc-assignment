# Corrections to the agent's first draft

| What the agent drew / said | Why it was wrong | Correction |
|----------------------------|------------------|------------|
| SQL + Service Bus + PayEx as live containers | `ops/README.md` describes the *planned* production shape; AGENTS.md says never treat ops as current | Removed from as-built; only on `target-state.mmd` with NOT BUILT |
| Approve under InvoicesController | `ApprovalsController` owns approve/reject; InvoicesController is CRUD + submit | Sequence uses `POST /api/approvals/{invoiceId}/approve` |
| Controllers → store only via service | `InvoicesController` injects `IInvoiceRepository` directly | Shown as C5 on container diagram; not used as the architecture test (would fail today) |
| Domain already calls PayEx | No PayEx types in Domain; INC-2041 is a *future* failure mode | Architecture test: Domain must not depend on `System.Net.Http` / AspNetCore / EF / ServiceBus |
