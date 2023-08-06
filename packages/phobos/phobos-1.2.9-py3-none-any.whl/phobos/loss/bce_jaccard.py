from typing import Optional, List
import logging

import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.nn.modules.loss import _Loss
from ._functional import soft_jaccard_score, to_tensor
from .constants import NONE, MEAN, SUM, BATCHWISE_MEAN

from .jaccard import JaccardLoss

__all__ = ["BCEJaccardLoss"]


class BCEJaccardLoss(_Loss):

    def __init__(
        self, 
        jaccard_weight: int,
        reduction: Optional[str] = "mean", 
        eps: float = 1e-7,
    ):
        r"""Creates a criterion that measures the BCE Jaccard Error
        between each element in the input :math:`X` and target :math:`Y`.

        Final loss is computed as a weighted average between BCE Loss and Jaccard Loss:

        .. math:: Loss(X,Y) = (1 - w_j) \cdot Loss_{BCE}(X,Y) + w_j \cdot Loss_{Jaccard}(X,Y)

        where :math:`w_j` is Jaccard Weight

        :math:`Loss_{BCE}(X,Y)` is the BCE Loss component, which is computed as:

        .. math::
            Loss_{BCE}(X,Y) = \sum\limits_{i=1}^N l(x_i,y_i), l(x_i,y_i) = - w_i \left[ y_i \cdot \log x_i + (1 - y_i) \cdot \log (1 - x_i) \right]

        where :math:`x_i \in X` and :math:`y_i \in Y`

        :math:`Loss_{Jaccard}(X,Y)` is the Jaccard Loss component, which is computed as:

        .. math::
            Loss_{Jaccard}(X,Y) = \frac{| X \cap Y | + \epsilon }{| X \cup Y | + \epsilon } = \frac{| X \cap Y | + \epsilon }{|X| + |Y| - | X \cap Y | + \epsilon }

        where :math:`\epsilon` is a constant added for numerical stability

        Parameters
        ----------
        jaccard_weight : jaccard weight
        reduction (string, optional): Specifies the reduction to apply to the output:
            'none' | 'mean' | 'sum' | 'batchwise_mean'. 'none': no reduction will be applied,
            'mean': the sum of the output will be divided by the number of
            elements in the output, 'sum': the output will be summed. Note: :attr:`size_average`
            and :attr:`reduce` are in the process of being deprecated, and in the meantime,
            specifying either of those two args will override :attr:`reduction`.
            'batchwise_mean' computes mean loss per sample in batch. Default: 'mean'
        eps: A small epsilon for numerical stability to avoid zero division error 
            (denominator will be always greater or equal to eps)

        Shape
        -----
        **y_pred** - torch.Tensor of shape (N, H, W)
        **y_true** - torch.Tensor of shape (N, H, W) 

        Examples
        --------
        >>> criterion = BCEJaccardLoss(jaccard_weight=0.5)
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.ones(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.3655

        >>> criterion = BCEJaccardLoss(jaccard_weight=0.5)
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.zeros(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.0

        References
        ----------
        https://pytorch.org/docs/stable/generated/torch.nn.BCELoss.html

        https://www.kaggle.com/bigironsphere/loss-function-library-keras-pytorch

        """
        assert reduction in {NONE, MEAN, SUM, BATCHWISE_MEAN}, logging.error("Invalid reduction method")
        super(BCEJaccardLoss, self).__init__()
        self.eps = eps
        self.jaccard_weight = jaccard_weight
        self.reduction = reduction
        self.nll_loss = nn.BCELoss(reduction=reduction)
        self.jaccard_loss = JaccardLoss(mode='binary', reduction=reduction)


        self._stash_bce_loss = 0
        self._stash_jaccard = 0

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        logging.debug("Inside binary_jaccard loss forward routine")
        y_pred = y_pred.float()
        y_true = y_true.float()

        self._stash_bce_loss = self.nll_loss(y_pred, y_true)
        loss = (1 - self.jaccard_weight) * self._stash_bce_loss + \
                self.jaccard_weight * (1. - self.jaccard_loss(y_pred, y_true))

        return loss
