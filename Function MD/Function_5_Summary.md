# Function 5 — Summary
**Last updated:** 2026-08-03 (wk10, submission 10 of 13: P29 = 8,115.43 NEW BEST — x4 boundary-dip retracted; kernel refit at n=29 confirms monotonic rise to corner; slice argmax [1,1,1,1] submitted as P30. 3 submissions remain after P30.)

---

## Problem Definition
- **Type:** 4D black-box optimisation
- **Description:** Chemical Process Yield
- **Goal:** Maximisation
- **Input space:** x₁..x₄ ∈ [0, 1]⁴
- **n evaluated:** 29 points (P1–P29); P30 submitted this session
- **Output scale:** 0.11 – 8,115 (~4.9 decades) → log10 transform mandatory
- **Noise:** effectively noiseless on log scale → scoring-rule question does NOT apply (best-observed and nominated-point converge). Unlike F1/F2/F4.

---

## Current Dataset (n=29, tail)

| # | x1 | x2 | x3 | x4 | y |
|---|----|----|----|----|---|
| P24 | 0.941 | 0.956 | 0.999 | 0.908 | 5,579 |
| P25 | 0.983 | 0.999 | 0.985 | 0.255 | 4,030 |
| P26 | 0.971 | 0.908 | 0.971 | 0.887 | 4,776 |
| P27 | 0.978882 | 0.989025 | 0.960622 | 0.895234 | 5,871 |
| P28 | 1.000000 | 1.000000 | 1.000000 | 0.850000 | 6,500 |
| **P29** | **1.000000** | **1.000000** | **1.000000** | **0.970000** | **8,115.43 ✅ best** |

(P1–P23 unchanged; see prior summaries / npy for full precision.)
Full precision: `./initial_data/function_5/merged_inputs.npy` / `merged_outputs.npy`.

### P29 result (returned this session) — corner rise confirmed, model under-predicted
- **[1.0, 1.0, 1.0, 0.97] → 8,115.43** (log10 = 3.9093), new best (+24.8% over P28).
- **Predicted μ_log=3.8366 (y≈6,869); actual 3.9093 (y=8,115)** → under-prediction of 0.073 nats, ~18.1% raw, ~1.0σ against σ_log=0.072. First under-prediction after two consecutive over-predictions (P27 +2.3%, P28 +6%) — direction flipped, signalling the true x4 slope is steeper near the boundary than the pre-P29 fit captured.
- **Key implication:** the previously-fitted dip at x4=1.00 (predicted 6,835, below the x4=0.97 point) is retracted. Re-profiling under the refit kernel confirms the slice is now monotonically increasing to the corner (see below).

