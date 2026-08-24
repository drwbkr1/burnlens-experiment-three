"""Mask-preserving loss functions used by the frozen scientific direction."""

from __future__ import annotations

import torch
from torch.nn import functional as F


def event_class_balanced_masked_bce(
    logits: torch.Tensor,
    targets: torch.Tensor,
    loss_mask: torch.Tensor,
    event_ids: torch.Tensor,
) -> torch.Tensor:
    """Average events equally, then average each present class equally per event.

    Masked or unknown locations receive zero weight and are never coerced to
    background. Each event must contain at least one valid location.
    """

    if logits.shape != targets.shape or logits.shape != loss_mask.shape:
        raise ValueError("logits, targets, and loss_mask must have identical shapes")
    if logits.ndim != 4 or logits.shape[1] != 1:
        raise ValueError("loss tensors must have shape [N, 1, H, W]")
    if event_ids.ndim != 1 or event_ids.shape[0] != logits.shape[0]:
        raise ValueError("event_ids must have one value per batch item")
    if not logits.is_floating_point() or not targets.is_floating_point():
        raise TypeError("logits and targets must be floating point")
    if loss_mask.dtype is not torch.bool:
        raise TypeError("loss_mask must be boolean")

    pixel_loss = F.binary_cross_entropy_with_logits(logits, targets, reduction="none")
    event_losses: list[torch.Tensor] = []
    for event_id in torch.unique(event_ids, sorted=True):
        event_selector = (event_ids == event_id).view(-1, 1, 1, 1)
        valid = loss_mask & event_selector
        if not torch.any(valid):
            raise ValueError(f"event {int(event_id)} has no valid locations")
        class_losses: list[torch.Tensor] = []
        for class_value in (0.0, 1.0):
            selected = valid & (targets == class_value)
            if torch.any(selected):
                class_losses.append(pixel_loss[selected].mean())
        if not class_losses:
            raise ValueError(f"event {int(event_id)} has no represented class")
        event_losses.append(torch.stack(class_losses).mean())
    return torch.stack(event_losses).mean()
