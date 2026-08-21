# Source: Hermes Vault & FFB Architecture

- **Type**: Memory Architecture Specification
- **Summary**:
  Hermes employs a 3-tier memory system designed for multi-day continuity across restarts:
  1. **Ephemeral Context**: In-memory prompt tokens.
  2. **Disk-backed Artifacts**: Durable run-state, logs, and intermediate results located at `artifacts/<task-id>/`.
  3. **Curated Knowledge Vault**: SherpaMD domain kits (`sherpa-kits`) providing structured, verified architectural facts and procedures.
  - **FFB (Flywheel Feedback / Fleet Routing)**: Ensures specialized tasks route deterministically to the node holding appropriate capabilities (e.g. Media/GPU to Local Compute Worker).
