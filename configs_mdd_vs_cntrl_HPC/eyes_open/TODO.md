# configs_MDD_vs_cntrl_mac_mini TODO

This directory is for the Mac Mini configuration set targeting the cleaned MDD vs control dataset.

We should not build these configs with naive search/replace from the FTD versions. The main risks are:

- wrong raw file paths
- stale project/config names
- incorrect subject counts or assumptions
- broken random-seed reproducibility
- incorrect LPSO fold definitions

## 1. Within-Subject Seed Configs

These are the easier configs to regenerate because they mostly reuse the same experiment structure and only need the new dataset paths plus the intended random seeds.

### 1.1 Create directory structure

Create the matching subdirectories:

- `anova_w_c`
- `anova_w_f`
- `pca_w_c`
- `pca_w_f`
- `test`

### 1.2 Decide canonical data source

Use the cleaned BIDS EDF files as the canonical inputs, not the original normalized FIF paths.

Reason:

- subject IDs are now standardized as `sub-###`
- file names match the existing pipeline assumptions well
- this is the format we want the pipeline to support going forward

### 1.3 Define group file lists

Build the two canonical groups from the new dataset:

- controls
- MDD

Need to decide whether these configs should use:

- eyes closed only
- eyes open only
- both, depending on config family

### 1.4 Map old config families to new MDD/control families

Figure out what each existing family in `configs_ftd_vs_cntrl_mac_mini` is intended to mean:

- `anova_w_c`
- `anova_w_f`
- `pca_w_c`
- `pca_w_f`

Need to confirm what `w_c` and `w_f` should mean in the MDD/control context so we preserve the intended experiment semantics.

### 1.5 Reuse config-maker logic for seeded configs

Do not hand-edit each YAML.

Find the `config-maker.py` logic that generated the seeded family configs and reuse it, or replicate that exact logic in a controlled way.

Important seed-linked fields to preserve:

- `project.name`
- `project.random_seed`
- `project.config_name`
- `data_transformation_strategy.intra_test_train_split.random_seed`

### 1.6 Regenerate seed ranges

Regenerate the seeded within-subject configs for the intended range:

- `seed42` through `seed51`

For each family:

- ANOVA
- PCA
- whichever condition variants we decide to preserve

### 1.7 Validate within-subject configs

For each generated YAML, check:

- paths exist
- group membership looks right
- project naming is consistent
- config naming is consistent
- random seeds match the filename
- config passes `config_handler`

### 1.8 Smoke-test at least one config per family

Before trusting the whole family, run one representative config from each group and check:

- raw files load correctly as EDF
- subject IDs are parsed correctly
- output directory naming looks right
- train/test split behavior still works

## 2. LPSO Random-50 Configs

These are significantly harder and should be regenerated only after the within-subject configs are in good shape.

### 2.1 Preserve the current experiment intent

Identify exactly what the existing LPSO random-50 configs represent:

- number of folds
- number of held-out subjects per fold
- whether folds are stratified by group
- how fold randomization was seeded

### 2.2 Find the fold-generation logic in `config-maker.py`

This is the key step.

We should not manually rewrite fold subject lists in YAML.

Find and isolate the code that generated:

- the random 50-fold selections
- the subject assignments in each fold

### 2.3 Define the new subject pool

Regenerate folds using the cleaned MDD/control BIDS subject set, not the old ds004504 FTD/control subject pool.

Need to confirm:

- total controls available
- total MDD subjects available
- whether any subjects should be excluded because one condition is missing

### 2.4 Recreate fold generation reproducibly

For LPSO, we must preserve reproducibility:

- same intended random-seed behavior
- same fold-count behavior
- same holdout-size logic

This should come from the real generator logic, not from ad hoc scripting.

### 2.5 Regenerate the four LPSO configs

Target equivalents of:

- `ANOVA_L_2_*`
- `ANOVA_L_6_*`
- `PCA_L_2_*`
- `PCA_L_6_*`

using MDD vs control data and regenerated folds.

### 2.6 Validate fold definitions

For each regenerated LPSO config, verify:

- every fold references existing files
- train/test split is complete
- held-out subjects are what we expect
- no fold accidentally duplicates malformed subject paths
- fold count matches the config name/intention

### 2.7 Smoke-test one LPSO config before batch generation

Run one representative LPSO config first and confirm:

- EDF loading works
- fold discovery works
- transformed output is created in fold directories
- Ray/ML phase sees the expected number of folds

## 3. Cross-Cutting Checks

### 3.1 Naming conventions

Settle the naming convention for the new directory and files:

- directory: `configs_MDD_vs_cntrl_mac_mini`
- per-config project names
- per-config YAML names

### 3.2 Output directories

Make sure output directory names do not collide with old FTD/control runs.

### 3.3 Reuse flags

Decide which reuse/save flags should stay enabled for the new dataset so we do not accidentally mix outputs across experiments.

### 3.4 Documentation

Once configs exist, add a short README or note explaining:

- which dataset they target
- whether they use BIDS EDF inputs
- how they were regenerated
- what still needs validation
