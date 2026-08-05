# Function 1 — Raw Y Maximisation (2D)

**Last updated:** 2026-08-02 (Submission 10 of 13 cycle — **major objective correction**: FAQ confirms raw-y maximisation, detection framing retired, log transform and epsilon floor dropped, straddle acquisition retired, EI re-run with corrected incumbent and rescaled xi. P20 candidate identified. 3 submissions remain.)

**Objective framing — CORRECTED THIS CYCLE:** Per the Capstone Project FAQ (`Capstone Project FAQs-1.pdf`), every function is a **plain maximisation problem on the raw output value**. Quote: *"Each task should be treated as a maximisation problem... framed as a maximisation problem (even if the real-world analogy is minimisation, as it's transformed so that higher is better)"*. There is no detection/source framing, no sign-inversion, no multi-source level-set structure implied anywhere in the FAQ. The "contamination source detection" narrative that drove weeks 1–9 of this function's strategy was an unverified assumption built on the problem's flavour text, not the actual scoring rule.

**Practical consequence:** the incumbent flips. **P19 (raw y = +0.011236) is the true best point, not P13** (raw y = −0.01464, previously treated as the "strongest source" and incumbent — it is now recognised as the **worst** observed point).

---

## Data state

n = 19 points, unchanged since P19 (no new evaluation this cycle — this session was spent correcting the objective and re-deriving acquisition from scratch).

| Point | x1 | x2 | y (raw) | Status under corrected objective |
|-------|-----|-----|---|----------------|
| P19 | 0.645355 | 0.665341 | **+0.011236** | **Best observed (incumbent)** |
| P17 | 0.696829 | 0.577612 | +7.474E-06 | Weak positive, negligible |
| P11 | 0.313131 | 0.333333 | +9.65E-15 | ~Zero |
| P3 | 0.731024 | 0.733000 | +7.71E-16 | ~Zero |
| P18 | 0.602765 | 0.773888 | +6.62E-16 | ~Zero |
| P15 | 0.587051 | 0.353482 | −4.67E-23 | ~Zero |
| P5 | 0.650114 | 0.681526 | −0.003606 | Poor |
| P13 | 0.636364 | 0.676768 | **−0.014641** | **Worst observed** |
| P1,2,4,6–10,12,14,16 | — | — | \|y\| < 1E-31 | ~Zero |

**Clustering note:** the three largest-magnitude points (P13, P5, P19) sit within a 0.017 radius of each other — P13↔P19 = 0.0145, P13↔P5 = 0.0146, P19↔P5 = 0.0169. Everything else of any real signal (P17) is ~0.10–0.12 away; the rest of the domain (P11, P3, P18, P15, and the noise points) is 0.27+ away and effectively featureless. This tight cluster spans nearly the full observed y-range in both directions (−0.0146 to +0.0112) within ~1.5% of the domain width — the source of this function's persistent kernel-fitting difficulty.

**Note on physical plausibility (retained from prior discussion, now reframed):** the sharp sign flip within 0.0145 doesn't cleanly match a smooth proximity-decay physical model (e.g. a radiation/contamination field), regardless of objective framing — more consistent with either a gradient/derivative-like quantity or a synthetic benchmark function chosen for optimisation difficulty rather than physical realism. No longer decision-relevant now the objective is confirmed as plain maximisation, but retained as report context.

---

## Transform pipeline — REMOVED THIS CYCLE

**The log transform, signed-log objective, and epsilon-floor noise classification are all retired.**

```python
y_fit = y   # no transform — raw y IS the maximisation objective per the FAQ
```

