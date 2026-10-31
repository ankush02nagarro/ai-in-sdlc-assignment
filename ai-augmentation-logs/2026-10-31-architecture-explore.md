# 2026-10-31 — Architecture exploration

**Goal:** Distinguish as-built code from ops planned infrastructure.

**Agent contribution:** Listed controllers, Domain service, in-memory store, Program.cs DI; flagged that ops describes SQL/Service Bus/PayEx not present in `src/`.

**What I kept:** Citation table C1–C6 / S1–S5; InvoicesController→store as C5; scoped ApprovalService.

**What I discarded:** Agent drafts that drew PayEx/SQL on as-built; inventing `DecisionResponse` / wrong approve route from INC-2041 logs.

**Tools:** Read assignment repo; no production credentials used.
