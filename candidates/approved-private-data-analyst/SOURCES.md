# Sources and design inferences

- [Microsoft: Enterprise data protection in Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/enterprise-data-protection) — describes tenant isolation, encryption, inherited permissions/policies, auditing, and treatment of prompts, responses, and Graph data.
- [Microsoft: Semantic indexing for Copilot](https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot) — describes Graph/semantic-index grounding and states that results surface only when the user already has access.
- [Microsoft: Azure AI Search security filters](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search) — documents query-time filtering using user or group principals.
- [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1) — generative-AI risk-management profile used for governance and evaluation framing.
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — motivates untrusted-content segregation, least privilege, output validation, and human approval.

## Inferences

- Product protections do not replace organization approval, correct tenant configuration, source ACL hygiene, or application testing.
- Permission-aware retrieval is necessary but not sufficient: calculations, exports, logs, and caches can still leak data unless governed separately.
- The Microsoft references are an implementation example, not a claim that every organization approves the same services.
