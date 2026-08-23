# AI-to-AI Bus Kit

Durable, asynchronous event bus and inter-agent coordination layer for distributed autonomous agent fleets.

## Core Capabilities

- **Destination-Aware Routing**: Direct point-to-point addressing (`to: node_id`), channel multiplexing (`handoffs`, `general`, `infra`), and fleet broadcast.
- **Durable Lifecycle Tracking**: Explicit lifecycle state tracking (`SENT` -> `RECEIVED` -> `STARTED` -> `COMPLETED` / `FAILED`).
- **Atomic Task Claims**: Prevents race conditions and duplicated effort across concurrent workers.
- **Autonomous Watchdog**: Monitors heartbeat cadences, reclaims stalled tasks, and alerts operators on unacknowledged claims.

## State Transition Matrix

```text
[SENT] --> [RECEIVED] --> [CLAIM / STARTED] --> [COMPLETED / DONE]
                                     |
                                     +--------> [FAILED / BLOCKED]
```

## Files & Artifacts

- [`AItoAIBus.sherpa.md`](AItoAIBus.sherpa.md) — Formal SherpaMD domain kit specification.
