# Privacy & security notes
- Eval inputs must be synthetic or sanitized; never real customer data.
- Snapshots contain model outputs — store with the same confidentiality as
  the inputs that produced them.
- Judge-model calls send eval data; keep judge and primary model under the
  same data-usage approval (see candidate kit 02).
