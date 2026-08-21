# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security and integrity of SherpaMD and all associated domain kits seriously.

If you discover a security vulnerability, credential leak, or sensitive information exposure within this repository, please report it responsibly:

- **Do NOT** open a public issue on GitHub.
- Submit a private security report through GitHub Security Advisories or contact repository maintainers.
- Provide a detailed summary of the vulnerability, reproduction steps, affected files, and potential impact.

Maintainers will acknowledge receipt within 48 hours and work on remediation and disclosure.

## Security & Secret Hygiene Directives

All contributors and automated agents must adhere to the following security principles:
1. **Zero Secrets in Repository**: Never commit API keys, auth tokens, private keys, session cookies, passwords, or personal credentials.
2. **Path Sanitization**: Never commit absolute local filesystem paths containing personal usernames (e.g. `/home/<username>/`). Use environment variables or relative repository paths.
3. **Infrastructure Abstraction**: Abstract private IP addresses, private ports, VPN hostnames, and internal infrastructure topologies into generic role archetypes.
4. **Validation**: Run `./validate.sh` and security linters before committing any domain kit or source document.
