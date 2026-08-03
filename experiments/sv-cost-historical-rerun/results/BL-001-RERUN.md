# SV-MATH-001: Complete Invariant Characterization of ALLOW Admissibility

---

## §1. Primitive Definitions and Abstract Framework

**Definition 1.1 (Policy Space).** Let $\mathcal{P}$ be a compact metric space of policy configurations with metric $d_\mathcal{P}$. A *policy trajectory* is a continuous map $\gamma: [0,1] \to \mathcal{P}$.

**Definition 1.2 (Semantic Domain).** Let $\mathcal{S}$ be a complete separable metric space of semantic states. Define the *semantic evaluation map* $\Phi: \mathcal{P} \to \mathcal{M}(\mathcal{S})$, where $\mathcal{M}(\mathcal{S})$ denotes the space of Borel probability measures on $\mathcal{S}$, equipped with the Wasserstein-1 metric $W_1$.

**Definition 1.3 (Admissibility Boundary).** The *admissibility boundary* is a closed set $\partial\mathcal{A} \subset \mathcal{P}$ such that:
- The *interior admissible region* is $\mathcal{A}^\circ = \mathcal{P} \setminus \partial\mathcal{A}$ (open).
- The *inadmissible region* is $\mathcal{I} = \mathcal{P} \setminus \overline{\mathcal{A}}$ where $\overline{\mathcal{A}} = \mathcal{A}^\circ \cup \partial\mathcal{A}$.

**Definition 1.4 (Geometric Boundary Preservation — GBP).** A policy map $f: \mathcal{P} \to \mathcal{P}$ satisfies *Geometric Boundary Preservation* if:

$$\text{GBP}(f) \;\equiv\; f(\partial\mathcal{A}) \subseteq \partial\mathcal{A} \;\land\; f(\mathcal{A}^\circ) \subseteq \overline{\mathcal{A}}$$

That is, $f$ maps boundary points to boundary points and interior admissible points to the closed admissible region. Equivalently, $f$ does not map any admissible point into $\mathcal{I}$.

**Definition 1.5 (Divergence Functional).** For measures $\mu, \nu \in \mathcal{M}(\mathcal{S})$, define the *semantic divergence* $\Delta: \mathcal{M}(\mathcal{S}) \times \mathcal{M}(\mathcal{S}) \to [0, \infty]$ by:

$$\Delta(\mu, \nu) = W_1(\mu, \nu) + \text{KL}(\mu \| \nu)$$

where $\text{KL}(\mu \| \nu) = \int \log\frac{d\mu}{d\nu} \, d\mu$ when $\mu \ll \nu$, and $+\infty$ otherwise.

**Definition 1.6 (Bounded Divergence — BD).** A policy $p \in \mathcal{P}$ has *Bounded Divergence* with constant $K > 0$ relative to a reference measure $\mu_0 = \Phi(p_0)$ for a designated $p_0 \in \mathcal{A}^\circ$ if:

$$\text{BD}(p, K) \;\equiv\; \Delta(\Phi(p), \mu_0) \leq K$$

**Definition 1.7 (Ontological Frame).** An *ontological frame* is a tuple $\mathcal{O} = (E, R, V, \models)$ where:
- $E$ is a set of entities (the *ontology*),
- $R \subseteq E \times E$ is a binary relation (the *commitment relation*),
- $V: E \to \{0,1\}$ is a valuation,
- $\models\; \subseteq \mathcal{P} \times \mathcal{O}$ is the *satisfaction relation*: $p \models \mathcal{O}$ means policy $p$ is consistent with frame $\mathcal{O}$.

**Definition 1.8 (Ontological Consistency — OC).** A policy $p \in \mathcal{P}$ is *Ontologically Consistent* with respect to a fixed frame $\mathcal{O}_0$ if:

$$\text{OC}(p) \;\equiv\; p \models \mathcal{O}_0 \;\land\; \forall e \in E,\; \bigl[(p \models \mathcal{O}_0) \Rightarrow \neg(p \models \mathcal{O}_0[V(e) \mapsto \neg V(e)])\bigr]$$

The second conjunct states that $p$ does not simultaneously satisfy $\mathcal{O}_0$ under complementary valuations — no internal ontological contradiction is induced by $p$.

