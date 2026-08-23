---
status: ai-sourced-untested
source_type: ai-synthesized
testing: not-tested
human_reviewed: false
model: qwen3.8-max
provider: qwen-cloud
risk_level: medium
batch: deep-candidates-batch1
---

# Parallel Review Swarm Conflict Safety — Multiple Agents Reviewing Without Breaking the Code

## Problem
Running several agents in parallel over one codebase speeds up review but
creates hazards: two agents edit the same file, one agent's fix invalidates
another's findings, or "fixes" pile up uncoordinated and the tree no longer
builds. This kit defines read-only swarm review with conflict-free output:
scoped read-only claims, finding dedup, and a single serial applier.

## Who experiences it
- Teams experimenting with multi-agent code review.
- Orchestrators whose parallel agents overwrite each other.
- Anyone whose "4 agents reviewed the PR" result was 4 conflicting diffs.

## Claims (sourced) vs inference
CLAIM: Git worktrees let multiple checkouts of one repo coexist
(documented by git; general git tooling — see
https://github.com/sherpa-md/sherpa-kits history where branch isolation is
used for exactly this pattern in this repo's own workflow).
CLAIM: In-repo verified fleet kits model claim-based concurrency control
(../../domains/ai-to-ai-bus/AItoAIBus.sherpa.md).
INFERENCE: Read-only parallel review + serial application removes write
conflicts entirely for review workloads. The validation plan tests the claim.

## Workflow
1. **Scope split**: partition the change into disjoint review scopes
   (directory/module). Fill in: `SCOPES=<path list>`. No scope overlaps.
2. **Read-only claims**: each reviewer posts
   `CLAIM task=<id> scope=<path> mode=review` — review mode means NO writes
   to the working tree, no git state changes.
3. **Isolation**: if a reviewer needs to run code, it uses a throwaway branch
   or worktree created for its scope only; never the shared branch.
4. **Findings format**: every finding is
   `{scope, file, line, severity, claim, evidence}`. Claims about behavior
   must carry evidence (test output, doc link) or be labeled INFERENCE.
5. **Dedup + reconcile**: one coordinator merges findings, dedupes
   file+line+topic, and resolves contradictory findings by evidence strength,
   recording why.
6. **Serial apply**: exactly one applier turns accepted findings into edits,
   one scope at a time, running the build/tests between scopes. No parallel
   writes at this stage, ever.
7. **Close-out**: release all claims with DONE + proof (build status, test
   output).

## Copy/paste finding record (fill-in)
```json
{"scope": "<PATH>", "file": "<FILE>", "line": 0,
 "severity": "<blocker|major|minor|nit>",
 "claim": "<WHAT IS WRONG>",
 "evidence": "<OUTPUT OR LINK>",
 "label": "<CLAIM|INFERENCE>"}
```

## Status
**AI-SOURCED / UNTESTED.** Conflict-elimination is designed-in but not yet
measured under real parallel load.
