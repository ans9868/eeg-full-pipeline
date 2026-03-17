# Subject-Level Evaluation — Summary Report
Generated: 2026-03-02

## Acceptance Criteria (best-per-fold across all models — replicates compute_real_statistics.py)

```
                     comparison                          test  delta_median_pp  cliffs_delta  p_value
       ANOVA vs PCA (Random-50) Wilcoxon signed-rank (paired)            15.65         0.851   0.0000
      ANOVA vs PCA (Uniform-12) Wilcoxon signed-rank (paired)            15.88         0.833   0.0005
Uniform-12 vs Random-50 (FTest)     Mann-Whitney U (unpaired)             0.59         0.150   0.4279
  Uniform-12 vs Random-50 (PCA)     Mann-Whitney U (unpaired)             0.82         0.087   0.6496
             P=6 vs P=2 (FTest)     Mann-Whitney U (unpaired)            -7.23        -0.319   0.0060
               P=6 vs P=2 (PCA)     Mann-Whitney U (unpaired)            -1.56        -0.167   0.1506
   MLP vs KNN (ANOVA Random-50) Wilcoxon signed-rank (paired)             1.61         0.206   0.0008
```

Overall: ✓ PASSED

## Subject Accuracy Summary (Mode 1: HP selected by epoch accuracy)

```
       experiment   model  n_folds  median_subject_acc  IQR_pp  min_subject_acc  max_subject_acc  CI_95_lo  CI_95_hi  is_best_model
 ANOVA_L_2_Random     KNN       50              100.00    0.00            50.00           100.00    100.00    100.00           True
 ANOVA_L_2_Random     MLP       50              100.00   50.00            50.00           100.00    100.00    100.00           True
 ANOVA_L_2_Random     SVM       50              100.00   50.00            50.00           100.00    100.00    100.00           True
 ANOVA_L_2_Random XGBoost       50              100.00   50.00             0.00           100.00     50.00    100.00           True
 ANOVA_L_6_Random     KNN       50               83.33   33.33            50.00           100.00     83.33     83.33           True
 ANOVA_L_6_Random     MLP       50               83.33   33.33            50.00           100.00     75.00     83.33           True
 ANOVA_L_6_Random     SVM       50               83.33   16.67            50.00           100.00     75.00     83.33           True
 ANOVA_L_6_Random XGBoost       50               83.33   16.67            50.00           100.00     66.67     83.33           True
ANOVA_L_6_Uniform     KNN       12               83.33   20.83            66.67           100.00     66.67     91.67           True
ANOVA_L_6_Uniform     MLP       12               83.33   16.67            33.33           100.00     66.67     83.33           True
ANOVA_L_6_Uniform     SVM       12               83.33   20.83            50.00           100.00     66.67     91.67           True
ANOVA_L_6_Uniform XGBoost       12               66.67   16.67            50.00           100.00     66.67     83.33          False
   PCA_L_2_Random     KNN       50               50.00    0.00             0.00           100.00     50.00     50.00           True
   PCA_L_2_Random     MLP       50               50.00    0.00            50.00           100.00     50.00     50.00           True
   PCA_L_2_Random     SVM       50               50.00    0.00            50.00           100.00     50.00     50.00           True
   PCA_L_2_Random XGBoost       50               50.00    0.00            50.00           100.00     50.00     50.00           True
   PCA_L_6_Random     KNN       50               50.00   16.67            33.33            83.33     50.00     50.00           True
   PCA_L_6_Random     MLP       50               50.00    0.00            33.33            83.33     50.00     50.00           True
   PCA_L_6_Random     SVM       50               50.00    0.00            50.00            83.33     50.00     50.00           True
   PCA_L_6_Random XGBoost       50               50.00    0.00            33.33            83.33     50.00     50.00           True
  PCA_L_6_Uniform     KNN       12               50.00   16.67            50.00           100.00     50.00     66.67           True
  PCA_L_6_Uniform     MLP       12               50.00    0.00            50.00            66.67     50.00     50.00           True
  PCA_L_6_Uniform     SVM       12               50.00    4.17            50.00            66.67     50.00     58.33           True
  PCA_L_6_Uniform XGBoost       12               50.00    0.00            50.00            66.67     50.00     50.00           True
```

