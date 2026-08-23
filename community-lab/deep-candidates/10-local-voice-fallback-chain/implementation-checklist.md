# Implementation checklist
- [ ] Define tiers for STT and TTS with reference probe assets.
- [ ] Implement probe loop as a supervised service/timer.
- [ ] Implement health state store with streak counters.
- [ ] Implement router with hysteresis constants.
- [ ] Add degradation announcement + tier-change alerting.
- [ ] Add text-channel last resort.
- [ ] Run outage drills; fill TEST-RESULT-TEMPLATE.md.