### P30 — Submitted this session (awaiting result)
- **Point:** [1.0, 1.0, 1.0, 1.0] — formatted `1.000000-1.000000-1.000000-1.000000`
- **Method:** boundary-slice grid search argmax under refit RBF5 ARD kernel (n=29) — genuine method output, not a hand-pick.
- **Predicted:** μ_log=3.9292 → **y ≈ 8,496 (+4.7% over P29)**, σ_log=0.0079 (tight — tighter than P29's pre-submission uncertainty, since the anchor gap is now only 0.03 in x4).
- **Rationale:** full-corner point [1,1,1,1] has never been evaluated (distinct from P28 [1,1,1,0.85] and P29 [1,1,1,0.97]). Resolves cleanly either way: confirms a true ceiling at the corner, or reveals the rise continues past it — informative with 3 queries left after P30.
- **Interpretation tree:**
  - **≥ ~8,450:** corner confirmed as (near-)ceiling; endgame = RSM/quadratic polish over the dense P23–P30 cluster.
  - **~8,100–8,450:** modest gain, consistent with continued deceleration; plateau confirmed, polish endgame.
  - **< ~8,100 (no improvement over P29):** true ceiling sits *before* the corner (likely near x4≈0.97); retreat to P29 as incumbent, do not push further toward x4=1.0.

---

## Current Best
**y_best = 8,115.43** at P29 [1.0, 1.0, 1.0, 0.97] (log10 = 3.9093), pending P30 result.

---

## x4 profile — boundary dip retracted (key event this cycle)
Prior fit (n=28) predicted a dip at x4=1.00 below the x4=0.97 argmax. **P29's result (8,115 vs. predicted 6,869) falsified this** — the real slope near the boundary is steeper than the pre-P29 model captured. Refitted x4 profile on the x1=x2=x3=1 edge (n=29):

| x4 | y (pred) | σ_log |
|----|----------|-------|
| 0.600 | 4,313 | 0.079 |
| 0.700 | 4,905 | 0.045 |
| 0.750 | 5,346 | 0.027 |
| 0.800 | 5,881 | 0.012 |
| 0.845–0.855 | ~6,495 | ~0.000 (P28 anchor) |
| 0.905 | 7,232 | 0.006 |
| 0.950 | 7,849 | 0.003 |
| 0.955 | 7,916 | 0.003 |
| **1.000 (argmax)** | **8,496** | **0.008** |

Slope is now monotonically increasing across the full slice — no dip, no interior optimum short of the corner. This is the second reversal in the x4 story this project: raw-scale interior optimum (~0.70) → retracted after P28 → shallow near-boundary optimum (~0.97) → retracted after P29 → monotonic rise to corner (current). Each reversal was triggered by a single boundary anchor point overturning an extrapolated conclusion — reinforces the standing lesson that interior optima near an edge should not be trusted until the edge itself is anchored.

---

## Transform (stable)
`y_fit = np.log10(y)` with positivity assert. Jacobian-corrected large LML win; noise pins at floor on log scale. Validated out-of-sample four times now (P27 +2.3%, P28 +6% over, P29 −18.1% under — direction flip flagged the slope change).

---

## Kernel Configuration (RBF5 ARD retained — fourth weekly confirmation)

**Fitted (n=29, log10):** `1.71² × RBF(ℓ=[1.35, 0.346, 0.906, 0.633])`, LML=−13.30

### Kernel comparison (wk10, n=29)
| Kernel | LML | AIC | BIC | Notes |
|--------|-----|-----|-----|-------|
| **RBF5 ARD** | **−13.30** | **36.60** | 43.44 | ✅ wins both; retained; margin over isotropic widened vs. last week |
| RBF6 ARD+White | −13.36 | 38.72 | 46.92 | noise pinned near floor (1e-5), rejected |
| Matérn 2.5 | −20.26 | 44.51 | 47.25 | |
| RBF1/2/3 iso | −20.49 | 44.98 | 47.71 | ℓ=0.48 |
| Matérn 1.5 | −21.12 | 46.24 | 48.97 | |
| Matérn 0.5 | −25.34 | 54.68 | 57.41 | |

- **ARD stability check PASSED fourth week:** ℓ=[1.35, 0.346, 0.906, 0.633] vs wk9 [1.37, 0.322, 0.85, 0.60] vs wk8 [1.52, 0.34, 0.86, 0.61] vs wk7 [1.45, 0.335, 0.82, 0.60] — all dims <10% drift (max 7.5%, x2). x2 always most sensitive, x1 always least — now a well-established result across four independent weekly refits, not a fragile one.
- LML improved notably (−15.39 → −13.30) despite P29 landing ~1.0σ outside the prior prediction — P29 added confirmatory curvature (correct direction, underestimated magnitude) rather than contradictory noise, consistent with noiseless-on-log-scale behaviour.
- RBF6's noise term continues to pin at the floor bound — noiseless-on-log confirmed for the fourth consecutive week.

---

## Acquisition Methods

### Boundary-slice grid search (primary)
Random LHS structurally under-samples boundary faces (P(coordinate=1.0)=0); search the slice directly when the GP favours an edge. This cycle's slice (table above) shows no dip — monotonic to x4=1.0, argmax = corner point [1,1,1,1], submitted as P30.

### LHS local search (cross-check)
r=0.10 around P28/P29 → [0.991, 0.941, 0.993, 0.985], predicted μ_log=3.878 (y≈7,555) — dominated by the slice, doesn't reach the true boundary. 12/50 candidates dropped (region dense with evaluated points). Confirms fit only, not used as candidate.

### EI cross-check — REJECTED corner probe THIRD week running
EI proposed a far-corner point [0.450, 0.018, 0.096, 0.992], **improvement = −0.413** (negative — pure uncertainty-driven, no genuine improvement signal), EI value 0.265 driven entirely by σ=1.10 (huge extrapolation variance). Rejected outright; same pattern as the two prior weeks' corner probes. The improvement-share heuristic (imp·Φ(z) vs. total EI) continues to reliably flag variance-in-disguise for this function.

### TuRBO / trust region
Not the operative method — the optimum is on/at the boundary, reached by direct slice search, not by a shrinking interior trust region.

---

## Remaining Budget & Priority Queue (3 after P30)
1. Await P30 → route via interpretation tree above
2. If corner confirmed as (near-)ceiling: RSM/quadratic polish over the dense P23–P30 cluster for final fractional gains
3. If P30 underperforms P29: retreat to P29 as incumbent; do not push further toward x4=1.0; polish around x4≈0.95–0.97 instead
4. No further exploration probes planned — corner EI rejected three weeks running; coverage gaps all in regions ruled out by radial/slice evidence

---

## Key Learnings (Function-specific)
- **The x4 story has now reversed twice**, each time triggered by a single boundary anchor: raw-scale ~0.70 optimum (retracted at P28) → near-boundary ~0.97 optimum (retracted at P29) → monotonic rise to corner (current, pending P30 confirmation). Extrapolated interior optima adjacent to an unanchored edge should be treated as provisional until the edge itself is evaluated — this function is now the clearest illustration of that principle in the project.
- **Prediction-error direction is diagnostic, not just magnitude.** Two consecutive over-predictions (P27, P28) followed by an under-prediction (P29) flagged the slope change before the slice re-profile confirmed it numerically.
- **LML can improve even when a new point is ~1σ off the prior prediction**, provided the error is in the direction the model already expected (confirmatory curvature vs. contradictory noise). Useful distinction when interpreting "surprising" GP updates.
- **ARD stability across four weeks** (<10% ℓ drift, consistent dimension ordering) is now a robust, established result for this function.
- **EI improvement-share heuristic** (imp·Φ(z)/EI, classify by share not sign) has rejected the same corner-probe pattern three weeks running — reliable, cheap insurance against variance-in-disguise; worth citing in the report as a repeatable diagnostic.
- **Manual pick vs. method output discipline maintained:** P29 and P30 both submitted as true slice argmax outputs, not hand-picks — consistent with the project-wide reproducibility standard.
- Noiseless-on-log-scale confirmed for a fourth consecutive week (RBF6 White term pins at floor) → scoring-rule question does not bite; F5 endgame remains "find the single highest-yield point."
- x2 most sensitive, x1 least (log-scale ARD, now four times confirmed).
