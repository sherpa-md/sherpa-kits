# Bounded Agent Control Plane Kit

Safe, bounded execution environment mediating interactions between autonomous LLM agents and system resources.

## Core Capabilities

- **No Arbitrary Shell**: Replaces unrestricted terminal access with strictly typed MCP endpoints and curated action schemas.
- **Parameter Allowlists**: Enforces declarative input validation, regex whitelisting, and strict path containment.
- **Automated Secret Redaction**: Stream filter strips API tokens, SSH keys, passwords, and private identifiers from all stdout/stderr and audit payloads.
- **Immutable Action Auditing**: Synchronous append-only JSONL logging capturing all agent invocations with timestamps, caller IDs, and exit states.

## Architecture

```text
Autonomous Agent --> Typed MCP/FastAPI Request --> Allowlist Validator --> Sandboxed Runner --> Secret Redactor & Audit Log --> Safe Return
```

## Files & Artifacts

- [`BoundedAgentControlPlane.sherpa.md`](BoundedAgentControlPlane.sherpa.md) — Formal SherpaMD domain kit specification.
