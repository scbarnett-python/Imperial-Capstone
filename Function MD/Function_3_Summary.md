# Function 3 — Summary

**Last updated:** 2026-08-02 (Submission 11 of 13 — **P24 processed: failure #1 at expanded r, TuRBO shrunk back to r=0.06**; kernel re-verified (RBF1/Matérn 2.5 tie now confirmed stable across 3 cycles); notebook reviewed (stale r bug fixed, EI cell role clarified, dead grid cell identified); P25 submitted from shrunk trust region. 2 submissions remain after P25.)

---

## Problem Definition
- **Type:** 3D black-box optimisation
- **Description:** Drug discovery — minimise side effects, framed as maximisation (less negative = better). Consistent with the FAQ's stated approach for minimisation analogies ("transformed into maximisation by negating the output") — no objective-correction risk here, unlike Function 1.
- **Input space:** x1, x2, x3 ∈ [0, 1]³, with a hard x3 ≤ 0.55 danger-zone ceiling (P7's −0.399 established this early and it remains enforced everywhere)
- **Goal:** Maximisation
- **n evaluated:** 24 points (P1–P24). P25 submitted this session. 2 submissions remain after P25.

---

## Current Dataset (n=24)

| # | x1 | x2 | x3 | y |
|---|----|----|----|----|
| P1 | 0.1715 | 0.3439 | 0.2487 | −0.11212 |
| P2 | 0.2421 | 0.6441 | 0.2724 | −0.08796 |
| P3 | 0.5349 | 0.3985 | 0.1734 | −0.11141 |
| P4 | 0.4926 | 0.6116 | 0.3402 | −0.03484 |
| P5 | 0.1346 | 0.2199 | 0.4582 | −0.04801 |
| P6 | 0.3455 | 0.9414 | 0.2694 | −0.11062 |
| P7 | 0.1518 | 0.4400 | 0.9909 | −0.39893 ⚠️ worst |
| P8 | 0.6455 | 0.3971 | 0.9198 | −0.11387 |
| P9 | 0.7469 | 0.2842 | 0.2263 | −0.13146 |
| P10 | 0.1705 | 0.6970 | 0.1492 | −0.09419 |
| P11 | 0.2205 | 0.2978 | 0.3436 | −0.04695 |
| P12 | 0.6660 | 0.6720 | 0.2463 | −0.10597 |
| P13 | 0.0468 | 0.2314 | 0.7706 | −0.11805 |
| P14 | 0.6001 | 0.7251 | 0.0661 | −0.03638 |
| P15 | 0.9660 | 0.8611 | 0.5668 | −0.05676 |
| P16 | 0.2754 | 0.2037 | 0.8272 | −0.07839 |
| P17 | 0.1106 | 0.3124 | 0.4587 | −0.01709 |
| P18 | 0.2853 | 0.3962 | 0.4877 | −0.00898 |
| P19 | 0.7175 | 0.9848 | 0.0074 | −0.12929 |
| P20 | 0.5080 | 0.1263 | 0.4982 | −0.03658 |
| P21 | 0.2612 | 0.3148 | 0.4619 | −0.01201 |
| P22 | 0.2153 | 0.3767 | 0.5066 | −0.02570 |
| P23 | 0.341940 | 0.383375 | 0.436052 | **−0.006363 ← current best (incumbent)** |
| P24 | 0.366844 | 0.433619 | 0.499863 | −0.009457 |

Full precision: `./Data/function_3/merged_inputs.npy` / `merged_outputs.npy`.

### P24 result — processed this cycle

**y = −0.009457.** Routes to the **"failure #1 at expanded r"** branch of the standing interpretation tree ([−0.02570, −0.006363)): worse than incumbent P23, but not as bad as P22. **Incumbent unchanged — remains P23.**

**Calibration check — overprediction pattern holds, fourth consecutive confirmation:**
```
Predicted μ: +0.00067
Actual y:    −0.009457
Overprediction: 0.0101
```
Consistent with the established sequence: P21 (0.006), P22 (0.018), P23 (0.0147), P24 (0.0101). The GP's tendency to overpredict in the SE search direction continues exactly as documented — not a new concern, the calibration discount remains valid as-is.

**TuRBO action taken: trust region shrunk from r=0.12 back to r=0.06**, per the standing shrink rule (failure at expanded r → shrink). RSM quadratic polish moved up in priority, now supported by a 6-point local cluster (P17, P18, P21, P22, P23, P24).

---

## Model — RBF1 retained; RBF1/Matérn 2.5 tie now confirmed stable across 3 cycles

Kernel comparison re-run at n=24:

| Kernel | LML | AIC | BIC | Fitted |
|--------|-----|-----|-----|--------|
| Matérn 2.5 | −25.7061 | **55.4122** | 57.7683 | 1.30² × Matérn(ℓ=0.309, ν=2.5) |
| RBF1 / RBF3 | −25.7279 | 55.4559 | 57.8120 | 1.13² × RBF(ℓ=0.199) ✅ retained |
| Matérn 1.5 | −26.2811 | 56.5621 | 58.9182 | 1.47² × Matérn(ℓ=0.429, ν=1.5) |
| RBF4 (+White) | −25.2756 | 56.5512 | 60.0853 | noise=0.00474 — still far smaller than actual observed misses (0.010–0.018); AIC/BIC-rejected, model bias not evaluation noise |
| Matérn 0.5 | −29.5944 | 63.1887 | 65.5448 | |
| RBF2 | −27.0352 | 58.0704 | 60.4265 | pinned ℓ=0.25 — drop candidate, non-competitive |

**ΔAIC (Matérn 2.5 vs RBF1) ≈ 0.044** — third consecutive cycle showing a statistical tie at this magnitude. History: RBF ahead by 0.017 → Matérn 2.5 ahead by 0.047 → Matérn 2.5 ahead by 0.044. Two consecutive cycles in the same direction, but the gap size itself hasn't grown — this reads as a stable, persistent near-tie rather than a trend toward Matérn 2.5. **Downgrading from "watch" to "confirmed stable statistical tie — treat as a genuine feature of the data (both kernels fit comparably well), not a signal pending resolution as n grows.** RBF1 retained; switching on a gap this small and non-widening would be exactly the in-sample-driven flip this project's own learnings warn against.

RBF4 noise estimate (0.00474) essentially unchanged from prior cycle (0.00696) — "effectively noiseless, trust single evaluations" still holds.

---

## Acquisition — LHS primary (trust region shrunk to r=0.06); EI reconfirmed diagnostic-only

### LHS local search — P25 candidate

```
r radius: 0.06  (shrunk this cycle from 0.12, per TuRBO failure rule)
Next point: [0.321486, 0.432266, 0.449924]
mu filtered: -0.004609
mu unfiltered: -0.004196
```

**Geometric check** relative to the local cluster:
```
P17: 0.2427   P18: 0.0635   P21: 0.1326
P22: 0.1326   P23 (incumbent): 0.0548 (within r=0.06)   P24: 0.0675
```
Sits genuinely between recent cluster points, clears the min_dist=0.05 duplicate filter, x3=0.450 comfortably inside the 0.55 ceiling. `mu_filtered = −0.004609` predicts an improvement over the current incumbent (−0.006363) — a well-placed local refinement candidate, not just a safe fallback.

### EI cross-check — reconfirms known collapse pattern, unchanged from prior cycles

```
Next point: [0.412485, 0.695826, 0.016673]
Predicted mean: -0.026123, Predicted std: 0.059143
Improvement: -0.029760
```
**0.53–0.66 away from every point in the current cluster** — not a local refinement or adjacent-basin probe, essentially a different region of the domain entirely (x2 jumped to 0.70, x3 dropped to 0.017, far outside the cluster's x3≈0.44–0.50 band). Predicted mean clearly worse than incumbent; improvement term more negative than any recent genuine miss. This is the same "pure variance-chasing once local gradient is absorbed" pattern documented in prior cycles — reconfirms, does not change, the standing decision to treat EI as a diagnostic only, never a candidate source.

### Decision: P25 = [0.321486, 0.432266, 0.449924]

Submitted this session (LHS candidate). Result not yet returned.

---

## Notebook review notes (2026-08-02 pass)

**Bug found and fixed: stale trust-region radius.** The LHS cell had `r = 0.12 #wk9` hardcoded, unchanged despite P24 triggering the shrink rule. If re-run as-is, the next candidate would have searched at the wrong (still-expanded) radius, contradicting the TuRBO discipline otherwise being followed carefully. Corrected to `r = 0.06 # wk10 — shrunk after P24 failure at r=0.12`. `x_best = X[np.argmax(y)]` itself was already correctly dynamic — only the `r` value had gone stale.

**Prediction-grid cell (domain-wide, x3≤0.55 constrained) — identified as dependent entirely on the EI cell.** Its `mu`/`sigma` output feeds only the EI acquisition cell; nothing else in the notebook (including the LHS cell, which predicts on its own local candidate array) consumes it. The notebook's "Plots for Uncertainty and Signal Strength" section (cells 20–21) is currently an **empty placeholder** — worth redirecting this grid cell's output toward that section instead of deleting it, since the FAQ requires progress/uncertainty visualisations in the final deliverable and this grid (with the x3 ceiling already correctly applied) is the right input for a domain-wide σ/μ surface plot.

**EI acquisition cell — functionally superseded by LHS for candidate selection, retained as a diagnostic.** Every actual submission for several cycles has come from LHS, not EI. Recommend relabelling the cell explicitly ("EI cross-check — diagnostic only, see LHS cell for actual candidate") rather than removing it outright, since its predictable collapse-to-domain-edge behaviour is itself informative confirmation that the local gradient has been absorbed — consistent with this cycle's result.

**LHS method — clarified as TuRBO-*inspired*, not full TuRBO.** Documented the differences explicitly for report accuracy: isotropic trust-region box (not anisotropic, length-scale-weighted per real TuRBO), pure GP-mean argmax candidate selection (not Thompson sampling — no exploration mechanism *within* the trust region itself), single-success/failure expand-shrink trigger (not a run-based trigger), no restart-on-convergence mechanism. These simplifications are reasonable given the 3D, low-n, tightly-budgeted setting, but should be described accurately in the report rather than implied to be full TuRBO. The retained EI cross-check partially substitutes for the missing in-region exploration mechanism, which is an additional reason to keep it rather than delete it.

**New visualisations added this session:**
- 3-panel projection matrix (x1-x2, x1-x3, x2-x3), colour = raw y, size = rank(y) (rank-based sizing used deliberately — min-max sizing was tried first and found to visually compress almost all points into a similar size due to the P7 outlier squashing the scale).
- Incumbent-centred GP slice plots: three 2×1 panel pairs (uncertainty top, mean bottom) sliced through P23 along each axis pairing, holding the third dimension at the incumbent's value. Documented limitation: scattered points are projected onto each 2D slice regardless of their true distance from the held third coordinate, so apparent proximity on any one panel can be a partial projection artefact — worth a caption note if used in the report.

---

## Interpreting P25 result
- **> −0.006363 (improvement):** gradient still live within the shrunk region; hold r=0.06, continue local refinement from new incumbent.
- **−0.009457 to −0.006363 (comparable to P24, not quite matching):** local search plateauing at this resolution — move to RSM quadratic polish using the now 7-point cluster rather than continuing LHS draws.
- **< −0.009457:** further evidence the region very close to P23 is close to its local ceiling — prioritise RSM polish for the final 2 queries rather than additional LHS exploration.

## Remaining Budget & Priority Queue (2 after P25)
1. Await P25 → route via tree above.
2. RSM quadratic polish — increasingly the right tool for the final 1–2 queries now that the local cluster has grown to 6–7 points, enough to support an analytic stationary-point solve rather than further sampling.
3. Redirect the domain-wide grid cell toward the still-empty uncertainty/mean plotting section, to satisfy the FAQ's visualisation requirement before final submission.
4. ARD check — effectively dropped, n unlikely to reach the ~40 threshold where it would matter.

---

## Key Learnings (Function-specific)

- **EI signal has a lifecycle, now reconfirmed twice:** a genuine positive-improvement EI point is not a standing reservation — must be re-derived at each new incumbent. Once the local gradient is absorbed by successful LHS exploitation, EI reliably collapses to domain-edge variance-chasing rather than offering a competing candidate. This is now an established, predictable pattern across multiple cycles, not a one-off.
- **TuRBO discipline (simplified version) continues to outperform optimistic extrapolation:** GP has overpredicted in the SE direction for four consecutive points (P21, P22, P23, P24) by 0.006–0.018, yet the shrink-then-validate approach has still delivered a net-improving trajectory (P18 → P23) without ever paying the full optimism penalty implied by the raw predicted means.
- **What's implemented is TuRBO-inspired, not full TuRBO** — isotropic box, mean-argmax (no Thompson sampling), single-step expand/shrink triggers, no restart mechanism. Reasonable simplifications for a 3D/low-n/tight-budget setting, but should be described accurately rather than presented as the full algorithm in the report.
- **Rank-based marker sizing is more robust than min-max scaling when one point is a severe outlier** (P7's −0.399 compressed all other points into a visually similar size band under min-max normalisation; rank-based sizing fixed this).
- **Kernel ordering ties can persist stably rather than resolve as n grows** — RBF1 vs Matérn 2.5 has now sat within ΔAIC≈0.02–0.05 for three consecutive cycles with the lead flipping direction but the gap not widening. Worth recognising a stable tie for what it is rather than continuing to flag it as "pending resolution."
- Candidate density must scale with trust-region size — expanding r without raising n_lhs re-creates the wk8 sparse-argmax artefact (standing caution, unchanged).
- x3 danger zone real (P7); x3≤0.55 ceiling enforced everywhere, including in the LHS bounds and the domain-wide grid cell.
- Function smooth and effectively noiseless; trust single evaluations (RBF4 fitted "noise" ~0.005 is model bias, not evaluation noise — consistent across cycles).
- Cells loading data independently = stale-data hazard; single load point, verify n at load after every update. Same caution now extended to hardcoded acquisition parameters (r) going stale between cycles — always re-check dynamic parameters, not just data freshness, before re-running acquisition cells.

---

## Full dataset (n=24, canonical)

```python
X = np.array([
    [0.1715,0.3439,0.2487],[0.2421,0.6441,0.2724],[0.5349,0.3985,0.1734],
    [0.4926,0.6116,0.3402],[0.1346,0.2199,0.4582],[0.3455,0.9414,0.2694],
    [0.1518,0.4400,0.9909],[0.6455,0.3971,0.9198],[0.7469,0.2842,0.2263],
    [0.1705,0.6970,0.1492],[0.2205,0.2978,0.3436],[0.6660,0.6720,0.2463],
    [0.0468,0.2314,0.7706],[0.6001,0.7251,0.0661],[0.9660,0.8611,0.5668],
    [0.2754,0.2037,0.8272],[0.1106,0.3124,0.4587],[0.2853,0.3962,0.4877],
    [0.7175,0.9848,0.0074],[0.5080,0.1263,0.4982],[0.2612,0.3148,0.4619],
    [0.2153,0.3767,0.5066],[0.341940,0.383375,0.436052],
    [0.366844,0.433619,0.499863],
])

y = np.array([
    -0.11212,-0.08796,-0.11141,-0.03484,-0.04801,-0.11062,-0.39893,
    -0.11387,-0.13146,-0.09419,-0.04695,-0.10597,-0.11805,-0.03638,
    -0.05676,-0.07839,-0.01709,-0.00898,-0.12929,-0.03658,-0.01201,
    -0.02570,-0.006363,-0.009456625735815145,
])
```

**P25 (submitted, result pending): [0.321486, 0.432266, 0.449924]**
