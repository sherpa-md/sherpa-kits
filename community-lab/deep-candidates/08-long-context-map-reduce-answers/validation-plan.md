# Validation plan
1. Build a synthetic long document (30+ pages of generated filler + 12 planted
   facts spread across early/middle/late sections; include 2 contradictory
   planted facts).
2. Ask 6 questions: 2 needing early facts, 2 middle, 2 late/contradiction.
3. Compare single-pass vs map-reduce: count missed facts and unflagged
   contradictions.
4. Success criteria: map-reduce misses fewer facts (especially middle/late)
   and flags both planted contradictions.
5. Record token cost ratio map-reduce vs single-pass.
