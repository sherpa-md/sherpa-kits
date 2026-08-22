# Sherpa Kits Project Status

- **Updated**: 2026-08-22T23:57:04Z
- **Organization**: `sherpa-md`
- **Repository**: `sherpa-kits`
- **Catalog entries**: 8

## Current state

| Kit | State | Notes |
|---|---|---|
| `core-fleet` | Active / verified | Public identifiers sanitized |
| `hermes-llm-wiki` | Active / verified | Public identifiers sanitized |
| `token-piggy-bank` | Active / verified | Shareable file uses Sherpa naming |
| `bounded-agent-control-plane` | Active / verified | Existing kit |
| `ai-to-ai-bus` | Active / verified | Existing kit |
| `multi-llm-watchdog` | Active / verified | Existing kit |
| `context-vault-efficiency` | Active / verified | Existing kit |
| `portable-agent-handoff` | Draft / unverified | First user-facing sharing kit; cross-platform tests pending |

## Release evidence

- Root public-release documents are present.
- Current-tree scan found no live credentials, private keys, personal names, email addresses, private IP addresses, or accidental medical content.
- GitHub Actions now runs `validate.sh` on pushes and pull requests.
- The portable handoff remains visibly unverified until the acceptance cases pass in two independent agent environments.

## Known limits

- This status does not certify the complete Git history; only the current default-branch tree was audited.
- The current validator checks catalog JSON, front-matter presence, public confidentiality, hardcoded personal home paths, and repository baseline documents. Schema validation should be strengthened in a later release.

