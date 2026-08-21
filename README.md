# Sherpa Kits Repository (`sherpa-kits`)

[![Validate Kits](https://github.com/sherpa-md/sherpa-kits/actions/workflows/validate.yml/badge.svg)](https://github.com/sherpa-md/sherpa-kits)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SherpaMD Spec: v0.1.0](https://img.shields.io/badge/SherpaMD-v0.1.0-blue.svg)](https://github.com/sherpa-md/sherpa-spec)

Official repository for verified domain kits, operational knowledge bases, and shared agent runbooks built on the **SherpaMD** standard (`v0.1.0`).

---

## Overview: Dual Human & AI Knowledge Architecture

**Sherpa Kits** provide structured, human- and AI-readable operational packages designed for deterministic agent collaboration, verified provenance, and curated domain knowledge.

By applying the **Karpathy LLM-Wiki anti-rot pattern**, Sherpa Kits eliminate unbounded chat logs and contradictory prompt context through continuous in-place synthesis and structured YAML provenance.

### Why Sherpa Kits?

- **Anti-Rot Architecture**: Instead of appending raw transcripts that inflate LLM prompt tokens, knowledge is continuously synthesized into curated Markdown living documents.
- **Dual Readability**: Clean, high-density documentation that human engineers can review instantly and AI agents can parse deterministically.
- **Verifiable Runbooks**: Every operational procedure includes concrete, executable verification commands.
- **Deterministic Provenance**: Complete traceability from source documentation through verification state and author metadata.

---

## Active Kits Catalog

The active domain kits registered in this repository:

| Kit ID | Domain | Path | Version | Status | Verification State | Confidentiality |
|---|---|---|---|---|---|---|
| [`core-fleet`](./domains/core/SHERPA.md) | Fleet Infrastructure & Ops | `domains/core/SHERPA.md` | `0.1.0` | `active` | `verified` | `public` |
| [`hermes-llm-wiki`](./domains/hermes-llm-wiki/SHERPA.md) | Fleet Knowledge & Vault | `domains/hermes-llm-wiki/SHERPA.md` | `0.1.0` | `active` | `verified` | `public` |
| [`token-piggy-bank`](./domains/token-piggy-bank/SHERPA.md) | LLM Quota & Value Governor | `domains/token-piggy-bank/SHERPA.md` | `1.0.0` | `active` | `verified` | `public` |

---

## Repository Structure

```text
.
├── catalog.json                  # Machine-readable registry of all domain kits
├── validate.sh                   # Fast local schema and YAML validator
├── domains/                      # Domain kits container
│   ├── core/                     # Core fleet coordination kit
│   │   └── SHERPA.md
│   ├── hermes-llm-wiki/          # Knowledge vault & anti-rot architecture
│   │   ├── SHERPA.md
│   │   └── sources/              # Upstream source summaries and reference specs
│   └── token-piggy-bank/         # Token governance and quota pacing kit
│       └── SHERPA.md
├── CONTRIBUTING.md               # Kit authoring and validation guide
├── SECURITY.md                   # Security policy & disclosure guidelines
└── LICENSE                       # MIT License
```

---

## Quickstart & Validation

To validate all kits locally:

```bash
./validate.sh
```

---

## Creating a New Kit

1. Scaffold a new kit using the official [`sherpa-kit-template`](https://github.com/sherpa-md/sherpa-kit-template).
2. Place the kit under `domains/<kit-id>/` with its own `SHERPA.md` and optional `sources/` folder.
3. Register the kit in `catalog.json` and update the table in this README.
4. Run `./validate.sh` to confirm schema and syntax compliance.
5. Submit a pull request following [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Ecosystem

- [`sherpa-spec`](https://github.com/sherpa-md/sherpa-spec): Normative SherpaMD specification and schema definitions.
- [`sherpa-kit-template`](https://github.com/sherpa-md/sherpa-kit-template): Starter repository template for scaffolding new domain kits.
- [`sherpa-kits`](https://github.com/sherpa-md/sherpa-kits): Standard collection of domain kits.

---

## License

This repository is licensed under the [MIT License](./LICENSE).
