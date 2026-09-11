---
schema_version: "0.1.0"
id: "estimate-actuals-analyst"
title: "Estimate-vs-Actuals Analyst — Calibrated Forecast Learning"
domain: "forecast-intelligence"
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
  - id: "nist-ai-rmf"
    title: "NIST AI Risk Management Framework 1.0"
    uri: "https://doi.org/10.6028/NIST.AI.100-1"
    type: "government-framework"
  - id: "w3c-prov-o"
    title: "W3C PROV-O"
    uri: "https://www.w3.org/TR/prov-o/"
    type: "web-standard"
  - id: "microsoft-edp"
    title: "Enterprise data protection in Microsoft Copilot"
    uri: "https://learn.microsoft.com/en-us/microsoft-365/copilot/enterprise-data-protection"
    type: "vendor-primary"
tags: ["estimates", "actuals", "forecasting", "calibration", "private-data"]
---

# Estimate-vs-Actuals Analyst

## Capability

Install a governed learning loop that compares historical estimates with actual cost, time, quantity, labor, or outcome data; explains systematic error; recommends bounded adjustment factors; and measures whether later estimates improve.

For proprietary company analysis, run this only inside the employer-approved AI and data environment. If the approved environment is Microsoft Copilot, keep the source workbooks, emails, estimates, and results inside the authorized Microsoft 365 tenant and its permission model.

## Unit of analysis

```json
{
  "case_id": "stable-id",
  "estimate_as_of": "ISO-8601",
  "estimate_version": "immutable-version",
  "scope_signature": "normalized-scope-id",
  "estimated": {"value": 0, "unit": "declared-unit"},
  "actual": {"value": 0, "unit": "declared-unit", "cutoff": "ISO-8601"},
  "known_at_estimate_time": {},
  "later_changes": [],
  "source_refs": [],
  "quality_flags": []
}
```

Freeze the information available at estimate time. Later knowledge must not be used to judge what the estimator “should have known.”

## Cohort and leakage controls

- Define comparable cohorts before analyzing error: work type, scale, region, customer class, complexity, season, technology, and contractual scope.
- Prevent the same case, revision, or near-duplicate from appearing in both training and evaluation sets.
- Keep a time-based holdout so evaluation represents future work.
- Separate scope change from estimation error. An approved later change is not automatically a bad original estimate.
- Exclude incomplete actuals or label them censored; do not treat current spend as final cost.

## Calculations

- Error: `actual - estimate`.
- Absolute percentage error: `abs(actual - estimate) / abs(actual)` when actual is nonzero and the metric is meaningful.
- Bias: mean signed error by cohort.
- Calibration: proportion of actuals falling inside each stated forecast interval.
- Uplift factor: derived from a declared robust statistic and bounded by policy.

All published metrics are calculated in code from versioned rows. The LLM explains patterns and proposes candidate features; it does not invent totals.

## Workflow

1. Register approved source systems, permissions, and business owner.
2. Extract immutable estimate versions and actuals with source timestamps.
3. Normalize units, currency basis, calendars, and scope taxonomy while retaining raw values.
4. Flag missing, censored, duplicated, and incomparable cases.
5. Create cohorts and a time-based evaluation split.
6. Compute baseline errors and uncertainty intervals deterministically.
7. Ask the model for pattern hypotheses tied to cohort metrics and source evidence.
8. Test those hypotheses with code or reviewed samples; reject unsupported narratives.
9. Produce an adjustment card: applicable scope, factor/rule, evidence window, sample size, uncertainty, exceptions, owner, and review date.
10. Apply the card prospectively to new estimates while retaining the original estimator output.
11. Compare adjusted and unadjusted performance on future cases.
12. Retire or revise the card when calibration deteriorates or the operating regime changes.

## Output

The useful deliverable is not “your estimates are usually low.” It is a versioned, bounded rule such as: for a defined cohort and evidence window, add a declared contingency range when a specific observable condition exists, with sample size, uncertainty, exclusions, and a future validation date.

## Safe failures

- Small or biased cohort: return `INSUFFICIENT_EVIDENCE`.
- Mixed units or scope: block aggregation.
- Incomplete actual: label censored and exclude from final-error metrics.
- Sensitive commercial slice: suppress small groups according to policy.
- Drift: mark adjustment card `STALE` and stop automatic recommendation.

## Promotion gate

Demonstrate prospective improvement on held-out cases without material degradation for protected or operationally important subgroups, and obtain business-owner approval.
