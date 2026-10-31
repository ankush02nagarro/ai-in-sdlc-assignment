# Risk audit: agent setup for this service

## Setup (summarise in 3 lines)
`ops/README.md` has **no** agent-setup section at the end (it ends at “No answers here”). The **actual** agent setup in the assignment repo is: Cursor/Claude guided by `AGENTS.md` / `CLAUDE.md`, plus Playwright MCP from `.mcp.json` (`npx @playwright/mcp@latest`). Incident work (INC-2047) additionally assumes humans run read-only `az`/log queries whose output includes supplier emails and untrusted notification text.

## Lethal trifecta
| Leg | Present? | Evidence |
|-----|----------|----------|
| Access to private data | **Yes** | Demo users/passwords in `appsettings.json`; invoice customer names in seed data; incident logs in `ops/incidents/*` include supplier emails and approval payloads. Agent can read the workspace. |
| Exposure to untrusted content | **Yes** | Incident packs and notification bodies are attacker-/supplier-controlled text; Playwright MCP can open pages and return their content into the model context. |
| Ability to communicate externally / act | **Yes** | Playwright MCP can drive a browser (navigate, click, fill) on the operator’s machine; the coding agent can run shell commands the user approves. (No production deploy credentials are in-repo, but local action capability is real.) |

**Verdict:** all three legs can be present in one session if a human uses the coding agent + Playwright MCP while an incident pack (private + untrusted text) is in context. That is the lethal trifecta.

## Decision (pick one)
- [x] **Accept in writing:** accepted by Ankush on 2026-10-31 for **workshop / local** use only.
- [ ] Redesign to remove leg — deferred as a tracked mitigation (below), not required to block local diagrams/evals.

**Residual risk:** a malicious string in an incident log or a page opened via Playwright could influence the agent to exfiltrate seed/customer-like data or to perform unwanted browser actions if the operator rubber-stamps tool calls.

**Mitigations kept while accepting:**
1. Do **not** point Playwright MCP at production URLs or paste production secrets into chat.
2. Autonomy policy: agent does not post to incident channels or run mutating `az` (L0/L1).
3. Prefer pasting **redacted** log excerpts rather than whole packs when using browser tools in the same session.

**Redesign backlog (if trifecta must be broken):** remove or disable Playwright MCP for incident sessions (drops external-act leg for browser), **or** keep MCP but forbid incident/PII files in the same workspace chat (drops private-data co-presence). Cost: slower UI debugging / more manual copy-paste.

## Revisit trigger
Re-open this decision when **any** of: Playwright MCP is enabled in a session that also has production credentials or unredacted customer data; the agent is granted non-interactive shell/`az` write; or an autonomy level ≥ L3 can post externally. Also revisit at SOC 2 evidence freeze.
