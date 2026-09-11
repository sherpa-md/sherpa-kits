---
schema_version: "0.1.0"
id: "token-piggy-bank"
title: "Token Piggy Bank — LLM Quota & Value Governor"
domain: "fleet-operations"
version: "1.0.0"
status: "active"
verification_state: "verified"
last_verified: "2026-08-21T20:45:00-05:00"
confidentiality: "public"
provenance:
  origin_task: "token-piggy-bank-v1.0.0"
  author_alias: "hermb"
  verifier_alias: "hermb"
sources:
  - id: "src-sherpa-spec"
    title: "SherpaMD Format Specification v0.1.0"
    url: "https://github.com/sherpa-md/sherpa-spec"
    trust_label: "specification"
tags:
  - "token-governance"
  - "quota-management"
  - "llm-routing"
  - "agent-fleet"
  - "burn-rate"
---

# Token Piggy Bank — LLM Quota & Value Governor

## 1. Overview & Architecture

The **Token Piggy Bank** provides deterministic quota governance, real-time burn pacing, reserve headroom protection, multi-tier routing, and outcome-based token accounting across multi-agent workflows.

---

## 2. Quota Telemetry & Verification States

- **Accounting Fields:** `used`, `available`, `reset` (ISO 8601 UTC timestamp).
- **Verification States:** `VERIFIED`, `ESTIMATED`, `STALE`, `UNKNOWN`.

---

## 3. Burn Ratio Pacing & Reserve Protection

$$\beta = \frac{\text{Actual Burn Rate}}{\text{Target Pace}}$$

| Burn Ratio ($\beta$) | Pacing Status | Fleet Governor Action |
|---|---|---|
| **$< 0.70$** | **Underusing** | Surplus capacity detected. Enable background batch harvesting. |
| **$0.70 - 1.10$** | **On Pace** | Nominal burn. Standard autonomous execution permitted. |
| **$> 1.10 - 1.50$** | **Elevated** | Consumption above target. Defer low-priority cron jobs; warn operators. |
| **$> 1.50 - 2.00$** | **Early Exhaustion** | High exhaustion risk. Enforce downgrade to economy models; throttle workers. |
| **$> 2.00$** | **Critical** | Circuit breaker tripped. Halt all autonomous jobs immediately. |

### 20–25% Reserve Headroom
An immutable reserve floor of 20% to 25% of total window allowance is reserved strictly for high-priority interactive human queries and emergency recovery commands.

---

## 4. Multi-Tier Routing & Failure Mitigation

- **Routing Tiers:** Economy (lightweight subagents/searches), Balanced (standard code/test synthesis), Premium (frontier reasoning/architectural design).
- **Retry-Storm Stop:** Exponential backoff with jitter, 3 retries max per task, and cooling on vendor error spikes.
- **Harvest Queue:** Dispatches low-priority batch synthesis when burn ratio $< 0.70$ near reset boundaries.
- **Task Outcome Ledger:** Records duration, tokens, cost estimate, and `value_delivered` flag to `usage_audit.jsonl`.
- **Security & Sanitization:** Strict secret redaction and untrusted data boundaries.
