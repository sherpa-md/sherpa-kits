---
schema_version: "0.1.0"
id: "approved-model-routing-gateway"
title: "Approved-Model Routing Gateway — Policy-Bound AI Execution"
domain: "ai-control-plane"
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
  - id: "nist-ai-600-1"
    title: "NIST AI 600-1 Generative AI Profile"
    uri: "https://doi.org/10.6028/NIST.AI.600-1"
    type: "government-framework"
  - id: "owasp-prompt-injection"
    title: "OWASP LLM01:2025 Prompt Injection"
    uri: "https://genai.owasp.org/llmrisk/llm01-prompt-injection/"
    type: "security-guidance"
  - id: "microsoft-edp"
    title: "Enterprise data protection in Microsoft Copilot"
    uri: "https://learn.microsoft.com/en-us/microsoft-365/copilot/enterprise-data-protection"
    type: "vendor-primary"
tags: ["routing", "approved-models", "policy", "data-boundary", "least-privilege"]
---

# Approved-Model Routing Gateway

## Capability

Install a deterministic gateway between users/agents and AI providers. The gateway classifies the requested task and declared data, resolves an approved route, minimizes the payload, issues scoped capabilities, validates outputs, and records a receipt.

The gateway is vendor-neutral. An organization's policy may allow only a tenant-bound Copilot experience for proprietary data while allowing other providers for public material. The policy—not user convenience or model preference—controls the route.

## Policy inputs

```json
{
  "request_id": "opaque-id",
  "principal": "verified-principal",
  "purpose": "declared-purpose",
  "data_classes": ["public|internal|restricted"],
  "modalities": ["text|image|audio|tabular"],
  "required_capabilities": ["reasoning", "vision", "tool-use"],
  "requested_actions": ["read", "draft"],
  "destination": "approved-boundary"
}
```

## Model registry

Each route record includes provider, exact model/profile, tenant/project, allowed data classes, regions, retention/training terms, modalities, tool permissions, maximum payload, cost/quota class, evaluation status, and policy effective dates. Marketing names without a pinned service profile are insufficient.

## Decision sequence

1. Authenticate principal and workload identity.
2. Validate purpose and requested actions against policy.
3. Classify data with deterministic labels and source metadata; model classification may suggest but not silently downgrade.
4. Compute the intersection of data class, purpose, modality, residency, retention, and capability requirements.
5. Deny when the intersection is empty. Never fall back across a trust boundary.
6. Select the least-privileged, lowest-cost approved route that meets the evaluated quality floor.
7. Minimize/redact payload fields not required for the task.
8. Issue short-lived scoped tool capabilities outside the model prompt.
9. Mark retrieved and user-supplied content as untrusted.
10. Validate the structured output and policy obligations.
11. Require approval for consequential actions or boundary-crossing exports.
12. Emit a receipt with policy version, route, data classes, redaction summary, tools, approvals, usage, and outcome.

## Separation of authority

- The model may propose a tool call; deterministic code authorizes and executes it.
- A task router may rank already-approved routes; it cannot add a route to the registry.
- Source content may never alter system policy.
- Provider outage cannot trigger an unapproved fallback.
- Administrator approval and request-time human approval are distinct controls.

## Output states

- `ROUTED`: approved route selected.
- `NEEDS_REDACTION`: payload can proceed after deterministic minimization.
- `NEEDS_HUMAN_APPROVAL`: allowed only with named approval.
- `BLOCKED_POLICY`: no route satisfies the policy.
- `BLOCKED_IDENTITY`: principal or workload identity unresolved.
- `BLOCKED_CAPABILITY`: approved routes lack required evaluated capability.

## Integration with quota governance

Cost and quota may choose among equally approved/evaluated routes, but never override data policy. Reserve protection and burn pacing can downgrade quality tiers only inside the permitted route set.

## Promotion gate

Pass the policy matrix and exfiltration/fallback tests in `VALIDATION.md`. An independent reviewer must verify that every allowed route corresponds to a current organizational approval.
