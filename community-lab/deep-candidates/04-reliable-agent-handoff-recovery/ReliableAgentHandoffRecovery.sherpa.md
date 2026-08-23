---
status: ai-sourced-untested
source_type: ai-synthesized
testing: not-tested
human_reviewed: false
model: qwen3.8-max
provider: qwen-cloud
risk_level: medium
batch: deep-candidates-batch1
---

# Reliable Agent Handoff Recovery — Durable Tasks That Survive Restarts

## Problem
Multi-agent systems lose work at the worst moments: a worker restarts mid-task,
a wake webhook drops, a claim sits unclaimed forever, or two agents run the
same job. The handoff itself arrives but the follow-through is unreliable.
This kit defines a durable handoff pattern: ledger-backed messages, narrow
claims with TTL, checkpoint artifacts on disk, a watchdog that expires stale
claims, and close-out receipts with proof.

## Who experiences it
- Anyone running cron-dispatched agents or webhook-woken workers.
- Fleet owners whose agents double-execute tasks after restarts.
- Teams where "the agent said DONE" but no verifiable artifact exists.

## Claims (sourced) vs inference
CLAIM: SherpaMD kits in this repo model inter-agent coordination with claims,
status transitions, and durable artifacts (see ../../domains/ai-to-ai-bus/
AItoAIBus.sherpa.md and ../../domains/core/CoreFleet.sherpa.md).
CLAIM: OpenTelemetry GenAI conventions include span/error attributes suitable
for recording handoff outcomes
(source: https://opentelemetry.io/docs/specs/semconv/gen-ai/, HTTP 200).
INFERENCE: TTL-bounded claims plus on-disk checkpoints reduce both duplicate
execution and silent task loss. Quantifying that reduction is the purpose of
the validation plan.

## Workflow
1. **Ledger**: every handoff is appended to a durable, append-only ledger
   with a unique id, from/to, channel, and timestamp. Fill in:
   `LEDGER=<path-or-service>` `CHANNELS=<handoffs,general,...>`.
2. **Narrow claim**: before touching shared state the worker posts
   `CLAIM task=<id> scope=<exact files/service/port> mode=<edit|test|deploy>
   ttl=<minutes>`. Scope must be the smallest real working set.
3. **Checkpoint loop**: after each meaningful substep write
   `<HOME>/.artifacts/<task>/checkpoint.md` with done/remaining lists, so a restart
   resumes instead of redoing. Never hold the whole plan only in context.
4. **Heartbeat**: for long steps, post STATUS with state=running at intervals
   below the claim TTL/2, so the watchdog can distinguish alive from dead.
5. **Watchdog**: a scheduled job scans claims older than TTL without STATUS;
   it either re-queues with retry+1 or posts BLOCKED with next action. Cap
   retries (fill in: `MAX_RETRIES=<2>`).
6. **Close-out**: DONE/BLOCKED/ABANDON releases the claim and must carry proof:
   commands run, artifact paths, test output, or service status — never a
   transcript dump. DONE without proof is treated as not done.
7. **Restart recovery**: on startup, each worker reads recent unclosed
   CLAIM/STATUS under its alias and continues or closes them before accepting
   new work.

## Copy/paste claim/status grammar (fill-in)
```text
CLAIM task=<short-id> owner=<alias> scope=<files|service|port|device>
  mode=<edit|test|deploy|review> ttl=<minutes> details=<why>
STATUS task=<short-id> owner=<alias> state=running checkpoint=<path>
DONE task=<short-id> owner=<alias> result=<1 line> proof=<paths|commands>
BLOCKED task=<short-id> owner=<alias> blocker=<1 line> next=<action>
```

## Status
**AI-SOURCED / UNTESTED.** Pattern derived from existing verified fleet kits
and common failure observation; reliability numbers do not exist yet.
