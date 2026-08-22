---
schema_version: "0.1.0"
id: "core-fleet"
title: "Core Fleet & Multi-Agent Coordination"
domain: "fleet-ops"
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
    title: "AI2AI Bus Protocol"
    uri: "../hermes-llm-wiki/sources/ai2ai-bus-protocol-summary.md"
    type: "protocol_spec"
tags:
  - "fleet-ops"
  - "nodes"
  - "coordination"
related_links:
  - rel: "spec"
    uri: "https://github.com/sherpa-md/sherpa-spec"
  - rel: "hermes-llm-wiki"
    uri: "../hermes-llm-wiki/SHERPA.md"
---

# Core Fleet & Multi-Agent Coordination Kit

## 1. Purpose & Scope
Defines the multi-agent node topology, communication mechanisms, and coordination rules for distributed agent operations.

## 2. Fleet Topology & Node Archetypes
- **Orchestrator Node (`orchestrator-node`)**: Central continuity pivot, scheduling orchestrator, and external gateway bridge.
- **Local Worker Node (`compute-worker`)**: High-performance compute node (GPU workloads, media processing, local computer execution).
- **Helper Worker Node (`helper-worker`)**: Dedicated subagent task worker for parallelized execution.
- **Workspace Node (`ho`)**: Isolated workspace and project execution environment.

## 3. Core Directives
1. **Bus-Centric State**: AI chat bus is the canonical coordination ledger for claims, handoffs, and status.
2. **Node Isolation**: Actions execute on the designated node owning the required capabilities and environment.
3. **Durable Artifacts**: Always write durable markdown checkpoints under project directories or `artifacts/<task-id>/`.

## 4. Verification Evidence
- Verified bus connectivity and coordination via `ai-chat read --channel general --limit 1` on 2026-08-21.
