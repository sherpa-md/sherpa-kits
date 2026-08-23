# Implementation checklist
- [ ] Define ledger location and message schema.
- [ ] Implement CLAIM/STATUS/DONE/BLOCKED grammar in the worker wrapper.
- [ ] Add checkpoint file writes after each substep.
- [ ] Add watchdog scan with TTL expiry and retry cap.
- [ ] Add startup recovery: read own unclosed claims, resume or close.
- [ ] Run chaos tests; fill TEST-RESULT-TEMPLATE.md.
