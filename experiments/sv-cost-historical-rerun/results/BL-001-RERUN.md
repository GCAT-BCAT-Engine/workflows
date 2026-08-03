# SV-MATH-001: Complete Invariant Characterization of ALLOW Admissibility

---

## Part I — Primitive Definitions

**Definition 1.1 (Semantic Space).** Let $\Omega$ be a compact metric space $(\Omega, d)$ called the *semantic space*, equipped with a $\sigma$-algebra $\mathcal{F}$ and a reference probability measure $\mu \in \mathcal{P}(\Omega)$.

**Definition 1.2 (Policy Manifold).** A *policy* is a measurable function $\pi : \mathcal{X} \to \mathcal{P}(\Omega)$, where $\mathcal{X}$ is a measurable input space. The set of all policies is $\Pi$.

**Definition 1.3 (Boundary Structure).** The *normative boundary* is a closed set $\partial \mathcal{B} \subset \Omega$ with the property that $\mu(\partial \mathcal{B}) = 0$ and $\Omega \setminus \partial \mathcal{B}$ decomposes as $\mathcal{A} \sqcup \mathcal{H}$, where:
- $\mathcal{A}$ is the *admissible interior* (open, $\mu$-positive),
- $\mathcal{H}$ is the *prohibited interior* (open, $\mu$-positive).

**Definition 1.4 (Geometric Boundary Preservation — GBP).** A policy $\pi$ satisfies *geometric boundary preservation* if for every $x \in \mathcal{X}$:
$$\pi(x)(\partial \mathcal{B}) = 0$$
and the support map $x \mapsto \mathrm{supp}(\pi(x))$ is upper-hemicontinuous with $\mathrm{supp}(\pi(x)) \subseteq \overline{\mathcal{A}}$ for all $x$.

**Definition 1.5 (Divergence Functional).** For $\nu, \mu \in \mathcal{P}(\Omega)$ with $\nu \ll \mu$, define the *policy divergence*:
$$D_\phi(\nu \| \mu) = \int_\Omega \phi\!\left(\frac{d\nu}{d\mu}\right) d\mu$$
where $\phi : [0,\infty) \to \mathbb{R}$ is a convex function with $\phi(1) = 0$ (an $f$-divergence generator). The canonical choice is $\phi(t) = t \log t$ (KL divergence).

**Definition 1.6 (Bounded Divergence — BD).** Fix a *reference admissible policy* $\pi^* \in \Pi$ satisfying GBP. A policy $\pi$ satisfies *bounded divergence* with constant $\delta > 0$ if:
$$\sup_{x \in \mathcal{X}} D_\phi(\pi(x) \| \pi^*(x)) \leq \delta$$

**Definition 1.7 (Ontological Type System).** Let $\mathcal{T}$ be a finite set of *semantic types* with a partial order $\leq_\mathcal{T}$ (a join-semilattice). Each $\omega \in \Omega$ carries a type assignment $\tau : \Omega \to \mathcal{T}$, assumed measurable. Define the *prohibited type set* $\mathcal{T}_{\mathcal{H}} = \{\tau(\omega) : \omega \in \mathcal{H}\}$ and the *admissible type ceiling* $T^* = \bigvee \{\tau(\omega) : \omega \in \mathcal{A}\}$ (join in $\mathcal{T}$).

**Definition 1.8 (Ontological Consistency — OC).** A policy $\pi$ satisfies *ontological consistency* if for every $x \in \mathcal{X}$ and every measurable $S \subseteq \Omega$:
$$\tau(S) \cap \mathcal{T}_{\mathcal{H}} \neq \emptyset \implies \pi(x)(S) = 0$$
where $\tau(S) = \{\tau(\omega) : \omega \in S\}$.

**Definition 1.9 (ALLOW Admissibility).** A policy $\pi \in \Pi$ is *ALLOW-admissible*, written $\pi \in \mathsf{ALLOW}$, if it satisfies all three of (GBP), (BD), and (OC).

---

## Part II — Auxiliary Lemmas

**Lemma 2.1 (GBP–OC Consistency).** If $\pi$ satisfies OC, then $\pi$ satisfies the mass condition of GBP, i.e., $\pi(x)(\mathcal{H}) = 0$ for all $x$.

