# Function 8 — Summary
**Last updated:** 2026-08-03 (wk10, submission 10 of 13: P49 = 9.9698, new best, excellent calibration (miss 0.012) — confirms x4-floor restoration and kernel switch fixed the P48 failure; kernel refit stable 2nd week running (Matérn ARD, all drift <10%); EI/LHS results show near-zero predicted headroom (LHS gain only +0.0022) → plateau confirmed; P41-P49 progression flat (9 submissions, minimal net gain); pivoted remaining budget to targeted diagnostics rather than further exploitation; P50 = x8 diagnostic probe (holds pocket centroid on x1-x7, tests x8=0.65, well outside cluster's tested 0.04-0.36 range) submitted to resolve the oscillating x8 length-scale pin. 2 submissions remain after P50.)

---

## Problem Definition
- **Type:** 8D black-box optimisation
- **Description:** 8D ML Hyperparameter Tuning
- **Goal:** Maximisation
- **Input space:** x₁–x₈ ∈ [0, 1]⁸
- **n evaluated:** 49 points (P1–P49); P50 submitted this session
- **Output range:** 5.59–9.97 (factor 1.8) — no transform (raw scale well-conditioned)
- **Budget constraint noted this session:** per-function budgets are fixed; F8's remaining 3 submissions cannot be reallocated to other functions even though F8 shows a plateau. Remaining budget redirected to targeted diagnostics (x8 resolution, ensemble maximin) rather than continued blind exploitation.

---

## Current Dataset (n=49, tail)

| # | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | y |
|---|----|----|----|----|----|----|----|----|---|
| P46 | 0.0947 | 0.1562 | 0.1279 | 0.0866 | 0.9449 | 0.6121 | 0.2160 | 0.3028 | 9.96 |
| P47 | 0.151773 | 0.179893 | 0.170627 | 0.084135 | 0.936107 | 0.608799 | 0.254540 | 0.325262 | 9.95 |
| P48 | 0.126019 | 0.180323 | 0.123866 | 0.002696 | 0.979366 | 0.597917 | 0.311669 | 0.349985 | 9.919 |
| **P49** | **0.107542** | **0.160528** | **0.109353** | **0.096175** | **0.970870** | **0.558758** | **0.174878** | **0.344019** | **9.9698 ✅ best** |

(P1–P45 unchanged; see prior summary / npy for full precision.)
Full precision: `./initial_data/function_8/merged_inputs.npy` / `merged_outputs.npy`.

### P49 result (returned this session) — new best, excellent calibration
- **[0.107542, 0.160528, 0.109353, 0.096175, 0.970870, 0.558758, 0.174878, 0.344019] → y = 9.9698** — new best, edges past P46 (9.96) by +0.0097.
- Predicted μ=9.982 (Matérn) / ~9.976 (RBF ARD); actual 9.9698 → miss of only 0.012–0.013, well within precision. Confirms the x4-floor restoration and kernel switch (Matérn 2.5 ARD) fully corrected P48's failure — surface accuracy is back to normal in this pocket.
- Margin of improvement over the pre-P48 best (P46, 9.96) is small (+0.0097) relative to earlier weekly gains — consistent with plateau economics already flagged.

### Progression shape (y_fit plot, this session) — flat since P41
Initial batch (P1–P40) shows no trend, ranging 5.6–9.3 with pure noise-like scatter. **P41 jumped almost instantly to ~9.9** once directed search began — unlike F5/F6/F7's gradual multi-step climbs, F8 found its high-value pocket essentially immediately. **P41–P49 (9 submissions) has stayed in a narrow 9.4–10.0 band with no further meaningful climb** (P48's dip being the one exception, already diagnosed as an extrapolation failure). This is the clearest visual evidence that F8's true optimum region was located almost immediately, and recent submissions have been fine-tuning within an already-found basin, not searching for a new one.

### Kernel refit (n=49) — Matérn ARD stable, margin widened
| Kernel | LML | AIC | BIC | Notes |
|--------|-----|-----|-----|-------|
| **Matérn ARD (0.05,20)** | **+23.25** | **−28.49** | **−11.46** | ✅ margin over RBF ARD widened to ~10 nats (LML), AIC gap more than doubled vs last week |
| RBF6 ARD+White | +13.33 | −6.65 | 12.27 | |
| RBF5 ARD | +13.18 | −8.36 | 8.66 | previous champion |
| Matérn 2.5 (iso) | −7.53 | 19.07 | 22.85 | **still pinned at old (0.05,2.0) cap — inconsistency flagged, does not affect selection** |
| RBF1/2/3 (iso) | −10.09 | 24.17 | 27.95 | |

- **Length-scale drift n=48→n=49:** x1 1.3%, x2 3.8%, x3 1.0%, x4 1.2%, x5 8.4%, x6 2.0%, x7 0%, x8 pinned at 20 (2nd consecutive week). All well under 10% — second-week stability confirms the wk9 kernel switch was not a one-off cap artifact.
- **x3 remains sharpest** (shortest ℓ), matches the tight visual clustering in the projection matrix.
- **x8 pin: two consecutive weeks at 20 now** (previously oscillated 20↔13.9↔20) — slightly more suggestive of a genuine boundary preference than earlier back-and-forth, but still unresolved. Directly targeted by P50 (below).
- **Notebook inconsistency flagged:** non-ARD Matérn variants (2.5/1.5/0.5) still fit under the OLD (0.05, 2.0) cap, not the widened (0.05, 20) bounds applied to ARD. Doesn't affect kernel selection (ARD wins overwhelmingly regardless) but should be fixed for a clean iso-vs-ARD comparison if ever needed.

### EI and LHS results this session — plateau confirmed numerically
- **EI (canary):** rejected as expected — improvement=−0.379, EI≈0 (1.46e-05), σ=0.115. Proposed point extrapolates wildly off the established x5/x8 faces. No signal.
- **LHS trust region (r=0.06 around P49, Matérn ARD):** candidate [0.125999, 0.166333, 0.139625, 0.146773, 0.940746, 0.572055, 0.158733, 0.354095], **μ=9.9719 — predicted gain of only +0.0022 over incumbent**. Smallest predicted improvement of any candidate this project has proposed for F8, an order of magnitude smaller than P49's own (already modest) +0.022 prediction. Given demonstrated calibration accuracy this week (miss 0.012), a gain this small is within the model's own noise floor — effectively "no meaningful change" predicted, not a genuine direction.
- **Decision: did not submit this LHS candidate.** The trust-region search itself indicates no further headroom via this method at r=0.06.

### P50 — Submitted this session (awaiting result): x8 diagnostic probe
- **Point:** [0.130029, 0.161582, 0.163271, 0.136689, 0.940368, 0.500783, 0.221107, 0.650000]
- **Formatted:** `0.130029-0.161582-0.163271-0.136689-0.940368-0.500783-0.221107-0.650000`
- **Method:** x1–x7 held at pocket centroid (mean of P41, P42, P43, P44, P46, P47); x8 set to 0.650 — meaningfully outside the top cluster's tested range (0.04–0.36), but not an extreme-corner value, to isolate x8's true effect from generic edge-extrapolation risk.
- **Rationale:** with LHS/EI showing no further headroom in the established directions, and x8's ARD length scale pinned at the 20 cap for two consecutive weeks, this is the one genuinely open structural question remaining. Resolves whether the pin reflects true irrelevance (result ≈9.97) or unexplored real structure (result meaningfully higher or lower).
- **Interpretation for P50 result:**
  - **≈9.90–10.0 (close to current best):** confirms x8 is genuinely low-impact across this range; pin reflects real irrelevance. Settles the question; treat remaining 2 submissions as confirmatory/reserve only.
  - **Meaningfully higher (>~10.05):** unexpected — real headroom in x8 previously unexplored; worth a follow-up step in that direction with remaining budget.
  - **Meaningfully lower (<~9.85):** x8 matters more than the pin suggests; the cluster's narrow x8 range (0.04–0.36) is informative, not incidental.

---

## Current Best
**y_best = 9.9698** at P49 [0.107542, 0.160528, 0.109353, 0.096175, 0.970870, 0.558758, 0.174878, 0.344019]. Pending P50 result.

---

## RSM endgame — plan unchanged, not yet executed
Still the fallback if diagnostics (x8 probe, ensemble maximin) don't surface further gains:
1. Argmax of GP mean in a tight box (what LHS trust-region already approximates).
2. Reduced quadratic in the 3–4 sharpest dims (x3, x1, x7, x4 by Matérn ordering), smooth dims held at cluster-mean — identifiable at current cluster size (~10 points).

## Remaining Budget & Priority Queue (2 after P50)
1. Await P50 → route via interpretation tree above
2. If x8 confirmed inert: consider ensemble maximin cross-rank (RBF ARD vs Matérn ARD candidates) as next diagnostic, or move to reduced-quadratic polish
3. If x8 probe reveals structure: follow-up step in the indicated direction
4. Final submission, if not already used: tight confirmatory nudge or reduced-quadratic polish result, whichever remains most informative

---

## Key Learnings (Function-specific)
- **A per-function budget constraint means a plateaued function still needs a plan** — "stop and reallocate" isn't available when budgets are fixed per function. The right response to a plateau is to redirect remaining submissions toward resolving genuinely open structural questions (here: the x8 pin) rather than continuing to submit low-expected-value exploitation steps.
- **LHS trust-region candidates predicting near-zero gain, cross-checked against known calibration accuracy, is a reliable plateau signal** — when the predicted improvement is smaller than the model's own demonstrated miss magnitude, the search has stopped finding anything the model itself believes in.
- **A length-scale pin persisting across multiple weeks (not oscillating) is a stronger signal than a single-week pin** — worth escalating from "monitor" to "actively test" once it's held steady for 2+ consecutive refits, which is why x8 was targeted directly this session.
- **F8's progression shape (instant jump to near-ceiling, then long flat stretch) is qualitatively different from F5/F6/F7's gradual climbs** — worth noting in the report as an example of a function where the optimum region was essentially found by early exploration, with subsequent budget spent on fine-tuning and validation rather than search.
- Carried forward: kernel comparisons inherit cap artefacts (verify widened bounds before rejecting a family); RBF extrapolation overconfidence vs Matérn; a single point below support can collapse a long length scale; margins/floors are constraints and go stale; pinned ARD length scales can oscillate near the identifiability limit.
