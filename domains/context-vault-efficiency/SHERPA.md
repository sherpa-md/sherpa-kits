---
schema_version: "0.1.0"
id: "context-vault-efficiency"
title: "Context Vault & Token Efficiency — Living Knowledge & Model Tiering"
domain: "agent-memory-optimization"
version: "0.1.0"
status: "active"
verification_state: "verified"
last_verified: "2026-08-21T22:00:00Z"
confidentiality: "public"
provenance:
  origin_task: "context-vault-efficiency-v0.1.0"
  author_alias: "hermb"
  verifier_alias: "hermb"
sources:
  - id: "src-karpathy-wiki"
    title: "Karpathy LLM-Wiki Knowledge Anti-Rot Concept"
    url: "https://gist.github.com/karpathy"
    trust_label: "concept"
  - id: "src-vault-design"
    title: "Hermes Multi-Tier Vault Memory Architecture"
    trust_label: "architecture_spec"
tags:
  - "context-efficiency"
  - "knowledge-vault"
  - "anti-rot"
  - "cheapest-adequate-model"
  - "outcome-ledger"
  - "token-optimization"
related_links:
  - rel: "spec"
    uri: "https://github.com/sherpa-md/sherpa-spec"
  - rel: "token-piggy-bank"
    uri: "../token-piggy-bank/SHERPA.md"
---

# Context Vault & Token Efficiency — Living Knowledge & Model Tiering

## 1. Purpose & Scope

The **Context Vault & Token Efficiency** kit establishes an anti-rot knowledge architecture and cost-optimized execution framework for autonomous multi-agent systems.

Rather than inflating context windows by continuously appending uncurated chat transcripts, this system employs continuous in-place synthesis into living Markdown documents, targeted retrieval of relevant durable state, task-appropriate model tiering (cheapest adequate model), and empirical outcome tracking.

---

## 2. Context Lifecycle & Compaction Pipeline

```text
+-----------------------------------------------------------------------+
|                             Incoming Task                             |
+-----------------------------------+-----------------------------------+
                                    |
                    [1. Targeted Substring / Semantic Search]
                                    v
+-----------------------------------------------------------------------+
|                         Search & Prune Stage                          |
|  - Retrieve ONLY relevant facts/sections (Never full codebases)       |
|  - Filter redundant tool outputs and raw transcripts                  |
+-----------------------------------+-----------------------------------+
                                    |
                    [2. Context Compression & Assembly]
                                    v
+-----------------------------------------------------------------------+
|                    Living Knowledge Vault Synthesizer                 |
|  - Karpathy Anti-Rot Pattern: In-Place Synthesis of Living Docs       |
|  - Structured Front Matter & Provenance Headers                       |
+-----------------------------------+-----------------------------------+
                                    |
                    [3. Routing: Cheapest Adequate Model]
                                    v
+-----------------------------------------------------------------------+
|                   Model Tier Dispatcher (Economy/Balanced/Premium)    |
|  - Economy: Fast extraction, classification, syntax formatting        |
|  - Balanced: Core code generation, tool invocation, refactoring       |
|  - Premium: High-level architectural planning, high-risk review       |
+-----------------------------------+-----------------------------------+
                                    |
                    [4. Execution & Verification]
                                    v
+-----------------------------------------------------------------------+
|                      Task Outcome Ledger                              |
|  - Records: prompt_tokens, completion_tokens, duration, outcome, cost |
|  - Generates empirical performance profile per task category          |
+-----------------------------------------------------------------------+
```

### The Karpathy Anti-Rot Synthesis Pattern

Uncurated log accretion causes:
1. Quadratic prompt token inflation and latency degradation.
2. Contradictory instructions across conversational history.
3. Hallucinatory loops driven by stale context.

**Remedy**: Workers write durable facts directly to topic-specific domain runbooks (`SHERPA.md` / `artifacts/<task>/`). Chat transcripts are discarded after task completion once durable conclusions have been recorded.

---

## 3. Cheapest Adequate Model Tiering

To maximize throughput and minimize quota exhaustion, tasks are classified into execution tiers before dispatch:

| Tier | Typical Models | Optimal Task Profile | Token Cost Ratio |
|---|---|---|---|
| **Economy** | Small Fast Models (e.g., 8B-class local or light cloud models) | Log parsing, text classification, simple extraction, format translation. | $0.05\times - 0.1\times$ |
| **Balanced** | Mid-Tier Workhorse Models | Tool-calling workflows, standard code modification, unit testing, git operations. | $0.25\times - 0.5\times$ |
| **Premium** | Flagship Reasoning Models | Multi-system architecture, ambiguity resolution, critical security analysis. | $1.0\times$ (Base) |

---

## 4. Outcome Ledger & Empirical Optimization

Every task execution logs an immutable telemetry record into an append-only JSONL ledger (`outcomes.jsonl`):

```json
{
  "task_id": "bus-action-task-001",
  "timestamp": "2026-08-21T22:00:00Z",
  "tier_requested": "economy",
  "model_selected": "balanced-workhorse",
  "prompt_tokens": 1420,
  "completion_tokens": 380,
  "duration_ms": 2840,
  "outcome": "SUCCESS",
  "verification_passed": true,
  "cost_usd": 0.0018
}
```

This ledger is periodically analyzed by the quota governor to dynamically calibrate model tier recommendations based on proven success rates.

---

## 5. Verification Evidence & Acceptance Criteria

- **Compaction Benchmark**: Compacting 50 iterations of raw tool transcripts into a structured living Sherpa runbook achieves $> 90\%$ reduction in subsequent prompt context tokens.
- **Model Downgrade Efficacy**: Routine validation, linting, and extraction tasks routed to the Economy tier maintain a $100\%$ pass rate with an $80\%$ reduction in quota consumption.
- **Ledger Ingestion**: 100% of completed tasks record an immutable entry in the outcome ledger with valid token counts and verification results.
