---
schema_version: "0.1.0"
id: "portable-agent-handoff"
title: "Portable Agent Handoff & Workspace Bootstrap"
domain: "agent-onboarding"
version: "0.1.0"
status: "draft"
verification_state: "unverified"
last_verified: "2026-08-22T21:30:00Z"
confidentiality: "public"
provenance:
  origin_task: "portable-agent-handoff-initial-release"
  author_alias: "sherpa-core"
  verifier_alias: "codex-work"
sources:
  - id: "src-sherpa-spec"
    title: "SherpaMD Format Specification"
    uri: "https://github.com/sherpa-md/sherpa-spec/blob/main/SherpaMDSpecification.sherpa.md"
    type: "normative-spec"
  - id: "src-ai-bus"
    title: "AI-to-AI Bus Kit"
    uri: "../ai-to-ai-bus/AItoAIBus.sherpa.md"
    type: "related-kit"
tags:
  - "handoff"
  - "onboarding"
  - "github"
  - "workspace-bootstrap"
  - "ai-to-ai-bus"
  - "sanitized-sharing"
related_links:
  - rel: "spec"
    uri: "https://github.com/sherpa-md/sherpa-spec"
  - rel: "extends"
    uri: "../ai-to-ai-bus/AItoAIBus.sherpa.md"
---

# Portable Agent Handoff & Workspace Bootstrap

## 1. Purpose & Scope

This kit creates a portable, sanitized handoff that another person can give to a coding agent to establish a local workspace, verify GitHub access, and optionally connect to an existing coordination bus.

It covers identity-safe placeholders, capability verification, repository bootstrap, least-privilege permissions, lifecycle receipts, and a shareable Sherpa file. It does not distribute credentials, clone a private machine topology, or grant remote execution by default.

## 2. Core Directives & Rules

1. **Recipient-owned values only.** Replace placeholders with the recipient's computer, account, repository, and preferred agent values.
2. **Never transport secrets in Markdown.** Authentication must use the recipient's credential manager, OAuth flow, SSH agent, or environment configuration.
3. **Verify before claiming failure.** An agent must discover the relevant connector or tool and perform a harmless read-only probe before saying access is unavailable.
4. **Separate local and remote capability.** A folder that is not a local Git checkout does not prove that a GitHub connector is disconnected.
5. **Least privilege first.** Begin with repository read access. Add branch/commit/PR access only when the recipient requests it.
6. **No remote execution by default.** Bus messaging and remote command execution are separate permissions.
7. **Produce receipts.** Every setup stage returns PASS, BLOCKED, or NEEDS-AUTH with the exact verified evidence and one bounded next action.
8. **Do not make the recipient restart or repeat setup without evidence.** Re-authentication, reconnection, or a new session is justified only by a failed capability probe.

## 3. Knowledge Graph & Architecture

| Component | Owner | Purpose | Default permission |
|---|---|---|---|
| Recipient workstation | Recipient | Local files and development tools | Local only |
| GitHub repository | Recipient or collaborator | Durable source and review history | Read first |
| Coding agent | Recipient | Inspect, edit, test, and explain | Workspace scoped |
| GitHub connector or CLI | Recipient | Repository read/write operations | Read probe first |
| Optional coordination bus | Bus operator | Agent-to-agent task/status exchange | Message only |
| Optional remote executor | Machine owner | Explicit remote actions | Disabled |

The portable handoff is the control document. It names capabilities and boundaries but never embeds credentials or private infrastructure identifiers.

## 4. Operational Procedures & Commands

### Procedure A: Sanitize and share

1. Copy `ComputerGithubSetup.sherpa.md` from the repository's `handoffs/` folder.
2. Replace only the angle-bracket placeholders that the recipient knows.
3. Leave unknown optional values as `NOT_CONFIGURED`.
4. Scan for secrets, private addresses, internal hostnames, usernames, and personal paths.
5. Send the single file to the recipient.

Verification:

```bash
grep -nE '(BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|github_pat_|ghp_|sk-[A-Za-z0-9_-]{20,}|/home/[^/< ]+|/Users/[^/< ]+)' ComputerGithubSetup.sherpa.md && exit 1 || true
```

### Procedure B: Bootstrap the recipient workspace

The recipient's agent follows the ordered workflow in `WORKFLOW.md`: inventory, capability discovery, read-only probes, local workspace creation, GitHub setup, optional bus setup, then final receipts.

Verification:

```bash
git --version
git status --short --branch
git remote -v
```

The Git commands apply only after a local checkout exists. Connector access must be tested through the connector itself.

### Procedure C: Prove GitHub capability

1. Discover available GitHub interfaces: connected app, MCP tool, CLI, or local remote.
2. Run the least invasive repository-list or repository-metadata request.
3. Record explicit permissions such as read, push, admin, or unknown.
4. Only then classify the capability.

Allowed classifications:

- `AVAILABLE_READ`
- `AVAILABLE_WRITE`
- `AUTH_REQUIRED`
- `PERMISSION_DENIED`
- `TOOL_UNAVAILABLE`
- `TRANSIENT_FAILURE`
- `UNKNOWN`

Verification evidence must name the interface tested, the repository, the operation, and the result without exposing credentials.

## 5. Contradiction Notes & Reconciliations

| Conflict | Wrong inference | Required resolution |
|---|---|---|
| Local directory is not a Git repository, but a GitHub connector exists | “GitHub is unavailable” | Probe the connector independently |
| Repository can be read, but write permission is unknown | “Full access is available” | Report read-only until a write-safe permission result exists |
| Bus messaging works, but remote execution is not configured | “The agent controls the remote computer” | Keep messaging and execution permissions separate |
| A copied handoff contains private topology | “The recipient needs the original values” | Replace with recipient-owned placeholders |

Unresolved contradictions must be marked `BLOCKED` rather than guessed through.

## 6. Related Links & Dependencies

- [Shareable Sherpa file](../../handoffs/ComputerGithubSetup.sherpa.md)
- [Instructions](./INSTRUCTIONS.md)
- [Workflow](./WORKFLOW.md)
- [Validation](./VALIDATION.md)
- [SherpaMD specification](https://github.com/sherpa-md/sherpa-spec)
- [AI-to-AI Bus kit](../ai-to-ai-bus/AItoAIBus.sherpa.md)

## 7. Verification & Audit Evidence

- **2026-08-22:** Schema and editorial review completed in ChatGPT Work/Codex.
- **Current state:** Cross-platform execution tests remain pending; therefore the kit remains `draft` and `unverified`.
- Promotion gate: pass the acceptance cases in `VALIDATION.md` on at least two independent agent/tool environments, with sanitized receipts.

## 8. Revision History

| Version | Date | State | Change |
|---|---|---|---|
| `0.1.0` | 2026-08-22 | Draft | Initial portable handoff, workspace bootstrap, safety boundaries, and capability verification workflow |
