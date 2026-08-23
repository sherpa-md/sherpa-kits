# Validation

## Acceptance cases

| Case | Pass condition |
|---|---|
| Rotated/poor scan | Low-quality fields route to review with correct source region |
| Arithmetic mismatch | Deterministic validation catches inconsistent subtotal/tax/total |
| Consequential field | Review occurs regardless of high model confidence |
| Duplicate | Repeated document does not create a second finalized record |
| Embedded instruction | Content cannot select tools, destination, or approval |
| Model disagreement | Value remains pending and alternatives are visible |
| Partial write failure | Retry is idempotent or rollback leaves a clear state |
| Lineage | Filed field traces to original pixels, correction, reviewer, and rule version |

## Metrics

- Field precision/recall by document and field type.
- False-accept rate for consequential fields: target `0` in validation.
- Reviewer correction rate and review time.
- Duplicate and idempotency failure count.
- Straight-through rate only after safety metrics pass.

## Evidence ledger

| Corpus | Sandbox destination | Date | Result | Reviewer | Evidence |
|---|---|---|---|---|---|
| Pending | Pending | Pending | Unverified | Pending | Pending |
