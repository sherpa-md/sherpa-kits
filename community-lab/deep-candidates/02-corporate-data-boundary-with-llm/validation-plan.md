# Validation plan
1. Build a SYNTHETIC company dataset: 30 rows of fake customer/employee data
   mixing names, emails, amounts, and internal hostnames.
2. Run the redaction pass; verify 0 restricted tokens remain (grep check).
3. Verify placeholder stability: same entity maps to same token across runs.
4. Send 5 sanitized prompts to the approved endpoint; confirm no restricted
   substring appears in any outgoing request (log inspection).
5. Attempt a negative test: confirm the automation REFUSES a prompt containing
   a T3 marker.
6. Record Pass/Partial/Fail and any policy gaps found.
