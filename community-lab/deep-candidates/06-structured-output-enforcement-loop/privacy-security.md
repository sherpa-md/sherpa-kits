# Privacy & security notes
- Validation errors echoed back to the model may contain input data — do not
  send errors to a different provider than received the original data.
- Telemetry logs schema errors, not payload contents, when shared.
- If schema fields include personal data, minimize collection: require only
  what downstream automation truly consumes.
