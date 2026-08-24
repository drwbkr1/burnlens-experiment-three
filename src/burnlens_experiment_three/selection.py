"""Protocol-frozen checkpoint and shared-threshold selection helpers."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class EpochObservation:
    epoch: int
    validation_loss: float


def select_checkpoint(observations: Sequence[EpochObservation]) -> EpochObservation:
    if not observations:
        raise ValueError("at least one completed epoch is required")
    if any(item.epoch < 1 for item in observations):
        raise ValueError("epoch zero is not eligible")
    if len({item.epoch for item in observations}) != len(observations):
        raise ValueError("epochs must be unique")
    if any(not _finite(item.validation_loss) for item in observations):
        raise ValueError("validation losses must be finite")
    return min(observations, key=lambda item: (item.validation_loss, item.epoch))


def early_stop_epoch(observations: Sequence[EpochObservation], patience: int = 25) -> int | None:
    if patience != 25:
        raise ValueError("protocol patience is exactly 25")
    best: float | None = None
    stale = 0
    for item in sorted(observations, key=lambda value: value.epoch):
        if not _finite(item.validation_loss):
            raise ValueError("validation losses must be finite")
        if best is None or item.validation_loss < best:
            best = item.validation_loss
            stale = 0
        else:
            stale += 1
        if stale == patience:
            return item.epoch
    return None


@dataclass(frozen=True)
class ThresholdScore:
    threshold: float
    minimum_seed_event_macro_dice: float
    median_seed_event_class_macro_iou: float


def threshold_grid() -> tuple[float, ...]:
    return tuple(k / 100.0 for k in range(1, 100))


def select_shared_threshold(scores: Iterable[ThresholdScore]) -> ThresholdScore:
    candidates = list(scores)
    if {item.threshold for item in candidates} != set(threshold_grid()):
        raise ValueError("scores must cover the exact 99-value threshold grid")
    if any(
        not _finite(value)
        for item in candidates
        for value in (
            item.minimum_seed_event_macro_dice,
            item.median_seed_event_class_macro_iou,
        )
    ):
        raise ValueError("threshold scores must be finite")
    return min(
        candidates,
        key=lambda item: (
            -item.minimum_seed_event_macro_dice,
            -item.median_seed_event_class_macro_iou,
            abs(item.threshold - 0.5),
            item.threshold,
        ),
    )


def build_threshold_scores(
    seed_event_scores: Mapping[float, Sequence[tuple[float, float]]]
) -> list[ThresholdScore]:
    """Aggregate per-threshold (event macro Dice, seed macro IoU) pairs.

    The caller supplies six Dice values (three seeds times two events) and three
    seed-level macro-IoU values per threshold as tuples. This compact interface
    is used only after metric computation has retained the full underlying rows.
    """

    rows: list[ThresholdScore] = []
    for threshold in threshold_grid():
        values = list(seed_event_scores[threshold])
        if len(values) != 6:
            raise ValueError("each threshold requires six seed-event rows")
        dice_values = [value[0] for value in values]
        seed_iou = [values[index][1] for index in (0, 2, 4)]
        rows.append(ThresholdScore(threshold, min(dice_values), median(seed_iou)))
    return rows


def _finite(value: float) -> bool:
    return value == value and value not in {float("inf"), float("-inf")}
