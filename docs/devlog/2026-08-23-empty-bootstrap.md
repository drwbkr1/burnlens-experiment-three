# Devlog: Truthful Empty Bootstrap

| Field | Value |
| --- | --- |
| Date | 2026-08-23 |
| Milestone | 0 |
| Tracker | [Issue #1](https://github.com/drwbkr1/burnlens-experiment-three/issues/1) |

## What existed

The canonical GitHub repository existed publicly but contained no commit,
branch, tag, release, pull request, workflow, deployment, roadmap, authority
record, source code, dataset, model, validator, pipeline, replay, or rendered
evidence surface. The canonical local checkout at
`C:\Projects\Active\burnlens-experiment-three` therefore began from an unborn
`main` rather than from an implementation checkpoint.

No runnable build could be played, trained, evaluated, or rendered. Those
surfaces were reported as missing rather than inferred to pass.

## What the inherited work establishes

BurnLens Deschutes provides the retrospective benchmark and historical
controls. Its previously reported RBR result and rejected U-Net result motivate
the question, but they are not Experiment Three metrics. Experiment 2 and 2B
provide lessons about checkpoint loading, deterministic validation, custody,
and honest failure retention; they did not produce transferable scientific
model-evaluation evidence for Experiment Three.

Both prior repositories remain read-only. No code, data, model, environment, or
output was copied during this milestone.

## Direction selected

Experiment Three will test a deliberately data-sized neural detector rather
than another large U-Net:

```text
Conv1x1(6 -> 8) -> ReLU -> Conv1x1(8 -> 8) -> ReLU -> Conv1x1(8 -> 1)
```

The 137-parameter pointwise model is a genuine neural network and produces
dense logits, while avoiding a claim that sparse core supervision can support
a sophisticated spatial segmenter. Its size, model family, bounded optimizer
and budget, three seeds, prohibited rescue features, checkpoint direction, and
validation-only threshold direction are owner-approved. The exact executable
bindings and hash-bound protocol artifact do not exist yet, so no substantive
training is authorized.

## What this milestone adds

The bootstrap candidate adds human-readable project and control records,
machine-readable governance and milestone records, a bootstrap-only repository
validator and focused tests, GitHub issue/PR templates, and a pinned CI
workflow.

It deliberately adds no benchmark bytes, neural implementation, dependency
lock, checkpoint, prediction, scientific result, model-runtime validation
claim, or release.

## Local validation

At candidate-validation time, the complete candidate passed the bootstrap
repository validator, all 9 focused control tests, the project-control profile
validator, and the controlled-milestone validator. Those passes established
local control-plane consistency only; live acceptance still required the exact
commit, public CI, and repository-surface checks recorded below.

## Acceptance update

Milestone 0 was accepted on live `main` at commit
[`4543a2dad5c2630249906aab763ae0cbf91097ba`](https://github.com/drwbkr1/burnlens-experiment-three/commit/4543a2dad5c2630249906aab763ae0cbf91097ba),
tree `6387e91f071609605f7fcc3a05842782423fbb6d`. GitHub Actions
[run 32671370937](https://github.com/drwbkr1/burnlens-experiment-three/actions/runs/32671370937)
completed successfully. The live README and execution-goal blobs matched the
verified local checkpoint, and the public description was corrected to the
bounded retrospective framing. A separate rendered-page inspection showed the
expected public `main` file table and README, bounded About description, one
commit, two issues, zero tags, and zero releases.

Issue #1 closed at `2026-08-23T22:55:18Z` after those checks. Issue #2 and the
issue-backed `codex/benchmark-provenance-001` branch carry the next milestone;
the one-time direct-to-`main` exception is consumed.

Acceptance does not turn the bootstrap into a release or scientific result.
It still contains no benchmark bytes, model implementation, training,
inference, evaluation, metric, or rendered scientific output.

## Claim discipline

The known Experiment 1 test will be described as a retrospective compatibility
benchmark. Sparse selected cores cannot establish dense segmentation quality,
population generalization, independent accuracy, significance, superiority, or
operational wildfire usefulness. A failed comparison may still close a
successful model lifecycle.

Fresh-event confirmation remains a separate future decision and cannot be used
to keep this experiment open indefinitely.

## Next checkpoint

Issue [#2](https://github.com/drwbkr1/burnlens-experiment-three/issues/2)
opens Milestone 1 with read-only inspection of the exact inherited benchmark
sources, provenance, terms, attribution, redistribution boundaries, and
intended roles. No benchmark byte may be copied or admitted before the rights,
integrity, and custody gate permits it. The approved protocol values still
require a later executable, content-addressed freeze before training.
