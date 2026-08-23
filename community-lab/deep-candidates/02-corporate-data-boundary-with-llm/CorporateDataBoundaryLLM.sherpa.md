---
status: ai-sourced-untested
source_type: ai-synthesized
testing: not-tested
human_reviewed: false
model: qwen3.8-max
provider: qwen-cloud
risk_level: medium
batch: deep-candidates-batch1
---

# Corporate Data Boundary with an Employer-Approved LLM — Safe Mixing of Private Company Data

## Problem
Employees want AI help with real company data (spreadsheets, tickets, internal
docs), but most consumer AI tools log prompts, train on inputs, or route data
through regions the employer has not approved. The result is either total
avoidance of useful tools or accidental data leakage. This kit defines a
boundary workflow: classify data, sanitize what leaves, use only the
employer-approved endpoint, and audit what was sent.

## Who experiences it
- Knowledge workers whose employer approved one specific LLM (e.g. an
  enterprise deployment) but not public chat tools.
- Team leads writing AI usage policy.
- Automation builders wiring company data into agent pipelines.

## Claims (sourced) vs inference
CLAIM: The OWASP Top 10 for LLM Applications lists sensitive information
disclosure and supply-chain/prompt-injection risks as recognized failure
classes (source: https://owasp.org/www-project-top-10-for-large-language-model-applications/).
CLAIM: NIST SP 800-122 defines PII and guidance for its protection
(source: https://csrc.nist.gov/pubs/sp/800/122/final).
INFERENCE: A three-tier classification plus redaction step materially lowers
leakage risk compared to ad-hoc copy/paste. This is the hypothesis under test.

## Workflow
1. **Inventory the approved channel**: write down the exact approved
   endpoint/model, its retention setting, and the data classes it is cleared
   for. Fill in: `APPROVED_MODEL=<name>` `RETENTION=<logs? trains?>`
   `CLEARED_CLASSES=<e.g. public, internal>`.
2. **Classify every input chunk** before it goes anywhere:
   - T1 public: safe anywhere;
   - T2 internal: cleared only for the approved endpoint;
   - T3 restricted (PII, secrets, customer data): never sent; must be
     redacted or replaced with placeholders like `<CUSTOMER_1>`.
3. **Redact with a script, not by eye**: maintain a redaction pass that
   replaces names, emails, account numbers, and internal hostnames with
   stable tokens; keep the token map local and never send it.
4. **Send only through the approved endpoint**; any tool that cannot target
   that endpoint is forbidden for T2 data. Add the approved endpoint as the
   only allowed URL in your automation config.
5. **Audit log**: append every outgoing prompt hash + data class + timestamp
   to a local ledger. Weekly, spot-check 5 entries against the redaction map.
6. **Prompt-injection guard**: when the model's answer will be acted on
   automatically, treat model output as untrusted input (see OWASP LLM01/LLM06
   framing in sources.md).

## Copy/paste policy prompt (fill-in)
```text
You are assisting with <TEAM> data classified as internal-only under
<POLICY NAME>. Rules:
1. Never ask for fields I have marked restricted.
2. If you need a restricted value to answer, say which placeholder blocks you.
3. Answer only from the provided context; mark anything you infer as INFERENCE.
Context:
<SANITIZED CONTEXT>
Question: <QUESTION>
```

## Status
**AI-SOURCED / UNTESTED.** No employer has validated this workflow; the audit
and redaction steps have not been exercised in a real compliance review.
