# Milestone 3 protocol-freeze log

## Why this checkpoint exists

The synthetic lifecycle proved the small neural detector can learn, serialize,
reload, infer, and replay. It did not decide exactly how the admitted benchmark
would be loaded, trained, thresholded, evaluated, compared, or judged. Those
details had to be fixed before outcomes could influence them.

## What was frozen

The protocol binds the exact admitted dataset, whole-event roles, masks,
train-only normalization, RBR and U-Net comparator records, 137-parameter
architecture, deterministic CPU runtime, three seeds, Adam settings, full-batch
order, 200-epoch budget, patience, checkpoint tie rule, one shared
validation-only threshold grid and ranking, metrics, collapse gates, artifact
schemas, replay rules, one-time test opening, terminal decisions, and claim
limits. It prohibits best-seed selection, model shopping, test-driven rescue,
and post-opening changes inside Experiment Three.

The protocol makes a deliberate distinction: finishing a valid neural
lifecycle is one result, while comparative performance is another. A lifecycle
can pass even if the model loses to the controls.

## What was exercised

The dependency-free validator rehashed repository controls and five admitted
metadata/comparator artifacts in external custody. The dry-run used fabricated
values only and exercised checkpoint selection, threshold ranking, confusion
metrics, and collapse semantics. Seven focused protocol tests passed. The full
suite passed 33 controls with six expected neural skips under system Python and
all 39 tests under the approved embedded CPU runtime.

No benchmark array was decoded, no test value was opened, and no substantive
training, scientific checkpoint, inference, evaluation, metric, render, tag,
or release was created.

## Retained corrections

The first dependency-free dry-run failed because the package initializer pulled
in PyTorch before a pure helper could load. The repair changed only how the
dependency-free scripts import those helpers and preserved the accepted neural
package source. A fabricated metric test also initially expected `0.75`; the
implementation correctly returned `0.625`, and the expected value was fixed.
Both failures remain recorded because a clean final test count should not hide
how the checkpoint was made trustworthy.

## Next gate

The freeze is only a locally verified candidate. It must merge through a
reviewed pull request and match live `main` with successful merge-triggered CI
before Milestone 4 may load train or validation arrays and begin the three
predeclared runs.
