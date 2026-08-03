SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY

SV-MATH-001 is formalized against a canonical GCAT/BCAT evaluator, not an unspecified production implementation.

1. An engine has entities, states, GCAT and BCAT endomorphisms, a state-indexed boundary predicate, a natural-number divergence measure, and an ontology label.
2. Geometric boundary preservation means GCAT and BCAT preserve and reflect boundary membership.
3. Bounded divergence means one finite natural-number bound applies to both transformations at the selected state.
4. Ontological consistency means GCAT and BCAT preserve ontology labels.
5. The canonical evaluator returns `ALLOW` exactly when all three predicates hold.
6. A deployed implementation inherits the theorem only after extensional conformance to this evaluator is established.

This is a repository-native formal specification. It does not establish that every production GCAT/BCAT implementation already conforms to it.
