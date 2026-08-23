# Validation plan
1. Baseline: run 10 synthetic tasks with no recovery machinery; kill 3 workers
   mid-task; count lost and duplicated executions.
2. Enable the kit: rerun the same 10-task/3-kill scenario.
3. Success criteria: 0 lost tasks (all resumed or re-queued), 0 duplicate
   executions (claim isolation), stale claims expired within TTL + scan period.
4. Restart test: kill a worker after its first checkpoint; verify it resumes
   from checkpoint, not from zero.
5. Double-claim test: two workers attempt the same task; exactly one CLAIM
   accepted.
Record results in the community test result template.