**Why they were adopted originally, and why that reasoning no longer applies:**
- The floor/log pipeline existed to (a) classify signal vs noise among near-zero points, and (b) compress ~120 orders of magnitude of range so faint "sources" (e.g. P15, y=−4.67E-23) remained distinguishable from true-zero noise. Both of these were in service of a *multi-source detection* task — telling weak signals apart from noise, and ranking sources by strength.
- Under plain raw-y maximisation, neither problem exists: you don't need to resolve P15 from noise, or compress the range, to find which single point has the largest raw y — P19 already answers that directly. `GaussianProcessRegressor(normalize_y=True)` handles the raw scale fine on its own; float64 has no precision issue at 1e-124 (nowhere near underflow ~1e-308).
- The floor/log approach was actively counter-productive under the corrected objective: without care, a naive `log10(|y|)` on a near-zero point like P4 (+3.34E-124) produces a *nonsensical* extreme negative score, ranking a harmless near-zero point as catastrophically bad, when in raw-max terms it's actually *better* than P13.

Retired code kept in a graveyard cell (`find_epsilon_floor`, floor-anchored signed log) with an explanatory comment — not deleted outright, in case a future function's raw-y range genuinely can't be handled without compression (this was a per-function judgement call, not a pipeline-wide rule).

---

## Model — Matérn 0.5 CONFIRMED on raw y (independently re-verified, not just carried over)

Re-ran the full kernel comparison on raw `y` (not the old log-space `y_fit`) to check whether the AIC preference for Matérn 0.5 still held under completely different input data. It does, and more decisively than before:

| Kernel | LML | AIC | BIC | Fitted kernel | Pinned at bound? |
|--------|-----|-----|-----|---------------|-------------------|
| **Matérn 0.5** | −38.6768 | **81.3536** | 83.2425 | 1.95² × Matérn(ℓ=0.05, ν=0.5) | length_scale only (lower, 0.05) |
| Matérn 1.5 | −47.5552 | 99.1104 | 100.9993 | 3.16² × Matérn(ℓ=0.05, ν=1.5) | constant_value (upper, 10) + length_scale (lower) |
| Matérn 2.5 | −51.5175 | 107.0350 | 108.9239 | 3.16² × Matérn(ℓ=0.05, ν=2.5) | constant_value (upper, 10) + length_scale (lower) |
| RationalQuadratic | −56.7663 | 119.5327 | 122.3660 | 3.16² × RQ(α=0.0683, ℓ=0.05) | constant_value (upper, 10) + length_scale (lower) |
| RBF | −60.4456 | 124.8911 | 126.7800 | 3.16² × RBF(ℓ=0.05) | constant_value (upper, 10) + length_scale (lower) |
| TwoScale_Matern | −32.6178 | 73.2356 | 77.0134 | 1.37² × Matérn(ℓ=0.02,ν=0.5) + 0.1² × Matérn(ℓ=2,ν=2.5) | **all three free params pinned** (two lower, one upper) — same degenerate pattern diagnosed previously, confirmed again on raw y |

**New diagnostic evidence for Matérn 0.5, beyond AIC rank:** it is the *only* kernel in the comparison whose amplitude (`constant_value`) converged freely, without pinning at the upper bound of 10. Every smoother kernel (1.5, 2.5, RBF, RQ) pins amplitude at its ceiling, straining to inflate overall variance as a workaround for a smoothness assumption that can't otherwise represent the sharp P13↔P19 local structure. Matérn 0.5's short length scale can represent that sharpness directly, so it doesn't need to compensate via amplitude. This is a structurally stronger justification than the AIC number alone — it shows *why* the other kernels fit worse, not just that they do.

**Decision: kernel selection unchanged — Matérn 0.5 remains correct**, now independently confirmed under the corrected objective rather than carried over from the old log-space comparison.

---

## Acquisition — Straddle RETIRED, EI corrected and re-run

### Straddle — retired this cycle

Straddle/level-set acquisition was built to answer "where is the model unsure whether a point is above or below a detection threshold T" — a question that only makes sense under multi-source detection framing. There is no meaningful threshold to straddle under plain raw-y maximisation. Moved to graveyard with explanatory comment; retained (not deleted) in case a future function genuinely needs level-set/threshold logic.

