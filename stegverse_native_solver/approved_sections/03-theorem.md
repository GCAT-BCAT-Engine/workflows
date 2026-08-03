SECTION 3: THEOREM STATEMENT

**SV-MATH-001 — Canonical ALLOW completeness theorem**

For every canonical engine `e` and state `s`:

`Admissible(e,s) ↔ GBP(e,s) ∧ BD(e,s) ∧ OC(e,s)`.

The theorem is necessary and sufficient by construction of the canonical evaluator. Its transfer to another implementation requires an independently checked conformance relation between that implementation and `evaluate`.
