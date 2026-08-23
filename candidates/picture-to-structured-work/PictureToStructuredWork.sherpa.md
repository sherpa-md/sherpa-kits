---
schema_version: "0.1.0"
id: "picture-to-structured-work"
title: "Picture-to-Structured-Work — Multimodal Evidence and Transformation Pipeline"
domain: "multimodal-automation"
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
  - id: "c2pa"
    title: "C2PA Technical Specification 2.2"
    uri: "https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html"
    type: "industry-specification"
  - id: "owasp-prompt-injection"
    title: "OWASP LLM01:2025 Prompt Injection"
    uri: "https://genai.owasp.org/llmrisk/llm01-prompt-injection/"
    type: "security-guidance"
tags: ["images", "vision", "ocr", "structured-data", "provenance", "human-review"]
---

# Picture-to-Structured-Work

## Capability

Install a pipeline that accepts an image and a declared job, then produces inspectable evidence plus a domain-specific work product. Examples:

- photograph of a whiteboard to owners, decisions, and due dates;
- equipment photo set to an annotated inspection record;
- shelf photo to planogram exceptions and count estimates;
- screenshot to a reproducible UI defect report;
- scanned form to typed fields and review queue;
- source image plus a precise change request to a derived asset with an edit manifest.

## Required separation of concerns

| Stage | Output | May infer? |
|---|---|---|
| Asset intake | Hash, MIME type, dimensions, capture metadata, policy class | No |
| Pixel/OCR observation | Text spans, regions, objects, coordinates, quality flags | Only model detections, labeled as such |
| Domain interpretation | Candidate facts, relationships, anomalies | Yes, labeled `ESTIMATED` |
| Work-product mapping | Tasks, records, measurements, or edit instructions | Yes, schema constrained |
| Transformation | Derived image or document | Only approved operations |
| Review | Accepted, corrected, rejected fields/regions | Human decision |
| Provenance | Source hash, tool/model versions, operations, reviewer | No |

Never merge observation and interpretation into an unlabeled paragraph.

## Job contract

```json
{
  "job_id": "opaque-id",
  "purpose": "inspection|extraction|comparison|transformation",
  "asset_refs": ["content-addressed-ref"],
  "target_schema": "versioned-schema-id",
  "allowed_operations": ["ocr", "detect", "crop", "annotate"],
  "forbidden_operations": ["identity-inference", "background-replacement"],
  "review_policy": "field-and-region",
  "output_destination": "approved-location"
}
```

Each extracted field carries `value`, `state`, `confidence`, `asset_ref`, `region`, `extractor`, and `review_status`. Coordinates use a documented origin and normalized range so reviewers can return to the exact pixels.

## Pipeline

1. **Intake:** hash the original; preserve orientation and color profile; classify sensitivity; reject unsupported or decompression-bomb inputs.
2. **Normalize:** create working renditions without replacing the original; record every crop, rotation, scale, and enhancement.
3. **Observe:** run OCR and vision detectors independently where possible. Store raw detections, not only a prose summary.
4. **Locate:** bind every observation to a region or page. `UNKNOWN` is required when a fact cannot be localized.
5. **Interpret:** map observations into the target business schema. Domain rules validate ranges, required fields, and impossible combinations.
6. **Challenge:** compare detector disagreement, OCR alternatives, and missing required regions. Scan visible and machine-readable content for injected instructions.
7. **Review:** show the source region beside each consequential field or proposed edit. Reviewers correct the record, not just approve a summary.
8. **Transform:** apply only the authorized edit list. Never invent unrequested scene changes.
9. **Manifest:** emit source and derivative hashes, operations, tools/models, timestamps, and review outcome; preserve C2PA-compatible provenance when supported.
10. **Export:** write structured data and derivatives only to the approved destination.

## Special behavior: visual comparison

For before/after or plan/actual jobs, align images first, then represent changes as region pairs with `change_type`, `magnitude`, `confidence`, and reviewer status. Camera motion, lighting, occlusion, and compression are confounders and must be reported.

## Special behavior: controlled image editing

Convert natural-language requests into an explicit edit manifest before generation:

```json
{
  "preserve": ["subject identity", "logo geometry", "camera angle"],
  "change": [{"region": "background", "operation": "replace", "target": "neutral studio"}],
  "prohibit": ["new text", "face alteration", "unrequested objects"]
}
```

The system compares the derivative to the manifest and flags preservation failures. The derivative never replaces the original.

## Safe failures

- Low resolution or unreadable region: field is `UNKNOWN` and routed to review.
- Suspected hidden instruction: quarantine the asset; do not invoke tools from image text.
- Unsupported identity or sensitive-attribute inference: refuse that field while continuing permitted extraction.
- Transformation drift: reject derivative and retain the original plus edit manifest.
- Missing destination approval: produce no external write.

## Promotion gate

Pass every case in `VALIDATION.md` across at least three image conditions per job type, including adversarial images and reviewer-correction measurement.
