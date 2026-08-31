# HOW TO: Build a Loop-Safe Discord and SillyTavern Bot Fleet

This implementation guide turns the main Sherpa file into an ordered build. It is vendor-neutral where possible and uses Hermes Agent examples for the text gateway.

## Before you start

You need:

- a Discord server where you can invite bots;
- one Discord application per visible bot;
- a Linux host with Python, ffmpeg, and user systemd for voice bots;
- Hermes Agent for text agents, or another gateway with equivalent address gating;
- optional SillyTavern for character authoring/history;
- an OpenAI-compatible model endpoint or supported hosted provider;
- an STT backend such as faster-whisper, Whisper API, or an OpenAI-compatible local speech server;
- a TTS backend such as Edge TTS, Kokoro, or Piper.

Never put Discord tokens or provider credentials in this guide, source control, chat, or the coordination bus.

## Part 1 — Make a private deployment worksheet

Create a local file outside source control with mode `0600`:

```text
server_id=
operator_user_id=
shared_text_channel_id=
group_voice_channel_id=
private_voice_channel_id=

bot_1_name=
bot_1_application_id=
bot_1_user_id=
bot_1_token_secret_location=

bot_2_name=
bot_2_application_id=
bot_2_user_id=
bot_2_token_secret_location=
```

Record immutable IDs, not only names. Do not copy this worksheet into a public issue or AI prompt.

## Part 2 — Create each Discord bot

For each identity:

1. Open Discord Developer Portal.
2. Create an application and bot.
3. Enable Message Content Intent.
4. Enable Server Members Intent only if your allowlist/role code needs member lookup.
5. Leave Requires OAuth2 Code Grant off for normal bot invitation.
6. Generate an invite with `bot` and `applications.commands` scopes.
7. Grant View Channels, Send Messages, Read Message History, Add Reactions, and Use Application Commands.
8. Add Connect and Speak only for voice identities.
9. Invite the bot to the server.
10. Store the token only in the owning profile's secret file.

## Part 3 — Configure a Hermes text bot

Install and configure Hermes Agent using its current documentation. In the profile that owns this bot, set Discord values locally:

```env
DISCORD_BOT_TOKEN=<LOCAL_SECRET>
DISCORD_REQUIRE_MENTION=true
DISCORD_ALLOWED_USERS=<OPERATOR_ID>,<APPROVED_USER_ID>
DISCORD_ALLOWED_CHANNELS=<HOME_CHANNEL_ID>,<SHARED_CHANNEL_ID>
DISCORD_ADDRESS_REQUIRED_CHANNELS=<SHARED_CHANNEL_ID>
DISCORD_ADDRESS_ALIASES=mybot,my bot,MyBot
DISCORD_AUTO_THREAD=false
DISCORD_NO_THREAD_CHANNELS=<SHARED_CHANNEL_ID>
DISCORD_ALLOW_BOTS=all
DISCORD_REACTIONS=true
```

Use each bot's own aliases. Do not copy another bot's alias list.

Start or restart only after checking active work:

```bash
hermes gateway status
hermes gateway restart
hermes gateway status
```

Verify sanitized logs show a Discord connection. Do not print the token.

### Confirm `.env` settings are actually loaded

A service may not inherit application `.env` values. Verify effective non-secret settings through the adapter or configuration loader. If the adapter uses only `os.getenv()`, make sure gateway startup loads the application `.env` before adapter construction or add a profile-aware lookup helper.

## Part 4 — Prove the text address gate

In the shared channel, test each case separately:

| Test | Expected result |
|---|---|
| Human starts with this bot's alias | This bot replies once |
| Human starts with another bot's alias | This bot sends nothing |
| This bot's alias appears only in quoted history | This bot sends nothing |
| Bot-origin message directly addresses this bot | One reply only if bot-origin traffic is enabled |
| `ack`, `done`, `closed`, `stop`, blank, zero-width, retry notice | No outbound message |
| Human uses true all-agent summons | Each included bot replies briefly; bots do not reply to each other |

Verify visible results in actual Discord history. Local gateway logs and the coordination bus are insufficient because loop guards may intentionally hide bot-origin messages from a bot's model context.

## Part 5 — Install SillyTavern safely

Install SillyTavern from its upstream project. Create characters normally in the UI.

For bridge-managed history:

1. Find the selected user's character chat directory.
2. Create or reuse one JSONL chat file per character.
3. Append only cleaned conversational rows.
4. Include immutable Discord user ID in sanitized metadata, not in spoken text.
5. Read a bounded recent window.
6. Skip malformed rows and hidden model-control artifacts.
7. Enforce alternating user/assistant roles before calling a model.

