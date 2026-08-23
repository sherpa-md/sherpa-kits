# Implementation checklist
- [ ] Build eval set (10-30 items) with rules per item.
- [ ] Implement runner + scorer with evidence excerpts.
- [ ] Snapshot storage layout with model + prompt hash in name.
- [ ] Pin baseline; implement gate comparison.
- [ ] Wire gate into the promotion path (manual or CI).
- [ ] Seed one intentional regression to prove the gate trips.
