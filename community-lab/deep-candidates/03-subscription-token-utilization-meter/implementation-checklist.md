# Implementation checklist
- [ ] List lanes and windows; document reset policies.
- [ ] Implement one sampler per lane returning the standard JSON shape.
- [ ] Wire cache file with TTL and freshness check.
- [ ] Implement percent-left + usability rule.
- [ ] Add change-detection publisher with 30-min heartbeat.
- [ ] Integrate one real routing decision against the cache.
- [ ] Run validation plan; fill TEST-RESULT-TEMPLATE.md.