### EI — corrected incumbent, corrected candidate geometry, corrected xi scale

Three separate fixes required, in order of discovery:

1. **Incumbent**: was hardcoded to P13 with a comment; now resolves automatically via `y_best = np.max(y)`, so it can't silently go stale as new points are appended in future cycles. Correctly resolves to P19.
2. **Candidate geometry**: was previously restricted to a small disc (`radius=0.05`) hand-centred on P13 — a hardcoded assumption from the old cluster-exploitation strategy. Replaced with domain-wide uniform sampling (10,000 candidates, boundary_margin=0.05, min_dist=0.02 from existing points), matching the convention used elsewhere in the project.
3. **xi scale bug (significant)**: `xi=0.01` was calibrated for the old log-space `y_fit` scale (where the incumbent was ~29, so 0.01 was genuinely negligible). Under raw y (incumbent = 0.011236), this made `xi` **89% of the incumbent's own value** — verified this produced a near-degenerate EI (all 9,719 candidates showed positive EI, the winning candidate's predicted mean was actually *below* the incumbent, driven purely by uncertainty not exploitation). Corrected to `xi = 0.05 * (y.max() - y.min()) ≈ 0.0013`, restoring genuine exploitation signal.

**Corrected EI result:**
```
Candidates after min_dist filter: 9719
Incumbent y: 0.011236
Next point to evaluate: [0.664763, 0.644655]
EI: 0.000597
Predicted mean: 0.0060
Predicted std: 0.0068
Improvement term: -0.0065
```

Sanity checks: `mu` comfortably inside observed range (well under `1.5 × 0.011236 = 0.0169`), `EI > 0` reflects genuine (if modest) positive expected improvement, not a degenerate all-positive artefact.

**Improvement term is still negative** — by the project's own diagnostic convention this flags uncertainty-driven rather than exploitation-driven signal. Attributable to the pinned short length scale (ℓ=0.05): predictions decay toward the near-zero prior fairly quickly moving away from the tight P13/P5/P19 cluster, so any candidate beyond a small radius will show `mu` below incumbent almost by construction. Not necessarily a sign of a bad candidate — see directional check below.

**Directional corroboration (informal, worth noting):** the P20 candidate [0.664763, 0.644655] sits almost exactly on the extension of the P13→P19 gradient direction (P13→P19 ≈ (+0.009, −0.011); P19→candidate ≈ (+0.019, −0.021) — same direction, ~0.028 further along). This candidate emerged from an unconstrained, domain-wide 10,000-point search — it wasn't hand-anchored to this direction — so its independent alignment with the one real observed trend in the data is a corroborating signal beyond the raw EI number, even though the improvement term itself is weak.

### Decision: P20 = [0.664763, 0.644655]

Not yet submitted externally — awaiting user action.

---

## Notebook review notes (2026-08-02 pass)

Reviewed the corrected notebook end-to-end. Fixed correctly this cycle: kernel hardcoded to Matérn 0.5 (was RBF), duplicate `plot_progress` definition removed (was shadowing the Utils import), straddle and old EI properly moved to graveyard cells with explanatory comments, transform pipeline retired with explanation, EI candidate geometry and incumbent corrected.

**Remaining cleanup item (not yet actioned):** the GP mean/uncertainty plotting cell (final cell, "Signal Strength" panel) still uses hardcoded "source/anti-source" labels for P13, P5, P15, P11, P3, P17 and a "Contamination Source Detection" suptitle — vocabulary tied to the retired detection framing. Recommended fix drafted: replace hardcoded labels with dynamic top/bottom-N labelling by raw y (`np.argsort(-y)` / `np.argsort(y)`), so the plot self-updates as new points are appended rather than requiring manual relabelling each cycle, and drop `n_label` to 1 given the tight clustering causes label overlap at n_label=3. Colorbar/title language corrected to describe GP mean prediction rather than signal classification.

