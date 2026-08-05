**Black-Box Optimisation Capstone**

# Model Card for the BBO Optimisation Approach

## Overview

- **Name.** Bayesian Optimisation approach for the Black-Box Optimisation Capstone: a per-function Gaussian Process surrogate with adaptive kernel selection and acquisition strategy.

- **Type.** Gaussian Process Regression (scikit-learn GaussianProcessRegressor), combined with a per-function acquisition function and kernel configuration chosen via information criteria (AIC/BIC) and calibration checks.

- **Version.** Current as of week 10 (submission 10 of 13) across all eight functions.

## Intended use

- **Suitable tasks.** Sequential black-box maximisation problems with a small number of input dimensions (two to eight), expensive or rate-limited evaluations, for example one query per function per week, and no access to gradient or analytical structure.

- **Use cases to avoid.** High-dimensional problems beyond roughly ten dimensions without further adaptation, since candidate sampling and kernel identifiability both degrade. Problems with a genuinely large evaluation budget, where simpler grid or random search would suffice. Any setting requiring real-time or low-latency decisions, since the approach assumes a weekly evaluation cadence throughout.

## Details: strategy across the submission cycle

- **Core method.** The Gaussian Process surrogate is refit after every new observation. Kernel family and configuration are selected by comparing log-marginal-likelihood, AIC, and BIC across isotropic RBF and Matern variants and their ARD (automatic relevance determination) counterparts. The acquisition function is chosen per function based on its diagnosed characteristics.

- **Acquisition functions used.** Expected Improvement as the default choice for most functions. Upper Confidence Bound for multi-peak landscapes and deliberate coverage probes. Straddle or level-set acquisition for Function 1's weak-source detection problem. IMSE, or Active Learning Cohn, for Function 2's stationary-kernel coverage bias. Latin Hypercube Sampling within a trust region became the primary method across most functions once Expected Improvement proved unreliable near sharp optima or on flat, arbitrage-prone regions.

- **Kernel management.** ARD length-scale bounds were capped per function to resolve seed-dependent instability, since uncapped bounds produced highly seed-dependent fits with different seeds pinning different dimensions at the bound. Cap values were calibrated per function rather than applied uniformly. A (0.05, 2.0) cap stabilised Functions 6 and 7, while Function 8 required a widened (0.05, 20) cap once genuine long length scales, in the range of 9 to 20, were identified on several dimensions. Function 1's kernel family flipped from RBF to Matern 0.5 at week 9 after a decisive swing in AIC, illustrating that kernel family selection is not fixed once and forgotten but must be revisited as data accumulates.

- **Ensemble and maximin protocol.** Adopted from week 8 onward, originating with Function 6 and later applied to Functions 7 and 8. Whenever isotropic and ARD surfaces disagreed materially on a candidate's value, both were scored under both surfaces and the maximin, or worst-case, winner was submitted. This explicitly rejects candidates that score well under only one surface, a pattern diagnosed as model-specific arbitrage rather than a genuine improvement.

- **Strategy evolution.** Early weeks favoured broad Latin Hypercube and Expected-Improvement-driven exploration. As functions approached their optima, the approach shifted toward increasingly targeted, hypothesis-driven local search, informed by profile sweeps along individual dimensions. Several "located" optima were later falsified by direct evidence and required correction: Function 5's x4 optimum direction reversed twice as successive boundary points were evaluated, and Function 6's x2 and x3 "located" optima were both falsified and relocated via full-range sweeps after three consecutive submissions underperformed the existing incumbent.

- **Endgame (response-surface) methodology.** A quadratic response-surface polish was planned as an endgame method but required correction once attempted. A full-dimensional quadratic proved unidentifiable given available local cluster sizes, for example forty-five coefficients for an eight-dimensional quadratic against roughly eight local points. The corrected approach instead used either a reduced-dimension quadratic, fitted only on the most sensitivity-ranked dimensions per the ARD length scales, or a direct Gaussian-Process-mean argmax within a tightly bounded local box.

## Performance

- **Metrics used.** Best-observed output value, tracked as a running high-water mark, per function. Log-marginal-likelihood, AIC, and BIC for kernel model selection. Predictive mean and standard deviation calibration, expressed as a z-score of the actual result against the surrogate's prediction, used throughout to monitor surrogate reliability, particularly under extrapolation.

Summary across all eight functions, as of the most recent submission on each function at the time of writing:

| **Function** | **Dims** | **Goal** | **Current best**                   | **Active method**             | **Status**                                                              |
|--------------|----------|----------|------------------------------------|-------------------------------|-------------------------------------------------------------------------|
| 1            | 2D       | Maximise | In progress (signed log transform) | Straddle (level-set)          | Kernel flipped RBF to Matern 0.5 at wk9; surface being re-stabilised.   |
| 2            | 2D       | Maximise | y = 0.611 (Peak A)                 | EI + IMSE (coverage)          | Noise-aware kernel; basin-constrained EI active.                        |
| 3            | 3D       | Maximise | y = -0.00898                       | TuRBO trust region + LHS      | RBF kernel, noiseless and smooth, confirmed.                            |
| 4            | 4D       | Maximise | y = -0.0424                        | UCB / variance probe          | Noisy function; radial unimodal structure confirmed.                    |
| 5            | 4D       | Maximise | y = 8,115.43 (P29)                 | Boundary-slice grid search    | x4 direction reversed twice; corner test submitted.                     |
| 6            | 5D       | Maximise | y = -0.4139 (P26)                  | Constrained LHS               | x2/x3 optima falsified and relocated; corrected candidate submitted.    |
| 7            | 6D       | Maximise | y = 2.9098 (P39)                   | LHS + ensemble maximin        | Converging signals suggest local optimum; confirmatory nudge submitted. |
| 8            | 8D       | Maximise | y = 9.9698 (P49)                   | LHS trust region (Matern ARD) | Plateau confirmed since P41; x8 diagnostic probe submitted.             |

