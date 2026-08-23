---
schema_version: "0.1.0"
id: "ai-to-ai-bus"
title: "AI-to-AI Bus — Inter-Agent Coordination & Durable Event Routing"
domain: "fleet-coordination"
version: "0.1.0"
status: "active"
verification_state: "verified"
last_verified: "2026-08-21T22:00:00Z"
confidentiality: "public"
provenance:
  origin_task: "ai-to-ai-bus-v0.1.0"
  author_alias: "hermb"
  verifier_alias: "hermb"
sources:
  - id: "src-bus-spec"
    title: "Generalized Agent Bus Protocol Specification"
    trust_label: "protocol_spec"
tags:
  - "inter-agent-bus"
  - "event-routing"
  - "durable-messaging"
  - "watchdog"
  - "lifecycle-tracking"
related_links:
  - rel: "spec"
    uri: "https://github.com/sherpa-md/sherpa-spec"
  - rel: "core-fleet"
    uri: "../core-fleet/CoreFleet.sherpa.md"
---

# AI-to-AI Bus — Inter-Agent Coordination & Durable Event Routing

## 1. Purpose & Scope

The **AI-to-AI Bus** provides an asynchronous, durable coordination backbone and message exchange layer for multi-agent autonomous fleets.

By decoupling agent interactions through persistent append-only event logs, durable message tracking, destination-aware routing, claim-based concurrency control, and autonomous transport watchdogs, this kit prevents message loss, duplicate execution, and task deadlocks across distributed agent topologies.

---

## 2. Core Architecture & Message Lifecycle

```text
+-----------------------------------------------------------------------+
|                         Publishing Node / Agent                       |
|          (Posts Task Handoff, Query, or Status Notification)          |
+-----------------------------------+-----------------------------------+
                                    |
                        [1. Append to Message Ledger]
                                    v
+-----------------------------------------------------------------------+
|                      Durable AI Chat Bus Ledger                       |
|  - Append-Only Storage (`messages.jsonl` / Database)                  |
|  - Deduplication Engine (UUIDv4/v7 message IDs + Hash Window)         |
|  - Channel Routing (`general`, `handoffs`, `infra`, `alerts`)         |
+-----------------------------------+-----------------------------------+
                                    |
              [2. Destination-Aware Webhook Wakeup / Polling]
                                    v
+-----------------------------------------------------------------------+
|                        Worker Action Router                           |
|  - Target Filtering (`to: worker_alias` / `to: all`)                 |
|  - State Transitions (`CLAIM` -> `STARTED` -> `DONE` / `BLOCKED`)     |
|  - Durable Execution Checkpointing (`artifacts/<task_id>/`)           |
+-----------------------------------+-----------------------------------+
                                    ^
                                    | [3. Heartbeat & Recovery]
+-----------------------------------+-----------------------------------+
|                     Transport & Watchdog Monitor                      |
|  - Unacknowledged Claim Expiry & Re-queueing                          |
|  - Stale Worker Detection & Heartbeat Enforcement                     |
|  - Deduplicated Operator Alerting                                     |
+-----------------------------------------------------------------------+
```

### Protocol Lifecycle States

1. **`SENT`**: The message has been durably appended to the bus ledger with a unique message ID and routing headers.
2. **`RECEIVED`**: The target node's transport adapter has acknowledged ingestion and validated payload integrity.
3. **`STARTED` / `CLAIM`**: The receiving worker has atomically claimed the task, preventing race conditions or duplicate execution by other workers.
4. **`COMPLETED` / `DONE`**: The worker has verified task results, stored persistent artifacts, and reported final status proof.
5. **`FAILED` / `BLOCKED`**: The task could not proceed due to unmet dependencies, safety constraints, or errors, posting concrete next actions and diagnostic logs.

---

## 3. Protocol Schema & Routing Format

```json
{
  "id": "66a6dac2-9da5-4f06-82f6-b3bc8d04bf0b",
  "timestamp": "2026-08-21T22:00:00Z",
  "channel": "handoffs",
  "from": "orchestrator-node",
  "to": "compute-worker-1",
  "kind": "handoff",
  "task_id": "bus-action-task-001",
  "payload": {
    "instruction": "Execute verified domain kit release.",
    "context_uri": "artifacts/task-001/input-spec.md",
    "timeout_seconds": 3600
  },
  "signature": "hmac-sha256-signature"
}
```

### Destination-Aware Routing Rules
- **Explicit Addressing (`to: node_id`)**: Dispatches direct wake-up webhook to the designated node.
- **Broadcast Addressing (`to: all`)**: Broadcasts to all active fleet nodes; strict atomic claiming prevents duplicated task runs.
- **Ledger Only (No `to`)**: Recorded in chronological ledger without invoking immediate agent wakeups.

---

## 4. Transport Watchdog & Autonomous Healing

An autonomous transport watchdog runs in the background to guarantee continuity across network partitions or node restarts:
- **Claim Timeout Monitor**: Scans for tasks in `CLAIM` or `STARTED` states exceeding their execution TTL without intermediate status heartbeats.
- **Deadlock Breaker**: Automatically posts `NEEDS-APPROVAL` or releases abandoned claims back to the queue with incremented retry counts.
- **Transport Self-Test**: Issues periodic canary round-trip pulses across the private transport network.

---

## 5. Verification Evidence & Acceptance Criteria

- **Deduplication Verification**: Resending identical message IDs within the deduplication window produces idempotent acknowledgments without duplicate queueing.
- **Claim Isolation**: Concurrent workers attempting to claim the same task ID resolve with exactly one successful claim.
- **Watchdog Recovery**: Simulated ungraceful worker termination results in claim expiration and warning broadcast within configured timeout threshold.
