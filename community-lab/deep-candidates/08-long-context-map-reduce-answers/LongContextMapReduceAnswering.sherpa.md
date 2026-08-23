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

# Long Context Map-Reduce Answering — Faithful Answers From Very Long Documents

## Problem
Stuffing a 200-page manual into a context window produces confident answers
that skip the middle, contradict themselves across chunks, or silently drop
constraints. "Big context" does not mean "even attention." This kit breaks
long-document Q&A into map (per-chunk evidence extraction), reduce (merge with
conflict handling), and verify (cite-back against chunks) stages.

## Who experiences it
- Anyone asking questions over long reports, specs, transcripts, or legal-ish
  internal docs.
- Teams hitting "the answer missed section 7" failures.
- Automation builders whose pipeline chokes past a token limit.

## Claims (sourced) vs inference
CLAIM: OpenTelemetry GenAI conventions define token-usage attributes
(source: https://opentelemetry.io/docs/specs/semconv/gen-ai/, HTTP 200) —
used here to measure per-stage token cost.
CLAIM: In-repo context-vault-efficiency kit (../../domains/context-vault-efficiency/)
addresses assembling minimal sufficient context.
INFERENCE: Map-reduce with explicit conflict reporting yields fewer omissions
than single-pass stuffing for long inputs. The validation plan's omission
probe measures this.

## Workflow
1. **Chunk**: split the document at natural boundaries (headings/pages) into
   chunks under the model's comfortable working size. Fill in
   `CHUNK_TARGET=<words>`, `OVERLAP=<words>`. Preserve chunk ids + headings.
2. **Map**: per chunk, ask only: "Extract statements relevant to <QUESTION>,
   verbatim-ish, with chunk id; return NONE if nothing relevant." Cheap model
   is fine here. Collect the evidence list.
3. **Reduce**: feed the evidence list (not the raw document) to a stronger
   model with the instruction to merge, resolve duplicates, and flag
   contradictions with both chunk ids. If evidence says NONE everywhere,
   output NOT FOUND.
4. **Verify**: pick the top claims; re-check each against its cited chunk
   (small context, cheap call). Drop or downgrade unsupported claims.
5. **Cost ledger**: log tokens per stage (map total, reduce, verify). Compare
   against a single-pass baseline on the same question.

## Copy/paste map prompt (fill-in)
```text
From the chunk below, extract every statement relevant to:
<QUESTION>
Rules: keep original wording; prefix each with [<CHUNK_ID>]; if none relevant
output exactly NONE. Do not summarize away numbers, dates, or conditions.
Chunk:
<CHUNK_TEXT>
```

## Status
**AI-SOURCED / UNTESTED.** No omission-rate numbers claimed; the validation
plan defines the probe.
