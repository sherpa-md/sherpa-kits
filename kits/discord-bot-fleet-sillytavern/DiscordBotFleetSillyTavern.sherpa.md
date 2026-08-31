---
schema_version: "0.1.0"
id: "discord-bot-fleet-sillytavern"
title: "Discord Bot Fleet & SillyTavern Voice Bridge — Safe Multi-Agent Text and Voice"
domain: "conversational-agent-operations"
version: "0.1.0"
status: "active"
verification_state: "verified"
last_verified: "2026-08-31T01:00:00Z"
confidentiality: "public"
provenance:
  origin_task: "discord-bots-sillytavern-sherpa-20260830"
  author_alias: "hermx"
  verifier_alias: "hermx"
sources:
  - id: "src-hermes-discord"
    title: "Hermes Agent Discord gateway documentation and tested shared-channel routing"
    url: "https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord"
    trust_label: "documentation_and_live_operations"
  - id: "src-discord-api"
    title: "Discord Developer Documentation"
    url: "https://discord.com/developers/docs/intro"
    trust_label: "authoritative_specification"
  - id: "src-sillytavern"
    title: "SillyTavern project"
    url: "https://github.com/SillyTavern/SillyTavern"
    trust_label: "upstream_project"
tags:
  - "discord"
  - "multi-agent"
  - "loop-guard"
  - "voice-bots"
  - "sillytavern"
  - "speech-to-text"
  - "text-to-speech"
  - "dave-e2ee"
  - "incident-response"
related_links:
  - rel: "spec"
    uri: "https://github.com/sherpa-md/sherpa-spec"
  - rel: "ai-to-ai-bus"
    uri: "../ai-to-ai-bus/AItoAIBus.sherpa.md"
  - rel: "bounded-control-plane"
    uri: "../bounded-agent-control-plane/BoundedAgentControlPlane.sherpa.md"
---

# Discord Bot Fleet & SillyTavern Voice Bridge

## 1. Mission

Build or hand off a Discord fleet in which several AI bots can share a server without answering for each other, forming acknowledgement loops, exposing credentials, or falsely claiming that voice-chat conversation performed computer work.

The pattern covers:

- independent Hermes-style text agents;
- shared and private Discord text channels;
- separate character voice bots backed by SillyTavern-compatible history;
- local or hosted model providers;
- speech-to-text and text-to-speech backends;
- Discord DAVE/E2EE voice behavior;
- a durable private AI-to-AI coordination ledger;
- operator approvals, quiet alerts, watchdogs, recovery, and verification.

This is a public, portable kit. Replace every placeholder locally. Never copy deployment IDs, tokens, user allowlists, personal prompts, private infrastructure addresses, or raw chat history into a public repository.

## 2. System topology

```text
                           Human operator
                                  |
             +--------------------+--------------------+
             |                                         |
      Discord text channels                         Voice rooms
             |                                         |
   +---------+---------+                    +----------+----------+
   |                   |                    |          |          |
Text Agent A      Text Agent B         Character A Character B Worker Voice
(Hermes profile)  (Hermes profile)      process     process     process
   |                   |                    |          |          |
   +---------+---------+                    +----------+----------+
             |                                         |
     address/mention gate                     shared voice bridge code
             |                                         |
        model + tools                    STT -> routing -> model -> TTS
             |                                         |
             +--------------------+--------------------+
                                  |
                         private coordination bus
                    claims / handoffs / status / proof
                                  |
                 local state, SillyTavern JSONL, logs
```

Keep the planes separate:

1. Discord is the human-visible conversation plane.
2. The private AI-to-AI bus is the agent coordination and work ledger.
3. Tool execution happens only on the node that owns the relevant files, services, or devices.
4. SillyTavern history is conversational memory, not an authorization mechanism.
5. A webhook proves delivery or wake-up only; it does not prove that requested work happened.

## 3. Bot and channel model

Use one Discord application/token per independently visible bot identity. Use one local process or service per identity. Do not share a token between concurrently running processes.

Recommended channel classes:

