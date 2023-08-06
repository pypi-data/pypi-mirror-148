from typing import Optional, List
import logging

import torch
import torch.nn.functional as F
from torch.nn.modules.loss import _Loss
from ._functional import soft_tversky_score, to_tensor
from .constants import (BINARY_MODE, MULTICLASS_MODE, MULTILABEL_MODE, \
                        NONE, MEAN, SUM, BATCHWISE_MEAN)

__all__ = ["TverskyLoss"]


class TverskyLoss(_Loss):
    
    def __init__(
        self,
        mode:str,
        alpha: float = 0.5,
        beta: float = 0.5,
        gamma: float = 1.0, 
        classes: Optional[List[int]] = None,
        log_loss: bool = False,
        from_logits: bool = True,
        smooth: float = 0.0,
        ignore_index: Optional[int] = None,
        reduction: Optional[str] = "mean",
        eps: float = 1e-7,
    ):
        r"""Creates a criterion that measures the Tversky Error
        between each element in the input :math:`X` and target :math:`Y`.

        Tversky Coefficient is computed as:

        .. math:: TC(X,Y) = \frac{ TP + \epsilon }{ TP + \alpha \cdot FP + \beta \cdot FN + \epsilon }

        where,

        :math:`TP \equiv` Number of True Positives :math:`= \left| X \cap Y \right|`

        :math:`FP \equiv` Number of False Positives :math:`= \left| X \; \cap \sim Y \right|`

        :math:`FN \equiv` Number of False Negatives :math:`= \left| \sim X \cap Y \right|`

        and :math:`\epsilon` is a constant added for numerical stability.

        Tversky Loss is computed as:

        .. math:: Loss_{TC}(X,Y) = 1 - TC(X,Y)

        If :math:`\alpha = \beta = 0.5 , TC(X,Y) \equiv` Dice Coefficient

        If :math:`\alpha = \beta = 1.0 , TC(X,Y) \equiv` Tanimoto Coefficient

        If :math:`\alpha + \beta = 1.0 , TC(X,Y) \equiv` F Beta Coefficient

        Parameters
        ----------
        mode: Loss mode 'binary', 'multiclass' or 'multilabel'
        alpha: Weight constant that penalize model for FPs (False Positives)
        beta: Weight constant that penalize model for FNs (False Positives)
        gamma: Constant that squares the error function. Defaults to ``1.0``
        classes: List of classes that contribute in loss computation. By default, all channels are included.
        log_loss: If True, loss computed as ``-log(tversky)`` otherwise ``1 - tversky``
        from_logits: If True assumes input is raw logits
        smooth: Smoothness constant for tversky coefficient (a)
        ignore_index: Label that indicates ignored pixels (does not contribute to loss)
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
        **y_pred** - torch.Tensor of shape (N, C, H, W)
        **y_true** - torch.Tensor of shape (N, H, W) or (N, C, H, W)

        Examples
        --------
        >>> criterion = TverskyLoss(mode='binary', from_logits=False)
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.ones(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.0

        >>> criterion = TverskyLoss(mode='binary', from_logits=False)
        >>> predicted = torch.zeros(2, 1, 32, 32)
        >>> target = torch.ones(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        1.0

        >>> criterion = TverskyLoss(mode='multiclass', from_logits=False)
        >>> predicted = torch.zeros(2, 2, 32, 32)
        >>> target = torch.empty(2, 1, 32, 32, dtype=torch.long).random_(2)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        1.0

        References
        ----------
        https://arxiv.org/abs/1706.05721

        """
        assert mode in {BINARY_MODE, MULTILABEL_MODE, MULTICLASS_MODE}, logging.error("Invalid loss mode!")
        assert reduction in {NONE, MEAN, SUM, BATCHWISE_MEAN}, logging.error("Invalid reduction method")
        super(TverskyLoss, self).__init__()
        self.mode = mode
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        if classes is not None:
            assert mode != BINARY_MODE, logging.error("Masking classes is not supported with mode=binary")
            classes = to_tensor(classes, dtype=torch.long)

        self.classes = classes
        self.from_logits = from_logits
        self.smooth = smooth
        self.eps = eps
        self.log_loss = log_loss
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        logging.debug("Inside dice loss forward routine")

        assert y_true.size(0) == y_pred.size(0), logging.error("First dimension (batch) of y_true and y_pred do not match")

        y_true = y_true.long()

        if self.from_logits:
            # Apply activations to get [0..1] class probabilities
            # Using Log-Exp as this gives more numerically stable result and does not cause vanishing gradient on
            # extreme values 0 and 1
            if self.mode == MULTICLASS_MODE:
                y_pred = y_pred.log_softmax(dim=1).exp()
            else:
                y_pred = F.logsigmoid(y_pred).exp()

        bs = y_true.size(0)
        num_classes = y_pred.size(1)
        dims = (0, 2)

        if self.mode == BINARY_MODE:
            y_true = y_true.view(bs, 1, -1)
            y_pred = y_pred.view(bs, 1, -1)

            if self.ignore_index is not None:
                mask = y_true != self.ignore_index
                y_pred = y_pred * mask
                y_true = y_true * mask

        if self.mode == MULTICLASS_MODE:
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

        if self.mode == MULTILABEL_MODE:
            y_true = y_true.view(bs, num_classes, -1)
            y_pred = y_pred.view(bs, num_classes, -1)

            if self.ignore_index is not None:
                mask = y_true != self.ignore_index
                y_pred = y_pred * mask
                y_true = y_true * mask

        scores = self.compute_score(y_pred, y_true.type_as(y_pred), smooth=self.smooth, eps=self.eps, dims=dims)

        if self.log_loss:
            loss = -torch.log(scores.clamp_min(self.eps))
        else:
            loss = 1.0 - scores

        # Dice loss is undefined for non-empty classes
        # So we zero contribution of channel that does not have true pixels
        # NOTE: A better workaround would be to use loss term `mean(y_pred)`
        # for this case, however it will be a modified jaccard loss

        mask = y_true.sum(dims) > 0
        loss *= mask.to(loss.dtype)

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

    def compute_score(self, output, target, smooth=0.0, eps=1e-7, dims=None) -> torch.Tensor:
        return soft_tversky_score(output, target, self.alpha, self.beta, smooth, eps, dims)
