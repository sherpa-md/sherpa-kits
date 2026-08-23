# Validation plan
1. Positive control: run baseline twice; expect identical or near-identical
   scores (measures eval stability/noise).
2. Mutation tests: (a) subtly weaken the prompt, (b) swap to a smaller model,
   (c) delete one rubric rule. Confirm the gate blocks (a) and (b) and that
   (c) is flagged as a rule change requiring re-baseline.
3. Noise test: rerun the eval set 3x on same prompt/model; record score
   variance to set a sane tolerance.
4. Record false-block rate; adjust tolerance only with recorded evidence.
