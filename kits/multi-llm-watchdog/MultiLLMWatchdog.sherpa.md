---
schema_version: "0.1.0"
id: "multi-llm-watchdog"
title: "Multi-LLM Watchdog — Provider Health, Quota Telemetry & Deduplicated Alerts"
domain: "llm-observability"
version: "0.1.0"
status: "active"
verification_state: "verified"
last_verified: "2026-08-21T22:00:00Z"
confidentiality: "public"
provenance:
  origin_task: "multi-llm-watchdog-v0.1.0"
  author_alias: "hermb"
  verifier_alias: "hermb"
sources:
  - id: "src-llm-telemetry"
    title: "Multi-Provider Health & Quota Telemetry Specifications"
    trust_label: "specification"
tags:
  - "provider-health"
  - "model-watchdog"
  - "quota-telemetry"
  - "confidence-labels"
  - "alert-deduplication"
  - "read-only-dashboard"
related_links:
  - rel: "spec"
    uri: "https://github.com/sherpa-md/sherpa-spec"
  - rel: "token-piggy-bank"
    uri: "../token-piggy-bank/TokenPiggyBank.sherpa.md"
---

# Multi-LLM Watchdog — Provider Health, Quota Telemetry & Deduplicated Alerts

## 1. Purpose & Scope

The **Multi-LLM Watchdog** provides continuous health monitoring, quota cadence observation, failure isolation, and deduplicated alerting across heterogeneous LLM provider fleets.

By standardizing telemetry across diverse upstream APIs, applying strict verification confidence labels, suppressing redundant alert storms, and serving a zero-dependency read-only dashboard, this kit gives operators transparent visibility into model availability and exhaustion risks without risking system lockup or credential exposure.

---

## 2. Telemetry Ingestion & Confidence Labels

```text
+-----------------------------------------------------------------------+
|                    Heterogeneous Model Providers                      |
|       (Cloud Vendor APIs / Self-Hosted Gateways / Local Runtimes)     |
+-----------------------------------+-----------------------------------+
                                    |
                    [1. Independent Periodic Polling]
                                    v
+-----------------------------------------------------------------------+
|                      Watchdog Telemetry Collector                     |
|  - Isolated Collector Tasks (One Failure Does Not Break Others)       |
|  - Strict Timeout Bounds (5s-15s Maximum Socket Wait)                 |
|  - Confidence Engine (VERIFIED / ESTIMATED / STALE / UNKNOWN)         |
+-----------------------------------+-----------------------------------+
                                    |
                    [2. Quota & Health Aggregation]
                                    v
+-----------------------------------------------------------------------+
|                 Alert Deduplicator & Dashboard Server                 |
|  - State-Transition Hysteresis (Suppresses Repeating Noise)           |
|  - Atomic State Snapshot (`watchdog_state.json`)                      |
|  - Read-Only Static SVG/HTML Web Telemetry Interface                  |
+-----------------------------------------------------------------------+
```

### Verification Confidence Hierarchy

To prevent dangerous false assumptions during routing or operational planning, telemetry fields are tagged with explicit confidence labels:

| Confidence State | Definition & Evidence Threshold | Operational Handling |
|---|---|---|
| **`VERIFIED`** | Confirmed directly by authoritative upstream vendor response headers (e.g., `x-ratelimit-remaining`) or authenticated quota endpoints. | Authoritative basis for burn pacing and autonomous rate calculation. |
| **`ESTIMATED`** | Calculated locally via request tokenizers, audit logs, or heuristic counters when vendor quotas are unmetered. | Usable for advisory warnings; clearly labeled as estimated in UI. |
| **`STALE`** | Telemetry source was previously reachable but has not refreshed within the expected cadence window ($> 900\text{s}$). | Triggers provider health warning; deprioritizes tier ranking. |
| **`UNKNOWN`** | Telemetry is unavailable or unmetered. **Never defaulted or faked as 0%.** | Safe neutral fallback; provider remains eligible for unmetered routing. |

---

## 3. Alert Deduplication & State Hysteresis

Alert spam during network blips or rapid retry loops causes notification fatigue and obscures critical failures.

```python
import time
from typing import Dict, Any, Optional

class AlertDeduplicator:
    def __init__(self, cooldown_seconds: int = 3600):
        self.cooldown_seconds = cooldown_seconds
        self.last_alerts: Dict[str, float] = {}
        self.current_states: Dict[str, str] = {}

    def should_alert(self, provider_id: str, new_state: str) -> bool:
        """Alert only on state change or after cooldown expires."""
        now = time.time()
        old_state = self.current_states.get(provider_id)

        # Transition to new degraded/exhausted state triggers immediate alert
        if old_state != new_state:
            self.current_states[provider_id] = new_state
            if new_state in {"DEGRADED", "EXHAUSTED", "DOWN"}:
                self.last_alerts[provider_id] = now
                return True
            return False

        # If remaining in bad state, suppress until cooldown expires
        if new_state in {"DEGRADED", "EXHAUSTED", "DOWN"}:
            last_time = self.last_alerts.get(provider_id, 0)
            if now - last_time > self.cooldown_seconds:
                self.last_alerts[provider_id] = now
                return True

        return False
```

---

## 4. Read-Only Telemetry Dashboard

The watchdog exports a lightweight, read-only JSON state file (`telemetry.json`) consumed by a zero-dependency static web interface:
- **Zero Write Surface**: Dashboard operates purely over HTTP `GET` with no mutation endpoints.
- **Redaction by Design**: No API keys, credentials, or user-identifying prompt data are written to the telemetry output.
- **Independent Refresh**: Client-side UI polls state periodically using background fetch or SSE.

---

## 5. Verification Evidence & Acceptance Criteria

- **Collector Fault Isolation**: Simulating network timeouts or HTTP 500 errors on one provider does not block or delay telemetry collection from remaining providers.
- **Honest Unknowns**: Providers without native quota metrics emit `UNKNOWN` without defaulting to zero percent available.
- **Alert Suppression**: Consecutive HTTP 429 errors emit exactly one alert upon transition, suppressing repeated identical alerts during the configured cooldown window.