| Channel class | Purpose | Default behavior |
|---|---|---|
| Agent home | Direct conversation with one text agent | Mention or configured free response |
| Shared agents | Human can address any bot | Address required; no automatic threads |
| Private 1:1 voice | Exactly one human and one selected voice bot | No group tests; explicit move/ownership lock |
| Group voice room | Human plus selected character/worker bots | Wake-gated or deliberately enabled conversation mode |
| Operations/log channel | Human-facing completion, blocker, or approval summaries | Never raw tokens, logs, or bus chatter |

Use stable bot aliases. Matching should be case-insensitive, punctuation-tolerant, and boundary-aware. A name in quoted history, an embed, a previous reply, or tool telemetry must not count as a new address.

## 4. Discord Developer Portal setup

For each bot application:

1. Create a Discord application and bot identity.
2. Reset/copy the bot token only into the owning machine/profile's secret store.
3. On the Bot page:
   - enable Message Content Intent for normal text processing;
   - enable Server Members Intent only if role/user lookup actually needs it;
   - Presence Intent is unnecessary for basic chat;
   - leave Requires OAuth2 Code Grant off for normal bot invites.
4. Generate an invite with scopes `bot` and `applications.commands`.
5. Grant the minimum useful permissions:
   - View Channels;
   - Send Messages;
   - Send Messages in Threads if threads are used;
   - Read Message History;
   - Add Reactions;
   - Attach Files and Embed Links if required;
   - Use Application Commands;
   - Connect and Speak only for voice bots.
6. Authorize the bot into the intended server as an administrator/operator.

Never paste a token into Discord, an AI prompt, an AI-to-AI bus message, source control, screenshots, command history, or logs. If exposed, revoke and rotate it.

## 5. Text-agent environment shape

Store non-secret routing values and secret tokens separately even if the runtime uses one `.env` file. A portable Hermes-style configuration is:

```env
DISCORD_BOT_TOKEN=<LOCAL_SECRET>
DISCORD_REQUIRE_MENTION=true
DISCORD_ALLOWED_USERS=<OPERATOR_OR_APPROVED_USER_IDS>
DISCORD_ALLOWED_CHANNELS=<HOME_CHANNEL_ID>,<SHARED_CHANNEL_ID>
DISCORD_ADDRESS_REQUIRED_CHANNELS=<SHARED_CHANNEL_ID>
DISCORD_ADDRESS_ALIASES=<BOT_NAME>,<BOT_ALIAS_1>,<BOT_ALIAS_2>
DISCORD_AUTO_THREAD=false
DISCORD_NO_THREAD_CHANNELS=<SHARED_CHANNEL_ID>
DISCORD_ALLOW_BOTS=all
DISCORD_REACTIONS=true
DISCORD_REACTION_SEEN_EMOJI=<BOT_SPECIFIC_SEEN_EMOJI>
DISCORD_REACTION_RESPONDED_EMOJI=<BOT_SPECIFIC_DONE_EMOJI>
DISCORD_REACTION_FAILED_EMOJI=<FAILURE_EMOJI>
```

`DISCORD_ALLOW_BOTS=all` is safe only when the address gate executes before model dispatch. If bot-origin traffic is unnecessary, deny bot messages. Allowing bot messages without a strict early gate is a loop hazard.

A free-response channel may still be address-required. Treat free-response and address-gating as distinct policy layers.

## 6. Hard shared-channel guardrails

Apply these checks before creating a model turn:

```text
1. Is this a current, visible message rather than quoted/replayed context?
2. Is the author allowed?
3. Is the channel allowed?
4. If this is a shared channel, does the new visible text directly address this bot?
5. If the author is a bot, is bot-origin traffic allowed and directly addressed?
6. Is the event substantive, rather than blank text, telemetry, a retry notice, or closure echo?
7. Is this exchange already closed or beyond its visible reply budget?
8. If any check fails: suppress dispatch and suppress send.
```

Only answer when:

