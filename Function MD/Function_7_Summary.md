# Function 7 — Summary
**Last updated:** 2026-08-03 (wk10, submission 10 of 13: P39 = 2.9098 NEW BEST (third consecutive ensemble win, close to maximin prediction); log-scale deceleration detected; maximin cross-rank bug found and fixed (was re-scoring stale P39 coords); corrected re-run found no candidate beating incumbent; RSM attempt failed sanity check (cluster too heterogeneous, optimizer pinned at box edges); explicit x6-down test confirmed gradient exhausted; tight multi-dim nudge P40 = [0.135, 0.145, 0.270, 0.305, 0.340, 0.660] submitted as confirmatory step. 2 submissions remain after P40.)

---

## Problem Definition
- **Type:** 6D black-box optimisation
- **Description:** ML Hyperparameter Tuning
- **Goal:** Maximisation
- **Input space:** x₁ … x₆ ∈ [0, 1]⁶
- **n evaluated:** 39 points (P1–P39); P40 submitted this session
- **Output character:** strictly positive, ~3 decades → log10 transform (retained)

---

## Current Dataset (n=39, tail)

| # | x1 | x2 | x3 | x4 | x5 | x6 | y |
|---|----|----|----|----|----|----|---|
| P36 | 0.1146 | 0.1529 | 0.1347 | 0.1803 | 0.3270 | 0.8655 | 1.710 |
| P37 | 0.066661 | 0.116010 | 0.283732 | 0.192233 | 0.387712 | 0.791659 | 2.070 |
| P38 | 0.141922 | 0.115034 | 0.203790 | 0.282529 | 0.341104 | 0.732189 | 2.699 |
| **P39** | **0.130864** | **0.149666** | **0.274621** | **0.299390** | **0.345033** | **0.643752** | **2.9098 ✅ best** |

(P1–P35 unchanged; see prior summary / npy for full precision.)
Full precision: `./initial_data/function_7/merged_inputs.npy` / `merged_outputs.npy`.

