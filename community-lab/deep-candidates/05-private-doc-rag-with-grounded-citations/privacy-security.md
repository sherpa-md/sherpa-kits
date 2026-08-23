# Privacy & security notes
- Corpus and index stay local unless the retrieval service is explicitly
  approved for that data class (see candidate kit 02 for the boundary pattern).
- Answers may be shared, but the underlying passages inherit their document's
  confidentiality — mark output accordingly.
- Never index secrets files; exclude .env, key files, credential dirs.
- Verify-pass logs store passage ids, not full private text, when shared.
