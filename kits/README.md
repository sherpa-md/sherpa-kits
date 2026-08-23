# Supporting Kits

This folder contains the deeper packages behind Sherpa files.

If you only want a file to send to a person or AI, go to **[handoffs/](../handoffs/)**.

## What is inside a kit?

- `<BriefDescription>.sherpa.md` — canonical technical entrypoint with a descriptive filename.
- `README.md` — short human explanation when available.
- Supporting instructions, workflow, checklist, compatibility, validation, changelog, or sources when the kit needs them.

## Kit index

| Folder | What it supports | Shareable Sherpa file |
|---|---|---|
| [`ai-to-ai-bus`](./ai-to-ai-bus/) | Agent-to-agent messaging and durable task states | Planned |
| [`bounded-agent-control-plane`](./bounded-agent-control-plane/) | Safe tool and API execution | Planned |
| [`context-vault-efficiency`](./context-vault-efficiency/) | Durable context and token efficiency | Planned |
| [`core-fleet`](./core-fleet/) | Multi-agent coordination | Planned |
| [`hermes-llm-wiki`](./hermes-llm-wiki/) | Living knowledge architecture | Planned |
| [`multi-llm-watchdog`](./multi-llm-watchdog/) | Provider health and quota monitoring | Planned |
| [`portable-agent-handoff`](./portable-agent-handoff/) | Collaborator computer and GitHub setup | [`ComputerGithubSetup.sherpa.md`](../handoffs/ComputerGithubSetup.sherpa.md) |
| [`token-piggy-bank`](./token-piggy-bank/) | Token quota and value governance | [`TokenPiggyBank.sherpa.md`](../handoffs/TokenPiggyBank.sherpa.md) |

## Adding a kit

Follow [CONTRIBUTING.md](../CONTRIBUTING.md), register the kit in [catalog.json](../catalog.json), and keep it marked draft until its validation evidence is complete.
