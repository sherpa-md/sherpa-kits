# Completion Checklist

## Sanitization

- [ ] No credentials, private keys, tokens, cookies, or recovery codes.
- [ ] No personal home-directory paths.
- [ ] No private IP addresses or internal hostnames.
- [ ] No sender-specific machine topology.
- [ ] Unknown optional settings are `NOT_CONFIGURED`.

## Capability verification

- [ ] Relevant tools and connectors were discovered before any availability claim.
- [ ] GitHub access was tested through the GitHub interface, not inferred from local Git state.
- [ ] Read and write capabilities were reported separately.
- [ ] Authentication and permission failures were distinguished.
- [ ] The receipt names the tested interface and sanitized target.

## Workspace safety

- [ ] Existing files and uncommitted changes were preserved.
- [ ] No destructive reset, deletion, overwrite, or force push occurred.
- [ ] Repository validation commands passed or failures were reported.
- [ ] First write uses the requested branch/PR policy.

## Optional coordination

- [ ] Bus values belong to the recipient.
- [ ] Messaging permission is distinct from execution permission.
- [ ] Remote execution remains disabled unless explicitly enabled.
- [ ] Message lifecycle receipts are visible.

