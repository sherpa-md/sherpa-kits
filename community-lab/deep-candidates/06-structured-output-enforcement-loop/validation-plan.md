# Validation plan
1. Define a moderately complex schema (nested object, enums, arrays).
2. Run 30 tasks across 3 modes: (a) prompt-only, (b) full-retry on failure,
   (c) this kit's targeted-repair loop.
3. Metrics: first-attempt validity rate, final validity rate, total tokens per
   valid result, wall time.
4. Success criteria: final validity >=95% for the loop; tokens-per-valid-result
   lower than full-retry mode.
5. Edge tests: oversized output, truncated JSON, wrong types — confirm repair
   prompt targets the right JSON path.
