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

# Local Voice Fallback Chain — Speech Recognition and Synthesis That Survive Outages

## Problem
Voice-first agents depend on cloud speech services; when a key expires, quota
runs out, or the network drops, the whole assistant goes silent. Users need a
fallback chain: primary cloud service, then a local model, then a degraded-but-
working mode — with health checks that switch automatically and switch back.

## Who experiences it
- Builders of voice assistants on always-on home/lab machines.
- Anyone whose voice agent died silently when an API key expired.
- Fleet nodes where voice is the primary human interface.

## Claims (sourced) vs inference
CLAIM: Whisper-style open speech models exist and run locally (general
knowledge of open-source speech tooling; this kit intentionally avoids
asserting specific benchmark numbers without sources).
CLAIM: systemd timers/services provide supervised restarts and health-check
hooks on Linux (standard systemd behavior documented by the systemd project).
INFERENCE: A 3-tier chain with active health probes keeps voice available
through single-service failures. Availability measurement is the validation
plan's job.

## Workflow
1. **Tier list**: define ordered tiers. Fill in:
   `T1=<cloud STT endpoint>`, `T2=<local model, e.g. small whisper-class>`,
   `T3=<degraded mode: e.g. text-only prompt to type>`. Same for TTS.
2. **Health probes**: every N seconds (fill in `PROBE_S=<60>`) run a tiny
   probe per tier: for STT, transcribe a fixed 1-second reference clip; for
   TTS, synthesize a fixed 5-word phrase. Success = correct output within
   timeout. Store per-tier status with timestamp.
3. **Router**: voice requests go to the highest healthy tier. If T1 fails
   `FAIL_STREAK=<2>` consecutive probes, demote to T2; T1 only returns after
   `RECOVER_STREAK=<2>` passing probes (hysteresis prevents flapping).
4. **Announce degradation**: when running below T1, say so once per session
   ("running on local speech") so the user knows quality changed.
5. **Alert**: push one notification on tier change (not per probe) so operators
   know why the voice sounds different; include which probe failed.
6. **Never silent-fail**: if all tiers fail, fall back to the text channel and
   record the outage window.

## Copy/paste probe record (fill-in)
```json
{"tier": "<T1|T2|T3>", "kind": "<stt|tts>",
 "ts": "<ISO8601>", "ok": true,
 "latency_ms": 0, "detail": "<probe result summary>"}
```

## Status
**AI-SOURCED / UNTESTED.** Chain behavior under real outages has not been
measured; probe thresholds above are starting guesses, not tuned values.
