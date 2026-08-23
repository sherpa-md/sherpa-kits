# Sources and evidence

## Direct sources
- systemd project documentation (service supervision/timers):
  https://systemd.io/ (HTTP 200 on 2026-08-22; the freedesktop.org wiki
  mirror was unreachable from the test host at check time).
- Open speech/synthesis model ecosystems exist (Whisper-class STT and
  TTS engines run locally); specific project choice is left to the
  implementer and must be verified at build time.

## Claims vs inference
- We deliberately avoid citing benchmark numbers for any speech model
  without a checked source.
- Inference: hysteresis-based tier switching maintains availability through
  single-tier failures. The outage drill in the validation plan measures it.
