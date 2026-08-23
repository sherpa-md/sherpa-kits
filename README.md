# Sherpa Kits

[![Validate Kits](https://github.com/sherpa-md/sherpa-kits/actions/workflows/validate.yml/badge.svg)](https://github.com/sherpa-md/sherpa-kits/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![SherpaMD Spec: v0.1.0](https://img.shields.io/badge/SherpaMD-v0.1.0-blue.svg)](https://github.com/sherpa-md/sherpa-spec)

Sherpa files are descriptive Markdown handoffs that a person can read and an AI can follow.

## Start here

| What you want | Where to go |
|---|---|
| Find a file to give an AI | **[handoffs/](./handoffs/)** |
| Read the supporting package behind a handoff | **[kits/](./kits/)** |
| Create your own Sherpa file | **[sherpa-kit-template](https://github.com/sherpa-md/sherpa-kit-template)** |
| Understand the SherpaMD format | **[sherpa-spec](https://github.com/sherpa-md/sherpa-spec)** |
| Contribute a file or correction | **[CONTRIBUTING.md](./CONTRIBUTING.md)** |

## Available Sherpa files

Shareable files use this naming format:

```text
<BriefDescription>.sherpa.md
```

| Sherpa file | What it does | State |
|---|---|---|
| [`ComputerGithubSetup.sherpa.md`](./handoffs/ComputerGithubSetup.sherpa.md) | Helps another person set up their own computer workspace and GitHub access, with optional AI-to-AI messaging | Draft; additional platform testing pending |
| [`TokenPiggyBank.sherpa.md`](./handoffs/TokenPiggyBank.sherpa.md) | Installs and integrates the Token Piggy Bank quota and value governor | Verified |

Each Sherpa file is available individually. A bundle is created only when somebody specifically requests one.

## Supporting kits

The [`kits/`](./kits/) folder contains the deeper documentation, validation evidence, compatibility notes, and source material behind the shareable files.

| Kit | Purpose | State |
|---|---|---|
| [`ai-to-ai-bus`](./kits/ai-to-ai-bus/) | Durable agent messaging and lifecycle receipts | Active |
| [`bounded-agent-control-plane`](./kits/bounded-agent-control-plane/) | Safe MCP and API execution boundaries | Active |
| [`context-vault-efficiency`](./kits/context-vault-efficiency/) | Context preservation and model-cost tiering | Active |
| [`core-fleet`](./kits/core-fleet/) | Multi-agent fleet coordination | Active |
| [`hermes-llm-wiki`](./kits/hermes-llm-wiki/) | Living knowledge and anti-rot architecture | Active |
| [`multi-llm-watchdog`](./kits/multi-llm-watchdog/) | Provider health and quota monitoring | Active |
| [`portable-agent-handoff`](./kits/portable-agent-handoff/) | Supporting package for collaborator computer and GitHub setup | Draft |
| [`token-piggy-bank`](./kits/token-piggy-bank/) | Token quota and value governance | Active |

## Repository map

```text
.
├── handoffs/        # Descriptive .sherpa.md files people actually share
├── kits/            # Supporting packages, instructions, and evidence
├── scripts/         # Maintainer validation and requested bundle tools
├── .github/         # Automation and project status
├── catalog.json     # Machine-readable kit index
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Rules that keep this usable

- Use descriptive `<BriefDescription>.sherpa.md` filenames.
- Keep shareable files in `handoffs/`.
- Keep supporting material in `kits/`.
- Never include credentials, private keys, personal paths, or private infrastructure identifiers.
- Keep unfinished work visibly marked `draft` and `unverified`.
- Do not generate a ZIP or bundle unless somebody asks for one.
- Give every canonical kit entrypoint a descriptive `<BriefDescription>.sherpa.md` filename.

## Validation

Run:

```bash
./validate.sh
```

GitHub Actions runs the same validation on pushes and pull requests.

## License

Licensed under the [MIT License](./LICENSE).
