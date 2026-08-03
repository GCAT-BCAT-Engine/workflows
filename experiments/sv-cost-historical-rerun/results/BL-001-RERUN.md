# SV-MATH-001: Complete Invariant Characterization of ALLOW Admissibility

---

## §1. Primitive Vocabulary and Definitions

**Definition 1.1 (Semantic Space).** Let $\mathcal{U}$ be a fixed countable universe of *discourse tokens*. A *semantic space* is a metric space $(S, d_S)$ together with a measurable map $\phi : \mathcal{U}^* \to S$ called the *embedding functor*, where $\mathcal{U}^*$ denotes finite strings over $\mathcal{U}$.

**Definition 1.2 (Ontological Region).** An *ontological region* is a pair $\mathcal{O} = (R, \partial R)$ where $R \subseteq S$ is a compact connected subset and $\partial R$ is its topological boundary in $S$. The *interior* is $\text{int}(R) = R \setminus \partial R$.

**Definition 1.3 (Policy Boundary System).** A *policy boundary system* is a triple $\mathcal{B} = (S, \{\mathcal{O}_i\}_{i \in I}, \mathcal{F})$ where:
- $\{R_i\}_{i \in I}$ is a locally finite cover of $S$ by ontological regions with $I$ a countable index set,
- $\mathcal{F} = \{f_j : S \to \mathbb{R}\}_{j \in J}$ is a finite family of *boundary functionals*, each $f_j$ Lipschitz continuous with constant $L_j < \infty$,
- The *admissible region* is $\mathcal{A} = \bigcap_{j \in J} f_j^{-1}((-\infty, 0])$.

**Definition 1.4 (Response Map).** A *response map* is a measurable function $\rho : \mathcal{U}^* \to \mathcal{U}^*$. Its *semantic image* is $\hat{\rho} = \phi \circ \rho : \mathcal{U}^* \to S$.

**Definition 1.5 (Geometric Boundary Preservation — GBP).** A response map $\rho$ satisfies *GBP* with respect to $\mathcal{B}$ if for every input $u \in \mathcal{U}^*$:

$$\phi(u) \in \mathcal{A} \implies \hat{\rho}(u) \in \mathcal{A}$$

and moreover the map $\hat{\rho}$ does not map the boundary $\partial \mathcal{A} = \bigcup_{j \in J} f_j^{-1}(\{0\})$ to $\text{ext}(\mathcal{A}) = S \setminus \mathcal{A}$:

$$\forall u : \phi(u) \in \partial\mathcal{A} \implies \hat{\rho}(u) \in \mathcal{A}.$$

*Remark.* GBP is a one-directional closure condition. It is not required that $\phi(u) \notin \mathcal{A}$ forces $\hat{\rho}(u) \notin \mathcal{A}$; inadmissible inputs may receive admissible responses (refusals, corrections).

**Definition 1.6 (Divergence Measure).** Let $\mu$ be a reference probability measure on $S$ (e.g., induced by empirical distribution over $\mathcal{U}^*$). For a response map $\rho$, define the *semantic divergence* as:

$$D(\rho) = \sup_{u \in \mathcal{U}^*} d_S\!\left(\phi(u),\, \hat{\rho}(u)\right).$$

**Definition 1.7 (Bounded Divergence — BD).** A response map $\rho$ satisfies *BD* with bound $\delta > 0$ if:

$$D(\rho) \leq \delta.$$

**Definition 1.8 (Ontological Consistency — OC).** For each ontological region $\mathcal{O}_i = (R_i, \partial R_i)$, define the *ontological assignment* $\omega : S \to 2^I$ by $\omega(x) = \{i \in I : x \in R_i\}$. A response map $\rho$ satisfies *OC* if:

$$\forall u \in \mathcal{U}^*, \quad \omega(\phi(u)) \cap \omega(\hat{\rho}(u)) \neq \emptyset$$

and additionally, for every $i \in I$:

$$\phi(u) \in R_i \implies \hat{\rho}(u) \notin \bigcup_{k \in \mathcal{E}(i)} R_k$$

where $\mathcal{E}(i) \subseteq I$ is the *exclusion set* of region $i$, a given parameter of $\mathcal{B}$ encoding mutually incompatible ontological categories (e.g., "factual" vs "fabrication", "safe" vs "harmful").