## Epoch–Subject Correlation

```
       experiment pipeline   strategy  P   model  n_folds  pearson_r  pearson_p  spearman_r  spearman_p
 ANOVA_L_2_Random    FTest  Random-50  2     KNN       50     0.7409     0.0000      0.6775      0.0000
 ANOVA_L_2_Random    FTest  Random-50  2     MLP       50     0.8227     0.0000      0.7667      0.0000
 ANOVA_L_2_Random    FTest  Random-50  2     SVM       50     0.8114     0.0000      0.7636      0.0000
 ANOVA_L_2_Random    FTest  Random-50  2 XGBoost       50     0.7663     0.0000      0.7730      0.0000
 ANOVA_L_6_Random    FTest  Random-50  6     KNN       50     0.8080     0.0000      0.8139      0.0000
 ANOVA_L_6_Random    FTest  Random-50  6     MLP       50     0.8365     0.0000      0.8464      0.0000
 ANOVA_L_6_Random    FTest  Random-50  6     SVM       50     0.7869     0.0000      0.7562      0.0000
 ANOVA_L_6_Random    FTest  Random-50  6 XGBoost       50     0.8235     0.0000      0.8172      0.0000
ANOVA_L_6_Uniform    FTest Uniform-12  6     KNN       12     0.8012     0.0017      0.7040      0.0106
ANOVA_L_6_Uniform    FTest Uniform-12  6     MLP       12     0.4717     0.1216      0.1181      0.7148
ANOVA_L_6_Uniform    FTest Uniform-12  6     SVM       12     0.8337     0.0008      0.7848      0.0025
ANOVA_L_6_Uniform    FTest Uniform-12  6 XGBoost       12     0.7834     0.0026      0.7518      0.0048
   PCA_L_2_Random      PCA  Random-50  2     KNN       50     0.5072     0.0002      0.3483      0.0132
   PCA_L_2_Random      PCA  Random-50  2     MLP       50     0.5654     0.0000      0.3395      0.0159
   PCA_L_2_Random      PCA  Random-50  2     SVM       50     0.6244     0.0000      0.5822      0.0000
   PCA_L_2_Random      PCA  Random-50  2 XGBoost       50     0.5960     0.0000      0.4114      0.0030
   PCA_L_6_Random      PCA  Random-50  6     KNN       50     0.6673     0.0000      0.6640      0.0000
   PCA_L_6_Random      PCA  Random-50  6     MLP       50     0.7388     0.0000      0.6322      0.0000
   PCA_L_6_Random      PCA  Random-50  6     SVM       50     0.7167     0.0000      0.6926      0.0000
   PCA_L_6_Random      PCA  Random-50  6 XGBoost       50     0.6384     0.0000      0.5465      0.0000
  PCA_L_6_Uniform      PCA Uniform-12  6     KNN       12     0.9014     0.0001      0.7858      0.0024
  PCA_L_6_Uniform      PCA Uniform-12  6     MLP       12     0.4888     0.1069      0.5182      0.0844
  PCA_L_6_Uniform      PCA Uniform-12  6     SVM       12     0.1512     0.6391      0.1394      0.6657
  PCA_L_6_Uniform      PCA Uniform-12  6 XGBoost       12     0.6080     0.0359      0.4804      0.1139
```

## All Statistical Tests (both epoch and subject accuracy)

