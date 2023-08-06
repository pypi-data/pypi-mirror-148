from typing import Optional
import logging

import torch
from torch.nn.modules.loss import _Loss
import torch.nn.functional as F
from ._functional import label_smoothed_nll_loss
from .constants import MEAN, SUM


__all__ = ["SoftCrossEntropyLoss"]


class SoftCrossEntropyLoss(_Loss):

    __constants__ = ["reduction", "ignore_index", "smooth_factor"]

    def __init__(
        self,
        reduction: str = "mean",
        smooth_factor: Optional[float] = 0.0,
        ignore_index: Optional[int] = -100,
        dim: int = 1,
    ):
        """Drop-in replacement for torch.nn.CrossEntropyLoss with label_smoothing
        
        Parameters
        ----------
        reduction (string, optional): Specifies the reduction to apply to the output:
            'mean' | 'sum'. 'mean': the sum of the output will be divided by the number of
            elements in the output, 'sum': the output will be summed. Note: :attr:`size_average`
            and :attr:`reduce` are in the process of being deprecated, and in the meantime,
            specifying either of those two args will override :attr:`reduction`.
        smooth_factor: Factor to smooth target (e.g. if smooth_factor=0.1 then [1, 0, 0] -> [0.9, 0.05, 0.05])
        ignore_index: Label that indicates ignored pixels (does not contribute to loss)

        Shape
        -----
        **y_pred** - torch.Tensor of shape (N, C, H, W)
        **y_true** - torch.Tensor of shape (N, H, W)
        
        Example
        -------
        >>> criterion = SoftCrossEntropyLoss()
        >>> predicted = torch.zeros(2, 3, 32, 32)
        >>> target = torch.empty(2, 32, 32, dtype=torch.long).random_(3)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        1.0986

        Reference
        ---------
        https://github.com/pytorch/fairseq/blob/master/fairseq/criterions/label_smoothed_cross_entropy.py
        """
        assert reduction in {MEAN, SUM}, logging.error("Invalid reduction method")
        super().__init__()
        self.smooth_factor = smooth_factor
        self.ignore_index = ignore_index
        self.reduction = reduction
        self.dim = dim

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        log_prob = F.log_softmax(y_pred, dim=self.dim)
        return label_smoothed_nll_loss(
            log_prob,
            y_true,
            epsilon=self.smooth_factor,
            ignore_index=self.ignore_index,
            reduction=self.reduction,
            dim=self.dim,
        )