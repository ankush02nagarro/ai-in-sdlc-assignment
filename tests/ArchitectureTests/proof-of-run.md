# Proof of run

## Green (current code)
Command:
```bash
dotnet test tests/ArchitectureTests --logger "console;verbosity=normal"
```
Result: **2 passed** (`Domain_must_not_depend_on_web_host_or_io_clients`, `Rule_detects_violations_when_they_exist`).
Captured excerpt in `green-run-capture.txt`.

## Red (temporary violation)
Added `InvoiceApp.Domain/PayExClient.cs` that constructs `HttpClient` and calls `PostAsync`, then:
```bash
dotnet test tests/ArchitectureTests --filter "FullyQualifiedName~Domain_must_not" --logger "console;verbosity=normal"
```
Result: **1 failed** — `Violations: InvoiceApp.Domain.PayExClient` (see `red-run-capture.txt`).
File was deleted immediately after capture so the assignment clone is clean again.

## Negative control (always on)
`Rule_detects_violations_when_they_exist` applies the same forbidden-dependency list to the **Api** assembly and asserts failure (expects `ApprovalsController` among failing types). So the rule is proven capable of failing without leaving Domain broken.
