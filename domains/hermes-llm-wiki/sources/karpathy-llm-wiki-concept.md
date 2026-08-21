# Source: Andrej Karpathy LLM-Wiki Synthesis Concept

- **Type**: Design Concept / Architectural Pattern
- **Summary**:
  Andrej Karpathy proposed that human knowledge bases and AI memory should function like a dynamic, synthesized Wikipedia rather than an unstructured append-only transcript archive.
  - **The Problem**: Linear chat logs grow unboundedly, accumulate contradictory instructions, and cause LLM context rot.
  - **The Pattern**:
    1. Raw evidence is ingested into a staging area (`sources/`).
    2. An LLM curator continuously extracts durable concepts, architectural decisions, and verifiable runbooks.
    3. Knowledge articles are updated in-place, pruning superseded facts.
    4. Agents query or inject distilled knowledge articles rather than megabytes of raw chat history.