- the human directly names this bot or mentions it;
- a true all-agent summons explicitly includes this bot;
- an authorized bus handoff requires a visible test; or
- another bot directly names this bot and supplies useful new work that cannot remain on the bus.

Stay silent when:

- another agent is the target;
- this bot's name occurs only in quoted history;
- a message is blank, whitespace, punctuation-only, zero-width, boilerplate, or tool telemetry;
- the previous message says `ack`, `confirmed`, `done`, `closed`, `stop`, `standby`, `no further response`, or equivalent;
- the content is a gateway interruption/retry/model-empty notice;
- a bot posts routine status, proof, or a self-suppression statement.

Silence means no outbound message. Do not replace silence with `No action`, `Stopped`, `(empty)`, a zero-width character, or a loop-guard explanation. Placeholder silence is still a message and can restart the loop.

## 7. Visible reply budget

For agent-to-agent Discord exchanges:

- allow at most one substantive visible reply per bot per exchange;
- never request acknowledgement unless required for a human decision;
- never visibly acknowledge another bot's acknowledgement;
- after the substantive reply, move follow-up coordination to the private bus;
- if the operator says stop, suppress the send immediately and do not post a textual acknowledgement.

A safe visible route test is:

```text
<TARGET_BOT> — Reply once with <UNIQUE_TOKEN>. No acknowledgement chain; I will verify silently.
```

Test one target at a time. Verify from Discord history, not from the bus and not solely from the sender's gateway logs.

## 8. AI-to-AI bus discipline

Routine coordination belongs on a private durable bus:

```text
CLAIM task=<id> owner=<node> scope=<files/services/test-environment> mode=<edit|test|deploy|review> ttl=<minutes>
STATUS task=<id> owner=<node> state=<state> details=<sanitized update>
DONE task=<id> owner=<node> result=<summary> verify=<commands or evidence>
BLOCKED task=<id> owner=<node> reason=<blocker> next=<needed decision>
NEEDS-APPROVAL task=<id> owner=<node> decision=<exact gate> risk=<impact> options=<safe choices>
ABANDON task=<id> owner=<node> reason=<why work stopped>
```

Rules:

- claim before edits, service changes, shared tests, device use, or voice-room tests;
- claim the narrowest scope;
- reread recent bus entries before completion;
- close every claim;
- never put tokens, passwords, cookies, private keys, auth JSON, `.env` values, personal raw transcripts, or private infrastructure identifiers on the bus;
- target the node that owns the environment rather than trying to control another machine;
- use webhooks only as wake signals; reread the durable ledger before action.

## 9. Voice bridge architecture

Run each character as a separate service using the same tested bridge code with different environment variables:

```text
Discord voice receive
  -> per-speaker PCM buffer
  -> silence/max-duration chunker
  -> STT backend
  -> transcript cleanup and filler suppression
  -> immutable speaker ID + display-name mapping
  -> wake/focus/conversation router
  -> authorization and control-command gate
  -> recent SillyTavern-compatible context
  -> selected model provider
  -> output artifact cleanup
  -> reply-length shaping
  -> Discord text echo
  -> TTS backend and character voice filter
  -> encrypted Discord playback
  -> receiver/listener restart
```

Recommended process isolation:

- one service per bot/token/persona;
- one shared file-locked room-state file for group conversation coordination;
- one cross-process intro lock so bots do not all speak introductions simultaneously;
- one watcher and an optional independent audio-integrity auditor;
- localhost-only STT/TTS/model endpoints unless remote access is explicitly secured.

## 10. SillyTavern integration

SillyTavern can remain the human-facing character editor and chat archive while Discord is the live transport.

A bridge can append SillyTavern-compatible JSONL rows to the selected character chat directory. Each row should include:

- character or user name;
- `is_user` boolean;
- timestamp;
- cleaned text;
- sanitized extra metadata such as Discord source, immutable speaker ID, voice/text mode, selected character, or bus message ID.

Do not store credentials, raw backend prompts, hidden reasoning, or secret tool output in character history.

