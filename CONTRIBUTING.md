# Contributing to Sherpa Kits

Thank you for contributing to **Sherpa Kits**! This repository hosts standard, reusable domain knowledge kits built on the **SherpaMD** standard (`v0.1.0`).

---

## What is a Sherpa Kit?

A **Sherpa Kit** is a self-contained, domain-specific operational knowledge package. It bridges human architectural documentation and deterministic AI context prompts, eliminating context rot through continuous in-place synthesis (the Karpathy LLM-Wiki pattern).

Each kit lives in `kits/<kit-id>/` and consists of:
- `<BriefDescription>.sherpa.md`: The descriptively named primary domain entrypoint, directives, procedures, and knowledge graph.
- `sources/`: (Optional) Upstream reference documents, summaries, and source evidence.

---

## Contribution Workflow

1. **Scaffold Your Kit**: Use the canonical [`sherpa-kit-template`](https://github.com/sherpa-md/sherpa-kit-template).
2. **Directory Placement**: Create `kits/<kit-id>/` where `<kit-id>` is kebab-case (e.g., `kits/token-piggy-bank/`).
3. **YAML Front Matter**: Every `*.sherpa.md` entrypoint MUST include valid YAML front matter complying with schema `0.1.0`:
   - `schema_version`: `"0.1.0"`
   - `id`: Unique kebab-case identifier matching the directory name.
   - `title`: Descriptive title of the domain kit.
   - `domain`: High-level domain classification (e.g., `fleet-ops`, `fleet-knowledge`, `fleet-operations`).
   - `version`: Semantic version string (e.g., `"0.1.0"`, `"1.0.0"`).
   - `status`: One of `draft`, `active`, `deprecated`, `archived`.
   - `verification_state`: One of `verified`, `unverified`, `needs-retest`, `contradiction`.
   - `last_verified`: ISO 8601 timestamp.
   - `confidentiality`: `"public"` (or `"internal"`, `"restricted"` where applicable).
   - `provenance`: Author and origin metadata.
4. **Update Catalog**: Add your kit entry to `catalog.json` and the table in `README.md`.
5. **Run Validation**: Run `./validate.sh` to ensure all JSON and YAML schemas pass.
6. **Security Check**: Verify zero hardcoded local paths, zero private keys/tokens, and zero private network addresses.
7. **Submit Pull Request**: Open a pull request describing the domain scope, sources, and verification evidence.

## Share a working project or alternate implementation

You do not need to change the canonical Sherpa Kit to share something you built from it.

1. Pick the matching showcase under `projects/`. Token Piggy Bank builds belong in `projects/token-piggy-bank/`.
2. Copy `projects/PROJECT_TEMPLATE.md` into a new folder named with your project slug, such as `projects/token-piggy-bank/ocean-dashboard/README.md`.
3. Credit the builder, link the source or demo, explain what is different, and state what has actually been tested.
4. Put screenshots in that same folder under `screenshots/`. Remove names, tokens, email addresses, private URLs, account totals, and internal hostnames first.
5. Submit a pull request. If Git is unfamiliar, open a **Share a community project** issue and a maintainer can help turn the submission into a pull request.

Community projects are credited implementations, not endorsements. They stay separate from `kits/`, and they cannot silently replace a canonical Sherpa file.

---

## Style Guidelines

- Use standard GitHub Flavored Markdown.
- Write concise, dense, verifiable operational procedures with executable verification commands.
- Resolve contradictions in-place rather than appending uncurated logs.


---

## Shareable Sherpa filenames

Put directly shareable handoffs in `handoffs/` and name them:

```text
<BriefDescription>.sherpa.md
```

Use a short outcome description, preserve useful acronyms, and make the filename understandable before the file is opened. Examples: `BOMbilling.sherpa.md`, `ComputerGithubSetup.sherpa.md`, and `TokenPiggyBank.sherpa.md`.


---

## Repository map

- `handoffs/`: individually shareable `<BriefDescription>.sherpa.md` files.
- `kits/`: supporting packages and canonical descriptively named `*.sherpa.md` files.
- `projects/`: credited community builds, screenshots, demos, and alternate implementations.
- `scripts/`: maintenance and validation tools.
- `.github/`: automation and project status.

New visitors should be able to find the shareable outcome in `handoffs/` without reading the supporting package first.
