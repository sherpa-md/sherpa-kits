# Validation plan
1. Baseline: measure T1 latency/accuracy on the reference clip (10 runs).
2. Failover drill: disable T1 (block endpoint); confirm demotion to T2 within
   FAIL_STREAK probes and that voice keeps working on T2.
3. Recovery drill: restore T1; confirm switch-back only after RECOVER_STREAK
   passes and no flapping over 10 minutes.
4. Total-failure drill: disable T1+T2; confirm text fallback engages and the
   outage window is logged.
5. Record: downtime seconds per drill, false-switch count (target 0).
