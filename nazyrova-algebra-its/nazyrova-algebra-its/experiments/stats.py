"""Statistical testing (Section 3.8): bootstrap CI for kappa, paired Wilcoxon for
RMSE, Holm-Bonferroni correction. Reproduces the significance claims of Section 4.1."""
from __future__ import annotations
import numpy as np
from scipy.stats import wilcoxon


def bootstrap_kappa_ci(y_true, y_model, kappa_fn, n_boot=10000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    stats = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        stats.append(kappa_fn(y_true[idx], y_model[idx]))
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return float(np.mean(stats)), float(lo), float(hi)


def paired_rmse_test(err_model_per_learner, err_baseline_per_learner):
    """Wilcoxon signed-rank on per-learner squared errors."""
    stat, p = wilcoxon(err_model_per_learner, err_baseline_per_learner)
    return float(stat), float(p)


def holm_bonferroni(pvalues):
    order = np.argsort(pvalues)
    m = len(pvalues)
    adj = np.empty(m)
    prev = 0.0
    for rank, i in enumerate(order):
        val = (m - rank) * pvalues[i]
        prev = max(prev, min(val, 1.0))
        adj[i] = prev
    return adj
