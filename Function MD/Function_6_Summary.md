# Function 6 — Summary
**Last updated:** 2026-08-03 (wk10, submission 10 of 13: P29 = −0.490 (third consecutive miss below P26 high-water mark); kernel refit flips leader to RBF4 iso+White; x2 sweep CONFIRMS peak at 0.110 (= P26, not the stale 0.175 target); x3 sweep FALSIFIES the 0.66 pin — extended sweep finds real interior peak at ≈0.58; corrected candidate P30 = [0.502914, 0.098573, 0.584217, 0.720294, 0.160457] submitted. 1 submission remains after P30.)

---

## Problem Definition
- **Type:** 5D black-box optimisation
- **Description:** Cake Recipe Optimisation
- **Goal:** Maximisation (less negative = better)
- **Input space:** x₁..x₅ ∈ [0, 1]⁵
- **n evaluated:** 29 points (P1–P29); P30 submitted this session
- **Output range:** −2.57 to −0.414
- **Noise:** RBF4's noise term now fits a genuine non-floor value (0.0048) for the first time — previously always pinned at floor. Worth monitoring; may indicate real local variability rather than pure noise.

---

## Current Dataset (n=29, tail)

| # | x1 | x2 | x3 | x4 | x5 | y |
|---|----|----|----|----|----|----|
| P25 | 0.532 | 0.229 | 0.310 | 0.809 | 0.023 | −0.723 |
| **P26** | **0.518** | **0.109** | **0.648** | **0.673** | **0.134** | **−0.4139 ✅ best** |
| P27 | 0.476586 | 0.131212 | 0.673662 | 0.697427 | 0.199804 | −0.44065 |
| P28 | 0.519116 | 0.051684 | 0.666052 | 0.678189 | 0.121254 | −0.49723 |
| P29 | 0.517446 | 0.167864 | 0.661411 | 0.665938 | 0.143036 | −0.49004 |

(P1–P24 unchanged; see prior summary / npy for full precision.)
Full precision: `./initial_data/function_6/merged_inputs.npy` / `merged_outputs.npy`.

### P29 result (returned this session) — third consecutive miss, x2-optimum-at-0.175 story falsified
- **[0.517446, 0.167864, 0.661411, 0.665938, 0.143036] → −0.49004.** Predicted μ=−0.3930, sd=0.0305 → miss of 0.097, ~3.2σ. Larger miss than P28 (0.082).
- **P27, P28, P29 have now ALL landed below the P26 high-water mark** — three consecutive exploitation attempts around the basin have undershot P26, not just one. Strong signal that P26 sits very close to the true local peak, not partway up a rising flank.
- **Consequence:** the wk9 "interior x2 optimum ≈0.175" reading is RETRACTED. See x2 sweep below.

### Kernel refit (n=29) — leader flips
| Kernel | LML | AIC | BIC | Notes |
|--------|-----|-----|-----|-------|
| **RBF4 iso+White** | **−19.83** | **45.66** | 49.76 | ✅ NEW leader; noise=0.0048 — genuine, not floor-pinned (first time) |
| Matérn 1.5 | −22.19 | 48.38 | 51.11 | previous leader; ℓ shortened 1.13→0.754 (~33%), independently confirms sharper-than-modelled basin |
| Matérn 2.5 | −24.81 | 53.62 | 56.35 | |
| Matérn 0.5 | −22.69 | 49.38 | 52.11 | ℓ pinned at cap |
| RBF1/2/3 iso | −27.09 | 58.17 | 60.91 | ℓ=0.313 |
| RBF5 ARD | −20.50 | 52.99 | 61.20 | |
| RBF6 ARD+White | −17.81 | 49.62 | 59.19 | |

Both signals (shortened Matérn length scale + genuine RBF4 noise term) point the same direction: the basin has more local structure/variability than previously modelled. Matérn 1.5 sweeps below still used as the working surface for diagnostics this session.

### x2 sweep (n=29, Matérn 1.5) — CONFIRMS peak at P26, retracts wk9 reading
| x2 | 0.025 | 0.05–0.055 (P28) | 0.075 | 0.10 | **0.105–0.115 (P26)** | 0.125 | 0.13–0.135 (P27) | 0.15 | 0.175 | 0.20 | 0.25 | 0.30 |
|----|-------|-------|-------|------|------|-------|-------|------|-------|------|------|------|
| μ | −0.503 | −0.467→−0.460 | −0.435 | −0.415 | **−0.414→−0.4137** | −0.420 | −0.423→−0.428 | −0.445 | −0.480 | −0.514 | −0.580 | −0.643 |
| sd | 0.035 | 0.022→0.020 | 0.013 | 0.004 | **0.002→0.0005** | 0.006 | 0.008→0.009 | 0.011 | 0.016 | 0.027 | 0.059 | 0.093 |

**Sweep argmax: x2=0.110, μ=−0.4137 — essentially reproduces P26 exactly.** Clean unimodal profile, declining in both directions. The wk9 "interior optimum at 0.175" reading is now understood as an artefact of the previous (too-long) Matérn length scale over-smoothing past P26 into the rising-looking P27 region. Corrected model now predicts decline in both directions from P26, matching observed P27/P28/P29 results in direction (though not fully in magnitude for P29).

### x3 sweep (n=29, Matérn 1.5) — FALSIFIES the 0.66 pin, locates real peak near 0.58
Initial narrow sweep (0.60–0.70) showed monotonic decline with argmax pinned at the window's own lower edge (0.600) — the classic edge-artifact tell. Extended sweep (0.05–0.70) revealed the true shape:

