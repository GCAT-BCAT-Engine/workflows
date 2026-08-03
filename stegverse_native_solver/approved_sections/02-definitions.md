SECTION 2: DEFINITIONS

For an engine `e` and state `s`:

- `GBP(e,s)` holds when both `e.gcat s` and `e.bcat s` preserve and reflect the boundary predicate `e.boundary s`.
- `BD(e,s)` holds when there exists `K : Nat` such that every entity's distance from its GCAT image and BCAT image is at most `K`.
- `OC(e,s)` holds when both transformations preserve each entity's ontology label.
- `Joint(e,s) := GBP(e,s) ∧ BD(e,s) ∧ OC(e,s)`.
- `evaluate(e,s)` returns `ALLOW` when `Joint(e,s)` and otherwise returns `DENY`.
- `Admissible(e,s)` means `evaluate(e,s) = ALLOW`.

These definitions make the proof obligation explicit and executable.
