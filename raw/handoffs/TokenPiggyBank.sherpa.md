# Token Piggy Bank — Sherpa

> Give this single file to a capable coding/operations AI and say: **“Install this on my system.”**
>
> Designed for Claude, OpenAI/Codex, Gemini, Qwen, Kimi, DeepSeek, local coding agents, OpenAI-compatible endpoints, and future LLMs.

## EXECUTION DIRECTIVE

Install a **Token Piggy Bank**: a vendor-neutral quota, budget, routing, and value governor for one or more LLM providers.

**Do the work. Do not return only a design or tutorial.**

Your job is to:

1. safely inventory the existing AI system;
2. discover providers, models, workers, orchestration, logs, databases, and quota/status interfaces;
3. reuse existing components instead of building competing infrastructure;
4. implement normalized provider/resource snapshots;
5. calculate burn rate, reset pacing, reserve, projected exhaustion, and surplus;
6. implement vendor-neutral adapters;
7. prevent retry storms and accidental overspend;
8. record task outcomes so useful work—not raw token burn—is optimized;
9. expose an appropriate read-only API/dashboard;
10. test the implementation;
11. return proof of what was installed and what remains unknown.

Do not ask routine questions that can be resolved by inspection. Use safe defaults. If something cannot be verified, label it honestly and continue.

---

# 1. NON-NEGOTIABLE RULES

## Never invent quota data

Every measurement must carry one of:

```text
VERIFIED
ESTIMATED
STALE
UNKNOWN
```

Rules:

```text
missing data != zero
parser failure != zero
collector failure != provider exhaustion
unknown quota != unlimited quota
```

Use `ESTIMATED` only when derived from defensible local history. Otherwise use `UNKNOWN`.

## Never expose secrets

Never print, persist, commit, return, or expose API keys, OAuth tokens, cookies, passwords, private keys, B3AR3R_MARK tokens, session secrets, or credential files.

Reuse existing authentication. Sanitize provider output **before persistence**. Mask identities where possible.

## Never silently enable paid fallback

Do not buy credits, change subscriptions, create paid resources, enable metered fallback, or raise spending limits unless already explicitly authorized.

Default:

```yaml
paid_fallback:
  enabled: false
```

## Do not create a competing orchestrator

Reuse existing provider adapters, routing, task queues, databases, dashboards, model registries, request ledgers, and health checks where practical.

## Do not burn tokens to measure tokens

Prefer provider-native status/usage interfaces, APIs, CLIs, local ledgers, or request metadata. Do not send meaningless prompts just to consume or inspect capacity.

## Preserve productive work

Do not interrupt healthy jobs just to install this. Apply policy to new work first and alter active jobs only at safe checkpoints.

---

# 2. SUCCESS TARGET

Optimize for:

> **MAXIMUM VERIFIED USEFUL WORK COMPLETED PER RESOURCE WINDOW**

Do not optimize primarily for raw token consumption, maximum model size, maximum concurrency, fastest single answer, or always using premium models.

---

# 3. READ-ONLY DISCOVERY FIRST

Before modifying anything, inventory:

## Providers / models
- configured providers;
- active models;
- local models;
- subscriptions;
- metered APIs;
- OpenAI-compatible endpoints;
- model aliases;
- existing routing tiers.

## Status / quota interfaces
Discover provider-supported mechanisms such as status, usage, quota, billing APIs, CLI status commands, or local account telemetry. Do not assume exact command names.

## Existing orchestration
Find:
- provider adapters;
- router/load balancer;
- worker registry;
- task queue;
- retry logic;
- request middleware/proxy;
- model-selection rules;
- token/cost accounting.

## Existing storage
Find:
- SQLite/Postgres/MySQL;
- JSONL/event logs;
- metrics;
- task ledgers;
- cached provider state.

## Existing web/API surfaces
Find dashboards, FastAPI/Flask/Express apps, admin/status APIs, or monitoring pages.

## Existing schedulers
Find systemd, cron, containers, Kubernetes, or application schedulers.

Create an internal inventory, then choose the least invasive implementation.

---

# 4. DEPLOYMENT MODE

Choose one:

### A — Read-only monitor
Human chooses providers/models. Piggy Bank reports and recommends.

### B — Sidecar governor
Existing orchestrator queries Piggy Bank for routing/policy and reports outcomes back.

### C — Embedded governor
Piggy Bank forecasting/policy is integrated into the existing router.

Prefer B or C when a real orchestrator already exists.

---

# 5. VENDOR-NEUTRAL ADAPTER CONTRACT

