# Architecture test

**Rule:** TODO (one sentence: e.g. "Controllers never depend on the store; only the service layer does.")
**Why it matters:** TODO (what breaks when persistence / PayEx lands).

## Setup (once)
1. Clone `ai-in-sdlc-assignment` next to this repo.
2. Fix the `ProjectReference` path in `ArchitectureTests.csproj`.
3. Replace the TODO names in `StructuralRuleTests.cs`.

## Command
```bash
dotnet test tests/ArchitectureTests --logger "console;verbosity=normal"
```

## Proof it can fail
Record a run that is green, then temporarily add a violating reference and record the red run
(paste output into `proof-of-run.md`). A test that cannot fail proves nothing.
