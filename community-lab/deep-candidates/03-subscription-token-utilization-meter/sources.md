# Sources and evidence

## Direct sources (verified reachable 2026-08-22)
- OpenAI rate limits: https://platform.openai.com/docs/guides/rate-limits (HTTP 200)
- Anthropic rate limits: https://docs.anthropic.com/en/api/rate-limits (HTTP 200)
- OpenTelemetry GenAI semantic conventions:
  https://opentelemetry.io/docs/specs/semconv/gen-ai/ (HTTP 200)

## Claims vs inference
- Claims: providers publish rate-limit docs; OTel defines GenAI token
  telemetry attributes.
- Inference: the normalized meter improves routing decisions. Must be shown
  by the validation plan's before/after comparison.
- Provider dashboard mechanics change; any scraping approach must be rechecked
  against the provider's current terms before use.
