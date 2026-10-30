# Autonomy policy: <PICK ONE: month-end log triage | dependency bumps | first-response incident summaries>

**Owner:** TODO  **Version:** 0.1  **Review cadence:** TODO

## Levels
- **L0** Agent off. **L1** Suggests, human does the work. **L2** Drafts, human reviews and applies. **L3** Acts within a sandbox/guardrails, human reviews after. **L4** Acts, exceptions only.

## Tasks by level
| Task | Level now | Controls that make it safe | Evidence to move up | Who approves the move |
|------|-----------|----------------------------|---------------------|------------------------|
| TODO | | | | |
| TODO | | | | |
| TODO | | | | |

## Controls (per level)
- Read/write scope, secrets exposure, rate limits, audit trail, kill switch, rollback.

## Promotion evidence
Quantified: e.g. N consecutive weeks, ≥X% accepted without edit, 0 incidents attributable, sampled review of Y%.

## Demotion triggers
TODO

## Day-one level for this team
**Level: TODO**, because two of six engineers are new to the codebase: they cannot yet catch a plausible-but-wrong agent output, so TODO (pairing rule, who reviews, what stays human-only).
