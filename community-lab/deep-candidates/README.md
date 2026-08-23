# Deep Community-Lab Candidates (batch 1)

Ten AI-sourced, untested candidate kit file sets for advanced real-world AI
problems. Generated 2026-08-22 by qwen3.8-max (qwen-cloud) under bus task
bus-action-b451cfe5 on branch community-lab/deep-candidates-batch1.

These are NOT verified SherpaMD kits. They live outside the 100-seed flat
collection in `../ai-sourced-untested/` and do not modify it. Every kit states
AI-SOURCED / UNTESTED explicitly and ships with sources, an implementation
checklist, a validation plan, and privacy/security notes.

## Index

| # | Directory | Kit file | Problem |
|---|-----------|----------|---------|
| 01 | 01-multimodal-image-intake-pipeline | MultimodalImageIntakePipeline.sherpa.md | Metadata stripping + OCR triage before vision calls |
| 02 | 02-corporate-data-boundary-with-llm | CorporateDataBoundaryLLM.sherpa.md | Mixing private company data with one employer-approved LLM |
| 03 | 03-subscription-token-utilization-meter | SubscriptionTokenUtilizationMeter.sherpa.md | Measuring/pacing subscription quota across windows |
| 04 | 04-reliable-agent-handoff-recovery | ReliableAgentHandoffRecovery.sherpa.md | Handoffs that survive restarts: claims, checkpoints, watchdog |
| 05 | 05-private-doc-rag-with-grounded-citations | PrivateDocRagGroundedCitations.sherpa.md | Private-corpus Q&A with mandatory citations |
| 06 | 06-structured-output-enforcement-loop | StructuredOutputEnforcementLoop.sherpa.md | Schema validation + bounded repair loop for JSON output |
| 07 | 07-reproducible-generation-regression-gate | ReproducibleGenerationRegressionGate.sherpa.md | CI-style eval gate against prompt/model regressions |
| 08 | 08-long-context-map-reduce-answers | LongContextMapReduceAnswering.sherpa.md | Faithful Q&A over very long documents |
| 09 | 09-parallel-review-swarm-conflict-safety | ParallelReviewSwarmConflictSafety.sherpa.md | Parallel agent review without write conflicts |
| 10 | 10-local-voice-fallback-chain | LocalVoiceFallbackChain.sherpa.md | Cloud->local->degraded speech chain with health probes |

## Conventions
- Each kit: `Name.sherpa.md` (workflow), `README.md`, `sources.md`
  (claims vs inference), `implementation-checklist.md`, `validation-plan.md`,
  `privacy-security.md`.
- Sources distinguish CLAIM (linked evidence) from INFERENCE (design
  hypothesis to be tested). All external links in sources files were checked
  reachable on 2026-08-22 except where explicitly noted.
- Promotion path: follow `../ai-sourced-untested/CONTRIBUTING.md` — human test
  + `TEST-RESULT-TEMPLATE.md` before anything here can move toward the
  verified catalog.
- No medical content in this batch by design.
