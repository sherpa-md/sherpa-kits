---
schema_version: "0.1.0"
id: "institutional-memory-builder"
title: "Institutional Memory Builder — Permission-Aware Living Knowledge"
domain: "knowledge-governance"
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
  - id: "microsoft-semantic-index"
    title: "Semantic indexing for Microsoft Copilot"
    uri: "https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot"
    type: "vendor-primary"
  - id: "microsoft-edp"
    title: "Enterprise data protection in Microsoft Copilot"
    uri: "https://learn.microsoft.com/en-us/microsoft-365/copilot/enterprise-data-protection"
    type: "vendor-primary"
tags: ["knowledge", "memory", "freshness", "permissions", "provenance"]
---

# Institutional Memory Builder

## Capability

Install a living memory system that discovers authoritative artifacts, extracts atomic knowledge, links decisions to their evidence and owners, detects contradictions, expires stale claims, and answers questions within the requester's permissions.

It is not a chat transcript dump and not a single undifferentiated vector database.

## Knowledge object

```json
{
  "knowledge_id": "stable-id",
  "statement": "atomic and testable",
  "type": "policy|decision|fact|procedure|assumption|lesson",
  "state": "VERIFIED|ESTIMATED|STALE|UNKNOWN",
  "source_refs": [],
  "owner": "role-or-principal",
  "effective_from": "ISO-8601",
  "review_by": "ISO-8601",
  "supersedes": [],
  "permission_refs": [],
  "scope": []
}
```

## Architecture

| Component | Function |
|---|---|
| Source registry | Names systems of record, owners, authority rank, retention, and sync behavior |
| Permission-preserving index | Retrieves only content the user can access |
| Extractor | Proposes atomic knowledge objects and source spans |
| Resolver | Links aliases, projects, assets, people, and versions |
| Contradiction engine | Finds mutually inconsistent claims within overlapping scope/time |
| Freshness engine | Applies review dates and source-change invalidation |
| Answer composer | Produces cited answers plus uncertainty and disagreement |
| Steward queue | Routes ownership, correction, merge, and retirement tasks |

## Ingestion workflow

1. Register a source owner, authority class, data classification, ACL model, and synchronization window.
2. Ingest metadata and content without broadening source permissions.
3. Chunk by meaningful structure while preserving document, section, version, and ACL lineage.
4. Extract proposed knowledge objects with exact source spans.
5. Resolve entities without destructive merging; ambiguous identities remain candidates.
6. Compare new objects with active knowledge in the same scope.
7. Create `supports`, `contradicts`, `supersedes`, `derived-from`, and `applies-to` links.
8. Assign owner and review date. Knowledge without an owner is provisional.
9. Publish only after automatic contract checks and the configured stewardship rule.
10. On source change, re-evaluate dependents and mark affected answers stale.

## Retrieval and answering

Query-time identity and permission checks occur before evidence reaches the model. Rank evidence by authority, applicability, freshness, and direct support—not similarity alone. Answers must include:

- direct response;
- supporting sources and dates;
- active contradiction or supersession notes;
- claim state;
- owner and next review date when applicable;
- a bounded “not found” or `UNKNOWN` response when evidence is insufficient.

## Memory hygiene

- Decisions and policies must include effective scope and dates.
- Meeting summaries are leads until linked to authoritative outcomes.
- Repeated statements do not become more true through frequency.
- Deleted or access-revoked content must stop surfacing within a measured synchronization objective.
- The system retains tombstones and provenance where policy permits, without exposing removed content.
- User corrections become review proposals, not silent fact rewrites.

## Promotion gate

Pass permission, contradiction, freshness, deletion, provenance, and answer-grounding tests in `VALIDATION.md` on a controlled corpus.