*Proof.* Take $S = \mathcal{H}$. Then $\tau(S) \supseteq \mathcal{T}_{\mathcal{H}}$, so $\tau(S) \cap \mathcal{T}_{\mathcal{H}} \neq \emptyset$. OC gives $\pi(x)(\mathcal{H}) = 0$. Since $\mu(\partial\mathcal{B}) = 0$ and the decomposition $\Omega = \mathcal{A} \sqcup \partial\mathcal{B} \sqcup \mathcal{H}$ is disjoint, $\pi(x)(\mathcal{A}) = 1$. ∎

**Lemma 2.2 (GBP Closure Under Convex Combination).** If $\pi_1, \pi_2$ both satisfy GBP and $\lambda \in [0,1]$, then $\pi_\lambda(x) = \lambda \pi_1(x) + (1-\lambda)\pi_2(x)$ satisfies GBP.

*Proof.* $\pi_\lambda(x)(\partial\mathcal{B}) = \lambda \cdot 0 + (1-\lambda)\cdot 0 = 0$. Upper-hemicontinuity of the support map is preserved under convex combination with fixed closed support $\overline{\mathcal{A}}$. ∎

**Lemma 2.3 (BD Is a Metric Ball).** The set $\{\pi : D_\phi(\pi(x)\|\pi^*(x)) \leq \delta\}$ is convex and $\mathcal{F}$-measurable for each fixed $x$, by convexity of $\phi$ and measurability of the Radon-Nikodym derivative.

*Proof.* Convexity follows from the joint convexity of $f$-divergences. Measurability follows from Fubini and the fact that $\phi \circ (d\pi/d\pi^*)$ is measurable when $\pi$ is measurable. ∎

**Lemma 2.4 (OC Implies Absolute Continuity on $\mathcal{A}$).** If $\pi$ satisfies OC and $\pi^*$ satisfies GBP with $\mathrm{supp}(\pi^*(x)) = \overline{\mathcal{A}}$ for all $x$, then $\pi(x)|_{\mathcal{A}} \ll \pi^*(x)|_{\mathcal{A}}$.

*Proof.* Let $N \subseteq \mathcal{A}$ with $\pi^*(x)(N) = 0$. Since $N \subseteq \mathcal{A}$ and $\pi^*$ dominates $\mu|_{\mathcal{A}}$ (by full support), $\mu(N) = 0$. OC restricts all mass of $\pi(x)$ to $\mathcal{A}$, and within $\mathcal{A}$ the measure $\pi(x)|_{\mathcal{A}}$ is absolutely continuous with respect to $\mu|_{\mathcal{A}}$ (since $\pi$ is defined via a measurable density). Hence $\pi(x)(N) = 0$. ∎

---

## Part III — Main Theorem

**Theorem 3.1 (Necessary and Sufficient Characterization of ALLOW Admissibility).**

*Let $(\Omega, d, \mu)$, $\mathcal{B}$, $\mathcal{T}$, $\pi^*$, and $\delta > 0$ be as defined above, with $\pi^*$ fixed and $\mathrm{supp}(\pi^*(x)) = \overline{\mathcal{A}}$ for all $x$. Then:*

$$\pi \in \mathsf{ALLOW} \iff [\text{GBP}(\pi)] \;\wedge\; [\text{BD}(\pi, \delta)] \;\wedge\; [\text{OC}(\pi)]$$

*Furthermore, $\mathsf{ALLOW}$ is:*
1. *Non-empty (contains $\pi^*$).*
2. *Convex in the space of policies under pointwise mixture.*
3. *Closed under uniform limits in the total-variation topology.*
4. *Characterized by the joint constraint:*

$$\pi \in \mathsf{ALLOW} \iff \sup_{x \in \mathcal{X}}\left[D_\phi(\pi(x)\|\pi^*(x)) + \mathbf{1}_{\pi(x)(\mathcal{H})>0} \cdot \infty + \mathbf{1}_{\pi(x)(\partial\mathcal{B})>0} \cdot \infty\right] \leq \delta$$

where the indicator penalties enforce GBP and OC by convention that $\infty > \delta$.

---

## Part IV — Proof

### 4.1 Forward Direction ($\pi \in \mathsf{ALLOW} \Rightarrow$ GBP $\wedge$ BD $\wedge$ OC)

This direction is immediate by Definition 1.9, which defines $\mathsf{ALLOW}$ as the conjunction. ∎

### 4.2 Reverse Direction (GBP $\wedge$ BD $\wedge$ OC $\Rightarrow \pi \in \mathsf{ALLOW}$)

This direction is also immediate by Definition 1.9. The content of the theorem lies in the structural claims (1)–(4) and the equivalence with the penalized functional in claim (4).

### 4.3 Non-emptiness (Claim 1)

