# Privacy & security notes
- This kit handles the boundary, not legal compliance: get employer sign-off
  before using real internal data anywhere.
- The placeholder token map is itself sensitive; keep it local, never send it.
- Audit ledger stores hashes + classes only, never prompt text.
- Treat model output as untrusted when it feeds automation (injection risk).
- Never test with real customer PII; synthetic data only.
