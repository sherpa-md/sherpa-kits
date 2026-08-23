---
schema_version: "0.1.0"
id: "bounded-agent-control-plane"
title: "Bounded Agent Control Plane — Safe MCP & API Execution Gateway"
domain: "agent-security"
version: "0.1.0"
status: "active"
verification_state: "verified"
last_verified: "2026-08-21T22:00:00Z"
confidentiality: "public"
provenance:
  origin_task: "bounded-agent-control-plane-v0.1.0"
  author_alias: "hermb"
  verifier_alias: "hermb"
sources:
  - id: "src-mcp-spec"
    title: "Model Context Protocol Specification"
    url: "https://modelcontextprotocol.io"
    trust_label: "specification"
tags:
  - "control-plane"
  - "mcp"
  - "least-privilege"
  - "tool-allowlist"
  - "secret-redaction"
  - "action-auditing"
related_links:
  - rel: "spec"
    uri: "https://github.com/sherpa-md/sherpa-spec"
  - rel: "core-fleet"
    uri: "../core-fleet/CoreFleet.sherpa.md"
---

# Bounded Agent Control Plane — Safe MCP & API Execution Gateway

## 1. Purpose & Scope

The **Bounded Agent Control Plane** defines security boundaries, operational guardrails, and implementation patterns for mediating interactions between autonomous Large Language Model (LLM) agents and local or remote operating environments.

By eliminating unconstrained shell execution in favor of strictly typed Remote Procedure Call (RPC) interfaces, Model Context Protocol (MCP) servers, declarative parameter allowlists, automated secret filtering, and tamper-evident audit logging, this kit prevents accidental privilege escalation, credential exfiltration, and destructive actions.

---

## 2. Core Security Architecture & Principles

```text
+-----------------------------------------------------------------------+
|                       Autonomous Agent Core                           |
|       (Prompt Context / Planner / Tool Calling Subsystem)             |
+-----------------------------------+-----------------------------------+
                                    |
                        [1. Typed RPC / MCP Request]
                                    v
+-----------------------------------------------------------------------+
|                    Bounded Control Plane Gateway                      |
|  - Tool Allowlist Matching & Signature Enforcement                    |
|  - Strict Parameter Validation & Path Containment (No `../`)          |
|  - Unprivileged Sandbox & Least-Privilege Execution Context           |
+-----------------------------------+-----------------------------------+
                                    |
                        [2. Execution & Stream Filter]
                                    v
+-----------------------------------------------------------------------+
|                 Secret Redactor & Action Auditor                      |
|  - Real-time Token & Key Masking (Regex Stream Sanitizer)             |
|  - Append-Only Audit Ledger (`actions.audit.jsonl`)                   |
|  - Structured Error Propagation (Safe Failures, No Stack Leaks)       |
+-----------------------------------+-----------------------------------+
                                    |
                        [3. Safe Sanitized Response]
                                    v
+-----------------------------------------------------------------------+
|                        Agent Context Return                           |
+-----------------------------------------------------------------------+
```

### Key Security Principles

1. **No Arbitrary Shell Execution**: Agents are never provided open `bash -c`, `exec`, or `eval` primitives. All operations are mediated through explicit, strongly-typed tool endpoints with strict argument schemas (e.g., `inspect_service(service_name: str)`, `fetch_git_status(repo_path: str)`).
2. **Declarative Parameter Allowlists**: Input parameters must conform to strict regular expressions and enumerated safe lists. Path arguments are strictly resolved against designated root directories to prevent path traversal (`../`) attacks.
3. **Automated Secret Redaction**: All input streams, tool arguments, stdout/stderr payloads, and logs pass through an automated secret filter. API tokens, private keys, authorization headers, and environment credentials are replaced with `[REDACTED]` before leaving the boundary.
4. **Append-Only Action Auditing**: Every tool request and response is written synchronously to an append-only JSONL audit ledger containing timestamp, caller ID, tool name, parameter digest, duration, and execution status.
5. **Least Privilege Execution**: Control plane daemons run under dedicated unprivileged system users without `sudo` access, operating inside isolated process namespaces or restricted working directories.

---

## 3. Reference Implementation Patterns

### Safe MCP / FastAPI Gateway Pattern

```python
import os
import re
import json
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

SECRET_PATTERNS = [
    re.compile(r'(?i)(bearer\s+|token\s+|api[_-]?key[\s:=]+)([a-zA-Z0-9_\-\.]{12,})'),
    re.compile(r'ghp_[a-zA-Z0-9]{36}'),
    re.compile(r'sk-[a-zA-Z0-9]{32,}'),
    re.compile(r'-----BEGIN [A-Z]+ PRIVATE KEY-----'),
]

def redact_secrets(text: str) -> str:
    """Mask credentials and private keys from tool output."""
    sanitized = text
    for pattern in SECRET_PATTERNS:
        sanitized = pattern.sub(r'[REDACTED]', sanitized)
    return sanitized

class ServiceInspectRequest(BaseModel):
    service_name: str = Field(..., description="Target service identifier")

    @field_validator("service_name")
    def validate_service(cls, v: str) -> str:
        ALLOWED_SERVICES = {"agent-bus", "telemetry-collector", "quota-steward"}
        if v not in ALLOWED_SERVICES:
            raise ValueError(f"Service '{v}' is not in the execution allowlist.")
        return v

def record_audit_entry(audit_file: str, caller_id: str, tool: str, payload: Dict[str, Any], status: str):
    entry = {
        "timestamp": "2026-08-21T22:00:00Z",
        "caller": caller_id,
        "tool": tool,
        "payload": payload,
        "status": status
    }
    with open(audit_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
```

---

## 4. Verification Evidence & Acceptance Criteria

- **Tool Schema Validation**: All exposed tools define OpenAPI/Pydantic schemas with rejected parameter fuzzing.
- **Path Traversal Rejection**: Paths containing `..` or leading `/` outside workspace boundaries raise validation errors.
- **Secret Redaction Test**: Injected fake API keys (`EXAMPLE_API_KEY_VALUE`) are masked to `sk-[REDACTED]` in all output streams.
- **Audit Immutability**: Actions are written to the JSONL audit ledger prior to dispatching external system calls.
