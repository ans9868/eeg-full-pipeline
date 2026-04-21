# Eyes-Closed Random-50 LPSO Plan

This directory is for the eyes-closed MDD-vs-control `random50` LPSO configs.

The important idea is:

- generate the shared random fold bank once
- reuse the exact same fold bank for `ANOVA_L_2` and `PCA_L_2`
- reuse the exact same fold bank once again for `ANOVA_L_6` and `PCA_L_6`

That keeps the comparisons fair and matches the pattern already used in the FTD/control configs.

## Subject Pool

Use the cleaned BIDS EDF dataset:

- dataset root: `/Volumes/CrucialX6/Home/bigData/4244171_normalized/BIDS`
- metadata file: `participants.tsv`
- condition: `eyesclosed`

Current available eyes-closed subjects:

- `control`: 27
- `mdd`: 29

The canonical raw paths should be:

- `.../sub-XXX/eeg/sub-XXX_task-eyesclosed_eeg.edf`

## Shared Fold Logic

We only need two shared fold banks:

1. `L2`
   - fold size: `2`
   - balanced by group: `1 mdd + 1 control`
   - total folds: `50`

2. `L6`
   - fold size: `6`
   - balanced by group: `3 mdd + 3 control`
   - total folds: `50`

For both:

- random seed: `42`
- fold generation style: balanced random sampling
- sampling is without replacement inside a fold
- subjects may reappear across different folds

That last point is important: this is a random fold bank, not a partition of the dataset.

## Why One Shared Generation Pass

The subject pool and seed are the same across the four target configs:

- `ANOVA_L_2_mdd_cntrl_random50`
- `PCA_L_2_mdd_cntrl_random50`
- `ANOVA_L_6_mdd_cntrl_random50`
- `PCA_L_6_mdd_cntrl_random50`

So the only thing that should differ between ANOVA and PCA is the feature-transformation block, not the held-out folds.

That means:

- build the `L2` fold bank once
- build the `L6` fold bank once
- inject each bank into two configs

## Relationship To `config-maker.py`

`config-maker.py` still contains the reusable LPSO context we care about:

- `generate_lpso_folds(...)`
- `select_test_subjects_automatically(...)`

But the current `random50` configs appear to use a custom precomputed random fold list with metadata like:

- `fold_generation_method: random_sampling`
- `folds_per_size: 50`
- `balance_by_group: true`
- `random_seed: 42`

So for this MDD/control adaptation, the practical plan is:

1. keep the existing random-50 contract
2. generate the fold bank with a tiny standalone helper
3. paste the resulting `lpso_folds` and `lpso_metadata` into the four YAMLs

## Proposed Steps

### 1. Generate the canonical subject lists

Read `participants.tsv` and build:

- all `control` eyes-closed EDF paths
- all `mdd` eyes-closed EDF paths

These should also become the `data_input.groups` block in every EC random-50 config.

### 2. Generate the shared fold banks

Using seed `42`:

- generate 50 balanced `L2` folds
- generate 50 balanced `L6` folds

Each fold should be a flat list of full EDF paths.

### 3. Build the four YAMLs

Use the Mac Mini FTD/control random-50 configs as the structural base, but replace:

- project names
- config names
- group keys/paths
- `lpso_folds`
- `lpso_metadata`

The four targets are:

- `ANOVA_L_2_mdd_cntrl_random50.yaml`
- `ANOVA_L_6_mdd_cntrl_random50.yaml`
- `PCA_L_2_mdd_cntrl_random50.yaml`
- `PCA_L_6_mdd_cntrl_random50.yaml`

## Validation Checklist

Before trusting the generated configs, check:

1. all `data_input.groups` paths exist on disk
2. every fold has the expected size
3. every fold is balanced by group
4. no fold contains duplicate subjects within itself
5. there are exactly 50 folds for `L2` and 50 for `L6`
6. the `L2` ANOVA and PCA configs use identical fold lists
7. the `L6` ANOVA and PCA configs use identical fold lists
8. `lpso_metadata` matches the actual generated folds

## Helper Script

Use:

- [generate_shared_random50_folds.py](/Volumes/CrucialX6/Home/projects/eeg-full-pipeline/configs_mdd_vs_cntrl_mac_mini/eyes_closed/lpso_random_50/generate_shared_random50_folds.py)

It does two useful things:

- prints the relevant `config-maker.py` function blocks for reference
- previews or writes the shared `L2` and `L6` fold banks for the MDD/control eyes-closed dataset
