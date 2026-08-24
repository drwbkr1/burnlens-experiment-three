"""The single fixed, data-sized neural change detector."""

from __future__ import annotations

import torch
from torch import nn


ARCHITECTURE_ID = "burnlens-exp3-pointwise-6x8x8x1-v1"
EXPECTED_PARAMETER_COUNT = 137


class FixedBurnChangeDetector(nn.Module):
    """Shared pointwise detector: Conv1x1 6->8->8->1 with ReLU."""

    def __init__(self) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(6, 8, kernel_size=1, bias=True),
            nn.ReLU(),
            nn.Conv2d(8, 8, kernel_size=1, bias=True),
            nn.ReLU(),
            nn.Conv2d(8, 1, kernel_size=1, bias=True),
        )
        observed = parameter_count(self)
        if observed != EXPECTED_PARAMETER_COUNT:
            raise RuntimeError(
                f"fixed architecture parameter drift: {observed} != "
                f"{EXPECTED_PARAMETER_COUNT}"
            )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.ndim != 4 or inputs.shape[1] != 6:
            raise ValueError("inputs must have shape [N, 6, H, W]")
        if not inputs.is_floating_point():
            raise TypeError("inputs must be floating point")
        return self.network(inputs)


def parameter_count(model: nn.Module) -> int:
    """Return the exact number of trainable scalar parameters."""

    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
