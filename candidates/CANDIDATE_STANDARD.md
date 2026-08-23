# Deep Candidate Standard

Each candidate must answer five questions before promotion.

## 1. What capability is installed?

Name the repeatable outcome, the operator, the intended users, and the explicit non-goals. A general lesson or a collection of prompts is not a system.

## 2. Where are the trust boundaries?

Identify data classifications, approved execution environments, identity and permission sources, external-content boundaries, retention, and high-impact actions. The model is a probabilistic component inside the boundary; it is not the boundary.

## 3. What are the contracts?

Define machine-checkable input, intermediate, and output records. Every consequential assertion needs a source reference, confidence state, and transformation record. Use `VERIFIED`, `ESTIMATED`, `STALE`, or `UNKNOWN` for claim state.

## 4. How does it fail safely?

Specify abstention rules, human approvals, rollback, idempotency, redaction, permission failures, prompt-injection handling, and evidence preservation. `UNKNOWN` is a valid output. Invented certainty is not.

## 5. What proves it works?

Validation must include a happy path, permission-denied path, malicious or malformed input, stale evidence, model disagreement, reproducibility, and a measurable outcome. Promotion requires sanitized evidence and a named human reviewer.

## Required file set

- `<BriefDescription>.sherpa.md`: operating architecture and build directive.
- `README.md`: human-readable purpose and maturity.
- `VALIDATION.md`: adversarial acceptance plan and evidence ledger.
- `SOURCES.md`: primary or authoritative sources plus explicit design inferences.

## Publication rule

Candidate material must contain no proprietary examples, credentials, personal paths, internal hostnames, or private infrastructure identifiers. Private-company implementations must use organization-approved tools and data stores, with tenant identity and source permissions enforced at query time.
