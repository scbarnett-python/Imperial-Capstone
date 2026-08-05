# Function 4 — Summary

**Last updated:** 2026-08-02 (Submission 10 of 13 — **P39 processed: third confirming ridge draw**; over-smoothing exhibit resolved (RBF4 → Matérn 1.5+White, properly noise-calibrated); candidate-grid sparsity bug found and fixed in the EI cell; EI and LHS converge on the same region post-fix; P40 submitted as the EI candidate. 3 submissions remain after P40.)

---

## Problem Definition
- **Type:** 4D black-box optimisation
- **Description:** Warehouse ML hyperparameter tuning — output reflects deviation from an expensive baseline. Problem statement explicitly warns the system is dynamic and full of local optima.
- **Goal:** Maximisation
- **Input space:** x1..x4 ∈ [0, 1]⁴
- **n evaluated:** 39 points (P1–P39). P40 submitted this session. 3 submissions remain after P40.

---

## Current Dataset (n=39, tail)

| # | x1 | x2 | x3 | x4 | y |
|---|----|----|----|----|---|
| P28 | 0.578 | 0.429 | 0.426 | 0.249 | −4.03 |
| P31 | 0.433 | 0.449 | 0.413 | 0.441 | −0.0424 |
| P32 | 0.443 | 0.458 | 0.316 | 0.467 | −1.667 |
| P33 | 0.346 | 0.393 | 0.473 | 0.422 | −0.687 |
| P35 | 0.424 | 0.401 | 0.454 | 0.455 | −0.543 |
| P36 | 0.373 | 0.479 | 0.462 | 0.413 | −1.652 |
| P37 | 0.412548 | 0.401552 | 0.405457 | 0.439505 | **+0.343380 ← best observed** |
| P38 | 0.402129 | 0.388957 | 0.417730 | 0.442561 | +0.190681 |
| P39 | 0.392333 | 0.353703 | 0.398126 | 0.437857 | +0.304900 |

(P1–P27, P29, P30, P34 unchanged — all ≤ −4; full precision in `./Data/function_4/merged_inputs.npy` / `merged_outputs.npy`.)

### P39 result — ridge confirmed a third time

**y = 0.304900.** Routes to the "positive (third in a row)" branch of the standing interpretation tree — the strongest-signal outcome.

**Three-draw ridge statistics:**
```
P37: 0.343380, P38: 0.190681, P39: 0.304900
Mean: 0.279654
Sample std: 0.0794
```

**Key finding: empirical spread (σ≈0.079) is ~6× tighter than the model's fitted global noise level (~0.45 under RBF4).** Two plausible explanations: (a) genuine heteroscedastic noise — this ridge region is much quieter than the noisy, mostly-negative rest of the domain, and a single global `WhiteKernel` term averages across both regimes; (b) the same over-smoothing already diagnosed at this locus was also inflating the effective noise estimate. Either way: treat the ridge as considerably more precisely known than a naive σ≈0.45-based interval would suggest.

**Underprediction pattern — confirmed a third time under RBF4, tightly consistent:**
```
P38: predicted μ=−0.359, actual +0.191 → underprediction 0.55
P39: predicted μ=−0.251, actual +0.305 → underprediction 0.556
```
Two underpredictions within 0.006 of each other — this consistency is itself evidence the ~0.55 discount is a **systematic bias from over-smoothing**, not random miscalibration.

### Central-optimum finding (from projection matrix, this session)

