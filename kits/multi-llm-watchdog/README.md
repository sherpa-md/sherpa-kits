# Multi-LLM Watchdog Kit

Comprehensive observability, quota telemetry, and health monitoring kit for multi-provider LLM fleets.

## Core Capabilities

- **Provider & Model Health Tracking**: Continuous polling of latency, availability, rate-limiting headers, and error distributions.
- **Strict Confidence Labels**: Distinct classifications (`VERIFIED`, `ESTIMATED`, `STALE`, `UNKNOWN`) ensuring missing quotas are never faked as zero.
- **Deduplicated Alerting**: Hysteresis-driven alert suppression preventing notification storms during transient outages or rate limits.
- **Zero-Dependency Read-Only Dashboard**: Secure static telemetry interface for real-time fleet health inspection.

## Architecture

```text
Providers --> Isolated Polling Collectors --> Confidence Evaluator --> Alert Deduplicator --> Read-Only Dashboard
```

## Files & Artifacts

- [`MultiLLMWatchdog.sherpa.md`](MultiLLMWatchdog.sherpa.md) — Formal SherpaMD domain kit specification.