**Definition 1.9 (ALLOW Admissibility).** A response map $\rho$ is *ALLOW-admissible* with respect to $(\mathcal{B}, \delta)$ if and only if $\rho$ satisfies GBP, BD with bound $\delta$, and OC simultaneously. We write $\rho \in \text{ALLOW}(\mathcal{B}, \delta)$.

---

## §2. Auxiliary Constructions

**Definition 2.1 (GBP Tube).** For $\delta > 0$, define the *$\delta$-tube* around $\mathcal{A}$:

$$\mathcal{T}_\delta(\mathcal{A}) = \{x \in S : d_S(x, \mathcal{A}) \leq \delta\}.$$

**Definition 2.2 (Ontological Compatibility Graph).** Define the directed graph $G_\mathcal{O} = (I, E_\mathcal{O})$ where $(i, k) \in E_\mathcal{O}$ iff $k \notin \mathcal{E}(i)$ (i.e., $k$ is ontologically compatible as a target when source is $i$).

**Definition 2.3 (Combined Admissibility Kernel).** Define:

$$\mathcal{K}(\mathcal{B}, \delta) = \left\{(x, y) \in S \times S \;\middle|\; \begin{array}{l} \bigl(x \in \mathcal{A} \implies y \in \mathcal{A}\bigr) \\ \wedge\; d_S(x, y) \leq \delta \\ \wedge\; \omega(x) \cap \omega(y) \neq \emptyset \\ \wedge\; \forall i \in \omega(x),\, \omega(y) \cap \mathcal{E}(i) = \emptyset \end{array}\right\}.$$

---

## §3. Assumptions (Clearly Separated)

The following are **assumed** as axiomatic conditions on the instantiation; they are not proved here.

> **A1.** $(S, d_S)$ is a complete separable metric space.
>
> **A2.** The embedding functor $\phi$ is measurable and has bounded image on any finite input length class.
>
> **A3.** Each boundary functional $f_j$ is Lipschitz with constant $L_j < \infty$; in particular $\mathcal{A}$ is closed (hence compact when $S$ is locally compact).
>
> **A4.** Each ontological region $R_i$ is a closed set; the cover $\{R_i\}$ is locally finite.
>
> **A5.** The exclusion sets $\mathcal{E}(i)$ are given parameters of $\mathcal{B}$ and are assumed to be reflexively consistent: $i \notin \mathcal{E}(i)$ for all $i$ (a region does not exclude itself).
>
> **A6.** The bound $\delta > 0$ is chosen such that $\mathcal{T}_\delta(\mathcal{A}) \cap \bigcup_{j \in J} f_j^{-1}((0, \infty))$ is nonempty, i.e., the tube is non-trivially larger than $\mathcal{A}$ in at least one direction. (Ensures BD is not vacuously equivalent to GBP.)
>
> **A7.** The response map $\rho$ is given; its measurability is assumed.

---

## §4. Main Theorem (Necessary and Sufficient Characterization)

**Theorem 4.1 (Complete Invariant Characterization of ALLOW Admissibility).**

*Under assumptions A1–A7, a response map $\rho$ is ALLOW-admissible, i.e., $\rho \in \text{ALLOW}(\mathcal{B}, \delta)$, if and only if:*

$$\forall u \in \mathcal{U}^*,\quad \bigl(\phi(u),\, \hat{\rho}(u)\bigr) \in \mathcal{K}(\mathcal{B}, \delta). \tag{$\star$}$$

---

### §4.1 Proof: Forward Direction ($\Rightarrow$)

**Claim.** If $\rho \in \text{ALLOW}(\mathcal{B}, \delta)$ then $(\star)$ holds.

*Proof.* Assume $\rho \in \text{ALLOW}(\mathcal{B}, \delta)$. Fix arbitrary $u \in \mathcal{U}^*$. Let $x = \phi(u)$ and $y = \hat{\rho}(u)$. We verify each conjunct of $\mathcal{K}(\mathcal{B}, \delta)$.

**(K1)** $x \in \mathcal{A} \implies y \in \mathcal{A}$: This is exactly GBP (Definition 1.5, first clause). Since $\rho$ satisfies GBP, the implication holds for all $u$. $\checkmark$

