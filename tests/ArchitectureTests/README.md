# Architecture test

**Rule:** `InvoiceApp.Domain` must not depend on `InvoiceApp.Api`, `Microsoft.AspNetCore`, `System.Net.Http`, `Microsoft.EntityFrameworkCore`, `Microsoft.Data.SqlClient`, or `Azure.Messaging.ServiceBus`.

**Why it matters:** When Azure SQL / PayEx / Service Bus land, they must sit behind interfaces (like `IInvoiceRepository`), not inside `ApprovalService`. INC-2041 is the failure mode this blocks: a synchronous PayEx HTTP call on the approve path.

## Setup (once)
1. Clone `ai-in-sdlc-assignment` **next to** this submission repo (same parent folder).
2. Default `ProjectReference` resolves via `AssignmentRoot` → `../../../ai-in-sdlc-assignment`.
3. In CI, checkout the assignment to `ai-in-sdlc-assignment` beside the submission (see `.github/workflows/arch-test.yml`).

## Command
```bash
dotnet test tests/ArchitectureTests --logger "console;verbosity=normal"
```

## Proof it can fail
- Green: both tests pass on the real Domain assembly; the second test asserts the same rule **fails** when pointed at the Api assembly (negative control).
- Red (manual): temporarily add a Domain type that uses `HttpClient` (e.g. `PayExClient.cs`), re-run; `Domain_must_not_depend_on_web_host_or_io_clients` fails; delete the file. See `proof-of-run.md`.
