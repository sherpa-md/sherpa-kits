# Portable Agent Handoff & Workspace Bootstrap

Give another person one sanitized Markdown file that helps their AI set up a usable local workspace, connect to their own GitHub repository, and optionally join an AI-to-AI coordination bus.

This kit does **not** assume the recipient has DesktopBrian, H1, Tailscale, your usernames, your hostnames, or your secrets.

## Share this file

Send [`ComputerGithubSetup.sherpa.md`](../../handoffs/ComputerGithubSetup.sherpa.md) through Discord, email, or any file-sharing channel. The recipient fills in the marked placeholders and gives the file to their coding agent.

## Package contents

- [`SHERPA.md`](./SHERPA.md) — canonical SherpaMD kit definition.
- [`ComputerGithubSetup.sherpa.md`](../../handoffs/ComputerGithubSetup.sherpa.md) — the Sherpa file to share.
- [`INSTRUCTIONS.md`](./INSTRUCTIONS.md) — operator and agent rules.
- [`WORKFLOW.md`](./WORKFLOW.md) — setup and verification sequence.
- [`CHECKLIST.md`](./CHECKLIST.md) — completion checklist.
- [`VALIDATION.md`](./VALIDATION.md) — acceptance tests and evidence format.
- [`COMPATIBILITY.md`](./COMPATIBILITY.md) — supported environments and known limits.
- [`CHANGELOG.md`](./CHANGELOG.md) — release history.

## Safety boundary

Never place API keys, passwords, personal access tokens, private keys, private IP addresses, internal hostnames, or personal filesystem paths in the handoff. Use placeholders and the recipient's normal credential manager.
