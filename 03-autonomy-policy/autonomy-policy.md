# Autonomy policy: first-response incident summaries

**Owner:** Ankush (Invoice Approval)  **Version:** 0.1  **Review cadence:** monthly + after any incident where an agent draft was used

## Levels
- **L0** Agent off. **L1** Suggests, human does the work. **L2** Drafts, human reviews and applies. **L3** Acts within a sandbox/guardrails, human reviews after. **L4** Acts, exceptions only.

## Tasks by level
| Task | Level now | Controls that make it safe | Evidence to move up | Who approves the move |
|------|-----------|----------------------------|---------------------|------------------------|
| Draft timeline + hypothesis from `ops/incidents/*` pack | **L2** | Read-only pack + repo; no `az` write; draft stays in ticket/PR comment | 10 consecutive summaries accepted with ≤ minor edits; 0 material root-cause errors | Tech lead |
| Propose “next command to run” (read-only `az`/log queries) | **L1** | Human pastes/runs; commands listed, not executed by agent | 20 proposed commands reviewed; 0 would have mutated prod | On-call + tech lead |
| Post summary to incident channel / update status | **L1** | Human posts; agent never has webhook/token | After L2 draft bar met **and** 4 weeks with 0 wrong-status posts | Eng manager |
| Change Service Bus filters / redeploy / pay-ex config | **L0** | Out of scope for this workflow | n/a — separate change policy | n/a |

## Controls (per level)
- **Read scope:** incident folder + linked diffs/logs only; no customer DB dumps.
- **Secrets:** no production credentials in the agent session; INC-2047-style tooling stays human-held.
- **Rate / blast:** one draft per incident; no auto-loop on live channels.
- **Audit:** save agent draft + final human post side-by-side in the ticket.
- **Kill switch:** tech lead sets workflow to L0 in this file; revoke any MCP/tool tokens.
- **Rollback:** channel posts corrected by human; no automated “fix-forward” by agent.

## Promotion evidence
Move L2→L3 (auto-post draft to a **private** staging channel only) after: ≥8 weeks at L2, ≥10 incidents, ≥90% drafts accepted without material edit, **0** incidents where the agent’s wrong hypothesis delayed mitigation, sampled review of 100% of drafts by a second engineer for the first month at L3.

## Demotion triggers
Any material wrong root cause that reaches the channel; any agent-initiated prod mutation attempt; two new joiners on-call in the same week without a seasoned partner → drop posting to L1 until pairing coverage restored.

## Day-one level for this team
**Level: L1 for anything that leaves the laptop; L2 only for internal draft summaries**, because two of six engineers are new to the codebase: they cannot yet reliably catch a plausible-but-wrong agent narrative (e.g. blaming deprecated-config WARN lines in INC-2041). Pairing rule: a seasoned engineer reviews every agent draft before it is pasted into the incident. Production changes and Service Bus filter edits stay **human-only (L0)**.
