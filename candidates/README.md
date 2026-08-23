# Deep 10 AI System Candidates

These are not prompt tips or beginner AI lessons. Each folder defines a substantial system that an AI engineer, platform team, or capable agent can build, test, and govern.

Every candidate is deliberately marked `draft` and `unverified`. Candidates do not appear in `catalog.json` or `handoffs/` until the validation file in that candidate passes and a human reviewer approves promotion.

| Candidate | Useful outcome | High-risk boundary |
|---|---|---|
| [approved-private-data-analyst](./approved-private-data-analyst/) | Analyze private company data with an approved, permission-aware model | Data must never leave the approved tenant/tool boundary |
| [picture-to-structured-work](./picture-to-structured-work/) | Turn images into structured, reviewable work products | Images are untrusted input and may contain hidden instructions |
| [planned-actual-reconciler](./planned-actual-reconciler/) | Reconcile plans, telemetry, and actual outcomes | Correlation must not be presented as causation |
| [evidence-bound-decision-engine](./evidence-bound-decision-engine/) | Produce decisions tied to inspectable evidence | Unsupported claims remain `UNKNOWN` |
| [incident-replay-root-cause](./incident-replay-root-cause/) | Rebuild an incident timeline and test root-cause hypotheses | AI may propose hypotheses, never silently rewrite evidence |
| [institutional-memory-builder](./institutional-memory-builder/) | Convert scattered work into permission-aware institutional memory | Source permissions and provenance must survive indexing |
| [approved-model-routing-gateway](./approved-model-routing-gateway/) | Route each task only to approved models and tools | A model never chooses or expands its own privileges |
| [estimate-actuals-analyst](./estimate-actuals-analyst/) | Learn why estimates differ from actuals and improve forecasts | Sensitive commercial data stays in approved systems |
| [human-verified-document-automation](./human-verified-document-automation/) | Extract, draft, and file documents with review checkpoints | Low-confidence or consequential fields require human approval |
| [agent-outcome-qa-harness](./agent-outcome-qa-harness/) | Score agents on outcomes, safety, evidence, cost, and repeatability | Self-reported agent success is not accepted as proof |

## Candidate state model

1. `draft / unverified`: architecture and test plan exist; implementation evidence does not.
2. `draft / needs-retest`: some evidence exists, but a dependency, model, or policy changed.
3. `active / verified`: acceptance tests pass in the stated environments and evidence is reviewable.

See [CANDIDATE_STANDARD.md](./CANDIDATE_STANDARD.md) for the minimum bar.
