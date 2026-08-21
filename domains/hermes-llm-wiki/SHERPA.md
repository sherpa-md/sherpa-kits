---
schema_version: "0.1.0"
id: "hermes-llm-wiki"
title: "Hermes LLM Wiki & Vault Architecture"
domain: "fleet-knowledge"
version: "0.1.0"
status: "active"
verification_state: "verified"
last_verified: "2026-08-21T20:45:00-05:00"
confidentiality: "public"
provenance:
  origin_task: "release-v0.1.0"
  author_alias: "hermb"
  verifier_alias: "hermb"
sources:
  - id: "src-bus-protocol"
    title: "All Agents AI Chat Bus Protocol"
    uri: "./sources/ai2ai-bus-protocol-summary.md"
    type: "protocol_spec"
  - id: "src-karpathy-concept"
    title: "Karpathy LLM-Wiki Synthesis Concept"
    uri: "./sources/karpathy-llm-wiki-concept.md"
    type: "design_concept"
  - id: "src-hermes-vault"
    title: "Hermes Vault & FFB Memory Tiering Architecture"
    uri: "./sources/hermes-vault-design.md"
    type: "architecture_spec"
tags:
  - "hermes"
  - "llm-wiki"
  - "vault"
  - "ffb"
  - "anti-rot"
  - "fleet-coordination"
related_links:
  - rel: "spec"
    uri: "https://github.com/sherpa-md/sherpa-spec"
  - rel: "core-fleet"
    uri: "../core/SHERPA.md"
  - rel: "sources"
    uri: "./sources/README.md"
---

# Hermes LLM Wiki & Vault Architecture Kit

## 1. Purpose & Scope

This domain kit defines the **Hermes Knowledge Vault and Multi-Agent Coordination Architecture** across distributed agent topologies:
- **Orchestrator Node (`h1`)**: Central continuity pivot and orchestrator.
- **Local Worker Node (`hb`)**: Local compute node for GPU workloads, media pipeline, and local computer operations.
- **Helper Worker Node (`hx`)**: Dedicated subagent helper node.
- **Workspace Node (`ho`)**: Project workspace node.

### The Anti-Rot Paradigm (Karpathy LLM-Wiki)
Instead of appending infinite, unindexed chat logs that cause LLM context rot, Hermes utilizes **SherpaMD** to maintain a curated, synthesized, and continuously updated graph of verified facts, architectural topologies, and operational procedures.

---

## 2. Hermes Memory Vault & FFB Architecture

Hermes organizes state across three distinct persistence tiers:

```
+-------------------------------------------------------------------+
| Tier 1: Ephemeral Context Window                                  |
| (In-flight active prompt tokens; discarded at session end)        |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
| Tier 2: Task Artifact Store (artifacts/<task-id>/)                |
| (Durable checkpoints, tool logs, execution diffs, verify reports) |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
| Tier 3: Curated SherpaMD Knowledge Vault (sherpa-kits)            |
| (Distilled domain knowledge, verified runbooks, living specs)     |
+-------------------------------------------------------------------+
```

### Flywheel Feedback & Fleet Routing (FFB)
1. **Public Model Isolation**: The Orchestrator node is the sole node authorized to serve public web models. Worker nodes report back to the Orchestrator and never serve external requests directly.
2. **Specialized Worker Affinity**:
   - Media discovery, metadata, audio extraction -> routed strictly to designated local worker node.
   - Heavy CUDA/GPU workloads -> routed to local compute worker node.
   - Core orchestrator scheduling & continuous state -> managed by central orchestrator.

---

## 3. Core Directives & Anti-Rot Operating Rules

1. **Bus-Centric Task Claims**: Every agent MUST claim a scoped task on the AI chat bus (`ai-chat post --channel handoffs ...`) before modifying code, configurations, or databases.
2. **In-Place Knowledge Synthesis**: When ports, routes, models, or configurations change, edit the canonical document in-place. Prune stale instructions immediately.
3. **Absolute Secret Hygiene**: Never commit API keys, auth JSON, cookies, or credentials into Sherpa kits or bus messages. Use `[REDACTED]` or reference environment variables.
4. **Actionable Verification**: Technical directives must contain executable verify commands.

---

## 4. Operational Procedures & Runbooks

### Procedure 1: Bus Lifecycle Workflow
Agents interact with the AI Chat Bus using the `ai-chat` CLI:

```bash
# 1. Read incoming handoffs:
ai-chat read --channel handoffs --limit 10

# 2. Post a task claim:
ai-chat post --from worker --channel handoffs \
  "CLAIM task=<task-id> owner=worker scope=<narrow-scope> mode=edit ttl=60 details=<reason>"

# 3. Post interim status:
ai-chat post --from worker --channel handoffs \
  "STATUS task=<task-id> owner=worker scope=<narrow-scope> state=running details=<progress>"

# 4. Post completion proof:
ai-chat post --from worker --channel handoffs \
  "DONE task=<task-id> owner=worker result=<summary> verify=<proof-command-or-artifact>"
```

### Procedure 2: Durable Task Artifact Checkpointing
During long-running tasks, write persistent reports and execution records to disk rather than keeping them solely in context:
- Directory format: `artifacts/<task-id>/report.md`
- Checkpoint cadence: Write intermediate checkpoints after each major sub-step so state survives potential process restarts.

### Procedure 3: Service Health & Log Inspection
Agent services run under the systemd user manager:
```bash
# Check service status:
systemctl --user status ai-chat-bus-outbox-relay.timer

# View recent service journal logs:
journalctl --user -u agent-gateway -n 50 --no-pager
```

---

## 5. Contradiction Notes & Reconciliations

| Issue / Divergence | Obsolete / Conflicting Claim | Ground Truth (Reconciled) | Rationale |
|---|---|---|---|
| Model Serving Gateway | "Workers directly call public website models" | Only Orchestrator communicates with public model serving. | Prevents split-brain state and credential exposure. |
| Chat Transcripts | "Append raw chat logs for memory" | Synthesize into SherpaMD kits + write artifacts to disk. | Solves context rot and token saturation (Karpathy LLM-Wiki). |
| Bus Addressing | Vague names (`agent`, `bot`) | Explicit aliases (`orchestrator`, `worker-local`, `worker-helper`) | Eliminates race conditions and duplicate claims. |

---

## 6. Related Links & Cross-References

- **Specification**: [SherpaMD Specification v0.1.0](https://github.com/sherpa-md/sherpa-spec)
- **Kit Scaffold**: [Sherpa Kit Template](https://github.com/sherpa-md/sherpa-kit-template)
- **Core Fleet Domain**: [`../core/SHERPA.md`](../core/SHERPA.md)
- **Sources Directory**: [`./sources/README.md`](./sources/README.md)

---

## 7. Verification Evidence & Audit Log

- **2026-08-21T20:45:00-05:00**: Updated `hermes-llm-wiki` kit v0.1.0 under `sherpa-kits` for public release.
- **Validation**:
  - `ai-chat health` -> OK (connected to bus).
  - `./validate.sh` -> Verified schema compliance across all kits.
  - Front matter conforms to `sherpa-spec` schema v0.1.0.