**Definition 1.9 (ALLOW Admissibility).** A policy $p \in \mathcal{P}$ is *ALLOW-admissible* — written $\text{ALLOW}(p)$ — if there exists a policy map $f_p: \mathcal{P} \to \mathcal{P}$ and constant $K_p > 0$ such that:

$$\text{ALLOW}(p) \;\equiv\; \text{GBP}(f_p) \;\land\; \text{BD}(p, K_p) \;\land\; \text{OC}(p) \;\land\; f_p(p) \in \overline{\mathcal{A}}$$

---

## §2. Auxiliary Lemmas

**Lemma 2.1 (GBP Closure under Composition).** If $f, g: \mathcal{P} \to \mathcal{P}$ both satisfy GBP, then $f \circ g$ satisfies GBP.

*Proof.* Let $q \in \partial\mathcal{A}$. By $\text{GBP}(g)$: $g(q) \in \partial\mathcal{A}$. By $\text{GBP}(f)$: $f(g(q)) \in \partial\mathcal{A}$. Hence $(f \circ g)(\partial\mathcal{A}) \subseteq \partial\mathcal{A}$. Let $q \in \mathcal{A}^\circ$. By $\text{GBP}(g)$: $g(q) \in \overline{\mathcal{A}}$. If $g(q) \in \mathcal{A}^\circ$, then $f(g(q)) \in \overline{\mathcal{A}}$ by $\text{GBP}(f)$. If $g(q) \in \partial\mathcal{A}$, then $f(g(q)) \in \partial\mathcal{A} \subseteq \overline{\mathcal{A}}$. Thus $(f \circ g)(\mathcal{A}^\circ) \subseteq \overline{\mathcal{A}}$. $\square$

**Lemma 2.2 (BD Transitivity via Triangle Inequality).** If $\text{BD}(p, K_1)$ and $\text{BD}(q, K_2)$ hold with the same reference $\mu_0$, then $W_1(\Phi(p), \Phi(q)) \leq K_1 + K_2$.

*Proof.* By the triangle inequality of $W_1$:
$$W_1(\Phi(p), \Phi(q)) \leq W_1(\Phi(p), \mu_0) + W_1(\mu_0, \Phi(q)) \leq K_1 + K_2$$
since $W_1(\mu, \nu) \leq \Delta(\mu,\nu)$ for all $\mu, \nu$. $\square$

**Lemma 2.3 (OC Excludes Inadmissibility via Valuation Stability).** Suppose the ontological frame $\mathcal{O}_0$ encodes the admissibility predicate — i.e., for all $p \in \mathcal{P}$: $p \models \mathcal{O}_0 \Rightarrow p \in \overline{\mathcal{A}}$. Then $\text{OC}(p) \Rightarrow p \in \overline{\mathcal{A}}$.

*Proof.* By hypothesis, $\text{OC}(p)$ includes $p \models \mathcal{O}_0$, which by the encoding assumption gives $p \in \overline{\mathcal{A}}$. $\square$

**Lemma 2.4 (Compactness of Admissible Sublevel Sets).** For any $K > 0$, the set

$$\mathcal{B}_K = \{p \in \overline{\mathcal{A}} : \Delta(\Phi(p), \mu_0) \leq K\}$$

is compact when $\Phi$ is continuous and $\overline{\mathcal{A}}$ is closed in the compact space $\mathcal{P}$.

*Proof.* Since $\mathcal{P}$ is compact and $\overline{\mathcal{A}}$ is closed, $\overline{\mathcal{A}}$ is compact. The map $p \mapsto \Delta(\Phi(p), \mu_0)$ is lower semicontinuous (as $\Delta$ includes KL divergence, which is lower semicontinuous in the weak topology, and $W_1$ is continuous). Hence the sublevel set $\{p : \Delta(\Phi(p),\mu_0) \leq K\}$ is closed, and its intersection with the compact set $\overline{\mathcal{A}}$ is compact. $\square$

---

## §3. Main Theorem

### Theorem 3.1 (Complete Invariant Characterization of ALLOW Admissibility)