Do not hard-code the governor around one LLM vendor.

Conceptual interface:

```python
class ProviderAdapter:
    provider_id: str

    def collect_status(self) -> dict:
        # Collect non-work status/quota information.
        ...

    def normalize(self, raw: dict) -> dict:
        # Map provider-specific telemetry into the common schema.
        ...

    def sanitize(self, raw: dict) -> dict:
        # Remove secrets and unnecessary identity information.
        ...

    def healthcheck(self) -> dict:
        # Provider/collector health independent of quota.
        ...

    def usage_from_local_history(self) -> dict:
        # Optional fallback if native quota telemetry is unavailable.
        ...
```

Supported collection patterns may include:

```text
provider-native API
provider CLI status
controlled interactive CLI / PTY
local request ledger
reverse proxy / middleware telemetry
manual verified limit configuration
OpenAI-compatible metadata
local runtime metrics
```

Adapters must fail independently. One broken provider must not break the entire Piggy Bank.

---

# 6. MULTI-LLM BEHAVIOR

The same governor must work with:

- OpenAI / Codex;
- Anthropic / Claude;
- Google Gemini;
- Alibaba Qwen / Model Studio;
- Moonshot / Kimi;
- DeepSeek;
- OpenAI-compatible hosted endpoints;
- vLLM;
- Ollama;
- LM Studio;
- other local runtimes;
- future providers.

Do not require identical telemetry.

### Native quota available
Use it. Mark authoritative fields `VERIFIED`.

### Per-request tokens/cost only
Build local usage history. Provider-limit projections remain `ESTIMATED` unless the total limit/reset is verified.

### Local model with no subscription quota
Track meaningful finite resources if useful: concurrency, context, GPU time, operator-defined budget, or rate limits. Do not pretend it has a subscription quota.

### Unknown provider limit
Keep health, task outcomes, model tier, retry control, and observed usage. Leave remaining/reset `UNKNOWN`.

---

# 7. NORMALIZED SNAPSHOT

Use an equivalent common shape:

```json
{
  "provider_id": "provider_a",
  "collected_at": "2026-08-21T20:00:00-05:00",
  "source": "provider_native_status",
  "confidence": "VERIFIED",
  "health": "HEALTHY",
  "active_model": "example-model",
  "account_alias": "acct-***42",
  "active_jobs": 2,
  "windows": [
    {
      "id": "weekly",
      "kind": "weekly",
      "used_percent": 37.0,
      "remaining_percent": 63.0,
      "window_started_at": "2026-08-17T04:00:00-05:00",
      "reset_at": "2026-08-24T04:00:00-05:00",
      "shared_quota": true,
      "shared_models": ["model-a", "model-b"],
      "confidence": "VERIFIED"
    }
  ],
  "last_error": null
}
```

Recommended health states:

```text
HEALTHY
WARNING
RATE_LIMITED
EXHAUSTED
AUTH_FAILED
OUTAGE
STALE
UNKNOWN
```

---

# 8. TRACK INDEPENDENT RESOURCE WINDOWS

Keep independent limits separate:

```text
context
session
rolling
five-hour
daily
weekly
model-specific weekly
monthly
promotional
credit
API dollar budget
request-rate window
```

For each known window show:

```text
USED
AVAILABLE
RESET
```

When models share a quota pool, explicitly mark:

```text
SHARED QUOTA
```

Do not double-count shared pools.

---

# 9. STORAGE

Reuse existing durable storage when suitable. Otherwise SQLite is an acceptable default.

Minimum conceptual records:

```text
provider_snapshot
quota_window_snapshot
task_run
routing_event
harvest_task
```

For each task record, where observable:

```text
task_id
worker/agent
provider
model
logical_model_tier
task_category
selection_reason
start/end time
success/failure
verification result
retry count
escalation count
input/output/cache tokens
estimated/verified cost
quota before/after
result artifact/commit/reference
```

Do not persist unsanitized provider output by default.

---

# 10. CORE FORECASTING MATH

## Burn ratio

```text
usage_fraction = used_percent / 100
time_fraction  = elapsed_window_time / total_window_time
burn_ratio     = usage_fraction / time_fraction
```

If required timestamps are unknown, do not fabricate a ratio.

## Burn classification

```text
< 0.70          UNDERUSING
0.70 – 1.10     ON PACE
>1.10 – 1.50    ELEVATED BURN
>1.50 – 2.00    WILL EXHAUST EARLY
>2.00           CRITICAL
```

Keep thresholds configurable.

