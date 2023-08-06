from typing import Optional
import logging

import torch
import torch.nn.functional as F
from torch.nn.modules.loss import _Loss
from .constants import NONE, MEAN, SUM, BATCHWISE_MEAN

__all__ = ["SoftBCEWithLogitsLoss"]


class SoftBCEWithLogitsLoss(_Loss):

    def __init__(
        self,
        weight: Optional[torch.Tensor] = None,
        ignore_index: Optional[int] = -100,
        reduction: str = "mean",
        smooth_factor: Optional[float] = None,
        pos_weight: Optional[torch.Tensor] = None,
    ):
        """Drop-in replacement for torch.nn.BCEWithLogitsLoss with few additions: ignore_index and label_smoothing
        
        Parameters
        ----------
        ignore_index: Specifies a target value that is ignored and does not contribute to the input gradient. 
        smooth_factor: Factor to smooth target (e.g. if smooth_factor=0.1 then [1, 0, 1] -> [0.9, 0.1, 0.9])
        
        Shape
        -----
        **y_pred** - torch.Tensor of shape NxHxW
        **y_true** - torch.Tensor of shape NxHxW 

        Example
        --------
        >>> criterion = SoftBCEWithLogitsLoss()
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.ones(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.3133

        >>> criterion = SoftBCEWithLogitsLoss()
        >>> predicted = torch.zeros(2, 1, 32, 32)
        >>> target = torch.ones(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.6931
        
        References
        ----------
        https://github.com/BloodAxe/pytorch-toolbelt
        """
        assert reduction in {NONE, MEAN, SUM, BATCHWISE_MEAN}, logging.error("Invalid reduction method")
        super().__init__()
        self.ignore_index = ignore_index
        self.reduction = reduction
        self.smooth_factor = smooth_factor
        self.register_buffer("weight", weight)
        self.register_buffer("pos_weight", pos_weight)

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        logging.debug("Inside soft bce loss forward routine")
        y_pred = y_pred.squeeze()
        y_true = y_true.squeeze()

        assert y_pred.shape == y_true.shape

        if self.smooth_factor is not None:
            soft_targets = (1 - y_true) * self.smooth_factor + y_true * (1 - self.smooth_factor)
        else:
            soft_targets = y_true

        loss = F.binary_cross_entropy_with_logits(
            y_pred, soft_targets, self.weight, pos_weight=self.pos_weight, reduction="none"
        )

        if self.ignore_index is not None:
            not_ignored_mask = y_true != self.ignore_index
            loss *= not_ignored_mask.type_as(loss)

        return self.aggregate_loss(loss)

    def aggregate_loss(self, loss):

        if self.reduction == MEAN:
            loss = loss.mean()
        if self.reduction == SUM:
            loss = loss.sum()
        if self.reduction == BATCHWISE_MEAN:
            loss = loss.sum(0)

        return loss