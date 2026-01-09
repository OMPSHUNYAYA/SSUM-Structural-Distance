# ⭐ Shunyaya Structural Universal Mathematics — Structural Distance (SSUM-SD)

## Quickstart

**Deterministic • Structural Distance • Trajectory Analysis • Geometry Validation • Reproducible Metrics**

---

## WHAT YOU NEED

Structural Distance is intentionally **minimal**, **deterministic**, and **implementation-neutral**.

### Requirements

- **Python 3.9+**
- **Standard library only** (no external dependencies)
- **Modern browser** (for HTML demos)

Everything is:

- **deterministic**
- **offline**
- **reproducible**
- **identical across machines**

No randomness.  
No training.  
No probabilistic heuristics.  
No adaptive tuning.

---

## MINIMAL PROJECT LAYOUT

A minimal Structural Distance release contains:

/Structural_Distance  
&nbsp;&nbsp;structural_distance_extract.py  
&nbsp;&nbsp;structural_efficiency.py  
&nbsp;&nbsp;structural_distance_pisa.py  
&nbsp;&nbsp;Structural_Attention_Distance.html  
&nbsp;&nbsp;README.md  
&nbsp;&nbsp;Quickstart.md  

### Optional generated outputs (not committed):

/outputs  
&nbsp;&nbsp;*_summary.csv  
&nbsp;&nbsp;*_rows.csv  
&nbsp;&nbsp;*_trace.csv  

/plots  
&nbsp;&nbsp;*.png  

### Notes

- Structural Route Profiles are formally specified in **SSUM-SD**
- Route-profile generation scripts are intentionally **not included**
- Route-based traversal and safety analysis will be released separately as **Structural Safety Routing**

No build step.  
No compilation.  
No external libraries.

---

## ONE-MINUTE MENTAL MODEL

Classical distance asks:

**“How far did we move?”**

Structural Distance asks:

**“How far did this motion travel through structural space?”**

Structural Distance does **not** change solvers, equations, or geometry.  
It observes how motion accumulates **permission**, **resistance**, and **collapse pressure**.

Iteration and geometry are treated as **trajectories through structural space**, not just numerical steps.

---

## CORE STRUCTURAL IDEA (IN ONE LINE)

**Numerical motion accumulates structural cost, not just length.**

Structural Distance measures that cost deterministically.

---

## WHAT STRUCTURAL DISTANCE TRACKS

Structural Distance is computed from deterministic structural observables:

- **alignment** `a_k` (permission)
- **stress** `s_k` (resistance with memory)

Mapped into structural channels:

- **accepted channel** `u_k`
- **resisted channel** `v_k`

Where:

`u_k = atanh(clamp(a_k))`  
`v_k = atanh(clamp(s_k))`

### Structural posture quantities

`R_k = sqrt(u_k^2 + v_k^2)`  
`Psi_k = 0.5 * (u_k^2 + v_k^2)`

These describe **where the system sits structurally**, not how far it moves.

---

## FALLBACK WHEN STRUCTURAL CHANNELS ARE UNAVAILABLE

If alignment `a_k` and stress `s_k` are not available:

`u_k = 0`  
`v_k = 0`

Then:

`D_k = |m_k - m_{k-1}|`  
`L_struct = L_classical`  
`eta = 1`

Structural Distance **collapses cleanly** to classical distance.

This is **not a failure mode** — it is the correct deterministic collapse.

---

## STRUCTURAL DISTANCE (TRAJECTORY METRIC)

Structural Distance measures how much **structural space** is traversed between steps.

### Per-step Structural Distance (between k−1 and k)

`D_k = sqrt((m_k - m_{k-1})^2 + (u_k - u_{k-1})^2 + (v_k - v_{k-1})^2)`

### Cumulative Structural Distance

`L_struct = sum_k D_k`

### Classical Distance

`L_classical = sum_k |m_k - m_{k-1}|`

No arithmetic is changed.  
No motion is altered.  
Distance is **observed**, not imposed.

---

## IMPLEMENTATION NOTE — PRACTICAL TRAVERSAL COMPLETION

In the reference extraction implementation, `L_struct` is accumulated for `n−1` full structural transitions, followed by a final traversal completion term:

`L_struct_practical = (sum_{k=1..n-1} D_k) + |m_n - m_{n-1}|`

This is intentional and deterministic:

- final numerical motion is fully accounted for
- plateau endings are compensated exactly
- no artificial structural transition is implied

Any omitted final `(u, v)` contribution is negligible in convergent regimes and does not affect comparative interpretation.

---

## STRUCTURAL EFFICIENCY (KEY METRIC)

Structural efficiency is defined as:

`eta = L_struct / L_classical`

This reveals:

- how costly numerical motion is structurally
- when effort is spent against resistance
- why iterations “work hard” without progress
- when collapse pressure rises despite bounded motion

Efficiency becomes **interpretable**, not heuristic.

---

## RUNNING STRUCTURAL DISTANCE (ITERATIVE TRACES)

Structural Distance operates on deterministic iteration traces.

Example:

`python structural_distance_extract.py --in x2_minus_2_trace.csv x2_plus_1_trace.csv x4_plus_1_trace.csv --out structural_distance_summary.csv`

This produces:

- cumulative structural distance (`L_struct`)
- classical vs structural distance comparison
- maximum structural radius (`max_R`)
- maximum structural potential (`max_Psi`)

---

## REAL-WORLD GEOMETRY (PISA VALIDATION)

Structural Distance generalizes beyond equations.

Example:

`python structural_distance_pisa.py --in case07_grid_agg.csv --row_out pisa_structural_distance_rows.csv --summary_out pisa_structural_distance_summary.csv`

Despite visible tilt and asymmetry:

- Structural Distance remains bounded
- Structural potential remains stable
- no collapse signature appears

This confirms:

**stability is not symmetry**  
**balance is structural, not visual**

---

## STRUCTURAL ATTENTION (BROWSER-BASED)

Structural Distance integrates directly into deterministic Structural Attention.

Open in browser:

`Structural_Attention_Distance.html`

Baseline score:

`score = m + a + s`

Distance-regularized score:

`score_B = score - gamma * D`

This demonstrates:

- distant candidates are structurally penalized
- close candidates gain relative weight
- ranking shifts remain explainable
- no training or probability is involved

Distance acts as a **control-free regulator**.

---

## DETERMINISM GUARANTEE

Given identical inputs:

- same traces
- same distances
- same efficiencies
- same rankings

Structural Distance guarantees:

- no randomness
- no machine dependence
- no hidden state

Results are fully reproducible.

---

## WHAT STRUCTURAL DISTANCE IS — AND IS NOT

Structural Distance **is**:

- a structural metric
- a geometric interpretation of motion
- a unifying lens across math, geometry, and algorithms

Structural Distance **is not**:

- a solver
- an optimizer
- a convergence trick
- a replacement for classical distance

It does not change mathematics.  
**It clarifies it.**

---

## ONE-LINE SUMMARY

**Structural Distance lets you deterministically measure how costly, resistant, and viable motion truly is — across equations, algorithms, and real-world geometry — without changing a single computation.**
