---
status: ai-sourced-untested
source_type: ai-synthesized
testing: not-tested
human_reviewed: false
model: qwen3.8-max
provider: qwen-cloud
risk_level: low
batch: deep-candidates-batch1
---

# Subscription Token Utilization Meter — Measuring and Pacing LLM Quota

## Problem
Modern AI subscriptions grant usage in rolling windows (5-hour sessions,
weekly caps, message counts) but rarely expose a clean usage API. Users either
burn quota early and stall, or hoard it and waste it. Teams running multiple
agents on shared subscriptions have no common view of headroom, so routing
decisions are guesswork. This kit builds a utilization meter: sample usage,
normalize it into one schema, compute percent-left per window, and expose it
to humans and agents.

## Who experiences it
- Anyone on metered AI subscriptions with opaque usage dashboards.
- Fleet operators routing tasks across several provider accounts.
- Budget-minded teams that want burn-rate evidence, not vibes.

## Claims (sourced) vs inference
CLAIM: OpenAI documents rate limits tied to usage tiers and rolling windows
(source: https://platform.openai.com/docs/guides/rate-limits, HTTP 200).
CLAIM: Anthropic documents per-minute/per-day token and request rate limits
(source: https://docs.anthropic.com/en/api/rate-limits, HTTP 200).
CLAIM: OpenTelemetry defines semantic conventions for GenAI telemetry,
including token usage attributes
(source: https://opentelemetry.io/docs/specs/semconv/gen-ai/, HTTP 200).
INFERENCE: A normalized local cache of per-window percent-left plus a change-
detection publisher is sufficient for good routing. Effectiveness must be shown
by the validation plan, not assumed.

## Workflow
1. **Inventory windows**: for each subscription lane list every limit window
   (e.g. 5h, weekly, daily messages). Fill in: `LANE=<name>`
   `WINDOWS=<label,limit,reset-policy>`.
2. **Sampler**: write one script per lane that returns
   `{"ts", "windows": [{"label", "used", "reset"}], "error"}` where `used`
   is percent used (0-100). Prefer provider APIs; where none exist, scrape the
   official dashboard only where the ToS allows, else mark the lane
   `error: no-api` and treat it as informational.
3. **Cache**: write results to a single JSON cache file with a freshness TTL
   (fill in: `CACHE_TTL_MIN=<15>`). Never store credentials in the cache.
4. **Percent-left rule**: percent_left = 100 - used. A lane is usable when
   `error` is empty AND cache age < TTL AND percent_left > threshold
   (fill in: `MIN_PCT=<20>`).
5. **Publisher**: post a compact usage line to your coordination channel when
   any lane moves >=3 points, any lane drops below the threshold, or every
   30 minutes — whichever first. Duplicate suppression: only post when the
   serialized state hash changes.
6. **Router consumption**: any agent picking a lane reads the cache, filters
   by the usable rule, and breaks ties by fit-for-task, not by headroom alone.

## Copy/paste sampler skeleton (fill-in fields marked)
```python
# Lane sampler template — fill in the parts marked FILL
import json, time
def sample():
    # FILL: fetch usage for <LANE> from <API_OR_DASHBOARD>
    used_pct = None   # FILL: compute percent used for window <LABEL>
    reset = None      # FILL: ISO 8601 reset time
    return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "windows": [{"label": "<LABEL>", "used": used_pct, "reset": reset}],
            "error": None}
print(json.dumps(sample()))
```

## Status
**AI-SOURCED / UNTESTED.** No meter built from this kit has been validated
against provider billing; accuracy claims must come from the test report.
