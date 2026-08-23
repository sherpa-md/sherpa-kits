# Sources and design inferences

- [Google Cloud Document AI](https://docs.cloud.google.com/document-ai/docs) — authoritative example of document OCR and structured-data extraction.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) — provenance model used for original documents, extractions, corrections, activities, agents, and filed derivatives.
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — supports treating document content as untrusted and constraining tools/privileges.

## Inferences

- Human review should be triggered by consequence and rule failures as well as confidence.
- Field-level source regions and corrections create better auditability and learning signals than approval of a prose summary.
