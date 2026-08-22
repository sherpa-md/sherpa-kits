# Sherpa Handoffs

Every file in this folder is meant to be understandable before it is opened.

## Naming rule

```text
<BriefDescription>.sherpa.md
```

Examples:

- `BOMbilling.sherpa.md`
- `ComputerGithubSetup.sherpa.md`
- `TokenPiggyBank.sherpa.md`

Use a short description of the outcome. Preserve useful acronyms. Do not put dates, version numbers, marketing labels, or workflow jargon in the filename.

## Current handoffs

| File | What it does |
|---|---|
| [`ComputerGithubSetup.sherpa.md`](./ComputerGithubSetup.sherpa.md) | Helps another person set up their own computer workspace and GitHub access, with optional AI-to-AI bus messaging |
| [`TokenPiggyBank.sherpa.md`](./TokenPiggyBank.sherpa.md) | Installs and integrates the Token Piggy Bank quota and value governor |

## Optional requested ZIP

Do not generate a bundle automatically. Only when someone specifically requests all handoffs together, run from the repository root:

```bash
./scripts/build-handoff-bundle.sh
```

The result is `dist/SherpaHandoffs.zip`.