Read only a bounded recent context window. Enforce strict user/assistant role alternation before sending it to a model. Corrupt or unexpected rows should be skipped rather than breaking the live bridge.

Character identities must remain separate. A worker persona must not pretend to be a character persona. A character voice should not claim that it edited files, restarted services, sent messages, or controlled devices unless a real tool/bus handoff produced proof.

## 11. Conversation routing modes

### Wake-gated group mode

The default group-room mode should require a character's name or configured wake variant. Include realistic speech-recognition variants because STT may split or substitute names.

### Focus mode

After a human wakes one character, allow a short focused follow-up window without repeating the wake word. Store:

- focused character;
- focused human ID;
- last activity time;
- focus session ID.

Close focus on a clear goodbye/stop phrase, timeout, a different human taking the floor, or activation of group conversation mode. Do not treat unrelated phrases containing the word `stop` as a stop command.

### Deliberate group-conversation mode

An authorized human may start a shared multi-bot conversation. Use a file-locked shared state containing:

- active flag and session ID;
- last activity;
- bounded event list;
- number of bot turns since the last human turn;
- whether the turn-cap notice has already been announced.

Reset the bot-turn counter when a human speaks. Enforce a hard cap to prevent bot-to-bot runaway. When the cap is reached, emit at most one short pause notice and wait for a human.

### Open-mic mode

If a character is intentionally configured to answer every human speaker, use a wildcard human policy only after proving:

- bots and the process's own bot ID are excluded;
- filler/background utterances are suppressed;
- room/backend/mode control remains restricted to the authorized operator;
- the bot cannot hear its own TTS as a new human prompt.

Open-mic is a deployment policy, not a safe default.

## 12. Voice authorization rules

Separate conversational access from control access.

Any approved human may be allowed to converse, but only the operator should be able to:

- move bots between private and group rooms;
- enable bot-audio routing or multi-bot mode;
- change providers/models/backends;
- send coordination-bus handoffs;
- start/stop services;
- request external side effects;
- alter recording, retention, or privacy settings.

Use immutable Discord user IDs for authorization and audit. Display names are presentation only and can change.

A private 1:1 room must enforce exactly one selected bot plus one human. Do not run group or bot-to-bot tests there. Use a cross-process ownership lock so two bots cannot follow the same human into the private room.

## 13. STT design and lessons

Support at least two STT routes:

1. a local OpenAI-compatible transcription service; and
2. an in-process fallback such as faster-whisper.

Operational lessons:

- bind local speech endpoints to loopback by default;
- health-check the exact endpoint and model, not merely the process;
- distinguish dependency-down from bridge-down;
- return plain transcript text to the bridge; do not accidentally feed a JSON response envelope into the model as spoken text;
- tune minimum speech, silence, and maximum-chunk durations using real Discord audio;
- suppress common filler and background fragments before wake matching;
- normalize common STT variants of bot names before routing;
- keep a known audio fixture for offline regression tests;
- benchmark latency and accuracy on the target host before replacing a working backend;
- keep fallback activation explicit so repeated failures do not create a retry storm.

Local containerized Whisper can make experimentation reversible. Keep models cached, services `restart: no` during experiments, ports loopback-only, and leave the lab stopped after tests unless deployment is approved.

## 14. TTS design and lessons

Support interchangeable TTS engines such as Edge TTS, Kokoro, or Piper. Configure voice, speed, and post-filter per character.

Before synthesis:

- remove emoji and decorative symbols that a TTS engine may pronounce;
- bound reply length;
- strip model template/thought artifacts;
- normalize names and punctuation.

After synthesis:

- inspect sample rate/channels/duration;
- apply filters using the actual source sample rate;
- preserve duration when pitch shifting unless a speed change is intentional;
- verify the final file can be played through Discord;
- restart voice receiving after playback.

A learned failure mode was applying a legacy sample-rate filter to lower-rate Piper audio, making a character sound fast and high-pitched. Prefer a pitch-preserving filter such as Rubber Band for pitch changes, and compare input/output durations automatically.

## 15. Discord DAVE/E2EE voice handling

