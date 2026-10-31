# Citations (as-built)

Every box/arrow on the as-built diagrams maps to a row here. Paths are relative to `ai-in-sdlc-assignment/backend/`.

| Id | Claim | File | Symbol / line | Verified |
|----|-------|------|---------------|----------|
| C1 | Approval HTTP entry | `src/InvoiceApp.Api/Controllers/ApprovalsController.cs` | `ApprovalsController`, `[Route("api/[controller]")]`, lines 7–27 | ☑ |
| C2 | Approval business rules | `src/InvoiceApp.Domain/ApprovalService.cs` | `ApprovalService.Approve`, lines 31–40 | ☑ |
| C3 | In-memory store | `src/InvoiceApp.Api/InMemoryInvoiceRepository.cs` | `InMemoryInvoiceRepository : IInvoiceRepository`, lines 6–28 | ☑ |
| C4 | Session Bearer auth | `src/InvoiceApp.Api/Auth/SessionAuthMiddleware.cs` + `Program.cs` L21 | `UseMiddleware<SessionAuthMiddleware>()` | ☑ |
| C5 | InvoicesController also depends on store | `src/InvoiceApp.Api/Controllers/InvoicesController.cs` | ctor takes `IInvoiceRepository` | ☑ |
| C6 | DI wiring | `src/InvoiceApp.Api/Program.cs` | singleton store L14; scoped `ApprovalService` L15 | ☑ |
| S1 | Approve route | `ApprovalsController.cs` | `[HttpPost("{invoiceId}/approve")]` → `POST /api/approvals/{id}/approve` | ☑ |
| S2 | Role gate | `ApprovalsController.cs` L9 + `Auth/RequireRoleAttribute.cs` | `[RequireRole("Approver","Admin")]` | ☑ |
| S3 | Controller → service | `ApprovalsController.cs` L22–23 | `_approvals.Approve(..., GetSession().Username)` | ☑ |
| S4 | Service → store | `ApprovalService.cs` L33–39 | `Find` → `Update` | ☑ |
| S5 | HTTP status mapping | `Controllers/ApiControllerBase.cs` L9–26 | 404 / 409 / 400 | ☑ |
