# Sherpa Kits Repository (`sherpa-kits`)

[![Validate Kits](https://github.com/sherpa-md/sherpa-kits/actions/workflows/validate.yml/badge.svg)](https://github.com/sherpa-md/sherpa-kits/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SherpaMD Spec: v0.1.0](https://img.shields.io/badge/SherpaMD-v0.1.0-blue.svg)](https://github.com/sherpa-md/sherpa-spec)

Official repository for domain kits, operational knowledge bases, and shareable agent runbooks built on the **SherpaMD** standard.

## What is a Sherpa kit?

A Sherpa kit is a structured Markdown package that humans can read and an AI can follow. Each kit has a canonical `SHERPA.md` entrypoint and may include a named Sherpa file designed to be shared directly.

Sherpa kits use in-place synthesis instead of raw transcript dumps, explicit verification states instead of unsupported certainty, and sanitized placeholders instead of private infrastructure details.

## Kits catalog

| Kit ID | Domain | Version | Status | Verification | Shareable entry |
|---|---|---:|---|---|---|
| [`core-fleet`](./domains/core/SHERPA.md) | Fleet operations | `0.1.0` | Active | Verified | `SHERPA.md` |
| [`hermes-llm-wiki`](./domains/hermes-llm-wiki/SHERPA.md) | Fleet knowledge | `0.1.0` | Active | Verified | `SHERPA.md` |
| [`token-piggy-bank`](./domains/token-piggy-bank/SHERPA.md) | Token governance | `1.0.0` | Active | Verified | [`TokenPiggyBank.sherpa.md`](./handoffs/TokenPiggyBank.sherpa.md) |
| [`bounded-agent-control-plane`](./domains/bounded-agent-control-plane/SHERPA.md) | Agent security | `0.1.0` | Active | Verified | `SHERPA.md` |
| [`ai-to-ai-bus`](./domains/ai-to-ai-bus/SHERPA.md) | Agent coordination | `0.1.0` | Active | Verified | `SHERPA.md` |
| [`multi-llm-watchdog`](./domains/multi-llm-watchdog/SHERPA.md) | LLM observability | `0.1.0` | Active | Verified | `SHERPA.md` |
| [`context-vault-efficiency`](./domains/context-vault-efficiency/SHERPA.md) | Memory optimization | `0.1.0` | Active | Verified | `SHERPA.md` |
| [`portable-agent-handoff`](./domains/portable-agent-handoff/SHERPA.md) | Agent onboarding | `0.1.0` | Draft | Unverified | [`ComputerGithubSetup.sherpa.md`](./handoffs/ComputerGithubSetup.sherpa.md) |

## First sharing kit

The Portable Agent Handoff kit gives a collaborator a sanitized Sherpa file for setting up their own computer and GitHub repository, with optional AI-to-AI bus messaging. It does not assume the collaborator has the sender's machine names, network, private topology, or credentials.

Send the collaborator:

[`handoffs/ComputerGithubSetup.sherpa.md`](./handoffs/ComputerGithubSetup.sherpa.md)

## Repository structure

```text
.
├── catalog.json
├── validate.sh
├── domains/
│   ├── ai-to-ai-bus/
│   ├── bounded-agent-control-plane/
│   ├── context-vault-efficiency/
│   ├── core/
│   ├── hermes-llm-wiki/
│   ├── multi-llm-watchdog/
│   ├── portable-agent-handoff/
│   │   ├── SHERPA.md
│   │   ├── README.md
│   │   ├── INSTRUCTIONS.md
│   │   ├── WORKFLOW.md
│   │   ├── CHECKLIST.md
│   │   ├── VALIDATION.md
│   │   ├── COMPATIBILITY.md
│   │   └── CHANGELOG.md
│   └── token-piggy-bank/
│       ├── SHERPA.md
│       └── README.md
├── handoffs/
│   ├── README.md
│   ├── ComputerGithubSetup.sherpa.md
│   └── TokenPiggyBank.sherpa.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Validation

Run:

```bash
./validate.sh
```

GitHub Actions runs the same validation on every push to `main` and every pull request.

## Creating a kit

1. Start from [`sherpa-kit-template`](https://github.com/sherpa-md/sherpa-kit-template).
2. Add `domains/<kit-id>/SHERPA.md` using the [SherpaMD specification](https://github.com/sherpa-md/sherpa-spec).
3. Keep new work `draft` and `unverified` until its validation evidence is recorded.
4. Add human help, workflow, checklist, validation, compatibility, and changelog files when the kit is meant for direct sharing.
5. Register it in `catalog.json` and this README.
6. Run validation and scan for secrets, private topology, personal paths, and accidental personal information.

## Ecosystem

- [`sherpa-spec`](https://github.com/sherpa-md/sherpa-spec): normative format and schema.
- [`sherpa-kit-template`](https://github.com/sherpa-md/sherpa-kit-template): starter structure.
- [`sherpa-kits`](https://github.com/sherpa-md/sherpa-kits): public kit catalog.

## License

Licensed under the [MIT License](./LICENSE).