**Assumptions (A):**
- (A1) $\mathcal{P}$ is a compact metric space; $\overline{\mathcal{A}}$ is closed, $\mathcal{A}^\circ$ is open, $\partial\mathcal{A}$ is closed.
- (A2) $\Phi: \mathcal{P} \to \mathcal{M}(\mathcal{S})$ is continuous in the $W_1$ topology.
- (A3) The ontological frame $\mathcal{O}_0$ is *admissibility-encoding*: $\forall p \in \mathcal{P},\; p \models \mathcal{O}_0 \Rightarrow p \in \overline{\mathcal{A}}$.
- (A4) The admissibility boundary $\partial\mathcal{A}$ is *non-vacuous*: $\partial\mathcal{A} \neq \emptyset$.
- (A5) The identity map $\text{id}_\mathcal{P}$ satisfies $\text{GBP}(\text{id}_\mathcal{P})$ — i.e., $\text{id}$ preserves all regions (trivially verified).

**Statement.** Under assumptions (A1)–(A5), for any policy $p \in \mathcal{P}$:

$$\boxed{\text{ALLOW}(p) \;\iff\; p \in \overline{\mathcal{A}} \;\land\; \exists K > 0,\; \Delta(\Phi(p), \mu_0) \leq K \;\land\; \text{OC}(p)}$$

---

### Proof of the Forward Direction ($\Rightarrow$)

**Claim:** $\text{ALLOW}(p) \Rightarrow p \in \overline{\mathcal{A}} \land \exists K > 0,\, \Delta(\Phi(p), \mu_0) \leq K \land \text{OC}(p)$.

Assume $\text{ALLOW}(p)$. By Definition 1.9, there exists $f_p$ and $K_p > 0$ such that:

**(i) $p \in \overline{\mathcal{A}}$:** We have $\text{GBP}(f_p)$ and $f_p(p) \in \overline{\mathcal{A}}$. We need $p \in \overline{\mathcal{A}}$. Suppose for contradiction $p \in \mathcal{I} = \mathcal{P} \setminus \overline{\mathcal{A}}$. Since $\mathcal{I}$ is open (complement of closed $\overline{\mathcal{A}}$) and $\mathcal{I} \cap \mathcal{A}^\circ = \emptyset$, $\mathcal{I} \cap \partial\mathcal{A} = \emptyset$, we have $p \notin \mathcal{A}^\circ$ and $p \notin \partial\mathcal{A}$. But also $\text{OC}(p)$ holds by assumption, and by Lemma 2.3 under (A3), $\text{OC}(p) \Rightarrow p \in \overline{\mathcal{A}}$, contradicting $p \in \mathcal{I}$. Therefore $p \in \overline{\mathcal{A}}$.

**(ii) $\Delta(\Phi(p), \mu_0) \leq K_p$:** This is $\text{BD}(p, K_p)$, which is directly a conjunct of $\text{ALLOW}(p)$ by Definition 1.9. Since $K_p > 0$ exists by assumption, $\exists K > 0$ such that $\Delta(\Phi(p), \mu_0) \leq K$. $\square_{\text{(ii)}}$

**(iii) $\text{OC}(p)$:** Directly a conjunct of $\text{ALLOW}(p)$. $\square_{\text{(iii)}}$

Forward direction established. $\square_\Rightarrow$

---

### Proof of the Reverse Direction ($\Leftarrow$)

**Claim:** $p \in \overline{\mathcal{A}} \land \exists K > 0,\, \Delta(\Phi(p), \mu_0) \leq K \land \text{OC}(p) \Rightarrow \text{ALLOW}(p)$.

Assume the right-hand side. We must produce $f_p$ and $K_p > 0$ witnessing Definition 1.9.

**(Construction of $f_p$):** Define $f_p = \text{id}_\mathcal{P}$. By (A5), $\text{id}_\mathcal{P}$ satisfies $\text{GBP}(\text{id}_\mathcal{P})$:
- $\text{id}(\partial\mathcal{A}) = \partial\mathcal{A} \subseteq \partial\mathcal{A}$. ✓
- $\text{id}(\mathcal{A}^\circ) = \mathcal{A}^\circ \subseteq \overline{\mathcal{A}}$. ✓

So $\text{GBP}(f_p)$ holds. $\square_{\text{GBP}}$

**(BD holds):** By assumption, $\exists K > 0$ with $\Delta(\Phi(p), \mu_0) \leq K$. Set $K_p = K$. Then $\text{BD}(p, K_p)$ holds. $\square_{\text{BD}}$

**(OC holds):** By assumption directly. $\square_{\text{OC}}$

**(Final conjunct $f_p(p) \in \overline{\mathcal{A}}$):** Since $f