## Recent verified consumption rate

```text
recent_rate_percent_per_hour =
    change_in_used_percent / elapsed_hours
```

Prefer several recent verified samples.

## Projected exhaustion

```text
hours_until_exhausted =
    remaining_percent / recent_rate_percent_per_hour

projected_exhaustion_at =
    now + hours_until_exhausted
```

## Protected reserve

Default:

```yaml
reserve_percent: 25
```

Recommended initial range: **20–25%**.

```text
spendable_remaining =
    max(0, remaining_percent - reserve_percent)
```

Reserve is for failures, difficult debugging, human-critical work, final verification, and independent review.

## Safe allowance

```text
safe_percent_per_hour =
    spendable_remaining / hours_until_reset
```

## Projected unused capacity

```text
projected_additional_use =
    recent_rate_percent_per_hour * hours_until_reset

projected_used_at_reset =
    current_used_percent + projected_additional_use

projected_unused_at_reset =
    max(0, 100 - projected_used_at_reset)

safe_surplus_percent =
    max(0, projected_unused_at_reset - reserve_percent)
```

Clamp percentages.

---

# 11. SURPLUS STATES

Use:

```text
NO SURPLUS
POSSIBLE SURPLUS
SAFE SURPLUS
USE BEFORE RESET
UNKNOWN
```

Only use `USE BEFORE RESET` when:
- reset time is verified or strongly estimated;
- usable capacity exceeds reserve;
- recent burn predicts meaningful unused capacity;
- provider is healthy;
- no retry storm exists;
- useful approved backlog work exists.

---

# 12. LOGICAL MODEL TIERS

Map each vendor's models into configurable logical tiers.

### Tier 1 — Economy
File discovery, retrieval, formatting, summaries, docs, logs, inventory, basic tests, routine validation, repetitive transforms, low-risk edits.

### Tier 2 — Balanced
Normal coding, debugging, integration, test repair, refactoring, multi-file implementation, moderate reasoning.

### Tier 3 — Premium
Architecture, difficult root cause, security-sensitive review, ambiguous failures, high-risk changes, final verification, independent review, or lower-tier failures with evidence.

Do not derive the mapping solely from marketing names.

---

# 13. QUOTA-AWARE ROUTING

### 70–100% remaining
Economy/balanced allowed. Premium when justified. Protect reserve. Controlled parallelism if burn is safe.

### 40–70%
Prefer economy for routine work. Balanced available. Premium requires stronger reason. Reduce unnecessary parallelism.

### 20–40%
Economy default. Balanced only for blocking work. Premium only for urgent diagnosis/final review. Route elsewhere when practical.

### Under 20%
Preserve for emergencies/final review. No routine work. Prefer another healthy provider.

### Exhausted/rate limited
Stop new work on that provider. Preserve job state. Record exact error/reset. Do not retry-loop. Continue on healthy providers.

Routing inputs should include provider health, remaining quota, reset, burn ratio, surplus state, active jobs, failure/retry rate, task capability, logical tier, context size, observed success, review independence, and cost.

Return:

```text
1. RECOMMENDED
2. ACCEPTABLE FALLBACK
3. PRESERVE FOR REVIEW
4. DO NOT USE
```

---

# 14. PARALLELISM DEFAULTS

Per shared provider pool:

```text
premium:  max 1 concurrent job
balanced: max 2 concurrent jobs
economy:  dynamic while burn remains safe
```

If multiple machines/agents share an account, they must report into shared quota state or they can unknowingly saturate the same pool.

---

# 15. RETRY-STORM PROTECTION

Defaults:

```text
same model + same prompt:        1 retry
same provider + corrected input: 1 additional attempt
max provider attempts:           3
```

Stop normal retries immediately for quota exhaustion, billing/credit failure, auth failure, invalid credentials/session, provider outage, hard quota limit, or repeated HTTP 429 without a valid retry/reset strategy.

Record, preserve state, diagnose, then reroute only when justified.

---

# 16. USEFUL SURPLUS HARVESTING

Good surplus work:

```text
documentation cleanup
repository indexing
test generation
bounded test repair
log summarization
duplicate detection
dead-code review
dependency inventory
README/changelog improvements
issue classification
non-destructive security review
independent review
knowledge-base cleanup
regression tests
retrieval/cache optimization
investigation of repeated failures
```

Never use surplus for meaningless prompts, synthetic conversations solely to consume quota, repeated summaries of unchanged files, duplicate agents, uncontrolled rewrites, retry storms, model upgrades solely to burn quota, or unauthorized paid calls.

