# LOSO Original Feature Baselines Plan - 2026-07-26

## Goal

Create LOSO versions of the original AD/CN P=2 feature-band experiments for both ANOVA and PCA.

The goal is to preserve the original feature/preprocessing setup and change only the split design:

```text
original: random LPSO P=2 held-out subjects per fold
new: LOSO/P=1, one held-out subject per fold, 65 folds total
```

## Source Configs

- `configs_ad_vs_cntrl_HPC/lpso_random_50/ANOVA_L_2_ad_cntrl_random50.yaml`
- `configs_ad_vs_cntrl_HPC/lpso_random_50/PCA_L_2_ad_cntrl_random50.yaml`

## Generated Configs

- `yaml_plan/ANOVA_LOSO_ad_cntrl_smoke5.yaml`
- `yaml_plan/PCA_LOSO_ad_cntrl_smoke5.yaml`
- `yaml_plan/ANOVA_LOSO_ad_cntrl_all65.yaml`
- `yaml_plan/PCA_LOSO_ad_cntrl_all65.yaml`

## Preserved Settings

- AD/CN 65-subject input list.
- Welch band-power feature extraction.
- Delta, Theta, Alpha, Beta bands.
- `window_size: 3.0`.
- `sliding_window: 0.5`.
- Original ANOVA or PCA feature transformation block.
- Original model grid family: XGBoost, MLP, KNN, SVM.

## Changed Settings

- Replaced random P=2 LPSO fold list with one subject per fold.
- Full configs have 65 ordered LOSO folds.
- Smoke configs have first 5 ordered folds only.
- Full configs use longer HPC Slurm walltimes.

## Run Order

- [x] Validate `ANOVA_LOSO_ad_cntrl_smoke5.yaml`.
- [x] Validate `PCA_LOSO_ad_cntrl_smoke5.yaml`.
- [x] Validate `ANOVA_LOSO_ad_cntrl_all65.yaml`.
- [x] Validate `PCA_LOSO_ad_cntrl_all65.yaml`.
- [ ] Run ANOVA smoke.
- [ ] Run PCA smoke.
- [ ] Inspect smoke outputs for fold shape and zero subject overlap.
- [ ] Run ANOVA all65.
- [ ] Run PCA all65.

## Notes

These configs are intended as direct split-design sensitivity checks. They are not new hyperparameter optimization experiments.

Local and Torch/HPC `config_handler.py` validation passed for all four generated configs on 2026-07-26.