### Epoch accuracy tests (acceptance check):
```
                     comparison      model  delta_median_pp  cliffs_delta  p_value                          test
       ANOVA vs PCA (Random-50)        MLP            15.94         0.793   0.0000 Wilcoxon signed-rank (paired)
       ANOVA vs PCA (Random-50)        KNN            14.04         0.786   0.0000 Wilcoxon signed-rank (paired)
       ANOVA vs PCA (Random-50)        SVM            14.56         0.771   0.0000 Wilcoxon signed-rank (paired)
       ANOVA vs PCA (Random-50)    XGBoost            11.52         0.657   0.0000 Wilcoxon signed-rank (paired)
      ANOVA vs PCA (Uniform-12)        MLP            16.65         0.861   0.0005 Wilcoxon signed-rank (paired)
      ANOVA vs PCA (Uniform-12)        KNN            11.09         0.778   0.0005 Wilcoxon signed-rank (paired)
      ANOVA vs PCA (Uniform-12)        SVM            14.22         0.750   0.0005 Wilcoxon signed-rank (paired)
      ANOVA vs PCA (Uniform-12)    XGBoost            10.95         0.639   0.0093 Wilcoxon signed-rank (paired)
Uniform-12 vs Random-50 (FTest)        MLP            -0.59        -0.150   0.4279     Mann-Whitney U (unpaired)
Uniform-12 vs Random-50 (FTest)        KNN            -3.78        -0.137   0.4705     Mann-Whitney U (unpaired)
Uniform-12 vs Random-50 (FTest)        SVM             0.75         0.017   0.9361     Mann-Whitney U (unpaired)
Uniform-12 vs Random-50 (FTest)    XGBoost            -0.93        -0.113   0.5506     Mann-Whitney U (unpaired)
  Uniform-12 vs Random-50 (PCA)        MLP            -1.31        -0.117   0.5388     Mann-Whitney U (unpaired)
  Uniform-12 vs Random-50 (PCA)        KNN            -0.82        -0.087   0.6496     Mann-Whitney U (unpaired)
  Uniform-12 vs Random-50 (PCA)        SVM             1.09         0.053   0.7824     Mann-Whitney U (unpaired)
  Uniform-12 vs Random-50 (PCA)    XGBoost            -0.36        -0.033   0.8656     Mann-Whitney U (unpaired)
             P=6 vs P=2 (FTest)        MLP            -7.23        -0.319   0.0060     Mann-Whitney U (unpaired)
             P=6 vs P=2 (FTest)        KNN            -4.89        -0.228   0.0498     Mann-Whitney U (unpaired)
             P=6 vs P=2 (FTest)        SVM            -6.28        -0.267   0.0215     Mann-Whitney U (unpaired)
             P=6 vs P=2 (FTest)    XGBoost            -5.01        -0.221   0.0575     Mann-Whitney U (unpaired)
               P=6 vs P=2 (PCA)        MLP            -0.86        -0.036   0.7590     Mann-Whitney U (unpaired)
               P=6 vs P=2 (PCA)        KNN            -1.56        -0.167   0.1506     Mann-Whitney U (unpaired)
               P=6 vs P=2 (PCA)        SVM            -3.21        -0.164   0.1586     Mann-Whitney U (unpaired)
               P=6 vs P=2 (PCA)    XGBoost            -1.57        -0.187   0.1075     Mann-Whitney U (unpaired)
   MLP vs KNN (ANOVA Random-50) MLP vs KNN             1.61         0.206   0.0008 Wilcoxon signed-rank (paired)
```