Modern Discord voice may require DAVE/E2EE negotiation. Advertising no DAVE support can produce close code `4017` in rooms that require it.

Safe defaults:

- keep DAVE enabled;
- verify `can_encrypt`, selected DAVE protocol, and readiness after join;
- treat a voice-channel join as incomplete until encrypted playback and receive/listen both work;
- isolate and drop a disputed/corrupt frame rather than poisoning the entire decoder;
- bound repeated decrypt/decode log spam by SSRC and time;
- recover the listener after bad Opus frames;
- never claim success from service-active status alone.

DAVE receive paths can exhibit intermittent decrypt/drop churn even while real end-to-end speech works. Record the churn as degraded telemetry, but decide readiness from a live or controlled hear -> transcribe -> answer -> speak -> relisten test.

## 16. Model routing

Make provider selection per character/service explicit. Possible routes include:

- local LM Studio via an OpenAI-compatible endpoint;
- a local Hermes/OpenAI-compatible service;
- a subscription-backed CLI with strict timeout;
- a hosted OpenAI-compatible API.

Rules:

- do not silently substitute a different provider when an exact model is required;
- set a bounded timeout;
- clean provider artifacts before Discord/TTS/history;
- maintain a short voice-oriented token limit;
- mark recovery/fallback internally, but do not leak sentinel text;
- do not let a model claim tool work it did not perform;
- prefer a proven low-latency endpoint for live voice over a slow CLI route;
- use the private bus for real tool execution and return sanitized results to the character.

## 17. Safe character and user-specific behavior

Character profiles may define name, avatar, wake variants, style, TTS voice, speed, and filters. User-specific personas must be explicit, consensual, adult-only where applicable, and keyed by immutable user ID.

Never treat a display name as proof of identity. Never expose a private user-specific prompt in public source. Keep moderation, safety, and authorization independent of roleplay style.

## 18. The hard-won identity and spoken-output rules

These are not cosmetic details. They came from failures where a bot seemed deaf to certain people, used the wrong name, treated a display name as authority, or read machine syntax aloud.

### Route and authorize by immutable Discord ID

For every voice chunk and text message, carry the immutable Discord user ID through the complete pipeline:

```text
Discord event
  -> immutable user ID
  -> allowed-user / operator-control decision
  -> human-vs-bot decision
  -> stable audit alias
  -> optional consensual user-specific persona
  -> model prompt metadata
  -> SillyTavern row metadata
  -> sanitized logs
```

Rules:

- use numeric user ID for allowlists, operator-only controls, per-user security counters, focus ownership, and user-specific personas;
- use display/global/user name only for friendly speech and presentation;
- pair audit records with both stable alias and immutable ID so display-name spoofing is obvious;
- never authorize from a spoken name, display name, nickname, transcript text, or model guess;
- add every approved new participant to the text gateway allowlist if that gateway is configured as allowlist-only;
- distinguish `allowed to chat` from `allowed to control rooms/backends/services`;
- a wildcard open-mic policy means every human, never every Discord account: bots and the bridge's own bot ID stay blocked;
- preserve the source human ID through focus mode so only that human gets no-wake follow-ups;
- if a different human speaks, release or transfer focus deliberately rather than attributing their speech to the previous person.

A critical diagnostic lesson: a gateway that is active and receives other users may not be broken. It may be silently dropping a newly invited person because their immutable ID is absent from `DISCORD_ALLOWED_USERS`. Read permitted channel history and compare policy before calling the connection a zombie or restarting it. Discord will not redeliver events missed or rejected earlier, so safely backfill permitted messages when needed.

### Stable names without trusting names

Maintain a private mapping from immutable ID to canonical friendly alias. The conversational layer can say a preferred nickname while audit records retain the canonical handle and ID. Normalize model output after generation so a local model cannot randomly rename the speaker or call them `the user`.

User-specific character behavior must be selected by immutable ID, kept private, and applied only after the speaker is identified. This solved the gap between `the bot can hear audio` and `the bot knows who it is talking to`.