Every harvest job records:

```text
task ID
project
category
provider
tier
estimated quota impact
reason useful
verification method
deadline before reset
status
result
success/failure
```

---

# 17. TASK VALUE LEDGER

Primary metric:

> **verified useful tasks completed per quota window**

Useful secondary metrics:

```text
cost per verified task
tokens per verified task
retry rate
escalation rate
failure rate
idle time due to exhaustion
tokens avoided by cache/retrieval
duplicate/rework rate
```

---

# 18. READ-ONLY API / DASHBOARD

Reuse an existing monitoring surface if practical. Otherwise build the smallest safe surface.

Suggested API:

```text
GET  /api/summary
GET  /api/providers
GET  /api/providers/{provider_id}
GET  /api/tasks/recent
GET  /api/routing/recommendation
GET  /api/surplus
GET  /api/harvest-queue
POST /api/refresh
```

Protect write/action endpoints appropriately.

Top summary should show:
- usable/warning/rate-limited/exhausted providers;
- nearest reset;
- last refresh;
- collector health;
- stale-data warning;
- best routine/difficult-work provider;
- provider preserved for review;
- active jobs;
- surplus opportunities.

Each provider card should show:
- provider/model;
- health;
- every quota/resource window;
- used + available;
- reset timestamp/countdown;
- source;
- confidence/freshness;
- burn classification;
- projected exhaustion;
- safe allowance;
- reserve;
- active jobs;
- retries;
- routing recommendation.

---

# 19. REFRESH DEFAULTS

```yaml
refresh_seconds: 300
stale_after_seconds: 900
```

Provider-native polling every ~5 minutes and stale warning after ~15 minutes is a safe starting point. Local request telemetry can update faster.

---

# 20. DEFAULT CONFIG

```yaml
piggybank:
  refresh_seconds: 300
  stale_after_seconds: 900
  reserve_percent: 25

  paid_fallback:
    enabled: false

  retry_policy:
    same_prompt_retries: 1
    corrected_prompt_retries: 1
    max_provider_attempts_per_failure: 3

  parallelism:
    premium_per_shared_pool: 1
    balanced_per_shared_pool: 2
    economy_dynamic: true

providers:
  # Discover and populate from the existing system.
  # Never put credentials here.
```

---

# 21. NO NATIVE QUOTA? CONTINUE ANYWAY

Fallback evidence hierarchy:

```text
1. provider-native quota/status
2. provider billing/usage API
3. local proxy/request metadata
4. orchestrator task/token ledger
5. CLI/session token totals
6. manually configured verified limit/reset
7. observed local history
8. UNKNOWN
```

Do not fake percent remaining.

A provider with unknown total quota can still participate in health, cost, task-outcome learning, tier routing, retry control, and concurrency management.

---

# 22. CONTEXT EFFICIENCY

Use:

```text
search
  ↓
retrieve relevant state only
  ↓
compress
  ↓
cheapest adequate model
  ↓
work
  ↓
verify
  ↓
store durable result
```

Avoid repeated full repositories, long histories, duplicate tool output, huge unfiltered logs, and several workers rediscovering the same facts.

---

# 23. OPERATIONS / SECURITY

Use the host's existing process manager: systemd, Docker, Kubernetes, supervisor, cron, or app scheduler.

Require:
- least privilege;
- read-only dashboard by default;
- allowlisted collector commands;
- bounded timeouts;
- sanitization before storage;
- masked identities;
- no credentials in HTML/JSON/logs;
- authentication/TLS beyond trusted localhost/private networks;
- no accidental public exposure.

---

# 24. REQUIRED ACCEPTANCE TESTS

Do not call the implementation complete until evaluated.

## Collection
- [ ] Every configured provider is represented.
- [ ] One failed collector does not break others.
- [ ] Collector timeout cannot hang the system.
- [ ] Parser failure becomes `UNKNOWN`/`STALE`, never zero.

## Correctness
- [ ] Verified values are `VERIFIED`.
- [ ] Estimates are visibly `ESTIMATED`.
- [ ] Unknowns do not appear as zero.
- [ ] Used/available values are internally consistent.
- [ ] Independent windows remain independent.
- [ ] Shared pools are not double-counted.
- [ ] Reset timestamp/countdown agrees.

## Forecasting
- [ ] Burn math passes boundary tests.
- [ ] Zero elapsed time is safe.
- [ ] Projected exhaustion works on known sample data.
- [ ] Reserve boundary is correct.
- [ ] Safe allowance is correct.
- [ ] Surplus preserves reserve.

