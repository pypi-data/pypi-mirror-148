from optparse import Option
from typing import Optional, List
from functools import partial
import logging

import torch
import torch.nn.functional as F
from torch.nn.modules.loss import _Loss
from ._functional import focal_loss_with_logits, softmax_focal_loss_with_logits, to_tensor
from .constants import (BINARY_MODE, MULTICLASS_MODE, MULTILABEL_MODE, \
                        NONE, MEAN, SUM, BATCHWISE_MEAN)

__all__ = ["FocalLoss"]


class FocalLoss(_Loss):
    
    def __init__(
        self,
        mode: str,
        alpha: Optional[float] = None,
        gamma: Optional[float] = 2.,
        softmax: Optional[bool] = False,
        classes: Optional[List[int]] = None,
        ignore_index: Optional[int] = None, 
        reduction: Optional[str] = "mean",
        normalized: bool = False,
        reduced_threshold: Optional[float] = None,
        eps: float = 1e-7,
    ):
        r"""Creates a criterion that measures the Focal Error
        between each element in the input :math:`X` and target :math:`Y`..

        Focal loss is computed as:

        .. math:: Loss(X,Y) = \alpha \cdot (1 - E_{BCE}(X,Y))^{\gamma} \cdot Loss_{BCE}(X,Y) , \gamma \geqslant 0

        where :math:`Loss_{BCE}(X,Y)` is the BCE Loss component, which is computed as:

        .. math::
            Loss_{BCE}(X,Y) = \sum\limits_{i=1}^N l(x_i,y_i), l(x_i,y_i) = - w_i \left[ y_i \cdot \log x_i + (1 - y_i) \cdot \log (1 - x_i) \right]

        where :math:`x_i \in X` and :math:`y_i \in Y` and :math:`E_{BCE} = exp( - Loss_{BCE}(X,Y))`

        Parameters
        ----------
        mode: Loss mode 'binary', 'multiclass' or 'multilabel'
        alpha: Prior probability of having positive value in target.
        gamma: Power factor for dampening weight (focal strength).
        softmax: Softmax version of focal loss between target and output logits.
        classes:  List of classes that contribute in loss computation. By default, all channels are included.
        ignore_index: If not None, targets may contain values to be ignored.
            Target values equal to ignore_index will be ignored from loss computation.
        reduction (string, optional): Specifies the reduction to apply to the output:
            'none' | 'mean' | 'sum' | 'batchwise_mean'. 'none': no reduction will be applied,
            'mean': the sum of the output will be divided by the number of
            elements in the output, 'sum': the output will be summed. Note: :attr:`size_average`
            and :attr:`reduce` are in the process of being deprecated, and in the meantime,
            specifying either of those two args will override :attr:`reduction`.
            'batchwise_mean' computes mean loss per sample in batch. Default: 'mean'
        normalized: Compute normalized focal loss (https://arxiv.org/pdf/1909.07829.pdf).
        reduced_threshold: Switch to reduced focal loss. Note, when using this mode you should use `reduction="sum"`.

        Shape
        -----
        **y_pred** - torch.Tensor of shape (N, C, H, W)
        **y_true** - torch.Tensor of shape (N, H, W) or (N, C, H, W)

        Examples
        --------
        >>> criterion = FocalLoss(mode='binary', alpha=1, gamma=2)
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.ones(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.3133

        >>> criterion = FocalLoss(mode='binary',  alpha=1, gamma=0)
        >>> predicted = torch.zeros(2, 1, 32, 32)
        >>> target = torch.ones(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.6931

        >>> criterion = FocalLoss(mode='multiclass', alpha=0, gamma=0)
        >>> predicted = torch.randn(2, 4, 32, 32)
        >>> target = torch.empty(2, 1, 32, 32, dtype=torch.long).random_(4)
        >>> loss = criterion(predicted, target)
        0.5970

        >>> criterion = FocalLoss(mode='multiclass', gamma=2, softmax=True)
        >>> predicted = torch.randn(2, 4, 32, 32)
        >>> target = torch.empty(2, 32, 32, dtype=torch.long).random_(4)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        1.245

        References
        ----------
        https://arxiv.org/pdf/1708.02002.pdf

        """
        assert mode in {BINARY_MODE, MULTILABEL_MODE, MULTICLASS_MODE}
        assert reduction in {NONE, MEAN, SUM, BATCHWISE_MEAN}, logging.error("Invalid reduction method")
        if softmax:
            assert mode == MULTICLASS_MODE, logging.error("Softmax version is only for MULTICLASS mode")
        super(FocalLoss, self).__init__()

        self.mode = mode
        self.alpha = alpha 
        self.gamma = gamma
        if classes is not None:
            assert mode != BINARY_MODE, logging.error("Masking classes is not supported with mode=binary")
            classes = to_tensor(classes, dtype=torch.long)

        self.classes = classes
        self.softmax = softmax
        self.ignore_index = ignore_index
        self.reduction = reduction
        self.normalized = normalized
        self.reduced_threshold = reduced_threshold
        self.eps = eps 

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        logging.debug("Inside focal loss forward routine")

        assert y_true.size(0) == y_pred.size(0), logging.error("First dimension (batch) of y_true and y_pred do not match") 

        y_true = y_true.long()

        bs = y_true.size(0)
        num_classes = y_pred.size(1)


        if self.mode == BINARY_MODE:
            y_true = y_true.view(bs, 1, -1)
            y_pred = y_pred.view(bs, 1, -1)

            if self.ignore_index is not None:
                mask = y_true != self.ignore_index
                y_pred = y_pred * mask 
                y_true = y_true * mask 

        if self.mode == MULTICLASS_MODE:
            if not self.softmax:
                y_true = y_true.view(bs, -1)
                y_pred = y_pred.view(bs, num_classes, -1)

                if self.ignore_index is not None:
                    mask = y_true != self.ignore_index
                    y_pred = y_pred * mask.unsqueeze(1)

                    y_true = F.one_hot((y_true * mask).to(torch.long), num_classes)  # N,H*W -> N,H*W, C
                    y_true = y_true.permute(0, 2, 1) * mask.unsqueeze(1)  # H, C, H*W
                else:
                    y_true = F.one_hot(y_true, num_classes)  # N,H*W -> N,H*W, C
                    y_true = y_true.permute(0, 2, 1)  # H, C, H*W
            else:
                y_true = y_true.view(bs, -1)
                y_pred = y_pred.view(bs, num_classes, -1)


        if self.mode == MULTILABEL_MODE:
            y_true = y_true.view(bs, num_classes, -1)
            y_pred = y_pred.view(bs, num_classes, -1)

            if self.ignore_index is not None:
                mask = y_true != self.ignore_index
                y_pred = y_pred * mask
                y_true = y_true * mask

        loss = self.compute_score(y_pred, y_true)
        
        if self.classes is not None:
            loss = loss[self.classes]

        return self.aggregate_loss(loss)

    def aggregate_loss(self, loss):
        
        if self.reduction == MEAN:
            loss = loss.mean()
        if self.reduction == SUM:
            loss = loss.sum()
        if self.reduction == BATCHWISE_MEAN:
            loss = loss.sum(0)

        return loss

    def compute_score(self, output, target) -> torch.Tensor:
        if self.softmax:
            return softmax_focal_loss_with_logits(output, target, self.gamma, 
                                                  self.normalized, self.reduced_threshold, self.eps)
        else:
            return focal_loss_with_logits(output, target, self.gamma, self.alpha, 
                            self.normalized, self.reduced_threshold, self.eps)