We verify $\pi^* \in \mathsf{ALLOW}$:
- **GBP**: $\pi^*$ satisfies GBP by assumption.
- **BD**: $D_\phi(\pi^*(x)\|\pi^*(x)) = \phi(1) \cdot \mu(\Omega) = 0 \leq \delta$. ✓
- **OC**: Since $\mathrm{supp}(\pi^*(x)) = \overline{\mathcal{A}}$ and $\overline{\mathcal{A}} \cap \mathcal{H} = \emptyset$ (as $\mathcal{A}$ and $\mathcal{H}$ are disjoint open sets with $\partial\mathcal{B}$ separating them), for any $S$ with $\tau(S) \cap \mathcal{T}_\mathcal{H} \neq \emptyset$ we have $S \cap \mathcal{H} \neq \emptyset$, but $\pi^*(x)(S \cap \mathcal{H}) = 0$ since $\mathcal{H} \cap \overline{\mathcal{A}} = \emptyset$ and $\pi^*$ has no mass outside $\overline{\mathcal{A}}$. Hence $\pi^*(x)(S) = 0$. ✓

Therefore $\pi^* \in \mathsf{ALLOW}$. ∎

### 4.4 Convexity (Claim 2)

Let $\pi_1, \pi_2 \in \mathsf{ALLOW}$ and $\lambda \in [0,1]$. Set $\pi_\lambda(x) = \lambda\pi_1(x) + (1-\lambda)\pi_2(x)$.

- **GBP**: By Lemma 2.2. ✓
- **BD**: By joint convexity of $f$-divergences:
$$D_\phi(\pi_\lambda(x)\|\pi^*(x)) \leq \lambda D_\phi(\pi_1(x)\|\pi^*(x)) + (1-\lambda)D_\phi(\pi_2(x)\|\pi^*(x)) \leq \lambda\delta + (1-\lambda)\delta = \delta$$
✓
- **OC**: For any $S$ with $\tau(S) \cap \mathcal{T}_\mathcal{H} \neq \emptyset$: $\pi_\lambda(x)(S) = \lambda\pi_1(x)(S) + (1-\lambda)\pi_2(x)(S) = \lambda \cdot 0 + (1-\lambda)\cdot 0 = 0$. ✓

Hence $\pi_\lambda \in \mathsf{ALLOW}$. ∎

### 4.5 Closure Under TV Limits (Claim 3)

Let $\{\pi_n\}_{n\geq 1} \subseteq \mathsf{ALLOW}$ with $\sup_x \|\pi_n(x) - \pi_\infty(x)\|_{\mathrm{TV}} \to 0$ as $n \to \infty$.

- **GBP**: For each $x$, $|\pi_\infty(x)(\partial\mathcal{B})| \leq |\pi_\infty(x)(\partial\mathcal{B}) - \pi_n(x)(\partial\mathcal{B})| + 0 \leq \|\pi_n(x)-\pi_\infty(x)\|_{\mathrm{TV}} \to 0$. Hence $\pi_\infty(x)(\partial\mathcal{B})=0$. Upper-hemicontinuity of the support map is preserved in the TV limit since $\mathrm{supp}(\pi_\infty(x)) \subseteq \overline{\mathcal{A}}$ follows from $\pi_\infty(x)(\mathcal{H})=0$ (by same argument) and $\pi_\infty(x)(\partial\mathcal{B})=0$. ✓

- **BD**: Lower semicontinuity of $f$-divergences in the weak topology (and hence TV topology) gives:
$$D_\phi(\pi_\infty(x)\|\pi^*(x)) \leq \liminf_{n\to\infty} D_\phi(\pi_n(x)\|\pi^*(x)) \leq \delta$$
✓

- **OC**: For any $S$ with $\tau(S)\cap\mathcal{T}_\mathcal{H}\neq\emptyset$: $\pi_\infty(x)(S) = \lim_{n\to\infty}\pi_n(x)(S) = 0$ (since $|\pi_\infty(x)(S) - \pi_n(x)(S)| \leq \|\pi_n(x)-\pi_\infty(x)\|_{\mathrm{TV}} \to 0$ and each $\pi_n(x)(S)=0$). ✓

Hence $\pi_\infty \in \mathsf{ALLOW}$. ∎

### 4.6 Penalized Functional Equivalence (Claim 4)

Define $F(\pi, x) = D_\phi(\pi(x)\|\pi^*(x)) + \mathbf{1}_{\pi(x)(\mathcal{H})>0}\cdot\infty + \mathbf{1}_{\pi(x)(\partial\