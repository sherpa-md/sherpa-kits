---
status: ai-sourced-untested
source_type: ai-synthesized
testing: not-tested
human_reviewed: false
model: qwen3.8-max
provider: qwen-cloud
risk_level: low
batch: deep-candidates-batch1
---

# Structured Output Enforcement Loop — Schema-Valid Answers Without Begging

## Problem
Agents consuming LLM output break when the model returns prose instead of
JSON, drops required fields, or invents extra ones. Prompt-only enforcement
fails intermittently and teams waste quota on retries. This kit builds a
repair loop: attempt, validate against a schema, and on failure feed the exact
validation errors back as a targeted correction step, with a bounded retry
budget and a deterministic fallback.

## Who experiences it
- Automation builders parsing LLM JSON downstream.
- Fleet operators paying double tokens for malformed outputs.
- Anyone who has written "respond ONLY with valid JSON" and still got prose.

## Claims (sourced) vs inference
CLAIM: JSON Schema is the standard for describing/validating JSON structures
(source: https://json-schema.org, HTTP 200).
CLAIM: Outlines is an open-source library for constrained/structured
generation (source: https://github.com/outlines-dev/outlines, HTTP 200).
INFERENCE: A validate-repair loop with bounded retries yields higher valid-JSON
rates at lower total cost than naive re-prompting. The validation plan
measures this.

## Workflow
1. **Define the contract**: write the output JSON Schema. Fill in:
   `SCHEMA_PATH=<path>`; keep it small (required fields, enums, formats).
2. **First attempt**: prompt with the schema inline and one worked example of
   a valid object. Ask for nothing outside the schema.
3. **Validate**: parse + validate with any JSON Schema validator. On success,
   done in one call.
4. **Targeted repair**: on failure, send ONLY the validation errors back with
   the original output and ask for a corrected object (not a full redo). This
   is a focused correction step, not a full regeneration.
5. **Budget**: cap repairs (fill in: `MAX_REPAIRS=<2>`). After the budget:
   deterministic fallback — fill missing fields with explicit nulls and log
   the failure; never silently invent values.
6. **Measure**: log attempts, repairs, and final validity per task; this is
   your enforcement telemetry.

## Copy/paste repair prompt (fill-in)
```text
Your previous output failed schema validation. Fix ONLY these errors:
<VALIDATION_ERRORS with JSON paths>
Previous output:
<PREVIOUS_OUTPUT>
Schema:
<SCHEMA>
Return the corrected JSON object only, no commentary.
```

## Status
**AI-SOURCED / UNTESTED.** Repair-loop economics are hypothesized, not
measured; see validation plan.
