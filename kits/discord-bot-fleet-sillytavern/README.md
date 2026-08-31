# Discord Bot Fleet & SillyTavern Voice Bridge Kit

A portable, live-tested architecture for operating multiple Discord text agents and character voice bots without cross-talk, acknowledgement loops, secret leakage, false tool claims, or unsafe service churn.

## Core capabilities

- **Shared-channel address gating** before model dispatch.
- **No-message loop suppression** for blank, closure, telemetry, retry, and third-party-address events.
- **Private coordination ledger** with scoped claims, approvals, handoffs, and proof.
- **SillyTavern-compatible memory** with bounded, sanitized JSONL history.
- **Multi-character voice services** with wake, focus, group-conversation, and private-room modes.
- **Voice safety** through immutable-ID authorization, bot-turn caps, DAVE/E2EE verification, listener recovery, and audio-integrity auditing.
- **Pluggable local backends** for STT, models, and TTS.
- **Operational recovery** covering allowlist mistakes, env-loading drift, DAVE churn, bad audio filters, watcher storms, and clean rollback.

## Architecture

```text
Discord text -> address/allowlist gate -> text agent -> tools
Discord voice -> PCM -> STT -> router -> model -> TTS -> encrypted playback
                               |                     |
                               +-> SillyTavern JSONL +-> audio integrity audit
All agents/services <-> private coordination bus (CLAIM/STATUS/DONE/BLOCKED)
```

## Files

- [`DiscordBotFleetSillyTavern.sherpa.md`](DiscordBotFleetSillyTavern.sherpa.md) — complete architecture, guardrails, setup, lessons, test matrix, and rollback procedure.
- [`HOWTO.md`](HOWTO.md) — ordered implementation guide with configuration shapes, identity routing, spoken-output cleanup, services, and acceptance tests.
- [`../../handoffs/DiscordBotFleetSillyTavern.sherpa.md`](../../handoffs/DiscordBotFleetSillyTavern.sherpa.md) — individually shareable copy.

## Confidentiality boundary

The kit deliberately uses placeholders. Keep tokens, user/channel/server IDs, personal character prompts, raw transcripts, private endpoints, and machine-specific paths in a private deployment worksheet, never in source control or the coordination bus.
