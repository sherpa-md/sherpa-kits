---
schema_version: "0.1.0"
id: "human-verified-document-automation"
title: "Human-Verified Document Automation — Typed Extraction and Controlled Filing"
domain: "document-operations"
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
  - id: "google-document-ai"
    title: "Google Cloud Document AI documentation"
    uri: "https://docs.cloud.google.com/document-ai/docs"
    type: "vendor-primary"
  - id: "w3c-prov-o"
    title: "W3C PROV-O"
    uri: "https://www.w3.org/TR/prov-o/"
    type: "web-standard"
  - id: "owasp-prompt-injection"
    title: "OWASP LLM01:2025 Prompt Injection"
    uri: "https://genai.owasp.org/llmrisk/llm01-prompt-injection/"
    type: "security-guidance"
tags: ["documents", "extraction", "workflow", "human-review", "filing"]
---

# Human-Verified Document Automation

## Capability

Install a document workflow that turns approved inbound documents into structured records and controlled downstream drafts. It supports invoices, receipts, forms, reports, certificates, contracts, applications, and correspondence without relying on an unreviewed free-form summary.

## Document state machine

`RECEIVED -> QUARANTINED -> CLASSIFIED -> EXTRACTED -> VALIDATED -> NEEDS_REVIEW -> APPROVED -> FILED`

Exceptional states are `REJECTED`, `DUPLICATE`, `BLOCKED_POLICY`, and `FAILED_SAFE`. Every transition records actor, time, input hash, policy/rule version, and reason.

## Typed field contract

```json
{
  "field_id": "invoice.total",
  "value": 0,
  "type": "decimal",
  "unit_or_currency": "declared-code",
  "source_ref": "document-hash#page-region",
  "extractor": "tool-and-version",
  "confidence": 0.0,
  "validation_results": [],
  "review_status": "pending|accepted|corrected|rejected"
}
```

Confidence thresholds are field-specific. A high-confidence bank account, payment total, legal date, safety value, identity, or destination may still require review because consequence—not model confidence—controls the gate.

## Pipeline

1. **Receive:** accept only approved channels and formats; hash and malware-scan the original.
2. **Quarantine:** treat all text, macros, links, QR codes, and attachments as untrusted content.
3. **Classify:** choose a versioned document type/schema or route to unknown-type review.
4. **Extract:** use OCR/layout/parser tools to return fields, tables, and exact source regions.
5. **Normalize:** standardize dates, currencies, identifiers, and units while preserving raw text.
6. **Validate:** apply deterministic rules—required fields, checksums, cross-field arithmetic, duplicate detection, allowed counterparties, and source-system lookups.
7. **Reconcile:** compare extracted values to authoritative records; surface differences rather than silently choosing.
8. **Review:** present only flagged/consequential fields with source regions and validation explanations, while allowing full-document inspection.
9. **Draft:** populate a downstream record or document using approved fields. Keep it non-final until approval policy passes.
10. **File/write:** use idempotency keys and least-privileged connectors; never let document text select the destination or action.
11. **Receipt:** store hashes, field lineage, corrections, rules, approvals, destination ID, and rollback reference.

## Human-review policy

Review is mandatory when a required field is missing, models disagree, a deterministic rule fails, a consequential field is present, an unfamiliar counterparty/destination appears, a document is altered, or policy explicitly requires separation of duties.

The review UI must prevent automation bias: show the source region first, identify model output as a proposal, and capture corrections at field level.

## Safe failures

- Unknown document type: do not force it into the nearest schema.
- Malicious embedded instruction: quarantine; never convert content into a tool call.
- Duplicate: hold for review rather than create a second record.
- Destination mismatch: block filing.
- Partial downstream failure: retry idempotently or roll back; never create ambiguous double writes.
- Reviewer unavailable: queue remains pending; no silent approval.

## Promotion gate

Pass the validation corpus, demonstrate recoverable idempotent filing in a sandbox, and obtain process-owner approval for field and consequence thresholds.
