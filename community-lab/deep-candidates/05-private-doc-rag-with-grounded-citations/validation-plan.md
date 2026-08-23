# Validation plan
1. Use a synthetic corpus (public-domain text you can quote freely) with 3
   planted false facts in a decoy document.
2. Ask 10 questions: 5 answerable, 3 partially answerable, 2 unanswerable.
3. Score: citation present on every factual claim; cited passages actually
   support the claim (human check); unanswerable questions get NOT FOUND.
4. Trap check: does the model repeat the planted false facts? Any yes = Fail.
5. Compare against a free-form baseline (same model, no schema) and count
   unsupported claims in both.