| x3 | 0.05 | 0.20 | 0.40 | 0.50 | **0.55** | **0.60** | 0.645–0.65 (P26) | 0.665 (P28) | 0.67 (P27) | 0.70 |
|----|------|------|------|------|------|------|------|------|------|------|
| μ | −1.130 | −0.874 | −0.531 | −0.412 | **−0.382** | **−0.381** | −0.415→−0.422 | −0.445 | −0.453 | −0.508 |
| sd | 0.227 | 0.179 | 0.136 | 0.099 | 0.071 | 0.038 | 0.015→0.016 | 0.024 | 0.027 | 0.046 |

**Genuine interior peak located at x3 ≈ 0.55–0.60** (μ≈−0.381 to −0.382), broad and shallow — NOT the previously-assumed 0.66. The x3=0.66 pin that constrained every constrained-LHS search for several weeks was actively suboptimal. sd in the new peak zone (0.04–0.07) is moderate — better constrained than deep extrapolation (x3<0.3) but looser than the tight cluster at 0.645–0.670.

**Historical low-x3 points checked** (x3<0.55, n=15 points): none share the other four coordinates closely enough to directly anchor this specific basin slice, but all confirm the general far-left decline pattern (every point with x3<0.1 scores poorly, −1.3 to −2.6), consistent with the sweep's steep fall toward x3=0.05.

### P30 — Submitted this session (awaiting result)
- **Point:** [0.502914, 0.098573, 0.584217, 0.720294, 0.160457]
- **Formatted:** `0.502914-0.098573-0.584217-0.720294-0.160457`
- **Method:** constrained LHS, centre=[0.510, 0.110, 0.580, 0.680, 0.120], half-width=[0.05, 0.015, 0.020, 0.05, 0.05] — both x2 and x3 recentred on sweep-confirmed peaks (x2: 0.150→0.110; x3: 0.660→0.580). 80/80 candidates valid (0 dropped by dmin filter — entirely unexplored region).
- **μ=−0.3564, sd=0.0658** — predicted +0.0575 over incumbent P26, the largest predicted gain proposed for this function to date.
- **Caveat:** sd=0.0658 is wider than the last two submissions (P28 sd=0.022, P29 sd=0.031), both of which still missed by 0.08–0.10 despite tighter uncertainty. This candidate is qualitatively better-founded (both dims corrected via full-range sweeps, not partial/stale profiles) but should not be assumed safe.

---

## Current Best
**y_best = −0.4139** at P26 [0.518, 0.109, 0.648, 0.673, 0.134]. Pending P30 result.

---

## Good region (revised this cycle)
- x1 ≈ 0.48–0.52
- **x2 ≈ 0.10–0.12** (peak CONFIRMED at 0.110 via full sweep — retracts wk9's 0.175 reading)
- **x3 ≈ 0.55–0.60** (peak RELOCATED via extended sweep — retracts prior 0.65–0.66 reading; genuinely interior, broad/shallow)
- x4 ≈ 0.67–0.72
- x5 ≈ 0.12–0.16
Danger zones unchanged (high x2+x5; x1>0.9; x3<0.3 confirmed poor by both sweep and historical data).

---

## Interpreting P30 result
- **≥ ~−0.38 (near predicted):** both corrections confirmed; new best, basin genuinely shifted from where weeks of prior search assumed. Final submission (P31) → tight RSM/quadratic polish around P30.
- **−0.41 to −0.45 (small gain or wash vs P26):** partial credit — x2 correction likely real (matches clean sweep), x3 correction may be softer/broader than the point estimate suggests. Final submission → polish centred between P26 and P30, weighted toward whichever has higher y.
- **< −0.46 (miss, matches P27–P29 pattern):** fourth consecutive miss below P26. Strong signal to stop chasing corrected profiles and treat P26 as the true local optimum. Final submission → tight near-repeat of P26 (perturbation <0.02 per dim) as safest possible confirmation/polish, or accept P26 as final answer if budget is tightest priority.

## Remaining Budget & Priority Queue (1 after P30)
1. Await P30 → route via tree above
2. Final submission (P31): RSM/quadratic polish OR tight confirmatory repeat near best incumbent (P26 or P30), depending on P30 outcome
3. No further profile-correction cycles possible — this is the last opportunity to test a hypothesis before the budget is spent on exploitation only

---

## Key Learnings (Function-specific)
- **Three consecutive misses below a high-water mark is a stronger signal than any single miss** — P27, P28, P29 all undershooting P26 was the trigger to re-examine the located optima directly via sweeps, rather than continuing to chase the original "interior optimum at 0.175" hypothesis.
- **An argmax pinned exactly at a sweep window's edge is not a real optimum — it's a sign the window is too narrow.** Caught twice this project (x2's floor test earlier, now x3's initial 0.60–0.70 window). Always extend the sweep range when this happens before trusting the result.
- **A previously "located" optimum can itself be wrong, not just imprecise** — the x3≈0.66 pin, treated as settled for several weeks and used to constrain every subsequent search, was actively suboptimal once directly swept. Located optima should be periodically re-validated via full-range sweep, not assumed permanent once found.
- **Kernel disagreement (shortened Matérn length scale + newly-nontrivial RBF4 noise term) independently corroborated the "basin sharper than modelled" read** before the sweeps confirmed it directly — worth treating a kernel-ranking flip as an early warning sign, not just a technical footnote.
- **0/80 candidates dropped by the dmin filter on the corrected search** confirms the new centre lands in genuinely unexplored territory — appropriate given two coordinates shifted, but a reminder that the wider sd on this candidate is a real reflection of novelty, not overcaution.
- EI canary excursed a fourth consecutive week (kernel-independent); remains canary-only, not a candidate source.
