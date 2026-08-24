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

As of 2026-08-23, the truthful empty bootstrap is accepted on live `main` at
commit
[`4543a2dad5c2630249906aab763ae0cbf91097ba`](https://github.com/drwbkr1/burnlens-experiment-three/commit/4543a2dad5c2630249906aab763ae0cbf91097ba)
(tree `6387e91f071609605f7fcc3a05842782423fbb6d`). Public validation
[run 32671370937](https://github.com/drwbkr1/burnlens-experiment-three/actions/runs/32671370937)
completed successfully, and the live README and execution-goal blobs matched
the verified local checkpoint. Issue
[#2](https://github.com/drwbkr1/burnlens-experiment-three/issues/2) now tracks
Milestone 1's read-only benchmark-provenance and rights work. Draft pull
request [#3](https://github.com/drwbkr1/burnlens-experiment-three/pull/3)
contains the accepted-checkpoint-to-Milestone-1 control transition; transition
commit `74171043ddd543979e9773d5ffdd06da116bbaa1` passed push run
`32674532003` and pull-request run `32674546780`.

- No dataset or benchmark bytes have been admitted.
- A metadata-only identity inventory now binds the clean Experiment 1 source
  revision, all 48 declared benchmark arrays, all eight historical U-Net
  prediction/probability arrays, and the relevant source and terms records.
  Every inventoried byte identity matches, but this is not asset admission.
- No model code, model weights, checkpoints, or predictions exist here.
- No training or evaluation has run here.
- No Experiment Three metrics, scientific result, or release exists.
- A bootstrap-only repository validator, focused tests, and pinned CI workflow
  are present on live `main` and have passed. No scientific pipeline, model
  replay command, or rendered evidence surface exists yet.
- Prior BurnLens repositories are read-only provenance sources. Their files and
  decisions are not Experiment Three evidence until they are explicitly
  hash-bound and admitted.

The accepted bootstrap establishes scope and truthful state. Milestone 1's
metadata identity gate is `PASS`; controlled copying and scientific use remain
`DEFER`, and repository or raw-provider redistribution remains `BLOCK`. The
current stop is an explicit owner/rightsholder decision about the exact
project-authored derivative artifacts. No benchmark byte may enter Experiment
Three custody before that decision and a separate current upstream-source gate
permit it. Substantive training and evaluation remain unauthorized.

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

Experiment Three is designed to bind the exact Experiment 1 dataset, whole-
event split, masks, normalization, metrics, RBR result, canonical U-Net result,
and constant-class controls. Until provenance, integrity, and rights checks are
complete, those materials remain external read-only references and are not
part of this repository.

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