**Convergence warning handling:** added optional warning-capture wrapper to the kernel comparison cell (`warnings.catch_warnings(record=True)`) that summarises which parameters pinned at which bounds per kernel, printed inline as `[PINNED: ...]` rather than as separate stack-trace-style warning blocks. Useful for catching future kernel pathologies (like TwoScale's degeneracy) without manually re-enabling verbose warnings each time. Not yet decided whether to keep this permanently on or toggle per-session.

---

## Remaining budget (3, none spent yet this cycle)

**Recommended next step:** submit P20 = [0.664763, 0.644655]. This is the first submission of the corrected-objective era — worth treating its returned value as a validation check on the whole pipeline change (kernel + incumbent + acquisition all corrected simultaneously this cycle).

**After P20 returns:**
1. Re-fit kernel and re-run EI with n=20 to confirm Matérn 0.5 preference and pinning pattern hold with one more point.
2. If P20 improves on P19, the directional hypothesis (P13→P19 gradient continuing) gains support — consider a further step in the same direction for P21.
3. If P20 does not improve, treat the P13/P5/P19 cluster as likely local and consider a broader exploration probe for P21 rather than continued local refinement, given only 2 submissions would remain after that.

## Open items

- Finish the plotting-cell relabel (source/anti-source language → dynamic best/worst-by-raw-y labels) before this notebook is treated as report-ready.
- Consider whether the `[PINNED: ...]` warning-summary wrapper should be made a permanent fixture of the kernel comparison cell across all functions, given its diagnostic value in catching degenerate fits (as it did for TwoScale, twice).
- No leaderboard check needed any further — resolved definitively by the FAQ document this cycle.

## NeurIPS 2020 BBO Challenge context (for report)

This cycle is strong report material in its own right, beyond the earlier kernel-reversal story: it demonstrates the practical cost of an unverified problem-framing assumption propagating through an entire modelling pipeline (objective, transform, acquisition strategy) for multiple cycles before being caught by consulting primary source documentation (the FAQ) rather than continuing to reason from the problem's narrative framing. Directly supports a report point about validating assumptions against ground-truth specification early, and about how a plausible-sounding physical narrative ("contamination source detection") can quietly substitute for the actual, simpler stated objective ("maximise the output") if not explicitly checked. The xi-rescaling bug is a second, smaller instance of the same class of error — a parameter tuned correctly for one data scale silently becoming wrong when the underlying objective (and therefore data scale) changed.

---

## Full dataset (n=19, raw y, canonical)

```python
X = np.array([
    [0.319403889, 0.762959374],
    [0.574329215, 0.879898105],
    [0.731023631, 0.732999876],
    [0.840353417, 0.264731614],
    [0.650114060, 0.681526352],
    [0.410437137, 0.147554299],
    [0.312691157, 0.078722778],
    [0.683418169, 0.861057464],
    [0.082507252, 0.403487506],
    [0.883889829, 0.582253974],
    [0.313131,    0.333333   ],
    [0.515151,    0.878787   ],
    [0.636364,    0.676768   ],
    [0.192105,    0.571053   ],
    [0.587051,    0.353482   ],
    [0.672735,    0.190266   ],
    [0.696829,    0.577612   ],
    [0.602765,    0.773888   ],
    [0.645355,    0.665341   ],
])

y = np.array([
     1.32e-79,   1.03e-46,   7.71e-16,   3.34e-124,
    -3.606063e-03, -2.16e-54, -2.09e-91,  2.54e-40,
     3.61e-81,   6.23e-48,   9.65e-15,   1.04e-53,
    -1.4641144e-02, -7.31e-53, -4.67e-23, 7.71e-82,
     7.474096842056762e-06, 6.62e-16,
     0.011236118978605795,
])
```

**P20 candidate (EI, corrected objective, Matérn 0.5): [0.664763, 0.644655]** — not yet submitted.