Do not let raw Discord events, tool output, provider JSON, credentials, or hidden reasoning enter character history.

## Part 6 — Create the voice bridge virtual environment

Use a dedicated virtual environment:

```bash
python3 -m venv ~/.local/share/discord-voice-venv
~/.local/share/discord-voice-venv/bin/pip install \
  discord.py discord-ext-voice-recv faster-whisper edge-tts
```

Your exact Discord library may differ. Confirm that the selected library supports current Discord DAVE/E2EE voice requirements.

The bridge needs these modules:

```text
config loader
Discord client and voice receiver
per-speaker PCM chunker
STT adapter
speaker-ID and authorization policy
wake/focus/group router
SillyTavern history adapter
model adapter
output cleaner
TTS adapter
DAVE/Opus recovery guard
shared room-state lock
watchdog hooks
```

## Part 7 — Configure one character first

Use a local non-secret configuration like:

```env
VOICE_CHARACTER=character_a
DISCORD_TOKEN_ENV=DISCORD_CHARACTER_A_TOKEN
GROUP_VOICE_CHANNEL_ID=<GROUP_ID>
PRIVATE_VOICE_CHANNEL_ID=<PRIVATE_ID>
ENABLE_PRIVATE_ROOM=1
ALLOW_STARTUP_PRIVATE_FOLLOW=0
WAKE_WORDS=character a,character,common stt variant
AUTO_RESPOND_USER_IDS=
ALLOW_BOT_AUDIO=0
MAX_BOT_TURNS=8
FOCUS_IDLE_SECONDS=120
STT_URL=http://127.0.0.1:9021/v1/audio/transcriptions
MODEL_URL=http://127.0.0.1:1234/v1/chat/completions
TTS_ENGINE=edge
DISABLE_DAVE=0
```

Start with wake-gated human speech. Do not enable open-mic or bot audio until the exclusion and turn-cap tests pass.

## Part 8 — Implement immutable-ID identity

For every Discord event:

```python
speaker_id = str(event.author.id)
is_bot = bool(event.author.bot)
display = event.author.display_name
```

Then:

1. deny self/bot audio unless explicitly in bounded group mode;
2. check allowed conversational users by ID;
3. check operator controls by ID using a separate policy;
4. map the ID to a stable friendly alias for speech;
5. retain the ID in audit/history metadata;
6. select any private consensual persona by ID only.

When adding a participant, update the gateway's allowed-user IDs and test their own message. A successful reply to the operator does not prove everyone else is allowed.

## Part 9 — Implement the speech chunker

Maintain PCM buffers per speaker. Finalize a chunk when:

- speech exceeds the minimum duration;
- silence exceeds the configured silence window; or
- speech reaches the maximum duration.

Starting values to tune with real audio:

```text
minimum voice: 0.75 seconds
silence close: 1.05 seconds
maximum voice: 15 seconds
```

Discard empty transcripts and common filler before wake matching.

## Part 10 — Add STT with a fallback

Primary path:

```text
PCM -> temporary WAV -> localhost transcription API -> parse JSON -> plain transcript
```

Fallback path:

```text
PCM -> temporary WAV -> in-process faster-whisper -> plain transcript
```

Test with a planted WAV. Assert the bridge receives plain text, not a JSON object string. Bound timeouts and avoid repeated fallback storms.

## Part 11 — Add wake and focus routing

Wake matching should return both character and stripped prompt.

When an authorized human says the character name:

1. route to that character;
2. open focus for `(character, human_id)`;
3. allow short follow-ups from that same human without the wake word;
4. refresh focus on substantive speech;
5. close on timeout, clear goodbye, different human, or group-mode start.

Do not let a transcript intended for Character A wake Character B's service.

## Part 12 — Add bounded group conversation

Store shared state in one file protected by an OS file lock:

```json
{
  "active": false,
  "session_id": "",
  "last_activity": 0,
  "bot_turns_since_human": 0,
  "cap_announced": false,
  "events": []
}
```

A human turn resets the bot counter. A bot must atomically reserve its turn. At the configured cap, announce one pause at most and wait for a human.

Bot audio is accepted only when all are true:

```text
ALLOW_BOT_AUDIO=true
AND current room is the group room
AND group conversation mode is active
AND speaker is not this bot
AND atomic turn reservation succeeds
```

## Part 13 — Keep the private room private

Use a shared ownership lock. Only one selected bot may follow one human into the private room.

Do not:

- start all character services in the private room;
- run bot-to-bot tests there;
- allow startup auto-follow by default;
- infer ownership from a display name.

