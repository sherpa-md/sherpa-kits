# Validation plan
1. Run samplers for >=2 lanes for 48h; record cache writes.
2. Cross-check reported `used` against the provider dashboard at 5 timestamps;
   deviation >5 points = Fail for that sampler.
3. Verify staleness handling: stop a sampler; confirm the cache is flagged
   STALE after TTL and no lane is routed as usable.
4. Verify publisher posts only on change/heartbeat (count posts vs state
   changes).
5. Simulate exhaustion: force one lane to 95%+ used; confirm router skips it.
Record Pass/Partial/Fail per step.
