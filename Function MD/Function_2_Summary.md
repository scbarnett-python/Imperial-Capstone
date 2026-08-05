# Function 2 — Summary

**Last updated:** 2026-08-02 (Submission 10 of 13 — **P19 processed: peak lead reverses back to Peak B**; kernel re-verified at n=19; Peak A basin-refinement candidate P20 submitted despite losing the EI race, to resolve which basin is genuinely leading before committing the endgame. 2 submissions remain after P20.)

---

## Problem Definition
- **Type:** 2D black-box optimisation
- **Description:** Noisy Log-Likelihood Maximisation — two inputs (x1, x2) standing in for parameters of a hidden model; output is a noisy log-likelihood-style score. Genuinely small in magnitude (range roughly −0.07 to +0.63) rather than the very large negative values a literal multi-observation log-likelihood would typically produce — consistent with this being a synthetic benchmark using "log-likelihood" as narrative framing rather than a literal implementation. Doesn't change strategy (still plain raw-y maximisation per the FAQ), noted for report context only.
- **Goal:** Maximisation (raw y, per FAQ — no detection/transform framing applies here, unlike Function 1's resolved issue)
- **Input space:** x1, x2 ∈ [0, 1]²
- **Output:** noisy — genuine measurement noise confirmed via kernel comparison and out-of-sample misses (P16 historically, P19 this cycle)
- **n evaluated:** 19 points (P1–P19). P20 submitted this session. 2 submissions remain after P20.

---

## Current Dataset (n=19)

| # | x1 | x2 | y |
|---|----|----|---|
| P1 | 0.665800 | 0.123969 | 0.539 |
| P2 | 0.877791 | 0.778628 | 0.421 |
| P3 | 0.142699 | 0.349005 | −0.066 |
| P4 | 0.845275 | 0.711120 | 0.294 |
| P5 | 0.454647 | 0.290455 | 0.215 |
| P6 | 0.577713 | 0.771973 | 0.023 |
| P7 | 0.438166 | 0.685018 | 0.245 |
| P8 | 0.341750 | 0.028698 | 0.039 |
| P9 | 0.338648 | 0.213867 | −0.014 |
| P10 | 0.702637 | 0.926564 | 0.611 |
| P11 | 0.707070 | 0.000000 | 0.564 |
| P12 | 0.686869 | 0.000000 | 0.593 |
| P13 | 0.787879 | 0.979800 | 0.159 |
| P14 | 0.700000 | 0.020000 | **0.633** ← raw best |
| P15 | 0.730023 | 0.546276 | 0.393 |
| P16 | 0.673367 | 0.050251 | 0.486 |
| P17 | 0.653266 | 0.934673 | 0.483447 |
| P18 | 0.718593 | 0.874372 | 0.601905 |
| P19 | 0.708809 | 0.892037 | **0.509792** ← processed this cycle |

Data source: `./initial_data/function_2/merged_inputs.npy` / `merged_outputs.npy` (full merged dataset).

### P19 result and interpretation — REVERSES last cycle's conclusion

**y = 0.509792.** Checked against the pre-submission prediction (μ=0.5998, σ=0.0733): **z = 1.228σ below prediction.** Under the standing interpretation gate this falls just short of the formal 1.5σ "reopen" trigger, and above the literal 0.50 threshold — but its *practical* effect on the denoised estimate is significant regardless of which side of the formal threshold it lands on.

**Re-fit at n=19 (both RBF7 and Matérn 1.5) confirms: Peak B is back in the lead.**

| Kernel | Peak A denoised μ | Peak B denoised μ | Leader |
|--------|--------------------|--------------------|--------|
| RBF7 | 0.553–0.560 | 0.572–0.583 | Peak B, by ~0.02–0.03 |
| Matérn 1.5 | 0.557 | 0.580–0.586 | Peak B, by ~0.02–0.03 |

Raw sample means tell the same story:
```
Peak A (P10, P17, P18, P19): mean=0.5515, std=0.0644  (n=4)
Peak B (P11, P12, P14, P16): mean=0.5690, std=0.0621  (n=4)
```

**This is the second lead flip on a single draw** (P18 → Peak A ahead; P19 → Peak B ahead again). Both peaks currently sit within ~0.02–0.03 of each other, comparable to noise/2–3 — this reads as a genuine dead heat, not a settled contest. The caution already flagged last cycle ("leading, not settled — treat with the same caution as any single noisy observation") has now been validated directly by events, not just held as a hypothesis.

---

## Model — Matérn 1.5 marginally ahead; RBF7 retained per standing protocol

Kernel comparison re-run at n=19 (noise-family only, correctly excluding noiseless kernels from consideration per standing protocol):

| Kernel (+White) | LML | AIC | BIC | Fitted noise std (raw) | ℓ | Pinned? |
|---|---|---|---|---|---|---|
| Matérn 1.5 | −21.6947 | **49.3894** | 52.2227 | 0.0712 | 0.136 | No |
| Matérn 0.5 | −21.6934 | 49.3867 | 52.2200 | 1e-5 (pinned) | 0.211 | **Yes — noise floor, confirmatory diagnostic only** |
| Matérn 2.5 | −21.7218 | 49.4435 | 52.2768 | 0.0789 | 0.122 | No |
| RBF7 | −21.8406 | 49.6812 | 52.5146 | 0.0863 | 0.103 | No |

- Matérn 0.5+White pinned to the noise floor again, as every prior cycle — self-identifying as the wrong model, correctly excluded from consideration despite its nominal AIC edge.
- Among genuine noise models, **Matérn 1.5 edges out RBF7** (ΔAIC≈0.29) — still well under the ~2 meaningful-difference threshold, so **RBF7 retained per standing protocol** (incumbent, stable, ΔAIC below threshold; switching now would be exactly the in-sample-driven flip the project's own learnings warn against).

**Noise estimate inflation, explained:** fitted noise std rose substantially across all genuine kernels vs. the last recorded n=18 fit (RBF7: 0.061 → 0.086; Matérn 1.5: 0.037 → 0.071; Matérn 2.5: 0.044 → 0.079). This is P19's effect directly — the model now has to reconcile P18 (surprisingly high for Peak A) and P19 (surprisingly low for Peak A) within the same basin, and absorbing two draws pulling in opposite directions widens the fitted noise term. Cross-checked against the raw Peak A sample std (0.0644) — consistent with the inflated estimate, not an overreaction.

**Action: update working noise-std reference from 0.061 to ~0.086 (RBF7) for all future EI improvement-term judgment calls** — the 0.061 figure used in P19's own pre-submission check is now stale.

---

## Acquisition — two basin-constrained EI candidates generated; Peak A candidate deliberately selected over higher-EI Peak B candidate

### Unconstrained EI (re-confirmed still drifts)

```
Next point to evaluate: [0.773869, 0.040201]
Predicted mean: 0.5506, Predicted std: 0.1614
EI: 0.0454, Improvement: -0.0424
```
Improvement judged against the *updated* noise std (0.086, not the stale 0.061): −0.0424/0.086 ≈ −0.49σ — legitimate near-exploitation by the project's own convention, not drift. Distance/direction check confirms this sits at Peak B's genuine eastern edge (~0.10 from nearest Peak B sample, same style of basin extension as P18 was for Peak A last cycle) — not a repeat of the earlier basin-jumping failure mode.

### Peak A basin-constrained EI

```
Peak A candidate: [0.750894, 0.846897]
mu=0.5362  sigma=0.1096  improvement=-0.0568  EI=0.0211
```

### Head-to-head comparison

| | Peak A candidate | Peak B candidate |
|---|---|---|
| Point | [0.750894, 0.846897] | [0.773869, 0.040201] |
| μ | 0.5362 | 0.5506 |
| σ | 0.1096 | 0.1614 |
| Improvement | −0.0568 | −0.0424 |
| EI | 0.0211 | **0.0454 (winner on paper)** |

**Decision: submitted the Peak A candidate, overriding EI's own basin preference.** EI favours Peak B mainly via its larger σ (more unexplored variance in that direction), not because Peak B's mean is more promising — that's a variance artefact, not a signal Peak B is the better basin. Given the lead has flipped twice on single draws and Peak A's estimate (4 samples, ±0.05 swing across P18/P19) is the one that's genuinely uncertain, while Peak B (4 consistent samples) is comparatively well-established, resolving the fragile basin was judged more valuable to the 2-query endgame than banking a modestly-higher EI score in the basin already reasonably well understood. Documented explicitly as a deliberate override, in the same spirit as Function 1's ensemble cross-rank — not a blind EI follow.

**Geometry check on the submitted candidate**, relative to existing Peak A points:

| From | Distance | Direction |
|------|----------|-----------|
| P18 | 0.0424 (closest) | +x1, −x2 |
| P19 | 0.0617 | +x1, −x2 |
| P10 | 0.0931 | +x1, −x2 |
| P17 | 0.1313 (farthest) | +x1, −x2 |

All four offsets point the same way (south-east of the existing cluster) — a conservative, close-in refinement of the P18/P19 neighbourhood rather than a bold basin-edge exploration. Sharpens the immediate estimate; doesn't test whether Peak A's basin extends further in an unexplored direction. Consistent with the goal of firming up the existing estimate rather than expanding the search.

### Decision: P20 = [0.750894, 0.846897]

Submitted this session. Result not yet returned.

---

## Peak picture after P19 (pending P20)

| | Denoised μ (RBF7) | Denoised μ (Matérn 1.5) | Raw sample mean | Samples |
|---|---|---|---|---|
| Peak A | 0.553–0.560 | 0.557 | 0.5515 (std 0.0644) | 4 (P10, P17, P18, P19) — P20 pending |
| Peak B | 0.572–0.583 | 0.580–0.586 | 0.5690 (std 0.0621) | 4 (P11, P12, P14, P16) |

**Status: genuine dead heat, not settled.** Margin (~0.02–0.03) is well within noise (std ~0.06–0.09 by both raw-sample and kernel estimates). Two consecutive single-draw lead flips (P18, P19) confirm this shouldn't be treated as resolved in either direction yet.

---

## Remaining Budget & Endgame (2 after P20)

**Plan:** P20 result determines whether Peak A's estimate stabilises near its current ~0.55 raw mean (basin genuinely settles slightly behind Peak B) or swings again (basin remains too noisy to characterise confidently with the budget available). Either way, with 2 queries left after P20:
- If P20 confirms Peak A ≈ 0.55 and Peak B holds ≈ 0.57–0.58: commit final 2 queries to Peak B (the more consistently-supported basin) rather than continuing to split budget.
- If P20 pulls Peak A back up (e.g. another high draw): dead heat persists — likely worth spending one more query in whichever basin remains less-sampled/more uncertain, holding the last query for final refinement of the confirmed leader.

**Scoring-method question (best-observed-y vs nominated-final-point) remains open** — checked against the FAQ this session (prompted by Function 1's resolved case); the FAQ only asks you to *record* your best input/output pair for repo documentation, it does not specify which the *portal* itself scores on. Unlike Function 1, this is not resolved by the FAQ and needs a portal/support-channel check before the final ~2 queries, as previously flagged. Re-confirming this is still live, not quietly answered.

---

## Notebook fixes this cycle

**Reshape bug in plotting cell (found and fixed):** the mean/uncertainty surface plot was reshaping `mu`/`sigma` left over from the most recent acquisition cell (a filtered candidate pool, e.g. 18,145 points) rather than a fresh full prediction grid — `mu.reshape(200,200)` failed with a size mismatch. Fixed by computing a dedicated `X_grid`/`mu_grid`/`sigma_grid` inside the plotting cell itself, independent of whatever acquisition cell ran last:
```python
n_grid = 200
x1g, x2g = np.meshgrid(np.linspace(0, 1, n_grid), np.linspace(0, 1, n_grid))
X_grid = np.column_stack([x1g.ravel(), x2g.ravel()])
mu_grid, sigma_grid = gpr.predict(X_grid, return_std=True)
mu_plot = mu_grid.reshape(n_grid, n_grid)
sigma_plot = sigma_grid.reshape(n_grid, n_grid)
```
Same class of bug as the "reshape only after acquisition, correct array" caution already documented in this project's graveyard comments — worth a general check across other functions' plotting cells for the same pattern.

**Label rendering fix:** Peak A/B annotations on the mean-surface plot had no `xytext` offset, so labels rendered directly on top of the data-point markers. Fixed with offset + arrow, matching the style used elsewhere in the project. Also dropped the hardcoded "(best)" qualifier from the Peak B label — no longer accurate given the lead has flipped twice; plain `'Peak A'` / `'Peak B'` labels used instead.

**Plot observations (n=19 surface):** both peaks render as comparably bright on the mean surface — visually consistent with the near-tie finding, no peak stands out the way Peak A did when its estimate briefly peaked at 0.5965. Uncertainty floor sits around 0.07–0.09 everywhere, including directly at sampled points — expected behaviour for a noisy function with `WhiteKernel`, not a modelling concern (unlike Function 1's noiseless case, σ can never approach zero here, since even exact repeats carry genuine measurement noise).

---

## Acquisition Settings

```python
xi_values = {"function_2": 0.01}
```

- EI incumbent = denoised best (`np.max(gpr.predict(X))`), never raw max — reconfirmed appropriate under noisy-function framing (unlike Function 1, this isn't an analogous "wrong objective" bug; denoising is a legitimate estimate of where the true max likely sits, not evidence of an unverified framing).
- Negative improvement terms judged against **current** noise std (now ~0.086, updated this cycle from the stale 0.061) — recalibrate this reference figure each cycle the kernel noise estimate shifts materially.
- Basin-constrain EI candidates when the incumbent sits in a low-σ well — reconfirmed again this cycle (unconstrained EI correctly re-derived the Peak B edge extension once judged against updated noise std, but the mechanism for why unconstrained EI can drift remains as documented).
- **New this cycle:** EI's basin/candidate ranking is a legitimate acquisition signal but not the only consideration — when two basins are within noise of each other and the acquisition ranking is driven mainly by relative sample density (variance) rather than mean, a deliberate override toward the less-certain basin can be more valuable than following EI mechanically, particularly late in a limited budget when resolving ambiguity matters more than marginal EI gain.

---

## Key Learnings (Function-specific)

- **A single high draw breaking a summit dead heat should be treated as fragile, not settled — now empirically confirmed, not just a stated caution.** P18 broke the tie toward Peak A; P19 broke it back toward Peak B. Two flips on two single draws is direct evidence the "leading" language used after P18 should have been read more cautiously at the time.
- **Kernel noise estimates should be re-checked each cycle a surprising point lands, not assumed stable.** A single unexpected draw (P19, 1.23σ below prediction) was enough to shift the fitted noise std by 40%+ across every kernel in the comparison — stale noise-std references (used in improvement-term judgment calls) can silently mislead if not refreshed alongside the kernel refit.
- **EI's basin/candidate choice can be driven by relative variance rather than relative promise** — worth checking explicitly (as done this cycle) rather than assuming the higher-EI candidate is always the better strategic choice, especially when deciding between two basins whose true means are close and the acquisition's ranking gap is mainly a function of how differently-sampled they are.
- Basin-constrained EI: when both summits are the lowest-σ regions and the incumbent sits in one, unconstrained EI is forced to the highest-σ region elsewhere and jumps basins on pure variance — same fix as F1 in-cluster refinement, reconfirmed working correctly this cycle once judged against updated noise std.
- Roughness and noise confounded in-sample at small n: Matérn 0.5 noiseless ranks best by absorbing noise; +White it pins noise to zero. Only out-of-sample calibration (P16 previously, P19 this cycle) breaks the tie. AIC/BIC cannot see this on their own.
- Under noise: incumbent = denoised best; raw max is partly luck; negative EI improvement compared to current noise std, not zero or a stale figure.
- EI grid reshape bug: reshape mu/sigma for plotting only after acquisition computation, and always from a fresh prediction grid, not a leftover acquisition-candidate array — now confirmed as a recurring class of bug worth checking in every plotting cell across functions.
- IMSE avoids corner/edge bias of max-variance sampling — use for coverage probes (not yet needed this cycle, retained as a standing option).

---

## Full dataset (n=19, canonical)

```python
X = np.array([
    [0.665800, 0.123969],
    [0.877791, 0.778628],
    [0.142699, 0.349005],
    [0.845275, 0.711120],
    [0.454647, 0.290455],
    [0.577713, 0.771973],
    [0.438166, 0.685018],
    [0.341750, 0.028698],
    [0.338648, 0.213867],
    [0.702637, 0.926564],
    [0.707070, 0.000000],
    [0.686869, 0.000000],
    [0.787879, 0.979800],
    [0.700000, 0.020000],
    [0.730023, 0.546276],
    [0.673367, 0.050251],
    [0.653266, 0.934673],
    [0.718593, 0.874372],
    [0.708809, 0.892037],
])

y = np.array([
    0.539, 0.421, -0.066, 0.294, 0.215, 0.023, 0.245, 0.039, -0.014,
    0.611, 0.564, 0.593, 0.159, 0.633, 0.393, 0.486, 0.483447, 0.601905,
    0.5097920158034481,
])
```

**P20 (submitted, result pending): [0.750894, 0.846897]**