Pairwise projection plots (all 6 axis combinations) show the ridge cluster (P37/P38/P39, all coordinates ≈0.35–0.44) sitting near the centre of the domain, clearly separated from the ~36 negative points. This matches and visually confirms the standing radial-correlation finding (`corr(y, distance_from_best) = −0.943`) — the basin is unimodal *and* centrally located, not off in a corner. Worth noting for the report as a second instance (alongside Function 1's implausible dipole) of a structural signature more consistent with a synthetic benchmark function than a literal simulation — many standard test-function suites default to centring the true optimum, as a generation convenience.

---

## Model — Over-smoothing exhibit resolved: RBF4 → Matérn 1.5 + White

### The investigation (this session)

Kernel comparison at n=39 initially showed Matérn 1.5 (noiseless) with a much-improved AIC (14.08 vs RBF4's 17.72), and its plug-in incumbent matched P37's raw y to 5+ decimal places (0.343380 vs 0.34337986889145). **This match was correctly flagged as a trivial artefact, not a genuine fix** — a noiseless GP is mathematically forced to interpolate exactly through training points; the near-perfect match would occur regardless of whether the model was any good, since F4 is an independently-established noisy function (this is the entire basis for the WhiteKernel term, the dmin>0.01 duplicate-exclusion rule, and the σ≈0.45 noise estimate).

**Re-fit with an explicit noise term (`Matern_1.5_Noisy`) to test fairly:**
```
Matern_1.5_Noisy   LML=-4.8637  AIC=15.7275  BIC=20.7181  kernel=2.34² × Matérn(ℓ=2, ν=1.5) + WhiteKernel(noise_level=0.000481)  [PINNED: length_scale near upper bound 2]
```
**The optimizer chose noise_level=0.000481 voluntarily, not because it was pinned** — no warning on the noise parameter. This is meaningful: even given full freedom to explain the P37/P38/P39 scatter as noise, the model prefers to explain it via a long, smooth trend instead. Still beats RBF4 by ΔAIC≈2.0 — borderline-meaningful, and now a fair, apples-to-apples comparison (both kernels carry a noise term).

**Locus prediction, the decisive test:**

| Kernel | Plug-in incumbent | vs. empirical ridge mean (0.2797) | Discount |
|--------|---------------------|--------------------------------------|----------|
| RBF4 | −0.1379 | far off | 0.48 |
| Matérn 1.5 (noiseless) | 0.3434 | trivial exact match to P37 alone — not meaningful | n/a, artefact |
| **Matérn 1.5 + White** | **0.2492** | **very close** | **~0.03** |

**Decision: adopt Matérn 1.5 + White.** This resolves the over-smoothing problem directly — its plug-in incumbent lands almost exactly at the genuine three-draw empirical mean, not because of trivial interpolation at one point, but through believable smoothing across the whole cluster.

**Outstanding, not yet closed:** `length_scale` is still pinned at the upper bound (2.0) even with noise now correctly included. A widened-bound diagnostic refit (same playbook as Function 1's lower-bound check) was recommended to confirm whether this is a genuine finite optimum being clipped by too-tight a ceiling, or a runaway toward an effectively-infinite length scale (a red flag, same class of concern as a kernel wanting to fit one global linear trend). **Not yet run as of this summary — flagged as the single remaining open item on kernel selection.**

### Full kernel comparison at n=39, for reference

| Kernel | LML | AIC | BIC | Notes |
|--------|-----|-----|-----|-------|
| Matérn 1.5 (noiseless) | −5.0385 | 14.0770 | 17.4041 | Pinned ℓ=2; interpolation artefact, not adopted |
| **Matérn 1.5 + White** | **−4.8637** | **15.7275** | 20.7181 | **✅ adopted** — pinned ℓ=2 (unresolved), voluntary small noise |
| RBF6 (ARD+White) | −5.6954 | 23.3907 | 33.3721 | ARD rejected again — near-identical ℓ across all 4 dims [0.799,0.803,0.725,0.757], no real anisotropy |
| RBF4 (iso+White) | −5.8617 | 17.7234 | 22.7141 | Previous incumbent — now superseded |
| Matérn 2.5 | −12.5870 | 29.1741 | 32.5012 | |
| RBF5 (ARD, no noise) | −18.1176 | 46.2351 | 54.5529 | ℓ₃=0.16 artefact persists — standing report exhibit |
| RBF1/2/3 (iso, no noise) | −19.8230 | 43.6460 | 46.9732 | All identical; non-competitive |
| Matérn 0.5 | −22.7002 | 49.4004 | 52.7275 | Pinned ℓ=2 |

---

## Notebook bug found and fixed this session: EI candidate-grid sparsity

**Symptom that led to the discovery:** the same EI candidate index (7257) kept winning across three different kernel fits (RBF4, Matérn 1.5 noiseless, Matérn 1.5+White) despite genuinely different predicted means at that location each time.

**Root cause, found in the notebook (cell 14):**
```python
rng = np.random.default_rng(42)
grid = rng.uniform(low=0, high=1, size=(10000, 4))
```
Fixed seed, domain-wide uniform sampling, regenerated identically every run regardless of kernel — this was already flagged as a known limitation in this project's own key learnings ("plain-random 10k cannot represent an EI peak hugging a point; Sobol + local cloud is the pattern") but had never actually been fixed in code.

**Quantified the severity:** the volume of a radius-0.08 ball in 4D is $\frac{\pi^2}{2}r^4 \approx 2.0\times10^{-4}$. Against 10,000 uniform points across the unit hypercube, the **expected candidate count within 0.08 of any point is only ~2** — meaning EI's proposed candidates weren't meaningfully optimized near the ridge, they were selected from whichever 1–2 points happened to land nearby by chance.

**Fix applied:**
```python
n_candidates = 10000
x_best = X[np.argmax(y)]
r_grid = 0.15
rng = np.random.default_rng(42)
low = np.maximum(0.0, x_best - r_grid)
high = np.minimum(1.0, x_best + r_grid)
grid = rng.uniform(low=low, high=high, size=(n_candidates, X.shape[1]))
```
Concentrates the same 10,000 points into a much smaller volume around the incumbent, giving EI a genuinely dense local candidate pool instead of ~2 points.

**Secondary finding, same investigation:** `y_best` in the EI cell is computed as `np.max(gpr.predict(X))` (max GP-predicted mean over all training points), not evaluated specifically at P37. For a noiseless kernel this is mathematically forced to equal `max(y)` exactly, which explains the earlier "perfect match" artefact precisely rather than approximately.

**LHS was unaffected throughout** — its candidate generation (`LatinHypercube` within an explicit local trust region, cell 19) never had this sparsity problem, which is why it remained the more trustworthy acquisition source for the whole thread until the EI grid was fixed.

---

## Acquisition — EI and LHS converge post-fix; EI candidate submitted

### Post-fix EI result (Matérn 1.5+White, corrected local grid)

```
Next point: [0.424802, 0.372355, 0.394098, 0.392007]
Predicted mean: 0.30579
Predicted std: 0.44399
Expected improvement: 0.20140
Improvement: +0.04659   ← first positive improvement term all campaign
```

**First EI result all campaign to clear every standing diagnostic:** positive improvement (exploitation-driven, not uncertainty-chasing), predicted mean at/above the empirical ridge mean (not discounted), and a properly dense local candidate pool.

### Geometric convergence with LHS

```
EI candidate distances:  P37=0.0582, P38=0.0625, P39=0.0593
LHS candidate distances: P37=0.0826, P38=0.0829, P39=0.0683
EI-to-LHS distance: 0.0274
```

**EI and LHS — two independently-generated candidates from different mechanisms — now land within 0.027 of each other**, roughly a third the distance of their earlier (pre-fix) disagreement. Strong corroboration for this region as the next query location.

**Head-to-head comparison, same corrected kernel:**
| | EI candidate | LHS candidate |
|---|---|---|
| Point | [0.424802, 0.372355, 0.394098, 0.392007] | [0.417905, 0.352367, 0.391154, 0.374899] |
| Predicted mean | 0.3058 | 0.1433 |
| vs. incumbent (0.2492) | **+0.0466 (predicted improvement)** | −0.106 (predicted regression) |

EI's candidate is not just more explicit about the comparison — it is genuinely predicted better than LHS's candidate under the same corrected kernel. **Decision: submitted the EI candidate.**

### Decision: P40 = [0.424802, 0.372355, 0.394098, 0.392007]

Submitted this session. Result not yet returned.

---

## Interpreting P40 result
- **Beats P37 (>0.343380):** new best; ridge extends meaningfully in this direction — strong case for continuing to explore this direction with remaining budget.
- **Within ridge range (~0.19–0.34):** confirms the ridge extends smoothly this direction, consistent with a broad rather than point-like feature; continue local exploitation.
- **Well below ridge range:** ridge may be narrower/more localised than the smooth Matérn 1.5 fit suggests; would warrant re-examining whether ℓ=2 (still pinned, unresolved) is overstating the basin's true smoothness.

## Remaining Budget & Priority Queue (3 after P40)
1. Await P40 → route via tree above.
2. **Still open: widened length-scale-bound diagnostic** for Matérn 1.5+White — confirm ℓ=2 is a genuine finite optimum, not a pinned artefact. Cheap to run (no query spent), should be closed out before final kernel conclusions go in the report.
3. Scoring-rule question (best-observed vs nominated-point) — still unresolved via FAQ (same open item as Functions 1/2/3); now more decision-relevant than ever given only 3 queries remain and the ridge's extent is still being mapped.
4. No further coverage/corner probes needed — unimodality and central-optimum placement both independently confirmed this session.

---

## Key Learnings (Function-specific)

- **A trivial interpolation artefact can masquerade as a well-calibrated fit — always check whether a "too-good" plug-in match is due to a noiseless kernel forced to interpolate, especially on a function already established as noisy.** The noiseless Matérn 1.5 fit's exact match to P37 looked like validation; it was actually a property every noiseless kernel has at every training point, regardless of quality.
- **When adding a noise term to test a promising kernel, check whether the optimizer chose the noise level voluntarily or was pinned at a bound** — a freely-chosen small noise level (as here, 0.000481, unpinned) is a much stronger endorsement than one forced there by a tight bound.
- **Candidate-grid density must be checked quantitatively in ≥4D, not assumed adequate from "10,000 points" alone.** A domain-wide uniform grid that sounds large can still leave almost no local resolution near a specific region of interest — worth the volume-ratio calculation ($V_{ball}/V_{cube} \times N$) whenever an acquisition function's candidate pool spans the full input space in 4+ dimensions.
- **Two independently-generated acquisition candidates converging geometrically, after fixing a known bug in one of them, is strong corroborating evidence** — worth treating as more informative than either candidate alone, similar in spirit to the ensemble cross-rank protocol used elsewhere in this project.
- **A mis-calibrated incumbent corrupts acquisition broadly, not just EI's headline candidate** — the over-smoothing discount affected the improvement-term sign, the apparent competitiveness of candidates, and indirectly the trustworthiness of every acquisition run until resolved.
- **Central, unimodal optimum placement (radial correlation −0.943, now visually confirmed via projection matrix) is a second instance of a synthetic-benchmark structural signature**, alongside Function 1's implausible dipole — useful, non-decision-critical report context.
- Duplicate-exclusion threshold remains per-function: dmin>0.01 for noisy F4 (a 0.02-away draw is a fresh independent sample), dmin>0.05 for noiseless F3.
- Basin unimodal (r=−0.943), corners closed (P34); remaining open question is the ridge's extent/direction, not its location.

---

## Full dataset reference (n=39, tail — full precision in .npy files)

```python
# Ridge cluster (the region of interest)
P37 = [0.412548, 0.401552, 0.405457, 0.439505]  # y = 0.343380 (best observed)
P38 = [0.402129, 0.388957, 0.417730, 0.442561]  # y = 0.190681
P39 = [0.392333, 0.353703, 0.398126, 0.437857]  # y = 0.304900
```

**P40 (submitted, result pending): [0.424802, 0.372355, 0.394098, 0.392007]**
