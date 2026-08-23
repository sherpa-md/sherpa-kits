# Sources and design inferences

- [Google Cloud Document AI](https://docs.cloud.google.com/document-ai/docs) — authoritative example of transforming unstructured documents into structured data.
- [C2PA Technical Specification 2.2](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html) — defines media provenance concepts, actors, assets, derived assets, actions, claims, and validation.
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — explicitly includes indirect and multimodal injection risks and recommends content segregation, least privilege, validation, and human approval.

## Inferences

- OCR or vision confidence alone cannot justify a consequential business fact; localization and review are also required.
- C2PA support is preferred when the toolchain supports it; a signed or content-addressed internal manifest is still needed when it does not.
