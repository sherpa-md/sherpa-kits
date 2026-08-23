# Sources and evidence

## Direct sources (verified reachable 2026-08-22)
- JSON Schema: https://json-schema.org (HTTP 200)
- Outlines (constrained generation): https://github.com/outlines-dev/outlines (HTTP 200)

## Claims vs inference
- Claims: JSON Schema validation and constrained-generation tooling exist as
  documented by their projects.
- Inference: repair loops beat naive re-prompting on cost and validity.
  Provider-native structured-output modes may outperform both; re-check
  provider docs at implementation time.