## Assumptions and limitations

### Assumptions

- Each function's underlying surface is smooth enough to be well approximated locally by a Gaussian Process with a stationary kernel.

- Evaluations are approximately noiseless except where explicitly diagnosed otherwise. Function 4 was confirmed noisy; Functions 3, 5, 6, 7, and 8 were confirmed effectively noiseless via consistent rejection of a WhiteKernel noise term.

- The input domain is genuinely bounded to the unit hypercube, with no queries permitted outside it.

### Constraints

- Exactly one query per function per week, with no opportunity to correct a submitted point until the following week's result returns.

- A total budget of thirteen submissions per function, which is non-transferable across functions even once a function's search has plateaued. This was confirmed explicitly for Function 8, where remaining budget had to be redirected toward targeted diagnostics rather than reallocated to a function with more apparent headroom.

### Failure modes observed

- **Extrapolation overconfidence.** RBF kernels showed severe overconfidence when queried outside the convex hull of observed data. On Function 8, a single extrapolating query missed its prediction by 6.6 standard deviations under an RBF kernel, but only 3.4 standard deviations under a Matern kernel fitted to the same data, showing that the choice of kernel smoothness materially affects how much a surrogate's stated uncertainty can be trusted off-support.

- **Expected Improvement failure near sharp optima.** Expected Improvement consistently failed in exploitation phases near optima with short length scales, producing negative improvement terms and unreliable boundary drift. This was resolved by switching to trust-region-constrained local search, using the Gaussian Process mean directly as the search objective.

- **Edge artefacts in profile sweeps.** A "located" interior optimum, identified from a partial-range profile sweep, was repeatedly revealed to be an artefact of an insufficiently wide search window rather than a genuine interior maximum. This was only resolved by explicitly extending the sweep range and confirming a true turnover on both sides, most clearly demonstrated on Function 6.

- **Unreliable response-surface fits on heterogeneous clusters.** A response-surface quadratic fit produced a stationary point pinned simultaneously at every dimension's search-box boundary, a clear sign of an unreliable fit, when the local cluster used for fitting was not sufficiently homogeneous. The candidate was decisively rejected once cross-checked against the trusted Gaussian Process surfaces, illustrating the value of always validating a new method's output against an established one before committing a submission.

## Ethical considerations

- **Transparency and reproducibility.** Every acquisition decision is logged with its generating method, predicted mean and uncertainty, and rationale in per-function markdown summaries. This allows any submitted candidate to be traced back to the exact kernel configuration, acquisition function, and constraint set that produced it. A standing discipline was maintained throughout the project: submit the genuine method argmax, or explicitly encode any manual step as a reproducible rule, rather than presenting a hand-chosen point as a method output. This discipline was also the primary mechanism by which errors were caught, for example a constraint-enforcement bug that was applied in one acquisition cell but silently missing from another for several consecutive weeks on Function 7.

- **Real-world adaptation.** The emphasis on documenting kernel calibration, extrapolation risk, and acquisition failure modes reflects considerations directly relevant to deploying Bayesian Optimisation in real-world resource-constrained settings, for example identifying top-performing funds or evaluating tail-risk hedging strategies in quantitative finance, where a single poorly calibrated query can carry a real and irreversible cost. Transparent documentation of assumptions and failure modes, as maintained throughout this project, is a precondition for any recommendation produced by the model being acted upon safely in such a setting.

## Reflection

The optimisation approach makes decisions by combining a fitted surrogate's predicted mean and uncertainty with an explicit, function-specific acquisition rule, and by cross-checking any candidate proposed through a secondary or experimental method (such as a response-surface fit) against the primary, already-validated surrogate before submission. Its principal strengths are the systematic use of information criteria for kernel selection, the ensemble maximin protocol for resolving surface disagreement, and the practice of logging every decision's rationale in a form that supports later audit. Its principal limitations are the reliance on relatively small local clusters when attempting response-surface polishing in higher dimensions, and the fixed, non-transferable per-function budget, which means a plateaued function cannot be abandoned in favour of one with more headroom.

Adding further detail to this model card, for example a complete per-week log of every acquisition decision across all eight functions, would not materially improve its clarity or usefulness for an external reader. The per-function markdown summaries already serve that granular record-keeping role, and reproducing their full content here would obscure the higher-level strategy and lessons this model card is intended to communicate. The current structure, an overview of method, a function-by-function performance summary, and an explicit account of assumptions, limitations, and failure modes, is judged sufficient for the model card's intended audience and purpose.
