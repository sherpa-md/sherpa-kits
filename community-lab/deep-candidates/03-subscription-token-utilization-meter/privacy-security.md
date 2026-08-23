# Privacy & security notes
- The cache must never contain API keys, session cookies, or OAuth tokens —
  only usage numbers and timestamps.
- Sampler credentials stay in a local secret file (0600) outside the repo.
- If a dashboard must be read with a logged-in session, confirm the ToS
  permits it and keep the session local to one machine.
- Usage lines posted to shared channels must not leak account identity.
