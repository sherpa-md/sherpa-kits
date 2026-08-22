# Instructions

## For the sender

1. Send only `ComputerGithubSetup.sherpa.md` unless the recipient wants the full package.
2. Do not prefill your own computer names, usernames, repository credentials, private addresses, or internal service details.
3. Explain what collaboration you are offering: repository access, messaging, review, or remote execution. These are separate permissions.
4. Grant repository access through GitHub, not by sharing credentials.

## For the recipient

1. Fill in only values you own or control.
2. Give the completed file to your coding agent.
3. Complete authentication directly in the official provider flow.
4. Review the final capability receipt before allowing the first write.

## For the coding agent

- Treat the handoff as the operating contract for setup.
- Preserve existing files and uncommitted changes.
- Use least-privilege, read-only probes first.
- Keep local Git state, GitHub connector state, and coordination-bus state separate.
- Never claim a capability is unavailable based on an unrelated failure.
- Never expose secrets in logs, receipts, commits, or chat.
- Stop at authentication and present one clear human action.
