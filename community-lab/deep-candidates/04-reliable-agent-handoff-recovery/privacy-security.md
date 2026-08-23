# Privacy & security notes
- Ledgers and checkpoints must not contain secrets; redact before writing.
- Claim scope strings must not leak credentials or customer identifiers.
- Watchdog re-queue must preserve approvals: a task that needed human
  approval re-queues as NEEDS-APPROVAL, never auto-approved.
- Keep artifact dirs user-private (0700) when they hold task context.
