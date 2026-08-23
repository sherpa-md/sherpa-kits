# Validation

## Policy matrix

Create synthetic requests across every supported data class, purpose, modality, action, and destination. Record expected allow/deny route before execution.

## Acceptance cases

| Case | Pass condition |
|---|---|
| Restricted data | Routes only to the explicitly approved restricted-data profile |
| Empty intersection | Returns `BLOCKED_POLICY`; no payload is sent |
| Provider outage | Does not fall back to an unapproved provider |
| Classification conflict | Highest applicable restriction remains until authorized review |
| Prompt injection | Content cannot change route, policy, destination, or tool scope |
| Excessive tool request | Deterministic authorization denies the extra capability |
| Model alias change | Unpinned or newly mapped model is blocked pending evaluation |
| Receipt | Route and policy decision can be audited without logging sensitive payloads |

## Metrics

- Unauthorized route count: target `0`.
- Policy false-allow rate: target `0` in the labeled matrix.
- Denial and routing latency.
- Payload reduction achieved through minimization.
- Quality/cost performance only within the allowed route set.

## Evidence ledger

| Registry version | Matrix version | Date | Result | Reviewer | Evidence |
|---|---|---|---|---|---|
| Pending | Pending | Pending | Unverified | Pending | Pending |
