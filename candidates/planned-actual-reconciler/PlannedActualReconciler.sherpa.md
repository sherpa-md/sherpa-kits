---
schema_version: "0.1.0"
id: "planned-actual-reconciler"
title: "Planned-vs-Actual Reconciler — Explainable Variance and Change Ledger"
domain: "operational-intelligence"
version: "0.1.0"
status: "draft"
verification_state: "unverified"
last_verified: "2026-08-23T00:00:00Z"
confidentiality: "public"
provenance:
  origin_task: "deep-10-ai-system-candidates"
  author_alias: "ai-research-candidate"
  verifier_alias: "UNKNOWN"
sources:
  - id: "w3c-prov-o"
    title: "W3C PROV-O"
    uri: "https://www.w3.org/TR/prov-o/"
    type: "web-standard"
  - id: "opentelemetry-traces"
    title: "OpenTelemetry Traces"
    uri: "https://opentelemetry.io/docs/concepts/signals/traces/"
    type: "open-standard-documentation"
  - id: "nist-ai-rmf"
    title: "NIST AI Risk Management Framework 1.0"
    uri: "https://doi.org/10.6028/NIST.AI.100-1"
    type: "government-framework"
tags: ["plan", "actual", "variance", "timeline", "provenance", "operations"]
---

# Planned-vs-Actual Reconciler

## Capability

Install an evidence-preserving reconciliation engine for projects, productions, deployments, logistics, construction, or other time-bound operations. It normalizes the baseline plan, records authorized revisions, aligns actual events, calculates variance, and produces testable causal hypotheses without confusing them with facts.

## Canonical records

### Plan item

```json
{
  "plan_item_id": "stable-id",
  "baseline_version": "v1",
  "owner": "principal-or-role",
  "planned_start": "ISO-8601",
  "planned_finish": "ISO-8601",
  "planned_quantity": 0,
  "dependencies": [],
  "source_ref": "plan-source#location"
}
```

### Actual event

```json
{
  "event_id": "stable-id",
  "event_type": "started|completed|blocked|changed|measured",
  "event_time": "ISO-8601",
  "observed_at": "ISO-8601",
  "subject_ref": "plan-item-or-asset",
  "value": {},
  "source_ref": "system-record#location",
  "state": "VERIFIED"
}
```

### Variance claim

Every variance includes baseline version, formula, units, evidence refs, freshness, and claim state. Causal language is prohibited unless an intervention, controlled comparison, or approved causal method supports it; otherwise use `associated_factor` or `hypothesis`.

## Architecture

1. **Source adapters:** read plans, change orders, schedules, telemetry, tickets, and outcome systems.
2. **Identity resolver:** maps source-specific IDs to stable work, asset, owner, and location IDs.
3. **Temporal normalizer:** preserves source timezone, event time, observation time, and ingestion time.
4. **Baseline registry:** makes the original baseline immutable and records every approved revision as a new entity.
5. **Event ledger:** append-only actuals with corrections represented as new events.
6. **Reconciliation engine:** deterministic formulas for schedule, quantity, cost, quality, and dependency variance.
7. **Hypothesis engine:** AI groups patterns and proposes explanations linked to evidence.
8. **Review surface:** operators accept, reject, or refine mappings and hypotheses.

## Operating workflow

1. Freeze and hash the baseline plan.
2. Import revisions separately; never overwrite the baseline.
3. Normalize units, calendars, identifiers, and timestamps while retaining raw values.
4. Match actual events to plan items using deterministic keys first, then AI-assisted candidates.
5. Require review for ambiguous or many-to-many matches.
6. Calculate variances in code and store the formula inputs.
7. Build an event timeline with causal links only where evidence supports them.
8. Ask the model to generate competing hypotheses, disconfirming evidence, and data gaps.
9. Produce a variance brief: facts, estimates, stale data, unknowns, hypotheses, and recommended next measurements.
10. Feed reviewer corrections into mapping rules, not directly into historical evidence.

## Important calculations

- Finish variance: `actual_finish - baseline_finish`.
- Quantity variance: `actual_quantity - planned_quantity`, with unit conversion recorded.
- Forecast error: `actual - forecast`, reported with absolute and percentage error where denominator is valid.
- Change contribution: compare baseline, approved revision, and actual; do not attribute the entire actual variance to the latest revision.

## Failure behavior

- No stable join key: produce candidate matches and `UNKNOWN`, not an automatic join.
- Conflicting timestamps: preserve all, choose none silently.
- Missing baseline: stop variance calculation; an actual without a baseline is not a variance.
- Late-arriving event: recompute affected windows and mark prior summaries stale.
- AI causal overreach: downgrade to hypothesis and request disconfirming evidence.

## Promotion gate

Pass the validation plan on a frozen, labeled scenario and one live-but-sanitized pilot. All published numbers must be reproducible without the LLM.
