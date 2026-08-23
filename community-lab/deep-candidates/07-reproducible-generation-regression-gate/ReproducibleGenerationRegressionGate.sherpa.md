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

# Reproducible Generation Regression Gate — Catching Prompt/Model Regressions Before They Ship

## Problem
Teams tune prompts and workflows against one model version, then silently lose
quality when the model updates, the prompt drifts, or a teammate edits the
template. There is no CI equivalent of "tests broke" for generation quality.
This kit defines a regression gate: a frozen eval set, a scoring rubric,
baseline snapshots, and a pass threshold that blocks promotion when quality
drops.

## Who experiences it
- Anyone whose prompt "suddenly stopped working" after a model refresh.
- Teams sharing prompt templates across people.
- Fleet operators promoting verified kits (like the ones in this repo's
  domains/) who need evidence that a change did not regress behavior.

## Claims (sourced) vs inference
CLAIM: lm-evaluation-harness is an open-source framework for evaluating LLMs
on standardized tasks (source:
https://github.com/EleutherAI/lm-evaluation-harness, HTTP 200).
CLAIM: The community-lab TEST-RESULT-TEMPLATE.md in this repo already captures
model/provider/version per test — the minimum metadata a regression gate needs.
INFERENCE: A small task-specific eval set with a rubric catches the regressions
that matter in practice better than generic benchmarks. This is the hypothesis;
the gate's own track record is the evidence.

## Workflow
1. **Eval set**: collect 10-30 representative input/expectation pairs covering
   normal, edge, and failure cases. Store as JSON lines:
   `{"id", "input", "expectation", "why"}`. Fill in: `EVAL_SET=<path>`.
2. **Rubric**: for each item define what counts as pass (exact field,
   must-include fact, must-not-include claim, format constraint). Prefer
   machine-checkable rules; use a judge-model pass only where rules can't
   express it, and log the judge model version.
3. **Runner**: run the current prompt+model over the eval set; score each item
   (pass/fail + evidence excerpt). Store snapshot:
   `evals/<timestamp>/<model>-<prompt-hash>.json`.
4. **Baseline**: pin the first accepted snapshot as baseline. Fill in
   `BASELINE=<snapshot-id>`.
5. **Gate rule**: on any prompt/model/template change rerun; promotion is
   allowed only if score >= baseline score - tolerance (fill in
   `TOLERANCE=<0>`). Any new hard failure (must-not-include violated) is an
   automatic block regardless of score.
6. **Report**: the gate emits a compact diff: which items flipped, with
   evidence excerpts. No diffs of raw transcripts.

## Copy/paste rubric item schema (fill-in)
```json
{"id": "edge-01",
 "input": "<INPUT>",
 "rules": [
   {"type": "must_include", "value": "<FACT>"},
   {"type": "must_not_include", "value": "<FORBIDDEN>"},
   {"type": "format", "value": "json-schema:<path>"}
 ]}
```

## Status
**AI-SOURCED / UNTESTED.** Gate mechanics are specified but no real regression
has been caught with it yet; track record starts with the first validation run.
