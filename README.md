# ⭐ Shunyaya Structural Universal Mathematics — Structural Distance (SSUM-SD)

**Redefining Distance as Structural Cost, Not Just Length**

![GitHub stars](https://img.shields.io/github/stars/OMPSHUNYAYA/SSUM-Structural-Distance?style=flat&color=brightgreen)
![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-brightgreen.svg)

**Deterministic • Structural Distance • Trajectory Geometry • Reproducible Metrics • Observation-Only**

---

## 🔎 What Is Structural Distance?

**Structural Distance (SSUM-SD)** is a deterministic mathematical system that measures **how costly motion is structurally**, not merely how far it moves numerically.

Classical distance answers:

- How far did we move?
- How close are we to a target?

Structural Distance answers:

- How far did this motion travel through **structural space**?
- How much **permission and resistance** accumulated during motion?
- Did **collapse pressure** rise even if motion appeared bounded?

Structural Distance does **not** modify solvers, algorithms, or geometry.

It observes structural cost through **SSUM structural channels** and reports **reproducible metrics** that remain identical across machines.

There are:

- no probabilistic assumptions
- no training
- no heuristics
- no hidden state

Everything is **deterministic** and **audit-friendly**.

---

## 🔗 Quick Links

### **Docs**
- [Concept Flyer (PDF)](docs/Concept-Flyer_SSUM-SD_v1.2.pdf)
- [Full Specification (PDF)](docs/SSUM-SD_v1.2.pdf)
- [Quickstart Guide](docs/Quickstart.md)
- [FAQ](docs/FAQ.md)

### **Python Scripts**
- [`structural_distance_extract.py`](scripts/structural_distance_extract.py) — structural distance from iteration traces (CSV → summary)
- [`structural_efficiency.py`](scripts/structural_efficiency.py) — structural efficiency summaries
- [`structural_distance_pisa.py`](scripts/structural_distance_pisa.py) — structural distance on real geometry aggregates (Pisa)

### **Browser Demo**
- [Structural_Attention_Distance.html](demo/Structural_Attention_Distance.html) — deterministic Structural Attention with Structural Distance regularization

---

## 🎯 Problem Statement — Why Classical Distance Misses Meaning

Classical distance measures **magnitude**:

- Euclidean length
- step size
- residual norm
- error magnitude

But real mathematical and geometric behavior often violates the assumption that **distance equals progress**:

- iterations can move very little yet accumulate collapse pressure
- iterations can move far while remaining structurally viable
- bounded non-closure is labeled “failure” without explanation
- real-world geometry can be asymmetric yet structurally stable

Classical distance reports **how much motion occurred**.  
It does not explain **how costly that motion was structurally**.

---

## 📐 Structural Distance — Core Definition

Structural Distance reframes distance as **trajectory cost through structural space**.

Let the structural state at step `k` be:

`(m_k, a_k, s_k)`

with hyperbolic structural channels:

`u_k = atanh(clamp(a_k))`  
`v_k = atanh(clamp(s_k))`

### Per-step Structural Distance

Between successive steps `k−1` and `k`:

`D_k = sqrt((m_k - m_{k-1})^2 + (u_k - u_{k-1})^2 + (v_k - v_{k-1})^2)`

### Cumulative Structural Distance

`L_struct = sum_{k=1..N} D_k`

### Classical Distance

`L_classical = sum_{k=1..N} |m_k - m_{k-1}|`

### Structural Posture (Not Distance)

`R_k = sqrt(u_k^2 + v_k^2)`  
`Psi_k = 0.5 * (u_k^2 + v_k^2)`

**Interpretation:**

- `D_k` measures structural space traversed per step
- `L_struct` measures total structural cost of the trajectory
- `R_k` measures instantaneous deviation from neutrality
- `Psi_k` measures accumulated structural posture

Distance becomes **interpretable as viability and resistance**, not just magnitude.

---

## ⚙️ Implementation Note — Practical Traversal Completion

In the reference implementation, cumulative Structural Distance is accumulated for `n−1` full structural transitions, followed by a final traversal completion term:

`L_struct_practical = (sum_{k=1..n-1} D_k) + |m_n - m_{n-1}|`

This is intentional and deterministic:

- final numerical motion is fully accounted for
- plateau endings are compensated exactly
- no artificial structural transition is implied

Any omitted final `(u, v)` contribution is negligible in convergent regimes and does not affect comparative interpretation.

---

## 📐 Structural Efficiency

Structural efficiency is defined as:

`eta = L_struct / L_classical`

**Interpretation:**

- `eta ≈ 1` → structurally efficient motion
- `eta > 1` → resistance accumulates faster than displacement
- `eta >> 1` → collapse pressure dominates
- `eta < 1` → structurally assisted motion (rare but possible)

This ratio is **diagnostic**, not evaluative.

---

## 🧪 What SSUM-SD Demonstrates (Validated Tests)

### 1) Iterative Root-Finding Traces (Deterministic)

Structural Distance computed from canonical iteration traces reveals:

- closed cases accumulate small `L_struct`
- roaming or non-closing cases accumulate larger `L_struct`
- structural cost grows independently of step size

---

### 2) Real-World Geometry Validation (Leaning Tower of Pisa)

Applied to real LiDAR-derived geometry aggregates, Structural Distance shows:

- bounded structural distance
- stable structural potential
- no collapse signature despite visible tilt

This confirms:

**stability is not symmetry**  
**balance is structural, not visual**

---

### 3) Structural Attention with Distance Regularization (Browser)

Structural Distance integrated into deterministic Structural Attention:

Baseline score:

`score = m + a + s`

Distance-regularized score:

`score_B = score - gamma * D`

This demonstrates:

- distant candidates are structurally penalized
- close candidates gain relative weight
- ranking shifts remain fully explainable
- no training or probability is involved

---

## ▶️ Running SSUM-SD (Python)

### 1) Structural Distance extraction

`python structural_distance_extract.py --in x2_minus_2_trace.csv x2_plus_1_trace.csv x4_plus_1_trace.csv --out structural_distance_summary.csv`

Produces:

- `L_classical`
- `L_struct`
- `max_R`
- `max_Psi`

---

### 2) Structural efficiency summary

`python structural_efficiency.py --in x2_minus_2_trace.csv x2_plus_1_trace.csv x4_plus_1_trace.csv --out structural_efficiency_summary.csv`

Outputs:

- `eta`
- `L_classical`
- `L_struct`
- `max_R`
- `max_Psi`

---

### 3) Real-world geometry (Pisa)

`python structural_distance_pisa.py --in case07_grid_agg.csv --row_out pisa_structural_distance_rows.csv --summary_out pisa_structural_distance_summary.csv`

Produces:

- per-row structural distances
- cumulative route distance
- summary metrics across modes

---

## 🌐 Structural Attention (Browser)

Open:

`Structural_Attention_Distance.html`

Features:

- deterministic candidate table
- `D_uv` and `D_muv` distance modes
- optional distance regularization
- live ranking updates
- explainable score decomposition

---

## ❄️ Determinism & Freeze Contract

For identical inputs:

- identical distances
- identical summaries
- identical efficiencies
- identical attention rankings

No randomness.  
No machine dependence.  
No hidden state.

**SSUM-SD is frozen by structure, not by version number.**

---

## 🚫 What Structural Distance Is Not

SSUM-SD is **not**:

- a solver
- an optimizer
- a convergence trick
- a probabilistic model
- a replacement for classical distance

It does not change mathematics.  
**It clarifies motion.**

---

## 🔍 Interpretation Boundaries (Brief)

**Structural Distance (SSUM-SD) is an observational framework, not a physical simulation or engineering solver.**

- `a` (alignment) and `s` (structural spread) are **derived structural observables**, not forces, loads, or material properties.
- Terms like **allowance** and **suppression** describe **structural permission and resistance**, not physical causation.
- The collapse rule `phi((m,a,s)) = m` guarantees that **classical geometry and physics remain unchanged**.
- Structural Distance **does not predict failure or replace engineering models**.
- It provides **early structural signals** (rising cost, exhaustion, instability) that may be interpreted *alongside* domain-specific analysis.

For detailed domain mapping and LiDAR interpretation, see **FAQ**.

---

## 📄 License & Attribution

**CC BY 4.0 — Public Research Release**

Attribution:  
**Shunyaya Structural Universal Mathematics — Structural Distance (SSUM-SD)**

Built within:  
**Shunyaya Structural Universal Mathematics (SSUM)**

No Warranty.
Provided "as is", without warranty of any kind, express or implied.

---

## 🔗 Related Projects & Case Studies

The following public projects demonstrate **Structural Distance** applied in broader structural and geometric contexts:

- **SSUM-Observatory**  
  A deterministic observability layer for Shunyaya Structural Universal Mathematics, enabling inspection of trajectories, structural posture, and accumulated structural cost across systems.  
  https://github.com/OMPSHUNYAYA/ssum-observatory

- **SSUM-Balance — Leaning Tower of Pisa**  
  A real-world geometry case study using LiDAR-derived aggregates to analyze structural balance, boundedness, and non-collapse despite visible asymmetry.  
  https://github.com/OMPSHUNYAYA/SSUM-Balance-Leaning-Tower-of-Pisa

These projects extend **Structural Distance** as a **measurement and interpretability tool**, not as a control or optimization mechanism.

---

## 🏷️ Topics

SSUM-SD, Structural-Distance, Structural-Mathematics, Deterministic-Mathematics, Structural-Geometry, Trajectory-Analysis, Explainable-Ranking, Structural-Attention, LiDAR-Geometry, Pisa, Shunyaya
