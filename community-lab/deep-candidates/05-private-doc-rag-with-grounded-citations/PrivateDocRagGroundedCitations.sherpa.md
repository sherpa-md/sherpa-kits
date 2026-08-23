---
status: ai-sourced-untested
source_type: ai-synthesized
testing: not-tested
human_reviewed: false
model: qwen3.8-max
provider: qwen-cloud
risk_level: medium
batch: deep-candidates-batch1
---

# Private Document RAG with Grounded Citations — Answers That Cite Your Files

## Problem
When people ask an LLM about their own documents, answers blend real content
with hallucinated detail and provide no way to check which is which. For
private corpora (manuals, contracts, meeting notes), an uncited answer is
unusable. This kit defines a retrieval-augmented workflow where every claim in
the answer carries a citation to a specific file and passage, and anything not
grounded is labeled INFERENCE or omitted.

## Who experiences it
- Anyone building Q&A over internal documents.
- Teams burned by hallucinated policy answers.
- Knowledge workers who must defend where an answer came from.

## Claims (sourced) vs inference
CLAIM: JSON Schema provides machine-checkable constraints for structured data
(source: https://json-schema.org, HTTP 200) — used here to constrain the
answer format so citations are structurally required.
CLAIM: This repo's context-vault-efficiency kit addresses context assembly
(see ../../domains/context-vault-efficiency/).
INFERENCE: Enforcing a citation schema at output time measurably lowers
unsupported claims versus free-form answers. Measured in the validation plan.

## Workflow
1. **Corpus prep**: gather source docs into `CORPUS_DIR` (fill in). Assign
   each doc a stable id. Split into passages (~300-600 words) preserving
   headings; store `{doc_id, passage_id, heading, text}` records.
2. **Index**: build a retrieval index (keyword or embedding — fill in your
   tool: `RETRIEVER=<bm25|embeddings>`). Index stays local.
3. **Query**: retrieve top-k passages (fill in `K=<5>`); include doc id and
   heading in each.
4. **Grounded generation**: prompt the model with the retrieved passages and a
   schema-constrained answer format (below). Rule: every factual claim maps to
   one or more `[doc_id:passage_id]`; anything not supported by retrieved text
   must be labeled INFERENCE or left out.
5. **Verify pass**: a second cheap check re-reads each cited passage and marks
   each claim SUPPORTED / NOT-SUPPORTED / PARTIAL. NOT-SUPPORTED claims are
   stripped or downgraded before delivery.
6. **Refusal over fabrication**: if retrieval returns nothing relevant, the
   correct output is "not found in corpus" — never a plausible guess.

## Copy/paste grounded-answer prompt (fill-in)
```text
Answer ONLY from the passages below. Each passage has an id like [d3:p12].
Rules:
1. Every factual sentence ends with its supporting passage ids.
2. If passages conflict, say so and cite both.
3. If the answer is not in the passages, output exactly: NOT FOUND IN CORPUS.
4. Mark anything you must add beyond the passages as INFERENCE.
Passages:
<RETRIEVED PASSAGES WITH IDS>
Question: <QUESTION>
```

## Status
**AI-SOURCED / UNTESTED.** No retrieval quality numbers are claimed; the
verify pass and validation plan define how grounding gets measured.
