# Validation

## Acceptance cases

| Case | Pass condition |
|---|---|
| Baseline immutability | A revision creates a new version and does not rewrite the original |
| Timezone boundary | Cross-timezone events reconcile to the correct instant and retain source timezone |
| Late event | A delayed event invalidates and recomputes affected summaries |
| Ambiguous join | The system requests review instead of silently choosing a match |
| Unit mismatch | Conversion is explicit or calculation stops |
| Causal restraint | Correlated factors are labeled hypotheses, with disconfirming evidence requested |
| Reproducibility | Independent code reproduces every published variance |
| Permission boundary | Reviewer sees only sources they are permitted to inspect |

## Metrics

- Correct mapping rate and ambiguous-match rate.
- Numeric reproduction rate: target `100%` for published metrics.
- Time-to-explain a selected variance compared with current manual work.
- Reviewer rejection rate for hypotheses.

## Evidence ledger

| Scenario | Dataset | Date | Result | Reviewer | Evidence |
|---|---|---|---|---|---|
| Pending | Synthetic | Pending | Unverified | Pending | Pending |