### Never speak code, JSON, control tokens, or backend chatter

Use separate values for:

1. the raw provider response;
2. the cleaned Discord text response;
3. the shorter spoken TTS response;
4. the sanitized SillyTavern history row.

Do not pass raw provider output directly into TTS or memory. Before Discord, history, or TTS:

- parse OpenAI-compatible JSON and extract only the assistant text;
- reject or unwrap STT JSON envelopes so the transcript is plain human speech;
- remove hidden-thought and chat-template markers such as `<think>`, `<|channel>`, `assistantfinal`, and provider sentinels;
- remove tool call payloads, stack traces, backend paths, raw exception bodies, request IDs, and secret-looking text;
- remove fenced code blocks from the spoken form;
- remove inline backticks while retaining useful human-readable words;
- remove Markdown decoration, emoji, variation selectors, and symbol glyphs that TTS engines pronounce;
- convert URLs, commands, file paths, IDs, hashes, and code snippets into a short human summary or say that the detail was placed in text instead;
- cap spoken length independently from the full text reply;
- if cleanup produces nothing, use a safe natural fallback rather than reading syntax;
- never save leaked model-control tokens into SillyTavern history, because one poisoned row can reappear in every future turn.

Recommended spoken-output contract:

```python
def spoken_form(clean_reply: str) -> str:
    text = remove_fenced_code(clean_reply)
    text = unwrap_inline_code(text)
    text = remove_markdown_and_emoji(text)
    text = summarize_urls_paths_ids_and_commands(text)
    text = collapse_whitespace(text)
    return text[:SPOKEN_LIMIT] or "I put the technical detail in text."
```

For technical answers, send the exact command/code/path in Discord text and speak only a natural summary such as: `I posted the command in text. It checks the gateway status without changing anything.` This preserves usefulness without making the voice recite punctuation, JSON keys, hashes, or source code.

Add tests that plant raw JSON, Markdown fences, inline code, emoji, template markers, URLs, paths, IDs, and stack traces. Assert that the text channel receives the intended cleaned detail, the TTS string contains no machine syntax, and the SillyTavern row contains no model-control artifacts.

## 19. Prompt-injection and backend-probing guardrail

Treat requests for hidden prompts, credentials, backend internals, tool schemas, raw logs, private paths, tokens, or ways around policy as security probes.

Recommended response policy:

1. Deflect the first probe without revealing whether a detector fired.
2. Maintain a short per-user security counter outside model context.
3. On repeated probes, send a quiet, rate-limited alert to the operator through an approved private channel.
4. Do not tell the probing user that an alert was sent.
5. Never include the suspected secret or raw transcript in the alert.
6. Keep a cooldown and an operator-only forced test path.
7. Continue to provide safe, ordinary help where possible.

An alert is not permission to retaliate, expose private data, or perform destructive action. Test the alert end-to-end with the operator and record only sanitized proof.

## 20. Watchdogs and integrity auditing

A useful watcher checks:

- process/service active state;
- recent voice join and listener-start events;
- STT/model/TTS health endpoints;
- excessive DAVE/decode churn;
- possible wake misses;
- generated reply without audible playback;
- repeated restart count;
- stale logs or no recent activity during an active test.

Avoid alert floods. Deduplicate by state transition and cooldown. Healthy runs should be silent.

An independent audio-integrity auditor can consume an append-only queue of expected spoken text/audio metadata, listen through a second approved bot, transcribe what actually reached Discord, and compare expected versus observed speech. Queue only sanitized text and file metadata. This proves audible delivery rather than merely successful local synthesis.

## 21. Service management

A generic user service template is:

