# BurnLens Experiment Three

BurnLens Experiment Three is a bounded, portfolio-first neural change-detection
study. It asks whether a deliberately data-sized neural network can avoid the
constant-class failure observed in the earlier BurnLens U-Net while completing
a real, replayable model lifecycle on the frozen BurnLens Deschutes
compatibility benchmark.

This is an experimental computer-vision and GEOINT case study for technical
reviewers. It is not an operational wildfire product, official fire
information, ground truth, field validation, emergency guidance, or a basis for
safety decisions.

## Current status

As of 2026-08-25, Milestone 4 is accepted and live-verified on `main` at
[`53983c09a03d7f8f9453e6f492b05e58b795b876`](https://github.com/drwbkr1/burnlens-experiment-three/commit/53983c09a03d7f8f9453e6f492b05e58b795b876),
tree `51dc4ba7b4e942ad7be884051e0ce8e2fe57c6aa`. Pull request
[#9](https://github.com/drwbkr1/burnlens-experiment-three/pull/9) and
merge-triggered GitHub Actions run
[`32875755932`](https://github.com/drwbkr1/burnlens-experiment-three/actions/runs/32875755932)
passed. Milestone 5 is active under issue
[#10](https://github.com/drwbkr1/burnlens-experiment-three/issues/10).

The exact owner/rightsholder review is now complete and reconciled as `yes` for
rights the owner controls. A separate current six-source gate is `READY`, and
the benchmark readiness audit is `PASS`. Controlled intake promoted exactly
131 approved artifacts (3,369,748 bytes) into isolated local custody at
`C:\Projects\Active\burnlens-experiment-three-custody\benchmark`; every
source, staging, and destination identity matched. No benchmark byte is stored
in this Git repository, and repository redistribution was not authorized by
the intake.

Runtime candidate 001 received an exact owner `yes`, but its signed normal
installer entered maintenance mode on an existing same-version Python product
instead of creating the required isolated runtime. That activation is retained
as `FAIL`; inspected existing-Python surfaces were restored, and no wheels,
model imports, synthetic runs, or scientific work followed. Candidate 002 then
received a separate exact owner `yes` and passed application-local activation
with Python.org's official embeddable ZIP and the unchanged 20-package Windows
CPU lock. The fixed 137-parameter model now passes a wholly synthetic lifecycle:
finite gradients, changed weights, reduced loss, strict state-dict packaging,
fresh-process reload, byte-identical replay, GeoTIFF reopen, and rendered proof.

The complete executable protocol is frozen and accepted
at canonical-LF SHA-256 `12a092e90586a819e6014ed181da82721675040ff2678c7d7115b1582b904f1e`.
It fixes all data roles, normalization, masks, training order, checkpoint and
shared-threshold rules, metrics, collapse gates, artifacts, replay, test
opening, decision logic, and claim limits. Exact metadata bindings, fabricated
replay, and all 39 approved-runtime tests pass without decoding a benchmark
array. This is accepted engineering-control evidence, not a scientific result:
no substantive training run, scientific checkpoint, inference, evaluation,
metric, result render, tag, or release existed at protocol acceptance.

Milestone 4 is an accepted live scientific checkpoint. Exactly three
predeclared seeds trained under the frozen protocol, selected checkpoints were
reconstructed in fresh isolated processes, and primary/replay packages match
byte for byte. The shared validation-only threshold is `0.5`. The first run
attempt is retained as `FAIL`, and the second as `INVALID` because its otherwise
replayable checkpoint package used the wrong frozen filename. The third full
attempt is also retained as `INVALID` because its receipt filenames violated
the frozen artifact list. The fourth is `INVALID` because its seeds trained in
one parent process rather than a fresh process per seed. The fifth full attempt
is protocol-conformant and is the sole accepted training package. Test values
were opened exactly once in Milestone 5 as `M5-OPENING-2026-001`. All three
frozen seeds and all four controls ran in one bounded invocation. The primary
and replay payloads match exactly at 53 files / 367,150 bytes / roster
`e322a101...`; independent re-inference, metric recomputation, all 36 GeoTIFF
reopens, and direct inspection of the 5360x2076 comparison render pass.

The neural lifecycle is `PASS`; the frozen comparative outcome is `FAIL`.
Across all three predeclared seeds, median event-class macro IoU is `0.2201`
and median worst-event macro Dice is `0.2919`, below the strongest constant
control's `0.2853` and `0.3333`. Seed `20260727` was stronger (`0.5794` macro
IoU), but it cannot replace the predeclared all-seed decision. No post-test
tuning, rescue, rerun, or seed selection occurred. The result is a locally
verified M5 candidate until reviewed merge and live verification.

## Research question

> Can a data-sized neural change detector avoid Experiment 1's constant-class
> U-Net collapse on the frozen Deschutes retrospective compatibility benchmark
> while completing an exact, replayable neural-network lifecycle?

Lifecycle completion and comparative scientific outcome are separate:

- `lifecycle_status` asks whether the model was built, preflighted, trained,
  checkpointed, safely reloaded, used for inference and evaluation, packaged,
  and replayed as specified.
- `comparative_status` records `PASS`, `FAIL`, `INCONCLUSIVE`, or `INVALID`
  under frozen decision rules.

A valid lifecycle with a comparative `FAIL` is a completed experiment. Beating
the previously reported perfect RBR prototype-core score is not a completion
condition.

## Primary neural architecture direction

The selected direction is a tiny, fully convolutional pointwise detector:

```text
Conv1x1(6 -> 8) -> ReLU
Conv1x1(8 -> 8) -> ReLU
Conv1x1(8 -> 1)
```

With biases, this model has exactly 137 trainable parameters:
`(6*8+8) + (8*8+8) + (8*1+1) = 137`. It consumes the six established pre/post
Sentinel-2 channels and emits a dense logit at every pixel. Its small size is
intentional: the inherited benchmark contains very little independent
supervision, so architectural restraint is part of the hypothesis rather than
an optimization after seeing test results.

The model family and parameter count are fixed for Experiment Three. The owner
has also approved event-class-balanced masked BCE; deterministic float32 local
CPU PyTorch; Adam at `0.001`; batch size `4`; at most `200` epochs with patience
`25`; seeds `20260725`, `20260726`, and `20260727` (the first is primary); and
no augmentation, positive-class weighting, BatchNorm, dropout, ensemble,
pretraining, or model search. Checkpoints use minimum validation balanced BCE,
and one validation-only threshold procedure must be sealed around the approved
worst-event-Dice/macro-IoU rule. Milestone 3 must turn these approved values and
the remaining implementation-level details into one executable, hash-bound
protocol before training; it is not a later opportunity to choose different
values. Changing the model family or an approved protocol value requires owner
approval, and any post-evaluation change belongs to a separately approved
Experiment 3B.

## Compatibility benchmark and claim limits

Experiment Three has hash-bound and admitted the exact Experiment 1 dataset,
whole-event split, masks, normalization, metrics, RBR result, canonical U-Net
result, and constant-class-control definitions to external controlled custody.
The bytes are not part of this Git repository and retain their source,
attribution, restriction, and claim boundaries.

The inherited test has already been observed. Therefore:

- Experiment Three is a retrospective compatibility comparison, not a fresh
  blind confirmation.
- Events, not pixels, are the relevant independent units.
- Sparse selected prototype cores do not establish dense segmentation quality.
- Results cannot establish population generalization, statistical
  significance, independent accuracy, model superiority, operational fitness,
  or wildfire-response utility.
- Predictions outside scored masks may be shown only as clearly labeled,
  qualitative model output.
- No test-driven tuning, best-seed selection, threshold rescue, architecture
  shopping, or silent replacement of failed runs is allowed.

A future fresh-event confirmation is a separate, owner-gated lane. It must be
independently sampled and reviewed, blind to RBR and model output, sealed until
one frozen opening, and never required for completion of the primary neural
build.

## Planned lifecycle

The project will proceed through bounded milestones:

1. Truthful repository and control-plane bootstrap.
2. Benchmark provenance, integrity, attribution, and rights binding.
3. Synthetic end-to-end neural and geospatial preflight using disposable
   weights.
4. Complete protocol freeze before substantive training.
5. Training and fresh-process checkpoint reconstruction for every declared
   seed.
6. One controlled retrospective evaluation against all frozen controls.
7. Reviewer-facing evidence, exact replay, terminal scientific disposition,
   and verified release.

See [the roadmap](docs/roadmap/ROADMAP.md) and
[current status](docs/status/STATUS.md) for gates and present truth.

## Repository and custody boundary

The canonical remote is
[`drwbkr1/burnlens-experiment-three`](https://github.com/drwbkr1/burnlens-experiment-three).
The canonical local checkout is:

```text
C:\Projects\Active\burnlens-experiment-three
```

All project work, custody roots, caches, environments, temporary files, and run
outputs must remain under `C:\Projects\Active`. OneDrive paths are prohibited.
Prior BurnLens repositories must not be modified by this experiment.

## Project records

- [Roadmap](docs/roadmap/ROADMAP.md)
- [Status](docs/status/STATUS.md)
- [Version history](docs/status/VERSION-HISTORY.md)
- [Changelog](CHANGELOG.md)
- [Evidence ledger](records/evidence/EVIDENCE-LEDGER.md)
- [Decision register](records/decisions/DECISION-REGISTER.md)
- [Experiment One benchmark identity inventory](records/provenance/EXPERIMENT-ONE-BENCHMARK-IDENTITY-INVENTORY-2026-001.json)
- [Owner-rights review item](records/decisions/reviews/EXPERIMENT-ONE-ARTIFACT-RIGHTS-REVIEW-ITEM-2026-001.json)
- [Owner-rights review contract](records/decisions/reviews/EXPERIMENT-ONE-ARTIFACT-RIGHTS-REVIEW-CONTRACT-2026-001.json)
- [Blank owner-rights response](records/decisions/reviews/EXPERIMENT-ONE-ARTIFACT-RIGHTS-RESPONSE-BLANK-2026-001.json)
- [Owner-rights decision](records/decisions/EXPERIMENT-ONE-ARTIFACT-RIGHTS-DECISION-2026-001.json)
- [Current source gate](records/source-gates/EXPERIMENT-ONE-BENCHMARK-SOURCE-GATE-2026-001.json)
- [Dataset readiness decision](records/readiness/EXPERIMENT-ONE-BENCHMARK-READINESS-DECISION-2026-001.json)
- [Controlled-intake receipt](records/intake/EXPERIMENT-ONE-BENCHMARK-INTAKE-RECEIPT-2026-001.json)
- [Frozen executable protocol](protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json)
- [Protocol-freeze evidence record](records/protocol/EXPERIMENT-THREE-PROTOCOL-FREEZE-2026-001.json)
- [Frozen-training evidence record](records/training/EXPERIMENT-THREE-M4-FROZEN-TRAINING-2026-001.json)
- [Retrospective evaluation result](records/evaluation/EXPERIMENT-THREE-M5-RETROSPECTIVE-EVALUATION-2026-001.json)
- [Model card candidate](docs/model-card/MODEL-CARD.md)
- [Current limitations](docs/limitations/LIMITATIONS.md)
- [Runtime candidate inventory](records/runtime/EXPERIMENT-THREE-RUNTIME-CANDIDATE-INVENTORY-2026-001.json)
- [Runtime source gate](records/source-gates/EXPERIMENT-THREE-RUNTIME-SOURCE-GATE-2026-001.json)
- [Runtime adoption review item](records/decisions/reviews/EXPERIMENT-THREE-RUNTIME-ADOPTION-REVIEW-ITEM-2026-001.json)
- [Runtime adoption review contract](records/decisions/reviews/EXPERIMENT-THREE-RUNTIME-ADOPTION-REVIEW-CONTRACT-2026-001.json)
- [Blank runtime adoption response](records/decisions/reviews/EXPERIMENT-THREE-RUNTIME-ADOPTION-RESPONSE-BLANK-2026-001.json)
- [Bootstrap devlog](docs/devlog/2026-08-23-empty-bootstrap.md)
- [Contributing rules](CONTRIBUTING.md)

## License and third-party materials

Repository-authored **software and documentation** are licensed under the
[MIT License](LICENSE), except where a file explicitly says otherwise.

That MIT license does **not** automatically apply to satellite imagery,
datasets, labels, benchmark packages, model weights, pretrained artifacts,
maps, source products, or other third-party materials. No such assets are
included at bootstrap. Any later-admitted data or model artifact must carry its
own source, license or terms, attribution, custody, redistribution decision,
and integrity record. Absence of a stated license is not permission to copy or
redistribute an asset.
