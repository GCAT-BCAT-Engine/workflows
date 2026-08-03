SECTION 4: MATHEMATICAL PROOF

Fix a canonical engine `e` and state `s`. Let

`G := GBP(e,s)`, `B := BD(e,s)`, `O := OC(e,s)`, and `J := G ∧ B ∧ O`.

The evaluator is defined by the exhaustive Boolean-style case distinction

`evaluate(e,s) = if J then ALLOW else DENY`,

and admissibility is defined by

`Admissible(e,s) := evaluate(e,s) = ALLOW`.

**Necessity.** Assume `Admissible(e,s)`. Then `evaluate(e,s) = ALLOW`. Suppose for contradiction that `J` is false. The evaluator must then take its false branch, so `evaluate(e,s) = DENY`. Since `ALLOW` and `DENY` are distinct constructors, this contradicts admissibility. Therefore `J` is true. Expanding `J` yields `GBP(e,s) ∧ BD(e,s) ∧ OC(e,s)`.

**Sufficiency.** Assume `GBP(e,s) ∧ BD(e,s) ∧ OC(e,s)`. This is exactly `J`. The evaluator therefore takes its true branch and returns `ALLOW`. Hence `evaluate(e,s) = ALLOW`, which is `Admissible(e,s)` by definition.

Combining both implications gives

`Admissible(e,s) ↔ GBP(e,s) ∧ BD(e,s) ∧ OC(e,s)`.

**Completeness relative to the evaluator.** A condition is complete for a decision procedure when satisfaction of that condition is equivalent to acceptance by the procedure. Here acceptance is definitionally controlled by `J`, so the conjunction is complete for this evaluator. Adding a fourth conjunct would change the evaluator unless that conjunct were already derivable from `J`; removing any conjunct would likewise define a different acceptance condition.

This completeness result is intentionally scoped. It proves the theorem for the canonical repository specification and for any conforming implementation shown to be extensionally equivalent to it. It does not infer that an unexamined production implementation has no additional state, invariant, authorization rule, or execution constraint. ∎
