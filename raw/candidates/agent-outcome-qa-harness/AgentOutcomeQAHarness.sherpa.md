---
schema_version: "0.1.0"
id: "agent-outcome-qa-harness"
title: "Agent Outcome QA Harness — Evidence, Safety, Cost, and Repeatability"
domain: "agent-evaluation"
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
  - id: "nist-airc"
    title: "NIST AI Resource Center"
    uri: "https://airc.nist.gov/"
    type: "government-resource"
  - id: "nist-ai-600-1"
    title: "NIST AI 600-1 Generative AI Profile"
    uri: "https://doi.org/10.6028/NIST.AI.600-1"
    type: "government-framework"
  - id: "opentelemetry-traces"
    title: "OpenTelemetry Traces"
    uri: "https://opentelemetry.io/docs/concepts/signals/traces/"
    type: "open-standard-documentation"
  - id: "owasp-prompt-injection"
    title: "OWASP LLM01:2025 Prompt Injection"
    uri: "https://genai.owasp.org/llmrisk/llm01-prompt-injection/"
    type: "security-guidance"
tags: ["agents", "evaluation", "qa", "outcomes", "telemetry", "safety"]
---

# Agent Outcome QA Harness

## Capability

Install a test and production-observation harness that evaluates agents against externally verifiable outcomes, policy compliance, evidence quality, recovery behavior, latency, and cost. It produces comparable scorecards across agent/model/tool versions.

An agent saying “done” is an assertion under test, not evidence.

## Evaluation case contract

```json
{
  "case_id": "stable-id",
  "task": "bounded user-visible outcome",
  "fixture_version": "content-hash-or-version",
  "allowed_tools": [],
  "forbidden_actions": [],
  "approval_points": [],
  "success_oracles": [],
  "safety_oracles": [],
  "budget": {"tokens": 0, "cost": 0, "seconds": 0},
  "cleanup": "reversible procedure"
}
```

## Oracle hierarchy

Use the strongest available proof:

1. Deterministic state check or test.
2. Independent system-of-record query.
3. Human review against a rubric.
4. Separate model judge for narrow subjective criteria.
5. Agent self-report only as diagnostic metadata.

No critical outcome relies solely on an LLM judge, especially when the evaluated agent and judge share failure modes.

## Trace schema

Represent one run as a trace with spans for planning, retrieval, model calls, tool proposals, authorization, execution, verification, approval, and cleanup. Record model/service profile, prompt/template version, tool version, policy decision, input/output hashes, tokens, latency, retries, and outcome. Redact sensitive payloads while retaining correlation.

## Test suites

- **Capability:** representative normal tasks with deterministic outcome checks.
- **Boundary:** forbidden tools, destinations, data classes, and privilege requests.
- **Adversarial:** direct/indirect prompt injection, poisoned retrieval, malformed tool output, and misleading screenshots/documents.
- **Recovery:** timeouts, partial writes, tool outage, rate limits, stale state, and interrupted approvals.
- **Regression:** frozen cases for every prior material failure.
- **Variance:** repeated runs across seeds/times to measure nondeterministic failure rate.
- **Cost/value:** resources consumed per verified useful outcome, not per completion.
- **Human factors:** approval clarity, correction effort, and automation-bias risk.

## Scoring

Keep dimensions separate before any composite score:

| Dimension | Example measure |
|---|---|
| Outcome | Oracle checks passed / required checks |
| Safety | Prohibited actions and data-boundary violations |
| Evidence | Claims supported and receipts complete |
| Recovery | Correct state after injected failure |
| Efficiency | Cost, tokens, latency, retries per verified outcome |
| Repeatability | Pass distribution over repeated runs |
| Human burden | Review time and correction count |

A safety violation is a release blocker, not a small score deduction that accuracy can average away.

## Release workflow

1. Freeze case, fixture, policy, tools, and oracle versions.
2. Run baseline and candidate multiple times under comparable conditions.
3. Inspect traces for contamination, hidden retries, and judge leakage.
4. Compare per-dimension results with confidence intervals where meaningful.
5. Require zero blocker regressions and declared thresholds for outcome/cost.
6. Conduct targeted human review of disagreements and new behaviors.
7. Approve, reject, or canary the candidate with rollback criteria.
8. Monitor production outcome proxies and sample real receipts.
9. Turn every material escaped failure into a regression case.

## Anti-gaming controls

- Keep evaluation-only identifiers and expected answers out of agent-visible context.
- Use hidden and rotating cases.
- Detect shortcut artifacts and answer memorization.
- Require state inspection after the agent finishes.
- Validate cleanup and absence of unauthorized side effects.
- Separate case author, system builder, and release approver where risk warrants.

## Promotion gate

The harness itself must pass `VALIDATION.md`, including planted false-success reports and unsafe high-scoring runs. It remains unverified until it correctly blocks them.
