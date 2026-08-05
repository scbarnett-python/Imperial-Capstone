import numpy as np
import matplotlib.pyplot as plt


def plot_progress(y_fit, labels=None, iteration_start=10, maximize=True,
                   objective_label="y_fit", function_name="Function",
                   save_path=None):
    """
    Plot objective progression per iteration with a running high-water mark
    and a marker for where weekly (post-initial) iterations began.

    Parameters
    ----------
    y_fit : array-like
        Observed objective values in submission order (P1, P2, ...).
    labels : list[str], optional
        Point labels for x-axis ticks. Defaults to P1..Pn.
    iteration_start : int, optional
        The point number (1-indexed, e.g. 10 for P10) at which weekly
        iterations began (i.e. initial data ends, sequential queries start).
        A vertical line is drawn just before this point. Set to None to
        skip the line entirely.
    maximize : bool, optional
        True if the objective is being maximised (running best = cummax).
        False for minimisation problems (F3, F4) (running best = cummin).
    objective_label : str, optional
        Y-axis label / name of the objective (e.g. "y_fit", "y").
    function_name : str, optional
        Used in the plot title, e.g. "Function 1".
    save_path : str, optional
        If given, saves the figure to this path.

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """
    y_fit = np.asarray(y_fit, dtype=float)
    n = len(y_fit)
    iterations = np.arange(1, n + 1)

    if labels is None:
        labels = [f"P{i}" for i in iterations]

    running_best = np.maximum.accumulate(y_fit) if maximize else np.minimum.accumulate(y_fit)
    best_idx = (np.argmax(running_best) if maximize else np.argmin(running_best))

    fig, ax = plt.subplots(figsize=(10, 6))

    # Observed objective per iteration
    ax.plot(iterations, y_fit, 'o-', color='tab:blue', label=f'{objective_label} (observed)', zorder=3)

    # High-water mark line
    hwm_label = 'High-water mark (running best)' if maximize else 'Low-water mark (running best)'
    ax.step(iterations, running_best, where='post', color='tab:red',
            linewidth=2, linestyle='--', label=hwm_label, zorder=2)

    # Vertical line marking start of weekly iterations
    if iteration_start is not None:
        ax.axvline(iteration_start + 0.5, color='tab:green', linewidth=1.5,
                   linestyle=':', zorder=1,
                   label=f'Weekly iterations start (after {labels[iteration_start - 1]})')

    # Annotate current best point
    ax.annotate(f'Current best: {running_best[-1]:.2f}\n({labels[best_idx]})',
                xy=(iterations[best_idx], running_best[best_idx]),
                xytext=(iterations[best_idx] + 0.5, running_best[best_idx] - 0.15 * np.ptp(y_fit)),
                fontsize=9, color='tab:red',
                arrowprops=dict(arrowstyle='->', color='tab:red', lw=1))

    ax.set_xlabel('Iteration (submission number)')
    ax.set_ylabel(objective_label)
    ax.set_title(f'{function_name} — {objective_label} progression with running best')
    ax.set_xticks(iterations)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.axhline(0, color='grey', linewidth=0.8, alpha=0.6)
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)

    return fig, ax


if __name__ == "__main__":
    # Example: Function 1
    y_fit_f1 = np.array([
        0, 0, -15.850239, 0, 28.520168, 0, 0, 0, 0, 0,
        -16.947710, 0, 29.128710, 0, 8.632887, 0,
        -25.836702, -15.784046, -29.013716
    ])
    plot_progress(y_fit_f1, iteration_start=10, maximize=True,
                  objective_label="y_fit", function_name="Function 1",
                  save_path="/mnt/user-data/outputs/Function1_progress_highwater.png")
    print("Saved.")
