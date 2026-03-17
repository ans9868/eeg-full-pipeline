# Uncertainty and Effect Size Analysis: Bootstrapped CIs and Cliff's Delta

> *Recomputed by `compute_real_statistics.py` on 2026-03-02.*
> *All values are derived from `all_experiments_combined.csv`.*
> *Previous version of this file contained fabricated values — this version is computed from data.*

---

## Scope

This document covers the **Uniform-12 vs Random-50** LPSO comparison for
ANOVA and PCA at P=6.  These two protocols use different fold compositions,
so the test used is **Mann-Whitney U** (unpaired, two-sided).
The earlier (incorrect) version used a paired Wilcoxon and reported p < 0.001
with Cliff's δ = 0.62; the correct answer is no significant difference (see below).

---

## Methodology

| Step | Detail |
|------|--------|
| Input vector | Best-per-fold test accuracy (max over 3 HP configs per fold) |
| Uniform folds | n = 12 (systematic, P=6) |
| Random folds  | n = 50 (random, P=6) |
| CI | Bootstrap percentile, 10,000 resamples, seed=42 |
| Hypothesis test | Mann-Whitney U, two-sided (folds differ → unpaired) |
| Effect size | Cliff's δ |

---

## ANOVA Results

- Best model Uniform-12: **MLP**
- Best model Random-50:  **MLP**

| Protocol | n folds | Median (all-runs) | Median (best-per-fold) | 95% CI (best-per-fold) |
|----------|---------|-------------------|------------------------|------------------------|
| Uniform-12 | 12 | 69.9% | 72.6% | [67.2%–74.8%] |
| Random-50  | 50 | 69.5% | 73.1% | [72.1%–76.2%] |

- **Δ median** = +0.6 pp (Random − Uniform, best-per-fold)
- **Bootstrap 95% CI for Δ** = [-1.9, +6.9] pp
- **Effect size (Cliff's δ)** = 0.15 (small)
- **Mann-Whitney U p-value** = 0.428 (n.s.)

> **Conclusion:** No statistically significant difference between Uniform-12 and Random-50
> for ANOVA at P=6 (p = 0.428 (n.s.)).  The CI for Δ includes zero.
> The previous version's claim of p < 0.001 and δ = 0.62 was incorrect.

---

## PCA Results

- Best model Uniform-12: **KNN**
- Best model Random-50:  **KNN**

| Protocol | n folds | Median (all-runs) | Median (best-per-fold) | 95% CI (best-per-fold) |
|----------|---------|-------------------|------------------------|------------------------|
| Uniform-12 | 12 | 54.1% | 56.7% | [52.8%–61.9%] |
| Random-50  | 50 | 53.2% | 57.5% | [56.0%–60.4%] |

- **Δ median** = +0.8 pp (Random − Uniform, best-per-fold)
- **Bootstrap 95% CI for Δ** = [-4.5, +5.1] pp
- **Effect size (Cliff's δ)** = 0.09 (negligible)
- **Mann-Whitney U p-value** = 0.650 (n.s.)

> **Conclusion:** No statistically significant difference between Uniform-12 and Random-50
> for PCA at P=6 (p = 0.650 (n.s.)).  The CI for Δ includes zero.
> The previous version's claim of p < 0.001 and δ = 0.62 was incorrect.

---

## Model-by-Model Detail

### ANOVA

| Model | Uniform median (bpf) | 95% CI | Random median (bpf) | 95% CI | Δ (pp) | Cliff's δ | p (MWU) |
|-------|---------------------|--------|---------------------|--------|--------|-----------|---------|
| KNN | 67.8% | [65.0%–75.4%] | 71.5% | [69.4%–72.9%] | +3.8 | 0.14 (negligible) | = 0.471 (n.s.) |
| SVM | 71.8% | [65.1%–75.9%] | 71.0% | [69.1%–74.1%] | -0.7 | -0.02 (negligible) | = 0.936 (n.s.) |
| XGBoost | 68.4% | [61.6%–70.4%] | 69.4% | [66.4%–73.0%] | +0.9 | 0.11 (negligible) | = 0.551 (n.s.) |
| MLP | 72.6% | [67.2%–74.8%] | 73.1% | [72.1%–76.2%] | +0.6 | 0.15 (small) | = 0.428 (n.s.) |

### PCA

| Model | Uniform median (bpf) | 95% CI | Random median (bpf) | 95% CI | Δ (pp) | Cliff's δ | p (MWU) |
|-------|---------------------|--------|---------------------|--------|--------|-----------|---------|
| KNN | 56.7% | [52.8%–61.9%] | 57.5% | [56.0%–60.4%] | +0.8 | 0.09 (negligible) | = 0.650 (n.s.) |
| SVM | 57.6% | [52.6%–64.1%] | 56.5% | [55.0%–59.1%] | -1.1 | -0.05 (negligible) | = 0.782 (n.s.) |
| XGBoost | 57.5% | [51.3%–61.1%] | 57.8% | [54.0%–59.7%] | +0.4 | 0.03 (negligible) | = 0.866 (n.s.) |
| MLP | 55.9% | [49.5%–62.4%] | 57.2% | [54.3%–59.7%] | +1.3 | 0.12 (negligible) | = 0.539 (n.s.) |

---

## Bootstrap / Cliff's Delta Implementation

```python
import numpy as np
from scipy import stats

def bootstrap_ci_median(data, n=10_000, seed=42, confidence=0.95):
    """Bootstrap percentile CI for the median."""
    rng = np.random.default_rng(seed)
    meds = [np.median(rng.choice(data, size=len(data), replace=True)) for _ in range(n)]
    alpha = 1 - confidence
    return np.percentile(meds, 100*alpha/2), np.percentile(meds, 100*(1-alpha/2))

def cliffs_delta(x, y):
    """Cliff's delta: P(x > y) - P(x < y)."""
    x, y = np.asarray(x), np.asarray(y)
    dominance = sum(np.sign(xi - y) for xi in x)
    return float(dominance) / (len(x) * len(y))

# Paired test (same fold IDs):
stat, p = stats.wilcoxon(vec_a, vec_b, alternative='two-sided', zero_method='wilcox')

# Unpaired test (different folds):
stat, p = stats.mannwhitneyu(vec_a, vec_b, alternative='two-sided')
```