## Routing / retries
- [ ] Lower quota downgrades/reroutes routine work.
- [ ] Premium capacity can be preserved for review.
- [ ] Exhausted provider gets no new work.
- [ ] Retry storms stop at configured limits.
- [ ] Auth/billing/quota failures do not loop.

## Value
- [ ] Task success/failure is recordable.
- [ ] Verification result is recordable.
- [ ] Provider/model/tier are recorded.
- [ ] Tokens/cost are recorded when observable.
- [ ] Quota before/after can be associated with tasks.

## Security
- [ ] No API keys committed.
- [ ] No secrets in HTML.
- [ ] No secrets in JSON.
- [ ] No secrets in logs.
- [ ] No raw secret-bearing provider output persisted.
- [ ] Paid fallback remains disabled unless explicitly authorized.

## Operations
- [ ] Process/service starts.
- [ ] Refresh works.
- [ ] Restart behavior is appropriate.
- [ ] Existing tests still pass.
- [ ] Existing productive work remains intact.

Burn boundary tests:

```text
0.69 -> UNDERUSING
0.70 -> ON PACE
1.10 -> ON PACE
1.11 -> ELEVATED BURN
1.50 -> ELEVATED BURN
1.51 -> WILL EXHAUST EARLY
2.00 -> WILL EXHAUST EARLY
2.01 -> CRITICAL
unknown -> UNKNOWN
```

---

# 25. IMPLEMENT IN THIS ORDER

```text
1. READ-ONLY INVENTORY
2. REUSE EXISTING STATE/ADAPTERS
3. NORMALIZED PROVIDER SNAPSHOTS
4. DURABLE SNAPSHOT HISTORY
5. CONFIDENCE + FRESHNESS
6. RESET COUNTDOWNS
7. BURN / FORECAST ENGINE
8. RESERVE POLICY
9. READ-ONLY API/DASHBOARD
10. RETRY-STORM PROTECTION
11. TASK OUTCOME LEDGER
12. ROUTING RECOMMENDATIONS
13. SHARED-QUOTA AWARENESS
14. SURPLUS CLASSIFICATION
15. USEFUL HARVEST QUEUE
16. ACCEPTANCE TESTS
17. FINAL PROOF REPORT
```

Keep the smallest useful version working as you add later stages.

---

# 26. REQUIRED FINAL REPORT

Return:

```text
STATUS
- complete / partial
- exact reason for anything incomplete

INSTALLATION
- module/project path
- services/processes added or changed
- storage/database used
- migrations
- dashboard/API location
- refresh cadence

PROVIDERS
For each provider:
- provider
- model(s)
- collection method
- native quota available? yes/no
- confidence
- resource windows
- reset information
- burn state
- routing state

MULTI-LLM SUPPORT
- adapters implemented
- discovered unsupported providers
- exact reason for any unsupported provider

SAFETY
- paid fallback enabled? (expected no unless pre-authorized)
- secret leakage? (expected no)
- retry-storm controls active?
- reserve configured?

VERIFICATION
- tests run
- passed
- failed
- remaining unknowns
- proof API/dashboard responds

CHANGES
- files created/modified
- commit SHA if source control exists
- commands to inspect/restart/disable Piggy Bank
```

Never claim `VERIFIED` for an untested item.

---

# 27. DEFINITION OF DONE

The Sherpa setup is complete when:

1. providers are enumerated;
2. provider collectors fail independently;
3. resource windows use one normalized schema;
4. unknown values remain honest;
5. burn/reset/reserve forecasting works where data permits;
6. the operator can see used, available, reset, confidence, and health;
7. routing can recommend a provider/model tier;
8. retry storms are bounded;
9. task outcomes can be measured;
10. no secret leakage or unauthorized paid fallback was introduced;
11. acceptance tests were run;
12. concrete proof was returned.

Advanced automatic routing/harvesting may remain advisory if the host cannot safely enforce it yet; state why.

---

# 28. OPTIONAL COMPANION

For additional detail, use the canonical supporting [`TokenPiggyBank.sherpa.md`](../kits/token-piggy-bank/TokenPiggyBank.sherpa.md) file.

**Do not stop if it is absent. This Sherpa file is self-contained.**

---

# 29. START NOW

Begin with read-only discovery.

Then implement, test, and verify.

Do not return merely a proposal.

Do not invent missing quota data.

Do not expose credentials.

Do not silently spend money.

**Fit the Token Piggy Bank to the system you actually find.**
