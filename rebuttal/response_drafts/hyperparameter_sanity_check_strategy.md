# Hyperparameter Sanity Check Strategy

## Purpose

The hyperparameter response should not become a state-of-the-art optimization
claim. Its purpose is narrower:

```text
Does automated tuning remove the subject-overlap versus subject-disjoint gap?
```

The expected answer is no. A tuner can optimize within a protocol, but it cannot
make a leaked protocol subject-disjoint.

## Minimal Useful Experiment

AD/CN only is sufficient for rebuttal if time is tight.

Recommended comparison:

- Same feature family as headline AD/CN result.
- One subject-overlap protocol.
- One subject-disjoint LPSO protocol.
- Same tuner/search budget where feasible.
- Report tuned overlap accuracy, tuned subject-disjoint accuracy, and the drop.
- Compare against fixed-pilot drop if available.

## Draft If Results Are Not Ready

We agree that the hyperparameter protocol needed clearer explanation. Our goal
is not to optimize a state-of-the-art classifier, but to audit evaluation
behavior under controlled conditions. Hyperparameter settings were established
on an initial AD/CN pilot using standard ranges and then held fixed across
disease cohorts. This prevents disease-specific hyperparameter tuning from
becoming another source of variation when the core question is how split design
changes conclusions.

We are preparing a nested/Ray Tune sanity check for AD/CN to test whether
automated tuning changes the core conclusion. We will only include those results
if the full run completes and the outputs are verified.

## Draft If Results Are Ready

To directly test whether hyperparameter selection changes the conclusion, we
reran AD/CN with automated hyperparameter search under both validation regimes.
Under the identity-leaked split, tuning achieved `[A]%` accuracy; under
subject-disjoint LPSO, tuning achieved `[B]%` accuracy. Although tuning changes
absolute performance within each split, it does not close the `[A-B]` point drop
caused by enforcing subject-disjoint evaluation. The corresponding fixed-setting
drop was `[C]` points, showing that the central trap is driven by partition
integrity, not hyperparameter sub-optimality.

For the XGBoost LPSO run, the job reached the practical stopping point at 19
completed Ax trials out of a planned 20-trial budget. The final trial was
started but stopped by the walltime limit before all folds completed, so the
reported value uses the best fully completed trial. This does not materially
change the conclusion: the search had already plateaued, with the top completed
trials clustered tightly (`0.7253`, `0.7250`, `0.7235`, and `0.7220` balanced
accuracy across 50 LPSO folds). We therefore treat the 19/20 run as an
effectively complete tuning sensitivity check rather than evidence of an
unfinished optimization trend.

## Verification Before Citing

- Tuning did not use test folds to choose hyperparameters.
- Subject-disjoint split has zero train/test subject overlap.
- Same search space is used across protocols, or differences are explicitly
  justified.
- Report tuned numbers as a sensitivity check, not as a new SOTA result.
