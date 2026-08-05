# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 18:43:21 2026

@author: scbar
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rankdata
from itertools import combinations

def plot_nd_projection_matrix(X, y, dim_names=None, cols=3, cmap='viridis',
                                highlight_idx=None, figsize_per_panel=6, maximize=True):
    """Pairwise 2D projection matrix for n-dimensional input data."""
    n, d = X.shape
    if dim_names is None:
        dim_names = [f"x{i+1}" for i in range(d)]

    pairs = list(combinations(range(d), 2))
    rows = int(np.ceil(len(pairs) / cols))

    ranks = rankdata(y)
    sizes = 30 + 400 * (ranks - 1) / (len(y) - 1)
    order = np.argsort(sizes)

    fig, axes = plt.subplots(rows, cols, figsize=(figsize_per_panel * cols, figsize_per_panel * rows))
    axes = np.atleast_1d(axes).ravel()

    sc = None
    for panel_idx, (i, j) in enumerate(pairs):
        ax = axes[panel_idx]
        sc = ax.scatter(X[order, i], X[order, j], c=y[order], cmap=cmap,
                         s=sizes[order], edgecolors='k', linewidths=0.6, alpha=0.85)
        if highlight_idx is not None:
            ax.scatter(X[highlight_idx, i], X[highlight_idx, j],
                       facecolors='none', edgecolors='red', s=sizes[highlight_idx] + 60,
                       linewidths=2, zorder=6)
        ax.set_xlabel(dim_names[i]); ax.set_ylabel(dim_names[j])
        ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
        ax.set_title(f'{dim_names[i]} vs {dim_names[j]}')
        ax.grid(alpha=0.3)

    for k in range(len(pairs), len(axes)):
        axes[k].axis('off')

    fig.colorbar(sc, ax=axes[:len(pairs)].tolist(), location='right', shrink=0.7, pad=0.02,
                 label = 'y (higher = better)' if maximize else 'y (closer to 0 = better)')
    return fig, axes

