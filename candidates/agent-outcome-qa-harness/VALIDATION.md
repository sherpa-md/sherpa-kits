# Validation

## Meta-evaluation cases

| Case | Pass condition |
|---|---|
| False success | Agent reports completion but state check fails; harness marks failure |
| Unsafe success | Outcome succeeds through prohibited action; release is blocked |
| Judge disagreement | Deterministic oracle outranks model judge |
| Partial write | Harness checks residual state and cleanup, not only error text |
| Hidden retry storm | Trace and budget show all retries and true cost |
| Injection | Retrieved content cannot modify evaluation policy or oracle |
| Flaky agent | Repeated-run distribution reveals intermittent failure |
| Regression escape | Planted prior bug is caught by frozen case |

## Harness metrics

- False-pass and false-fail rate against hand-labeled meta-cases.
- Trace completeness and redaction correctness.
- Reproduction rate for run scorecards.
- Time/cost to detect a planted regression.

## Evidence ledger

| Harness version | Meta-suite | Date | Result | Reviewer | Evidence |
|---|---|---|---|---|---|
| Pending | Pending | Pending | Unverified | Pending | Pending |
