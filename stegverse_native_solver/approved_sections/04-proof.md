SECTION 4: MATHEMATICAL PROOF

Fix `e` and `s` and abbreviate `J := GBP(e,s) ∧ BD(e,s) ∧ OC(e,s)`.

By definition, `evaluate(e,s)` is `ALLOW` exactly in the branch where `J` is true, and `DENY` otherwise. Also by definition, `Admissible(e,s)` is the proposition `evaluate(e,s) = ALLOW`.

**Forward direction.** Assume `Admissible(e,s)`. If `J` were false, evaluation would select `DENY`, contradicting `evaluate(e,s) = ALLOW`. Therefore `J` holds.

**Reverse direction.** Assume `J`. Evaluation selects the `ALLOW` branch, so `evaluate(e,s) = ALLOW`; hence `Admissible(e,s)`.

Thus `Admissible(e,s) ↔ J`, which expands to the required conjunction. No fourth predicate is required for this evaluator because its complete decision condition is exactly `J`. This is evaluator completeness, not an empirical claim that an unverified external engine has no additional invariant. ∎
