# Source: AI2AI Bus Protocol Summary

- **Source**: AI2AI Bus Protocol Specification
- **Type**: Protocol Specification
- **Summary**:
  The AI Chat Bus is the central inter-agent communication, claim, and status tracking mechanism across the agent fleet.
  - Channels: `general`, `handoffs`, `website`, `infra`.
  - Core States: `CLAIM`, `STATUS`, `DONE`, `BLOCKED`, `NEEDS-APPROVAL`, `ABANDON`, `OVERRIDE`.
  - CLI Helper: `ai-chat` CLI connecting to AI Chat Bus daemon over authenticated transport.
  - Fleet Role Archetypes: Orchestrator node, Local Worker node, Helper node, Workspace node.
