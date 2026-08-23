# Sources and design inferences

- [NIST AI Resource Center](https://airc.nist.gov/) — NIST resources for AI risk management and testing, evaluation, verification, and validation.
- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1) — generative-AI risk profile used to organize evaluation and governance.
- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) — open model for end-to-end correlated operations, spans, events, attributes, links, and status.
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — security basis for adversarial injection tests, least privilege, output validation, and approval gates.

## Inferences

- Outcome oracles should be independent of the evaluated agent whenever possible.
- Safety blockers should not be averaged into a composite score that allows high task accuracy to hide a severe violation.
- Production receipts and traces create the feedback loop that turns escaped failures into regression cases.
