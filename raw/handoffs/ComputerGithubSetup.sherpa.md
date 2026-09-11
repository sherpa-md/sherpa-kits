# Portable Agent Handoff

Give this entire file to your coding agent. Replace the marked placeholders with your own values. Do not paste credentials into this file.

## Your values

| Setting | Value |
|---|---|
| Your display name | `<YOUR_NAME>` |
| Your computer alias | `<YOUR_COMPUTER_ALIAS>` |
| Operating system | `<WINDOWS_MACOS_OR_LINUX>` |
| Workspace folder | `<YOUR_WORKSPACE_FOLDER>` |
| GitHub account or organization | `<YOUR_GITHUB_OWNER>` |
| GitHub repository | `<YOUR_REPOSITORY_NAME>` |
| Default branch | `main` |
| Preferred coding agent | `<YOUR_AGENT_NAME>` |
| Coordination bus | `NOT_CONFIGURED` |
| Remote execution | `DISABLED` |

## Mission

Set up a safe, working development workspace on this computer and connect it to `<YOUR_GITHUB_OWNER>/<YOUR_REPOSITORY_NAME>`. Verify every capability through the actual relevant interface before claiming it is unavailable. Do not assume my computer matches the sender's computer.

## Non-negotiable rules

1. Never request or print a password, token, API key, private key, recovery code, or session cookie.
2. Use normal OAuth, credential-manager, SSH-agent, or approved connector flows for authentication.
3. Before claiming a tool, connector, repository, permission, or access path is unavailable:
   - discover the relevant interfaces;
   - run a harmless read-only probe;
   - report the exact result.
4. Never infer GitHub connector access from whether the current local folder is a Git repository.
5. Do not tell me to reconnect, restart, repeat setup, or open a new session unless the probe proves that action is necessary.
6. Keep coordination-bus messaging separate from remote command execution. Remote execution stays disabled until I explicitly enable it.
7. Take one bounded next action at a time when human authentication or approval is required.
8. Stop and report `BLOCKED` if two instructions conflict. Do not guess through a conflict.

## Required workflow

### 1. Inventory

Inspect without changing anything:

- operating system and shell;
- installed Git and GitHub tooling;
- current workspace folder;
- available GitHub connectors or MCP tools;
- repository visibility and permissions;
- available build/test commands if a repository is present.

Return an inventory receipt before making changes.

### 2. Capability preflight

For each needed capability, report one classification:

- `AVAILABLE_READ`
- `AVAILABLE_WRITE`
- `AUTH_REQUIRED`
- `PERMISSION_DENIED`
- `TOOL_UNAVAILABLE`
- `TRANSIENT_FAILURE`
- `UNKNOWN`

At minimum test:

- local filesystem read/write inside the chosen workspace;
- Git availability;
- GitHub repository read access;
- GitHub write permission, if the connector exposes permission metadata;
- branch and pull-request capability, if requested.

### 3. Local workspace

Create or select `<YOUR_WORKSPACE_FOLDER>`. If the repository already exists locally, inspect it and preserve uncommitted work. If it does not exist locally, use the verified GitHub interface and approved authentication method to clone or initialize it.

Do not delete, reset, overwrite, or force-push existing work.

### 4. GitHub connection

Connect the local workspace to `<YOUR_GITHUB_OWNER>/<YOUR_REPOSITORY_NAME>`. Prefer a feature branch for changes. Before the first push, show:

- repository and branch;
- files that will change;
- validation results;
- whether the action creates a commit, branch, or pull request.

### 5. Optional coordination bus

Leave this section disabled unless I provide bus details.

If enabled later, require recipient-owned values for:

| Setting | Placeholder |
|---|---|
| Bus URL or transport | `<BUS_TRANSPORT>` |
| Recipient agent ID | `<RECIPIENT_AGENT_ID>` |
| Allowed channels | `<ALLOWED_CHANNELS>` |
| Authentication method | `<AUTH_METHOD_NAME_ONLY>` |
| Message signing | `<SIGNING_METHOD_NAME_ONLY>` |

Never put the authentication value or signing key in this file.

Use lifecycle receipts:

`SENT → RECEIVED → STARTED → COMPLETED` or `FAILED/BLOCKED`

### 6. Final receipt

Finish with this table:

| Check | Status | Evidence |
|---|---|---|
| Workspace ready | PASS/BLOCKED | Sanitized path or workspace name |
| Git installed | PASS/BLOCKED | Version only |
| Repository read | PASS/BLOCKED | Repository name and tested interface |
| Repository write | PASS/BLOCKED/NOT_REQUESTED | Permission result or safe test |
| Validation | PASS/BLOCKED | Commands and result |
| Coordination bus | DISABLED/PASS/BLOCKED | No secrets |
| Remote execution | DISABLED | Must remain disabled by default |

Then give exactly one next action if anything remains blocked.