### Subject accuracy tests (new results):
```
                     comparison      model  delta_median_pp  cliffs_delta  p_value                          test
       ANOVA vs PCA (Random-50)        MLP            33.33         0.802   0.0000 Wilcoxon signed-rank (paired)
       ANOVA vs PCA (Random-50)        KNN            33.33         0.727   0.0000 Wilcoxon signed-rank (paired)
       ANOVA vs PCA (Random-50)        SVM            33.33         0.796   0.0000 Wilcoxon signed-rank (paired)
       ANOVA vs PCA (Random-50)    XGBoost            33.33         0.702   0.0000 Wilcoxon signed-rank (paired)
      ANOVA vs PCA (Uniform-12)        MLP            33.33         0.917   0.0010 Wilcoxon signed-rank (paired)
      ANOVA vs PCA (Uniform-12)        KNN            25.00         0.701   0.0010 Wilcoxon signed-rank (paired)
      ANOVA vs PCA (Uniform-12)        SVM            33.33         0.750   0.0020 Wilcoxon signed-rank (paired)
      ANOVA vs PCA (Uniform-12)    XGBoost            25.00         0.653   0.0195 Wilcoxon signed-rank (paired)
Uniform-12 vs Random-50 (FTest)        MLP             0.00        -0.165   0.3516     Mann-Whitney U (unpaired)
Uniform-12 vs Random-50 (FTest)        KNN             0.00        -0.030   0.8713     Mann-Whitney U (unpaired)
Uniform-12 vs Random-50 (FTest)        SVM             0.00         0.033   0.8570     Mann-Whitney U (unpaired)
Uniform-12 vs Random-50 (FTest)    XGBoost            -8.33        -0.193   0.2836     Mann-Whitney U (unpaired)
  Uniform-12 vs Random-50 (PCA)        MLP             0.00        -0.130   0.4186     Mann-Whitney U (unpaired)
  Uniform-12 vs Random-50 (PCA)        KNN             8.33         0.027   0.8832     Mann-Whitney U (unpaired)
  Uniform-12 vs Random-50 (PCA)        SVM             0.00         0.015   0.9220     Mann-Whitney U (unpaired)
  Uniform-12 vs Random-50 (PCA)    XGBoost             0.00        -0.140   0.3544     Mann-Whitney U (unpaired)
             P=6 vs P=2 (FTest)        MLP           -16.67        -0.268   0.0097     Mann-Whitney U (unpaired)
             P=6 vs P=2 (FTest)        KNN           -16.67        -0.320   0.0020     Mann-Whitney U (unpaired)
             P=6 vs P=2 (FTest)        SVM           -16.67        -0.298   0.0067     Mann-Whitney U (unpaired)
             P=6 vs P=2 (FTest)    XGBoost           -16.67        -0.161   0.1406     Mann-Whitney U (unpaired)
               P=6 vs P=2 (PCA)        MLP             0.00         0.102   0.2659     Mann-Whitney U (unpaired)
               P=6 vs P=2 (PCA)        KNN             0.00         0.250   0.0092     Mann-Whitney U (unpaired)
               P=6 vs P=2 (PCA)        SVM             0.00         0.025   0.7585     Mann-Whitney U (unpaired)
               P=6 vs P=2 (PCA)    XGBoost             0.00         0.030   0.7471     Mann-Whitney U (unpaired)
   MLP vs KNN (ANOVA Random-50) MLP vs KNN             0.00         0.020   0.8551 Wilcoxon signed-rank (paired)
```

## Important: Subject Accuracy Quantisation
With P=6 subjects per fold, subject_acc is restricted to {0, 1/6, 2/6, 3/6, 4/6, 5/6, 6/6}
= {0%, 16.67%, 33.33%, 50%, 66.67%, 83.33%, 100%}.
With P=2: only {0%, 50%, 100%}.
This creates heavy tied ranks in Wilcoxon/Mann-Whitney; p-values are still valid
but power is substantially lower than for continuous epoch_acc.
Bootstrap CIs on subject_acc median may collapse to a single point.

## Label Mapping
  Group='alz'   → label=0.0 → AD (Alzheimer's Disease)
  Group='cntrl' → label=1.0 → Control
  prediction=0.0 → predicted AD
  prediction=1.0 → predicted Control
  AD_ratio = mean(prediction == 0.0)   [fraction of epochs predicted as AD]
  τ = 0.5: pred_subject_label = 0 (AD) if AD_ratio >= 0.5 else 1 (Control)

## HP Selection Rules
  Mode 1 (paper-consistent): select HP that maximises median(epoch_acc) across folds
  Mode 2 (deployment-aligned): select HP that maximises median(subject_acc) across folds