**(K2)** $d_S(x, y) \leq \delta$: By BD (Definition 1.7), $D(\rho) = \sup_{u'} d_S(\phi(u'), \hat{\rho}(u')) \leq \delta$. Since the supremum is bounded by $\delta$, every pointwise value satisfies $d_S(x, y) \leq \delta$. $\checkmark$

**(K3)** $\omega(x) \cap \omega(y) \neq \emptyset$: By OC (Definition 1.8, first clause), for all $u$, $\omega(\phi(u)) \cap \omega(\hat{\rho}(u)) \neq \emptyset$, i.e., $\omega(x) \cap \omega(y) \neq \emptyset$. $\checkmark$

**(K4)** $\forall i \in \omega(x),\, \omega(y) \cap \mathcal{E}(i) = \emptyset$: By OC (Definition 1.8, second clause), for every $i \in I$ with $x \in R_i$ (equivalently, $i \in \omega(x)$), we have $y \notin \bigcup_{k \in \mathcal{E}(i)} R_k$. Since $y \notin \bigcup_{k \in \mathcal{E}(i)} R_k$ means $y \notin R_k$ for all $k \in \mathcal{E}(i)$, equivalently $k \notin \omega(y)$ for all $k \in \mathcal{E}(i)$, we get $\omega(y) \cap \mathcal{E}(i) = \emptyset$. $\checkmark$

Since all four conjuncts hold, $(x, y) \in \mathcal{K}(\mathcal{B}, \delta)$. Since $u$ was arbitrary, $(\star)$ holds. $\blacksquare$

---

### §4.2 Proof: Reverse Direction ($\Leftarrow$)

**Claim.** If $(\star)$ holds then $\rho \in \text{ALLOW}(\mathcal{B}, \delta)$.

*Proof.* Assume $(\star)$: for all $u \in \mathcal{U}^*$, $(\phi(u), \hat{\rho}(u)) \in \mathcal{K}(\mathcal{B}, \delta)$. We verify GBP, BD, and OC.

**GBP:** Let $u \in \mathcal{U}^*$ be arbitrary.

*First clause:* Suppose $\phi(u) \in \mathcal{A}$. By $(\star)$, (K1) applies: $\phi(u) \in \mathcal{A} \implies \hat{\rho}(u) \in \mathcal{A}$. Hence $\hat{\rho}(u) \in \mathcal{A}$. $\checkmark$

*Second clause (boundary):* Suppose $\phi(u) \in \partial\mathcal{A}$. Since $\partial\mathcal{A} \subseteq \mathcal{A}$ (as $\mathcal{A}$ is closed by A3), we have $\phi(u) \in \mathcal{A}$. By (K1), $\hat{\rho}(u) \in \mathcal{A}$, satisfying the boundary condition of Definition 1.5. $\checkmark$

Since $u$ was arbitrary, GBP holds.

**BD:** For all $u \in \mathcal{U}^*$, $(\star)$ gives (K2): $d_S(\phi(u), \hat{\rho}(u)) \leq \delta$. Taking the supremum over all $u$:

$$D(\rho) = \sup_{u \in \mathcal{U}^*} d_S(\phi(u), \hat{\rho}(u)) \leq \delta.$$

Hence BD holds with bound $\delta$. $\checkmark$

**OC:**

*First clause:* For all $u$, $(\star)$ gives (K3): $\omega(\phi(u)) \cap \omega(\hat{\rho}(u)) \neq \emptyset$. This is exactly the first clause of OC. $\checkmark$

*Second clause:* Fix $u$ and $i \in I$ with $\phi(u) \in R_i$, i.e., $i \in \omega(\phi(u))$. By $(\star)$, (K4) gives $\omega(\hat{\rho}(u)) \cap \mathcal{E}(i) = \emptyset$. This means for all $k \in \mathcal{E}(i)$, $k \notin \omega(\hat{\rho}(u))$, i.e., $\hat{\rho}(u) \notin R_k$ for all $k \in \mathcal{E}(i)$. Hence $\hat{\rho}(u) \notin \bigcup_{k \in \mathcal{E}(i)} R_k$, which is exactly the second clause of OC. $\checkmark$

Since GBP, BD, and OC all hold, $\rho \in \text{ALLOW}(\mathcal{B}, \delta)$. $\blacksquare$

---

### §4.3 Biconditional Synthesis

Combining §4.1 and §4.2:

$$\rho \in \text{ALLOW}(\mathcal{B}, \delta) \iff \forall u \in \mathcal{U}^*,\; \bi