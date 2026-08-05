"""
IMSE / Active Learning Cohn (ALC) acquisition for Gaussian Process Bayesian Optimization.

Use this instead of pointwise max-variance ("argmax sigma") when you specifically want
COVERAGE/exploration points and want to avoid the boundary-clustering bias that pointwise
variance maximization exhibits for stationary kernels (RBF, Matern, etc).

Background
----------
Posterior variance sigma^2(x) under a stationary GP kernel depends only on the geometric
configuration of x relative to training points -- it has no notion of "this point is
*useful* to learn" vs "this point is merely far from data". Domain boundaries/corners
systematically have fewer neighbours (the domain doesn't extend past the edge), so they
appear maximally uncertain even though sampling them doesn't tell you much about the rest
of the space. This is documented in the computer-experiments literature (Sacks et al. 1989;
Santner, Williams & Notz, "The Design and Analysis of Computer Experiments").

IMSE / ALC fixes this by choosing the candidate that maximizes the *integrated* reduction
in posterior variance across the whole domain (or a representative reference set), rather
than the variance at a single isolated point. The one-step variance-reduction formula is
exact for GPs:

    delta_sigma2(x_ref ; x*) = k_post(x_ref, x*)^2 / sigma2_post(x*)

where k_post / sigma2_post are the posterior covariance / variance computed from the
*current* (pre-x*) fit. IMSE(x*) = mean over reference points of delta_sigma2(x_ref; x*).
"""

import numpy as np
from scipy.linalg import solve_triangular
from scipy.stats import qmc
from sklearn.gaussian_process import GaussianProcessRegressor


def imse_next_points(X, y, kernel, n_points=1, alpha=1e-6,
                      boundary_margin=0.05, n_candidates=2000, n_reference=2000,
                      domain=(0.0, 1.0), normalize_y=True, random_state=0):
    """
    Select next evaluation point(s) using the IMSE/ALC criterion.

    Parameters
    ----------
    X : array-like, shape (n_train, d)
        Training inputs.
    y : array-like, shape (n_train,)
        Training outputs.
    kernel : fitted sklearn kernel object
        Use the ALREADY-OPTIMIZED kernel, e.g. `gp.kernel_` after calling
        `gp.fit(X, y)` with the optimizer enabled. Do not pass an unfitted kernel.
    n_points : int, default 1
        Number of sequential coverage points to propose. Uses a "kriging-believer"
        heuristic (imputes the GP's own predicted mean as a placeholder y) to update
        the model between picks within the batch, so picks spread out rather than
        clustering on top of each other.
    alpha : float, default 1e-6
        Noise/jitter term -- should match the `alpha` used in your GaussianProcessRegressor.
    boundary_margin : float, default 0.05
        Candidates are restricted to [margin, 1-margin] (rescaled to `domain`) in every
        dimension, consistent with your existing acquisition functions. The REFERENCE
        grid still spans the full domain (margin doesn't apply there), since you still
        want credit for reducing uncertainty near the true edges.
    n_candidates, n_reference : int
        Number of Latin-Hypercube points used to approximate the candidate set and the
        integral, respectively. These are sample counts, not a per-dimension grid
        resolution, so this scales fine into higher dimensions (Functions 3-8) without
        the combinatorial blow-up of a meshgrid.
    domain : tuple (low, high)
        Input domain bounds, assumed identical across all dimensions (matches your [0,1]^d
        convention).
    normalize_y : bool, default True
        Should match the normalize_y setting used in your actual GaussianProcessRegressor
        fit (affects only the kriging-believer mean imputation step, not the variance
        integral itself, which is scale-invariant given a fixed fitted kernel).
    random_state : int

    Returns
    -------
    points : ndarray, shape (n_points, d)
        Selected next points, in the order they were chosen.
    scores : ndarray, shape (n_points,)
        IMSE score (integrated variance reduction) for each point at the time it was picked.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    d = X.shape[1]
    low, high = domain
    span = high - low
    lo_c, hi_c = low + boundary_margin * span, high - boundary_margin * span

    cand_sampler = qmc.LatinHypercube(d=d, seed=random_state)
    candidates = lo_c + cand_sampler.random(n_candidates) * (hi_c - lo_c)

    ref_sampler = qmc.LatinHypercube(d=d, seed=random_state + 1)
    ref_pts = low + ref_sampler.random(n_reference) * span  # full domain, including edges

    X_sim, y_sim = X.copy(), y.copy()
    picks, scores = [], []

    for _ in range(n_points):
        K = kernel(X_sim, X_sim) + alpha * np.eye(len(X_sim))
        L = np.linalg.cholesky(K)

        # posterior cross-covariance between every candidate and every reference point
        v_ref = solve_triangular(L, kernel(X_sim, ref_pts), lower=True)        # (n_train, n_ref)
        v_cand = solve_triangular(L, kernel(X_sim, candidates), lower=True)    # (n_train, n_cand)

        k_diag = np.array([kernel(c.reshape(1, -1))[0, 0] for c in candidates])
        sigma2_cand = k_diag - np.sum(v_cand ** 2, axis=0) + alpha             # posterior var at each candidate

        post_cov = kernel(candidates, ref_pts) - v_cand.T @ v_ref              # (n_cand, n_ref)

        var_reduction = (post_cov ** 2) / sigma2_cand[:, None]
        imse_score = var_reduction.mean(axis=1)                                # integrate over reference set

        idx = np.argmax(imse_score)
        pt = candidates[idx]
        picks.append(pt)
        scores.append(imse_score[idx])

        if n_points > 1:
            # kriging-believer: impute the GP's own predicted mean as a placeholder,
            # so the NEXT pick in this batch doesn't just choose the same spot again
            gp_tmp = GaussianProcessRegressor(kernel=kernel, normalize_y=normalize_y,
                                               alpha=alpha, optimizer=None)
            gp_tmp.fit(X_sim, y_sim)
            mu_pt, _ = gp_tmp.predict(pt.reshape(1, -1), return_std=True)
            X_sim = np.vstack([X_sim, pt])
            y_sim = np.append(y_sim, mu_pt[0])

    return np.array(picks), np.array(scores)


if __name__ == "__main__":
    # Quick self-test on Function 2's data
    from sklearn.gaussian_process.kernels import ConstantKernel, RBF

    X = np.array([
        [0.6658, 0.1240], [0.8778, 0.7786], [0.1427, 0.3490], [0.8453, 0.7111],
        [0.4546, 0.2905], [0.5777, 0.7720], [0.4382, 0.6850], [0.3418, 0.0287],
        [0.3386, 0.2139], [0.7026, 0.9266], [0.7071, 0.0000], [0.6869, 0.0000],
        [0.7879, 0.9798], [0.70, 0.02],
    ])
    y = np.array([
        0.539, 0.421, -0.0656, 0.294, 0.215, 0.0231, 0.245, 0.0387, -0.0139,
        0.6112, 0.564, 0.593, 0.159, 0.633053732246813,
    ])
    kernel = ConstantKernel(0.965 ** 2) * RBF(length_scale=0.0828)

    points, scores = imse_next_points(X, y, kernel, n_points=2, alpha=1e-6,
                                       boundary_margin=0.05, n_candidates=2000,
                                       n_reference=2000, domain=(0.0, 1.0),
                                       normalize_y=True, random_state=0)
    for p, s in zip(points, scores):
        print(f"Point: {p.round(3)}   IMSE score: {s:.5f}")