## Part 14 — Clean model output before text, speech, and memory

Create separate cleaning stages:

```text
raw provider response
  -> extracted assistant text
  -> cleaned Discord text
  -> spoken TTS summary
  -> sanitized SillyTavern row
```

The spoken stage must remove or summarize:

- JSON and provider envelopes;
- hidden thought/template markers;
- tool calls and stack traces;
- fenced code;
- Markdown formatting and inline backticks;
- emoji and decorative symbols;
- URLs, paths, hashes, IDs, and commands.

Post exact technical details in Discord text. Speak a natural summary such as: `I posted the command in text and explained what it checks.`

Test with planted code fences, JSON, emoji, URLs, paths, IDs, template tokens, and exceptions. Assert none are recited by TTS or saved as model-control text in SillyTavern.

## Part 15 — Add TTS and verify duration

Start with a simple engine. Generate a local audio file and inspect it before Discord playback.

If applying character filters:

1. detect the source sample rate;
2. apply filters for that sample rate;
3. compare input and output duration;
4. use pitch-preserving processing when changing pitch without intended speed change;
5. convert to Discord-compatible channels/rate after filtering.

A filter that assumes 48 kHz can badly distort 22.05 kHz Piper output.

## Part 16 — Verify DAVE/E2EE and listener recovery

Do not disable DAVE by default. After joining, require evidence of:

```text
DAVE protocol selected
can_encrypt=true
DAVE ready
intro or test audio played encrypted
voice receiver started
```

Drop isolated corrupt/decrypt-disputed frames instead of crashing the receiver. Bound per-SSRC error logs. After every TTS playback, prove the listener restarted.

## Part 17 — Install a user service

Example:

```ini
[Unit]
Description=Discord Character A voice bridge
After=network-online.target

[Service]
Type=simple
WorkingDirectory=%h
ExecStart=%h/.local/share/discord-voice-venv/bin/python %h/.local/bin/discord_voice_bridge.py
Restart=no
Environment=PYTHONUNBUFFERED=1
Environment=VOICE_CHARACTER=character_a
Environment=DISCORD_TOKEN_ENV=DISCORD_CHARACTER_A_TOKEN
EnvironmentFile=%h/.config/discord-voice/character-a.env

[Install]
WantedBy=default.target
```

Validate the unit, start it, and inspect sanitized status. Keep `Restart=no` during experiments.

## Part 18 — Add additional bots

Only after Character A passes the complete path:

```text
join -> DAVE ready -> hear -> transcribe -> identify ID -> route -> answer
-> clean text -> clean speech -> encrypted playback -> relisten
```

Clone the service configuration for the next character with a different token variable, identity, wake words, SillyTavern avatar/history, TTS voice/filter, and provider policy.

Use a cross-process intro lock so simultaneous service starts do not create overlapping greetings.

## Part 19 — Add the watcher last

Monitor:

- service and dependency health;
- fresh join/listen markers;
- generated reply without audible playback;
- DAVE/decode churn;
- wake misses;
- restart count;
- stale state during an active test.

Healthy checks produce no message. Deduplicate warnings by transition and cooldown. Do not let a dependency warning trigger an unlimited restart loop.

## Part 20 — Run the final acceptance test

### Text

- every bot answers only its current direct alias;
- third-party, quoted, blank, telemetry, closure, and stop messages produce no send;
- bot-origin tests work only when explicitly enabled and addressed;
- visible results are verified from Discord history.

### Identity

- each approved human can talk;
- each is identified by immutable ID;
- display-name changes do not alter authorization;
- only the operator can move rooms or change backend/mode;
- a new approved user is added to the allowlist and successfully tested.

### Spoken output

- raw JSON is never spoken;
- source code and commands appear in text but are summarized in voice;
- model-control tokens, emoji names, paths, IDs, hashes, and stack traces are not spoken;
- contaminated outputs are not written back to SillyTavern.

### Voice

- every bot passes the full hear/speak/relisten chain;
- DAVE encryption is ready;
- bot/self audio is excluded outside bounded group mode;
- group mode stops at its atomic bot-turn cap;
- private room remains one human plus one bot;
- stop-all procedure disconnects every bot and leaves no matching process.

## Rollback command plan

Prepare before testing:

```text
stop watcher
after preflight, stop each bot service
stop optional audio auditor
stop local STT/TTS lab containers
verify all services inactive
verify ports closed
verify no matching voice process
verify bots absent from voice rooms
restore previous script/unit/config if required
```

Never rejoin after an operator removal order until the operator explicitly asks.