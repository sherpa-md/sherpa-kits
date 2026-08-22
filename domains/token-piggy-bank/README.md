# Token Piggy Bank — LLM Quota & Value Governor

> Deterministic quota governance, real-time burn pacing, reserve headroom protection, multi-tier routing, and outcome-based token accounting across multi-agent workflows.

## Overview

Autonomous AI agent fleets can consume millions of LLM tokens in minutes if unrestrained. The **Token Piggy Bank** provides deterministic quota governance, real-time burn pacing, reserve headroom protection, and outcome-based token accounting across multi-agent workflows.

It couples a real-time visual telemetry ocean dashboard with a deterministic backend quota governor:
1. **Dynamic Wave Geometry:** Visualizes daily token burn against target allocations, where each crest represents one 24-hour cycle.
2. **Cumulative Seabed Accounting:** Sunken gold coins reflect permanent milestone token expenditures (e.g., 1 coin per 250k tokens consumed).
3. **Astronomical Synchronization:** Tracks temporal cadence and window rollovers alongside solar and lunar timeframes.
4. **Zero-Dependency Core:** Operates with pure static web standards (HTML5 SVG, CSS3, ES6) backed by flat-file JSON state contracts.

## Architecture

```text
+-------------------------------------------------------------------------+
|                        Autonomous Agent Fleet                           |
|       (Task Dispatcher / Subagent Spawner / Cron Workloads)             |
+------------------------------------+------------------------------------+
                                     |
                         [1. Quota Check & Routing]
                                     v
+-------------------------------------------------------------------------+
|                       Token Piggy Bank Governor                         |
|  - Normalized Windows (6h, 12h, 24h, 168h)                              |
|  - Burn Ratio Pacing (<0.70 to >2.00)                                   |
|  - 20-25% Reserve Protection                                            |
|  - Tier Routing (Economy / Balanced / Premium)                          |
|  - Retry-Storm Stop & Circuit Breaker                                   |
+------------------------------------+------------------------------------+
                                     |
                         [2. Execution & Telemetry]
                                     v
+-------------------------------------------------------------------------+
|                   Outcome Ledger & Audit Ingestion                      |
|  - usage_audit.jsonl (ts, model, tokens, duration, outcome, cost)       |
|  - Verification Engine (VERIFIED, ESTIMATED, STALE, UNKNOWN)            |
|  - Static tokens.json Contract Generator                                |
+------------------------------------+------------------------------------+
                                     |
                         [3. Visual Dashboard]
                                     v
+-------------------------------------------------------------------------+
|               SVG Ocean Dashboard & Operator Telemetry                  |
+-------------------------------------------------------------------------+
```

## Telemetry & Verification States

- **`VERIFIED`**: Confirmed by authoritative upstream response headers (e.g., `x-ratelimit-remaining-tokens`) or synchronous vendor billing API responses.
- **`ESTIMATED`**: Calculated locally via tokenizers (tiktoken) and local usage audit counters.
- **`STALE`**: Telemetry has not updated within the expected window interval.
- **`UNKNOWN`**: Provider endpoint unreachable or unmetered.

## Burn Ratio Pacing ($\\beta$)

$$\\beta = \\frac{\\text{Actual Burn Rate}}{\\text{Target Pace}}$$

| Burn Ratio ($\\beta$) | Pacing Status | Fleet Governor Action |
|---|---|---|
| **$< 0.70$** | **Underusing** | Surplus capacity detected. Enable background batch harvesting. |
| **$0.70 - 1.10$** | **On Pace** | Nominal burn. Standard autonomous execution permitted. |
| **$> 1.10 - 1.50$** | **Elevated** | Consumption above target. Defer low-priority cron jobs; warn operators. |
| **$> 1.50 - 2.00$** | **Early Exhaustion** | High exhaustion risk. Enforce downgrade to economy models; throttle workers. |
| **$> 2.00$** | **Critical** | Circuit breaker tripped. Halt all autonomous jobs immediately. |

### 20–25% Reserve Headroom
An immutable reserve floor of 20% to 25% of total window allowance is reserved strictly for high-priority interactive human queries and emergency recovery commands.

## Files & Artifacts

- [`SHERPA.md`](SHERPA.md) — Formal SherpaMD domain kit specification.
- `TokenPiggyBank.sherpa.md` — Portable Sherpa file available from [`../../handoffs/TokenPiggyBank.sherpa.md`](../../handoffs/TokenPiggyBank.sherpa.md).