### P39 result (returned this session) — new best, near-accurate maximin prediction
- **[0.130864, 0.149666, 0.274621, 0.299390, 0.345033, 0.643752] → 2.9098** — new best, +7.9% over P38. Fourth consecutive weekly best.
- Predicted (maximin, ARD#1 winner): 2.983. Actual 2.9098 — miss of 2.4%, well inside "P38-class, plausibly better" expectation. Best-calibrated split-resolved pick to date (vs. P37's larger miss under the same regime) — suggests split-picks that reject a self-exploiting arbitrage candidate may be more reliable than splits driven by genuine surface disagreement on value. Flagged as a refinement to the unanimity calibration rule, not yet fully established.
- Gradients continued: x4 0.283→0.299 (held near ceiling of rise), x6 0.732→0.644 (fifth cycle of retreat).

### Log-scale deceleration detected (y_fit progression plot)
P36→P39 log-scale steps: +0.082, +0.115, **+0.033** — the P38→P39 step is much smaller in log terms than the raw-y jump (2.70→2.91) suggested. Compare to the P30→P31 initial jump of +1.19 — the climb has shifted from large discrete jumps to small increments, consistent with approaching a local optimum. This was the trigger for this session's investigation into whether the exploitation phase has run its course.

### Kernel refit (n=39) — stable, no material change
- RBF1 (iso): `0.968² × RBF(ℓ=0.501)`, LML=−33.75, AIC=71.50 ✅ (wins AIC/BIC)
- RBF5 (ARD): `0.928² × RBF(ℓ=[0.80, 0.698, 0.652, 0.39, 0.36, 0.598])`, LML=−29.15 (wins raw LML)
- Per-param gain iso→ARD ≈ 0.92 nats/param — near-tie holds, ensemble protocol still the correct resolution.
- **Length-scale drift n=38→n=39:** x1 1.7%, x2 1.7%, x3 4.2%, x4 1.0%, x5 2.9%, x6 7.6% — all under 10%, hierarchy stable (x4/x5 most sensitive, x1 least). Noise still pins at floor on both White variants — noiseless confirmed again.
- Kernel stability itself (not still adapting) is a second independent signal supporting the "near local optimum" read.

### Maximin cross-rank bug found and fixed this session
The wk9 ensemble cell (`cands = np.array([...])`) had **hardcoded coordinates from the prior week**, rather than reading the fresh LHS output (`next_x`) generated in the cell above it. This meant "ARD#1" in the wk9-carried-forward comparison was silently re-scoring **P39's own coordinates** against the refit kernel — explaining why its iso/ard/maximin scores (0.4639/0.4639/0.4639) matched the current best exactly. Not new information; a stale-candidate artifact.
- **Fix applied:** regenerated both ARD#1 (from cell 20's live `next_x`) and a freshly-run iso#1 (same LHS trust-region logic, scored under `gpr_iso`) this session. See corrected re-run below.
- **Standing fix still needed:** wire `cands = np.array([next_x, iso1_x])` directly rather than hand-typing coordinates each week — same class of bug as the EI x3-ceiling issue (manual per-cell wiring, no shared source of truth).

### Corrected maximin re-run (n=39, fresh candidates both sides)
| candidate | iso score | ard score | maximin |
|---|---|---|---|
| **ARD#1** (fresh LHS/ARD) | 2.881 | 2.875 | **2.875** |
| iso#1 (fresh LHS/iso) | 3.224 | 2.736 | 2.736 |

iso#1 shows the familiar self-exploitation pattern (own-surface 3.224 collapsing to 2.736 under ARD) — maximin correctly rejects it, same discipline as P37/P39. **Key result: ARD#1's maximin score (2.875) is BELOW the current incumbent (2.910) for the first time this project** — the properly-run trust-region search could not find a candidate either surface believes beats P39.

---

## Current Best
**y_best = 2.9098** at P39 (log10 = 0.4639). Pending P40 result.

---

## RSM attempt this session — FAILED, cluster/method issue identified
Given the deceleration + kernel stability + failed-to-beat-incumbent maximin signals, attempted an RSM (quadratic response surface) polish as a possible endgame method.
- **Option A (full 6D, ridge):** 28 coefficients vs. 8-point cluster — A matrix not negative-definite (one positive eigenvalue), stationary point ~2.4 units outside the cluster centroid. Rejected outright.
- **Option B (reduced-dim: x3–x6 active, x1/x2 fixed at cluster mean):** first attempt (top-8-by-value cluster, y_fit range −1.86 to 0.46) produced a stationary point pinned at EVERY active-dimension bound of the constrained optimizer's box — the same edge-artifact signature caught in Function 6's sweeps. GP cross-check confirmed the RSM candidate scored far below incumbent (iso 0.470, ard 0.451 raw y vs. incumbent 2.910) — a decisive rejection by the trusted surfaces.
- **Root cause: cluster too heterogeneous.** "Last 8 points" pulled in P32/P33, the volatile dip immediately after weekly iteration started, not just the clean P36–P39 climb. RSM is not viable on this function's current data density/heterogeneity — needs either a tighter true-local cluster (likely too sparse even then) or more accumulated points before revisiting.
- **RSM shelved for this function** unless cluster composition can be fixed and re-validated; not pursued further this session.

## Direct x6-gradient exhaustion test — CONFIRMS gradient has run out
Given RSM's failure, tested the one high-confidence live gradient directly: single-axis step continuing x6-down trend (0.644 → 0.580, all other dims held at P39), scored under both surfaces before submission.
- **iso: 0.4238 (y~2.653), ard: 0.4421 (y~2.768), maximin: 0.4238 (y~2.653) — BELOW incumbent (2.910), ~9% predicted decline.**
- **The five-cycle x6-down gradient (0.866→0.792→0.732→0.644) has run out of room.** Both surfaces agree a further step down is a regression, not an improvement. Not submitted.

## P40 — Submitted this session (awaiting result)
- **Point:** [0.135000, 0.145000, 0.270000, 0.305000, 0.340000, 0.660000]
- **Formatted:** `0.135000-0.145000-0.270000-0.305000-0.340000-0.660000`
- **Method:** tight multi-dimensional nudge around P39 — small perturbations across all six dims (largest single change: x6 +0.016, back toward P38's x6 rather than continuing the exhausted downward trend), NOT a repeat (function noiseless, exact repeat gives no new information).
- **Rationale:** tests local surface stability around P39 in several directions simultaneously, rather than one axis at a time. A near-P39 result confirms P39 sits at/near a genuine local peak; a meaningfully different result would indicate the peak isn't quite where tracked single-axis gradients suggested.
- **Interpretation for P40 result:**
  - **≈2.85–2.95 (close to P39):** confirms local peak; treat P39/P40-region as the practical answer for this function; preserve remaining 2 submissions for other functions.
  - **Meaningfully higher (>~3.0):** unexpected — would mean real headroom missed by the tracked gradients; worth one more small step toward whichever dimension moved most.
  - **Meaningfully lower (<~2.7):** reinforces P39 as a fairly sharp local optimum; stop active exploration here.

---

## Sensitivity hierarchy (log scale, holding, n=39)
x1 very low (data-enforced) · x2 low · x3 ≤ 0.30 ceiling (cluster hugs ceiling — standing tension, function may want higher x3 if allowed) · **x4 sensitive, rising, now flattening (0.19→0.28→0.30)** · x5 anchor 0.34–0.39 · **x6 retreating five cycles then EXHAUSTED at P39 (0.866→0.792→0.732→0.644→[decline confirmed below 0.644])**

---

## Convergent evidence this session (five signals, same direction)
1. Log-scale gains shrinking three steps running (P37→P38→P39)
2. Kernel length scales stable, not still adapting to new structure
3. Corrected maximin search found no candidate beating incumbent
4. RSM attempt failed outright (data too sparse/heterogeneous for this method currently)
5. Direct x6-down test confirmed the one trusted gradient has reversed

**Working conclusion: P39 (pending P40 confirmation) is likely at or very near this function's practical optimum given remaining budget.** Recommend conserving remaining submissions after P40 rather than continuing active exploration, absent a surprising P40 result.

---

## Acquisition Methods
- **LHS trust region + ensemble maximin (primary, now with fix applied):** r=0.10, x3 ceiling in the LHS cell. Regenerate BOTH iso and ARD candidates fresh each week (see bug section) rather than reusing prior-week hardcoded values.
- **EI (weekly canary): rejected, x3 ceiling bug STILL LIVE (4th+ week).** Fix `candidates = candidates[candidates[:,2] <= 0.30]` in the EI cell — not yet applied despite repeated flagging; low priority since EI's pick is independently rejected each week, but worth closing off.
- **RSM:** attempted this session, shelved — insufficient/too-heterogeneous local data currently.
- **UCB:** not run.

## Notebook items (carried forward + new)
1. ⏳ **EI cell: enforce x3 ≤ 0.30 mask** — still open, 4th+ week.
2. ✅ **Persist gpr_iso and gpr_ard** — done, standing machinery now in place (cell 21).
3. ⏳ **Wire maximin `cands` array to live candidates** — was the root cause of this session's stale-candidate bug; needs to read `next_x` (ARD) and a freshly-generated iso pick directly, not hardcoded coordinates.
4. ⏳ EI prints: add 10** conversions (log10 label).
5. Cosmetic: LHS "Using Kernel:" prints the unfit template then the fitted kernel — print only `gpr.kernel_`.

---

## Remaining Budget & Priority Queue (2 after P40)
1. Await P40 → route via interpretation tree above
2. If P40 confirms local peak (most likely outcome): treat as practical endgame for this function; hold remaining 2 submissions in reserve for other functions unless a specific new hypothesis emerges
3. If P40 surprises upward: one more small step in the indicated direction
4. RSM revisit only if cluster composition/density improves substantially — not viable currently

---

## Key Learnings (Function-specific)
- **A stale hardcoded candidate array can silently reproduce the incumbent's exact score** — the giveaway is scores matching the current best to four decimal places. Always verify ensemble/cross-rank cells are reading live candidate output, not carried-forward literals from a prior week.
- **Log-scale deceleration is a more reliable "approaching optimum" signal than raw-y jumps**, which can look dramatic even as relative/log gains shrink. Track both, but weight the log view for endgame timing decisions.
- **RSM requires a genuinely local, homogeneous cluster** — "most recent N points" can silently include volatile/exploratory points from earlier in a run. Explicitly verify cluster composition (plot y range, check point indices) before trusting a quadratic fit, especially in higher dimensions where parameter count already strains the data.
- **A constrained optimizer pinning at every bound simultaneously is the multi-dimensional analogue of Function 6's single-axis edge-argmax tell** — always a sign the fit doesn't have genuine interior curvature to work with, not a real answer.
- **When multiple independent lines of evidence (kernel stability, deceleration, failed search, failed RSM, direct gradient test) converge on the same conclusion, trust the convergence over any single signal** — this session's five-signal alignment is stronger grounds for pausing active exploration than any one check alone would justify.
- Split-picks that reject a self-exploiting arbitrage candidate (P39's regime) appear to calibrate better than splits from genuine surface disagreement on value (P37's regime) — tentative refinement to the unanimity rule, needs more data points to confirm.
