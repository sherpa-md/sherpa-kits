# Sources and evidence

## Direct sources
- In-repo verified kit: ../../domains/ai-to-ai-bus/AItoAIBus.sherpa.md
  (claim-based concurrency control).
- In-repo practice: this repository's own branch-per-workflow history
  (see git log) demonstrates branch isolation for concurrent work.

## Claims vs inference
- Claims: claim lifecycle and isolation mechanisms exist in referenced kits.
- Inference: read-only swarms + serial apply eliminate write conflicts for
  review workloads. Measured in the validation plan's collision test.
