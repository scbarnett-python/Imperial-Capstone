**Black-Box Optimisation Capstone**

# Datasheet for the BBO Capstone Data Set

## Motivation

-   **Why was the data set created?** It supports a Bayesian Optimisation capstone project modelled on the structure of the NeurIPS 2020 Black-Box Optimization Challenge. The data set records the input-output history that underpins iterative maximisation of eight unknown black-box functions under a strict, non-renewable evaluation budget.

-   **What task does it support?** Sequential design of experiments under a Gaussian Process Regression surrogate model, where each new query is chosen using an acquisition function informed by every prior observation, and the analytical form of each function remains hidden throughout.

## Composition

-   **Contents.** Paired input-output arrays (X, y) for eight separate black-box functions, ranging from two to eight input dimensions, each defined over the unit hypercube [0,1]^d.

-   **Size.** Varies per function. Each began with an initial evaluated batch (roughly 15 to 48 points depending on dimensionality) and grows by one point per function per week as submissions return, toward a ceiling of thirteen total weekly submissions per function.

-   **Format.** Two .npy arrays per function under Data/{function_name}/, merged with weekly text files (Weekly_updates/{week}_inputs.txt and {week}_outputs.txt) via a central notebook, Update_Data_Points.ipynb, to produce the working arrays used in the main modelling notebook.

-   **Known gaps.** Files under Data/ are still named "initial_inputs.npy" and "initial_outputs.npy" for historical reasons, but by this stage actually contain the full merged data set, initial batch plus all weekly appends to date. A rename is planned but not yet complete. A stale-merge tripwire, printing n = len(y) at load time, guards against loading an out-of-date array.

## Collection process

-   **How queries were generated.** Each week, one candidate point per function was selected from a Gaussian Process Regression surrogate fitted to all prior observations, using an acquisition function chosen for that function's diagnosed characteristics, or a constrained trust-region local search when the acquisition function proved unreliable.

-   **Strategy.** Varied by function: straddle acquisition for weak-source detection (Function 1), a noise-aware kernel for a noisy log-likelihood surface (Function 2), a TuRBO-style adaptive trust region for an interior optimum (Function 3), and an ensemble maximin cross-rank between isotropic and ARD kernel surfaces wherever the two disagreed materially (Functions 6 through 8).

-   **Time frame.** Weekly cadence, one submission per function per week, across a thirteen-submission budget per function. This document reflects data through week 10 of that cycle.

## Preprocessing and uses

-   **Transformations applied.** Output values were transformed per function according to diagnosed scale and skew. A log10 transform was used where outputs spanned several decades or contained many near-zero values (Functions 5, 7 and 8). A signed, floor-anchored log transform was used for Function 1, to preserve sign information an unsigned log transform would otherwise discard. No transform was applied where the raw scale was already well conditioned (Functions 6 and 8's raw scale). Jacobian corrections were applied to log-marginal-likelihood comparisons whenever a log transform was active.

-   **Intended uses.** Fitting Gaussian Process surrogate models, running acquisition-guided sequential optimisation, and diagnosing kernel or acquisition performance for a bounded black-box maximisation task.

-   **Inappropriate uses.** The data set is not intended for training general-purpose supervised models unrelated to this optimisation task. It is not representative of any real-world distribution, since all eight functions are synthetic constructions built for this challenge. It should not be treated as independently and identically sampled data, since points were adaptively chosen based on prior observations rather than drawn independently.

## Distribution and maintenance

-   **Availability.** Not publicly distributed. Data resides locally within the project's Data/ and Weekly_updates/ directories, alongside per-function markdown summaries in MD/ and a central tracking sheet, Results/Data Points.xlsx. Will provide supporting data and notebook via Github.

-   **Terms of use.** Internal to this capstone project only. The underlying black-box functions and their outputs are provided by the course administrators and are not redistributed.

-   **Maintenance.** Maintained on a weekly cadence via Update_Data_Points.ipynb, which merges each new submission into the working arrays. Per-function markdown summaries in MD/ serve as the canonical living record of data set state, kernel configuration, and acquisition strategy after each update.

## Reflection

The most consequential data decisions in this project were the per-function output transforms and the treatment of stale or misleading file names. Documenting the transform choice for each function here made it possible to trace every downstream kernel comparison back to the scale it was actually fit on, which mattered directly when a transform was later found to be incorrect (Function 1's unsigned log transform, corrected to a signed floor-anchored version) or when a transform decision needed revisiting as more data arrived. The stale-merge tripwire exists because the "initial_inputs.npy" naming is misleading about what the file actually contains at this stage, and documenting that gap explicitly here is intended to prevent a future reader, including a later version of the author, from being misled by the file name alone.
