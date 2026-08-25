# BurnLens Experiment Three Model Card

## Model and intended role

The Experiment Three model is a 137-parameter pointwise fully convolutional
change detector: `Conv1x1(6 -> 8) -> ReLU -> Conv1x1(8 -> 8) -> ReLU ->
Conv1x1(8 -> 1)`. It consumes the six frozen pre/post Sentinel-2 channels and
emits one logit per pixel. Its intended role is a bounded portfolio experiment
on the retrospective BurnLens Deschutes compatibility benchmark.

It is not operational wildfire guidance, a burn-severity product, emergency
information, field-validated mapping, or a basis for safety decisions.

## Current lifecycle state

The frozen result is published as
[`v1.0.0`](https://github.com/drwbkr1/burnlens-experiment-three/releases/tag/v1.0.0)
from reviewed commit `8de60a3350a7c25942be8223bf9067c9460774d1`.
Independent live verification passed for the tag, assets, source archives,
release notes, and public page. Terminal PR #15 closes the experiment; the
scientific result is immutable and no successor model work is active.
All three predeclared seeds trained in separate fresh isolated processes with
the frozen CPU/float32 protocol,
produced complete histories and changed weights, selected checkpoints by
minimum validation balanced BCE, reconstructed tensor-only `weights.pt`
packages in fresh isolated processes, and reproduced byte for byte. The shared
validation-only threshold is `0.5`.

Opening `M5-OPENING-2026-001` consumed the known test exactly once. Independent
verification reproduced checkpoint inference and metrics, reopened all 36
GeoTIFFs exactly, confirmed byte-identical primary/replay packages, and passed
direct inspection of the actual comparison render. Lifecycle status is `PASS`;
comparative status is `FAIL`. The result cannot be tuned or rerun inside
Experiment Three.

## Training data and procedure

- Train: four 64x64 patches from Green Ridge and Tepee; 109 scored prototype-
  core pixels, 58 background and 51 burned.
- Validation: four 64x64 patches from Grandview and McKay; 89 scored prototype-
  core pixels, 32 background and 57 burned.
- Loss: event-class-balanced masked binary cross entropy.
- Optimizer: Adam, learning rate `0.001`, batch size four.
- Budget: at most 200 epochs, patience 25.
- Seeds: `20260725`, `20260726`, `20260727`; all reported.
- Prohibited: augmentation, class weighting, BatchNorm, dropout, pretraining,
  ensembling, model search, test-driven tuning, and best-seed selection.

## Candidate training evidence

| Seed | Epochs | Selected epoch | Validation balanced BCE | Selected tensor SHA-256 |
| --- | ---: | ---: | ---: | --- |
| `20260725` | 130 | 105 | 0.6794654131 | `50477e8f...` |
| `20260726` | 172 | 147 | 0.6747468710 | `19b0308c...` |
| `20260727` | 171 | 146 | 0.6462924480 | `078d4ffc...` |

These are validation-selection values, not test performance.

## Retained attempts

Attempt 001 is retained as `FAIL` after a reload-process runtime configuration
mismatch. Attempt 002 is retained as `INVALID` because its checkpoint filename
violated the frozen artifact contract despite exact computation and replay.
Attempt 003 is also retained as `INVALID` because its receipt filenames did not
match the frozen artifact list. Attempt 004 is `INVALID` because its seeds
trained sequentially in one process. Attempt 005 reran every seed from
initialization in a fresh isolated process and is the sole accepted local
candidate.

## Evaluation and reporting

| Seed or control | Event-class macro IoU | Worst-event macro Dice | Burn prevalence | Collapse gate |
| --- | ---: | ---: | ---: | --- |
| `20260725` | 0.2201 | 0.2919 | 0.9775 | Fail: Windigo constant |
| `20260726` | 0.2009 | 0.1136 | 0.7303 | Pass |
| `20260727` | 0.5794 | 0.4652 | 0.5843 | Pass |
| RBR | 1.0000 | 1.0000 | 0.4382 | Pass |
| Canonical U-Net / constant burned | 0.2147 | 0.2642 | 1.0000 | Fail |
| Constant background | 0.2853 | 0.3333 | 0.0000 | Fail |

The predeclared three-seed median is macro IoU `0.2201` and worst-event macro
Dice `0.2919`; it does not strictly beat the strongest constant-control values
of `0.2853` and `0.3333`. Seed `20260727` is reported but was not selected as a
replacement. Events—not pixels—are the independent units. Lifecycle completion
and comparative outcome remain separate.

See [current limitations](../limitations/LIMITATIONS.md), the
[frozen protocol](../../protocol/EXPERIMENT-THREE-FROZEN-PROTOCOL-2026-001.json),
and the [training record](../../records/training/EXPERIMENT-THREE-M4-FROZEN-TRAINING-2026-001.json).
The exact public evaluation record is
[`EXPERIMENT-THREE-M5-RETROSPECTIVE-EVALUATION-2026-001.json`](../../records/evaluation/EXPERIMENT-THREE-M5-RETROSPECTIVE-EVALUATION-2026-001.json).
