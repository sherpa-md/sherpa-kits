---
schema_version: "0.1.0"
id: "approved-private-data-analyst"
title: "Approved Private Data Analyst — Permission-Aware Company Intelligence"
domain: "enterprise-ai-governance"
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
  - id: "microsoft-edp"
    title: "Enterprise data protection in Microsoft Copilot"
    uri: "https://learn.microsoft.com/en-us/microsoft-365/copilot/enterprise-data-protection"
    type: "vendor-primary"
  - id: "microsoft-semantic-index"
    title: "Semantic indexing for Microsoft Copilot"
    uri: "https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot"
    type: "vendor-primary"
  - id: "azure-search-security"
    title: "Security filters for trimming results in Azure AI Search"
    uri: "https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search"
    type: "vendor-primary"
  - id: "nist-ai-600-1"
    title: "NIST AI 600-1 Generative AI Profile"
    uri: "https://doi.org/10.6028/NIST.AI.600-1"
    type: "government-framework"
tags: ["private-data", "rag", "copilot", "permissions", "audit", "citations"]
---

# Approved Private Data Analyst

## Capability

Install a governed analysis layer that can answer cross-source business questions, calculate metrics, surface contradictions, and draft decision briefs while preserving the requesting user's existing permissions.

Examples of legitimate outcomes include finding the drivers of late projects, comparing forecast assumptions with actual results, identifying repeated customer complaints, or producing a cited operating review. This is not permission to upload company data to any convenient model.

## Non-negotiable boundaries

1. The organization names the approved LLM, tenant, connectors, regions, retention policy, and permitted data classes before ingestion.
2. Source authorization is evaluated for every retrieval. Pre-filtering a shared index once is insufficient.
3. The LLM receives only the minimum retrieved fields needed for the current question.
4. Retrieved documents are untrusted data, never executable instructions.
5. Answers cite source records and distinguish `VERIFIED`, `ESTIMATED`, `STALE`, and `UNKNOWN` claims.
6. Cross-boundary export, bulk download, write-back, or external sharing requires a deterministic policy check and, when consequential, human approval.
7. Prompts, retrieved snippets, tool calls, model identity, policy decisions, and output hashes produce a sanitized audit receipt.

## Architecture

| Layer | Responsibility | Required control |
|---|---|---|
| Identity | Resolve the requesting employee and groups | Tenant identity; no model-invented principal |
| Policy broker | Decide permitted model, source, fields, and actions | Deny by default; versioned rules |
| Connectors | Read SharePoint, email, databases, or approved systems | Source ACLs retained and synchronized |
| Retrieval | Select relevant, authorized evidence | Query-time permission trimming |
| Structured tools | Compute aggregates and joins | Parameterized, read-only queries first |
| Approved LLM | Synthesize and explain | No privilege expansion; bounded context |
| Claim ledger | Bind statements to evidence and state | Immutable source IDs and timestamps |
| Review/export | Approve consequential outputs | Human identity and signed receipt |

## Required contracts

```json
{
  "request_id": "opaque-id",
  "requester_principal": "tenant-resolved-id",
  "purpose": "operational-analysis",
  "data_classes": ["internal"],
  "approved_model_profile": "policy-resolved-name",
  "allowed_actions": ["retrieve", "aggregate", "draft"],
  "forbidden_actions": ["external-export", "write-back"]
}
```

Every result claim must use this minimum shape:

```json
{
  "claim": "A specific, testable statement",
  "state": "VERIFIED",
  "evidence_refs": ["source-id#location"],
  "as_of": "ISO-8601",
  "method": "retrieval|calculation|inference",
  "confidence": 0.0
}
```

`confidence` is not proof. A `VERIFIED` claim requires inspectable evidence or reproducible calculation. An inference is labeled `ESTIMATED` even when confidence is high.

## Operating workflow

1. **Authorize:** resolve user, purpose, data classes, approved model profile, and permitted actions.
2. **Plan:** decompose the question into retrievals and deterministic calculations; show the plan for high-impact requests.
3. **Retrieve:** run identity-bound search against each source; record ACL decision and source version.
4. **Quarantine:** strip active content, mark retrieved text as untrusted, and detect likely prompt injection.
5. **Calculate:** use typed query or analysis tools for numbers; do not ask the LLM to perform hidden arithmetic over prose.
6. **Synthesize:** produce claims with citations and disagreement notes.
7. **Challenge:** run a second pass that seeks missing evidence, contradictory sources, stale dates, and unauthorized leakage.
8. **Approve:** require a human for external distribution, personnel decisions, contractual conclusions, or source-system mutation.
9. **Receipt:** store policy version, source refs, transformations, model profile, approvals, and output hash without duplicating sensitive payloads.

## Build slices

- Slice A: one read-only SharePoint folder, tenant identity, citations, and deny tests.
- Slice B: add one structured dataset with typed metrics and row-level controls.
- Slice C: add contradiction detection, freshness policy, and claim ledger.
- Slice D: add reviewed exports and audit dashboards.

Do not start with every company data source. Prove permission preservation on one narrow domain first.

## Safe failure behavior

- Missing policy or model approval: `BLOCKED_POLICY`.
- Unresolvable user identity: `BLOCKED_IDENTITY`.
- Source permission mismatch: exclude the record and emit a non-sensitive denial receipt.
- Stale or conflicting evidence: answer with the disagreement and `STALE` or `UNKNOWN` state.
- Suspected injection: quarantine the source; no tool calls derived from it.
- Model outage: preserve the analysis plan and evidence set; do not silently route to an unapproved provider.

## Promotion gate

Remain `draft / unverified` until every case in `VALIDATION.md` passes with synthetic or formally approved test data, and a security/privacy owner approves the implementation boundary.