```ini
[Unit]
Description=Discord character voice bridge
After=network-online.target

[Service]
Type=simple
WorkingDirectory=%h
ExecStart=<PYTHON> <VOICE_BRIDGE_SCRIPT>
Restart=no
Environment=PYTHONUNBUFFERED=1
Environment=VOICE_CHARACTER=<CHARACTER_KEY>
Environment=DISCORD_TOKEN_ENV=<TOKEN_VARIABLE_NAME>
Environment=GROUP_VOICE_CHANNEL_ID=<GROUP_CHANNEL_ID>
Environment=PRIVATE_VOICE_CHANNEL_ID=<PRIVATE_CHANNEL_ID>
Environment=ENABLE_PRIVATE_ROOM=1
Environment=ALLOW_STARTUP_PRIVATE_FOLLOW=0
Environment=ALLOW_BOT_AUDIO=0
Environment=MAX_BOT_TURNS=8
Environment=FOCUS_IDLE_SECONDS=120
Environment=STT_URL=http://127.0.0.1:<STT_PORT>/v1/audio/transcriptions
Environment=MODEL_URL=http://127.0.0.1:<MODEL_PORT>/v1/chat/completions
Environment=TTS_ENGINE=<edge|kokoro|piper>
Environment=DISABLE_DAVE=0

[Install]
WantedBy=default.target
```

Use `Restart=no` during risky voice experiments so a bad process does not repeatedly rejoin a room. Add controlled restart policy only after proving clean shutdown and bounded recovery.

Before restart/stop/update:

1. check private-bus claims and status;
2. inspect active voice sessions and tests;
3. inspect service/process/cron state;
4. obtain approval if interruption is possible;
5. stop the watcher before stopping dependencies if it would auto-restart them;
6. verify bot processes are gone and bots disconnected;
7. after start, verify the complete voice path.

A service that is `active` may still have a dead Discord receive path. Conversely, a gateway described as a zombie may actually be correctly dropping a user because the allowlist omitted them. Diagnose policy before restarting.

## 22. `.env` loading pitfall

A systemd user service may not export every value stored in an application `.env`. Adapter code that uses only `os.getenv()` can therefore ignore newly written Discord routing settings after restart.

Load the application's secret/config file before adapter construction, or use a helper that checks both process environment and the application config source:

```python
def discord_setting(key, default=None):
    return os.getenv(key) or application_env_lookup(key) or default
```

Use the same lookup path for allowed channels/users, address-required channels, aliases, bot-origin policy, thread policy, and reaction settings. Verify effective settings without printing tokens.

## 23. Failure patterns learned

| Symptom | Likely cause | Correct response |
|---|---|---|
| Every bot answers | Missing/late address gate | Gate before model dispatch; per-bot aliases |
| Bots keep saying `ack` | Acknowledgement chain | One visible reply maximum; use bus |
| `No action` creates more noise | Placeholder silence | Suppress outbound send entirely |
| Bot sees human aliases but not bot-authored tests | Bot-origin messages denied | Check `DISCORD_ALLOW_BOTS`; retain early address gate |
| `.env` change appears ignored | Process environment not populated | Use application env loader/helper and verify effective values |
| Visible reply appears absent | Sender cannot see bot-origin traffic | Read actual Discord history with a read-only probe |
| Gateway appears alive but a user gets no replies | User/channel allowlist omitted them | Compare immutable IDs and policy before restart |
| Gateway restart loses a message | Discord does not redeliver old events | Read permitted history and ask/resume safely |
| Voice service active but bot is deaf | Receive sink/decoder/listener failure | Verify real inbound chunk and listener restart |
| Voice join fails with 4017 | DAVE disabled/unsupported | Enable DAVE and verify negotiation |
| Replies generate but are not audible | Playback/encryption/filter failure | Verify final audio and encrypted playback |
| Character sounds too fast/high | Wrong sample-rate transform | Preserve duration and use correct source rate |
| STT speaks JSON | API envelope not parsed | Return plain transcript text |
| Watcher repeatedly restarts bridge | Dependency alarm coupled to restart | Separate alerts from bounded recovery |
| Bot claims computer action in voice | Model role confusion | Deterministic unperformed-action detector and bus handoff |
| Multiple bots talk over intros | Concurrent startup | Cross-process intro lock |
| Group chat runs away | Bot audio accepted without cap | Human reset plus atomic bot-turn cap |
| Private room becomes group room | Missing ownership lock | Exactly one bot plus one human; no group tests |

