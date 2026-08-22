# Token Piggy Bank — LLM Quota & Value Governor

[![SherpaMD Spec: v0.1.0](https://img.shields.io/badge/SherpaMD-v0.1.0-blue.svg)](https://github.com/sherpa-md/sherpa-spec)
[![Domain: fleet-operations](https://img.shields.io/badge/Domain-fleet--operations-green.svg)](../../catalog.json)
[![Status: active](https://img.shields.io/badge/Status-active-brightgreen.svg)](./SHERPA.md)

The **Token Piggy Bank** provides deterministic quota governance, real-time burn pacing, reserve headroom protection, multi-tier routing, and outcome-based token accounting across multi-agent workflows.

---

## Overview

Autonomous agent fleets can consume millions of LLM tokens in minutes if unrestrained. The Token Piggy Bank couples a real-time visual telemetry dashboard with a deterministic backend quota governor:

1. **Normalized Quota Windows**: Normalizes disparate vendor rate-limits (6h, 12h, 24h, 168h windows) into a unified accounting schema (`used`, `available`, `reset`).
2. **Telemetry Verification States**: Explicit confidence labeling across `VERIFIED`, `ESTIMATED`, `STALE`, and `UNKNOWN`.
3. **Burn Ratio Pacing**: Real-time burn velocity tracking ($\beta = \text{Actual Burn Rate} / \text{Target Pace}$) with automated throttling and circuit breakers.
4. **20–25% Reserve Headroom**: Immutable reserve floor allocated strictly for high-priority interactive queries and emergency multi-agent recovery.
5. **Multi-Tier Model Routing**: Intelligent task dispatching across Economy, Balanced, and Premium model tiers with automatic load shedding.
6. **Failure Mitigation & Circuit Breaker**: Exponential backoff with jitter and retry-storm protection (max 3 retries).
7. **Surplus & Harvest Queue**: Opportunistic background batch harvesting during low-burn periods near window rollovers.
8. **Task Outcome Ledger**: Immutable append-only audit trail (`usage_audit.jsonl`) tying token expenditure to verified delivered value.

---

## Kit Contents

```text
domains/token-piggy-bank/
├── SHERPA.md              # Canonical SherpaMD specification and governance policy
├── ONE_SHOT_INSTALL.md    # Self-contained multi-LLM portable installer
└── README.md              # Domain kit overview and documentation (this file)
```

---

## Quickstart & Installation

To install and configure the Token Piggy Bank in any AI agent environment or fleet host, execute the self-contained one-shot installer:

```bash
# Hand ONE_SHOT_INSTALL.md to your coding or operations AI agent:
# "Install this on my system."
```

Refer to [`ONE_SHOT_INSTALL.md`](./ONE_SHOT_INSTALL.md) for full implementation specifications, adapter contracts, acceptance tests, and deployment modes.

---

## Burn Ratio & Action Matrix

$$\beta = \frac{\text{Actual Burn Rate}}{\text{Target Pace}} = \frac{\text{Tokens Used} / \text{Elapsed Window Time}}{\text{Total Window Budget} / \text{Total Window Duration}}$$

| Burn Ratio ($\beta$) | Pacing Status | Fleet Governor Action |
|---|---|---|
| **$< 0.70$** | **Underusing** | Surplus capacity detected. Enable background batch harvesting. |
| **$0.70 - 1.10$** | **On Pace** | Nominal burn. Standard autonomous execution permitted. |
| **$> 1.10 - 1.50$** | **Elevated** | Consumption above target. Defer low-priority cron jobs; warn operators. |
| **$> 1.50 - 2.00$** | **Early Exhaustion** | High exhaustion risk. Enforce downgrade to economy models; throttle workers. |
| **$> 2.00$** | **Critical** | Circuit breaker tripped. Halt all autonomous jobs immediately. |

---

## Model Routing Tiers

- **Economy Tier**: Ultra-fast, lightweight models for subagent search, text extraction, and classification.
- **Balanced Tier**: Standard workhorse LLMs for code editing, test synthesis, and data formatting.
- **Premium Tier**: Frontier reasoning models reserved for architectural planning, root-cause analysis, and human-in-the-loop review.

---

## Governance & Specification

For complete metadata, provenance, and normative rules, see [`SHERPA.md`](./SHERPA.md).
