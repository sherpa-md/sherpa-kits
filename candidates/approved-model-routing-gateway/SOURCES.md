# Sources and design inferences

- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1) — generative-AI risk-management profile for governance and evaluation.
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — recommends constrained behavior, output validation, least privilege, untrusted-content segregation, approval, and adversarial testing.
- [Microsoft: Enterprise data protection in Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/enterprise-data-protection) — concrete example of enterprise contractual and technical protections for a named service boundary.

## Inferences

- “Approved vendor” is too broad; approval must bind the exact service profile, tenant/project, data class, and usage terms.
- Routing for cost or quality occurs only after policy filtering. An unapproved route with better benchmarks is still unavailable.