## 24. Installation workflow

1. Inventory existing Discord applications, Hermes profiles, voice scripts, services, channels, users, model endpoints, STT/TTS backends, SillyTavern directories, and logs without printing secrets.
2. Assign one stable bot identity and local owner per process.
3. Create a private deployment worksheet containing IDs and secret paths; do not commit it.
4. Configure Developer Portal intents and minimum permissions.
5. Configure per-bot text address gates and thread policy.
6. Install the private coordination bus or equivalent durable ledger.
7. Build one voice bot first and prove text-only routing.
8. Add inbound audio and STT; prove known fixture transcription.
9. Add model routing; prove output cleanup and no false tool claims.
10. Add TTS; prove final audio duration and local playback.
11. Join a test voice room; prove DAVE readiness, hear, reply, speak, and relisten.
12. Add SillyTavern-compatible bounded history.
13. Add focus mode, then optional group conversation with turn cap.
14. Add additional character services one at a time.
15. Add watcher and audio-integrity audit after the base path works.
16. Run shared-text loop tests and real Discord-history verification.
17. Document rollback and leave experimental services stopped when not approved.

## 25. Verification matrix

### Static checks

- configuration contains no token values;
- every bot has distinct token variable, aliases, and service identity;
- shared channels are address-required and no-thread;
- source compiles;
- systemd units verify;
- private paths and IDs are absent from public artifacts.

### Text routing tests

- direct human alias -> exactly one intended bot reply;
- another bot's alias -> silence;
- quoted own alias -> silence;
- bot-origin direct alias -> one reply only when enabled;
- blank/zero-width/telemetry/retry/closure -> silence;
- stop command -> no visible acknowledgement;
- visible test result verified from actual Discord history.

### Voice unit tests

- wake variants route to the right character;
- focus opens, refreshes, times out, and closes;
- a different human breaks focus safely;
- group mode file locking prevents duplicate reservations;
- bot-turn cap emits no repeated notice;
- bot/self audio is blocked unless explicitly enabled;
- control commands require operator ID;
- unperformed-action language is caught;
- SillyTavern rows append and malformed history is skipped;
- STT JSON is parsed to plain text;
- TTS filters preserve expected duration.

### Live voice acceptance

For every deployed bot, capture sanitized proof of:

```text
service active
-> Discord voice joined
-> DAVE protocol selected and encryption ready
-> inbound human speech received
-> transcript produced
-> correct bot selected
-> model reply completed within timeout
-> Discord text posted if configured
-> final TTS audio played encrypted
-> voice receiver/listener restarted
```

Do not call the system healthy from a subset of this chain.

## 26. Rollback

Maintain:

- previous bridge script or commit;
- previous unit files;
- previous non-secret routing config;
- a command to stop all bot/watcher/auditor services;
- a list of local lab containers and ports;
- a clean-disconnect handler;
- a way to prove no matching voice processes remain.

If the operator orders bots out, the newest direct order overrides pending experiments: abandon related claims, stop the watcher first, stop bots/auditor, verify disconnect and dead processes, and do not rejoin until explicitly requested.

## 27. Acceptance criteria

This kit is successfully implemented when:

1. shared text agents reply only when currently and directly addressed;
2. stop/closure/blank/telemetry events produce no outbound text;
3. agent coordination uses a private ledger with claims and proof;
4. secrets and private deployment identifiers never enter public artifacts or the bus;
5. each voice bot has a distinct identity, service, persona, and token variable;
6. private 1:1 and group voice policies remain separate;
7. group bot audio cannot run past the configured atomic turn cap;
8. every live bot passes hear -> transcribe -> route -> answer -> speak -> relisten;
9. DAVE/E2EE readiness and audible playback are verified, not assumed;
10. SillyTavern history is bounded, sanitized, and role-valid;
11. control and external actions remain operator-authorized;
12. watchdog alerts are deduplicated and healthy state is quiet;
13. stop/restart procedures preserve active work and provide rollback proof.
