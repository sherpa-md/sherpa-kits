# Validation plan
1. Prepare a small repo with 5 seeded defects across 3 disjoint scopes.
2. Run 3 reviewers in parallel under the kit's rules; collect findings.
3. Collision test: verify zero concurrent writes to the shared tree (git
   reflog/log inspection).
4. Quality: seeded defects found >=4/5; every finding has evidence or the
   INFERENCE label.
5. Negative control: rerun without scope enforcement and document at least one
   write conflict or duplicate edit to show the difference.
