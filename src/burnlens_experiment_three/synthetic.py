"""Wholly synthetic, benchmark-independent preflight fixtures."""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class SyntheticBatch:
    inputs: torch.Tensor
    targets: torch.Tensor
    loss_mask: torch.Tensor
    event_ids: torch.Tensor


def make_synthetic_batch(*, height: int = 32, width: int = 32) -> SyntheticBatch:
    """Create four deterministic pointwise samples across two synthetic events."""

    if height < 8 or width < 8:
        raise ValueError("synthetic dimensions must be at least 8x8")
    y = torch.linspace(-1.0, 1.0, height, dtype=torch.float32)
    x = torch.linspace(-1.0, 1.0, width, dtype=torch.float32)
    yy, xx = torch.meshgrid(y, x, indexing="ij")
    samples: list[torch.Tensor] = []
    targets: list[torch.Tensor] = []
    masks: list[torch.Tensor] = []
    event_ids = torch.tensor([0, 0, 1, 1], dtype=torch.int64)
    for index in range(4):
        phase = float(index) * 0.17
        channels = torch.stack(
            (
                xx,
                yy,
                xx * yy,
                torch.sin((xx + phase) * 2.3),
                torch.cos((yy - phase) * 1.7),
                (xx.square() + yy.square()) - 0.5 + phase * 0.1,
            )
        )
        score = (
            1.20 * channels[0]
            - 0.85 * channels[1]
            + 0.55 * channels[2]
            + 0.35 * channels[3]
            - 0.25 * channels[4]
            + 0.40 * channels[5]
            + (index - 1.5) * 0.08
        )
        target = (score > 0.05).to(torch.float32).unsqueeze(0)
        valid = torch.ones((1, height, width), dtype=torch.bool)
        valid[:, :2, :] = False
        valid[:, -2:, :] = False
        valid[:, :, :2] = False
        valid[:, :, -2:] = False
        valid[:, 5 + index, 6:10] = False
        samples.append(channels)
        targets.append(target)
        masks.append(valid)
    return SyntheticBatch(
        inputs=torch.stack(samples),
        targets=torch.stack(targets),
        loss_mask=torch.stack(masks),
        event_ids=event_ids,
    )
