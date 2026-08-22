# Compatibility

| Environment | Expected support | Verification state | Notes |
|---|---|---|---|
| ChatGPT Work / Codex with GitHub connector | Full workflow | Editorial review only | Connector and local workspace must be tested independently |
| Codex CLI with GitHub CLI or Git remote | Full workflow | Pending | Run from recipient-owned workspace |
| GitHub Copilot coding agent | Core handoff workflow | Pending | Map capability probes to available GitHub tools |
| Claude coding environments | Core handoff workflow | Pending | Tool names differ; classifications remain the same |
| Gemini coding environments | Core handoff workflow | Pending | Tool names differ; classifications remain the same |
| Other agent frameworks | Adaptable | Pending | Preserve the directives, lifecycle receipts, and safety boundary |

## Requirements

- Markdown support.
- Local filesystem access for workspace setup, or an explicit remote workspace.
- GitHub connector, GitHub CLI, or Git remote for repository operations.
- Human-controlled authentication.

## Non-requirements

- No specific operating system.
- No specific machine name or network.
- No Tailscale requirement.
- No DesktopBrian, H1, Hermes, or private fleet dependency.
- No coordination bus unless the recipient chooses to configure one.

