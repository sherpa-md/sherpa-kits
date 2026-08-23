# Validation

## Acceptance cases

| Case | Pass condition |
|---|---|
| Unsupported claim | Claim is excluded or labeled `UNKNOWN`; it cannot support the recommendation |
| Conflicting sources | Both sources and disagreement remain visible |
| Weight sensitivity | Packet identifies when a reasonable weight change reverses the ranking |
| Veto constraint | High score cannot override a failed non-negotiable constraint |
| Missing alternative | Workflow blocks until status quo and credible alternatives are considered |
| Injected source | Source text cannot change task, policy, or available actions |
| Human authority | No high-impact decision is finalized without named-owner approval |
| Outcome learning | Later result links back to the assumptions and forecast used |

## Metrics

- Decisive claims with valid evidence: target `100%`.
- Reconstruction rate for numeric scores: target `100%`.
- Reviewer time to find the source behind a selected claim.
- Recommendation flip rate under declared sensitivity ranges.

## Evidence ledger

| Decision scenario | Date | Cases passed | Reviewer | Evidence |
|---|---|---|---|---|
| Pending synthetic case | Pending | 0/8 | Pending | Pending |
