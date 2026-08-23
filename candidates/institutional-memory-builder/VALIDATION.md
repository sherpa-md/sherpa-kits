# Validation

## Acceptance cases

| Case | Pass condition |
|---|---|
| Permission split | Users with different ACLs receive appropriately different evidence |
| Revocation | Removed access stops retrieval within measured sync objective |
| Superseded policy | Old version remains traceable but is not presented as current |
| Contradiction | Conflicting active claims are shown and routed to an owner |
| Ambiguous identity | Similar names are not silently merged |
| Meeting rumor | Unapproved summary does not outrank the system of record |
| Source deletion | Content no longer surfaces; permitted tombstone/provenance remains |
| Unsupported answer | System returns `UNKNOWN` rather than a plausible invention |

## Metrics

- Unauthorized retrieval count: target `0`.
- Grounded-answer precision and citation support rate.
- Stale-claim detection lag.
- Steward correction and merge rates.
- Median time to locate the authoritative source.

## Evidence ledger

| Corpus | Date | Cases passed | Reviewer | Evidence |
|---|---|---|---|---|
| Pending | Pending | 0/8 | Pending | Pending |
