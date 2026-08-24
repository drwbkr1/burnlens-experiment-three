"""Pure-Python metric semantics frozen for Experiment Three."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median
from typing import Iterable, Sequence


@dataclass(frozen=True)
class ClassCounts:
    support: int
    predicted: int
    true_positive: int
    false_positive: int
    false_negative: int

    @property
    def dice(self) -> float | None:
        denominator = 2 * self.true_positive + self.false_positive + self.false_negative
        return None if denominator == 0 else 2 * self.true_positive / denominator

    @property
    def iou(self) -> float | None:
        denominator = self.true_positive + self.false_positive + self.false_negative
        return None if denominator == 0 else self.true_positive / denominator


def class_counts(truth: Sequence[int], prediction: Sequence[int], class_value: int) -> ClassCounts:
    if len(truth) != len(prediction) or not truth:
        raise ValueError("truth and prediction must be equal-length and nonempty")
    if class_value not in (0, 1) or any(value not in (0, 1) for value in (*truth, *prediction)):
        raise ValueError("binary values are required")
    support = sum(value == class_value for value in truth)
    predicted = sum(value == class_value for value in prediction)
    true_positive = sum(t == class_value and p == class_value for t, p in zip(truth, prediction))
    return ClassCounts(
        support=support,
        predicted=predicted,
        true_positive=true_positive,
        false_positive=predicted - true_positive,
        false_negative=support - true_positive,
    )


def event_metrics(truth: Sequence[int], prediction: Sequence[int]) -> dict[str, object]:
    classes = {value: class_counts(truth, prediction, value) for value in (0, 1)}
    dice = [item.dice for item in classes.values() if item.dice is not None]
    iou = [item.iou for item in classes.values() if item.iou is not None]
    return {
        "classes": classes,
        "class_macro_dice": mean(dice),
        "class_macro_iou": mean(iou),
        "predicted_burn_prevalence": sum(prediction) / len(prediction),
        "nonconstant": len(set(prediction)) == 2,
    }


def aggregate_events(events: Iterable[dict[str, object]]) -> dict[str, float]:
    rows = list(events)
    if not rows:
        raise ValueError("at least one event is required")
    dice = [float(row["class_macro_dice"]) for row in rows]
    iou = [float(row["class_macro_iou"]) for row in rows]
    return {
        "event_class_macro_dice": mean(dice),
        "event_class_macro_iou": mean(iou),
        "worst_event_macro_dice": min(dice),
    }


def three_seed_median(values: Sequence[float]) -> float:
    if len(values) != 3:
        raise ValueError("exactly three seed values are required")
    return median(values)
