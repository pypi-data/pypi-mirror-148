from typing import Optional, List
import logging

import torch
from torch.nn.modules.loss import _Loss

from .dice import DiceLoss
from .spline import SplineLoss

__all__ = ["DiceSplineLoss"]


class DiceSplineLoss(_Loss):

    def __init__(
        self, 
        alpha: float, 
        patch_size: int, 
        eps: Optional[float] = 1e-7,
    ):
        r"""Creates a criterion that measures the Dice Spline Error
        between each element in the input :math:`X` and target :math:`Y`.

        Dice Spline loss is computed as a weighted average between Dice Loss and Spline Loss:

        .. math:: Loss(X,Y) = (1 - \alpha) \cdot Loss_{DC}(X,Y) + \alpha \cdot Loss_{AC}(X,Y)

        where :math:`\alpha` is Dice Spline Weight

        :math:`Loss_{DC}(X,Y)` is the Dice Loss component,which is computed as:

        .. math:: Loss_{DC}(X,Y) = 1 - DC(X,Y)

        here, :math:`DC(X,Y)` is Dice Cofficient between inputs :math:`X` and :math:`Y`, which is computed as:

        .. math:: DC(X,Y) = \frac{2 \cdot | X \cap Y | + \epsilon }{|X| + |Y| + \epsilon}

        where :math:`\epsilon` is a constant added for numerical stability.

        :math:`Loss_{AC}(X,Y)` is the Active Contour loss or Spline Loss component, which is computed as:

        .. math:: Loss_{AC} = Length + \lambda \cdot Region

        in which,

        .. math:: Length = \int_C \left| \nabla X \right| ds

        .. math:: Region = \int_{\Omega} ((1-Y)^{2} - Y^{2})Xdu

        :math:`Length` and :math:`Region` can be written in pixel wise form as:

        .. math:: Length = \sum\limits_{\Omega}^{i=1,j=1} \sqrt{\left| (\nabla X_{u_{i,j}})^{2} + (\nabla X_{v_{i,j}})^{2}\right| + \epsilon }

        where :math:`u` and :math:`v` from :math:`X_{u_{i,j}}` and :math:`X_{v_{i,j}}` are horizontal and vertical directions respectively,

        and :math:`\epsilon` is a constant added for numerical stability.

        .. math:: Region = \left| \sum\limits_{\Omega}^{i=1,j=1} X_{i,j} \cdot (1-Y_{i,j})^{2}\right| + \left| \sum\limits_{\Omega}^{i=1,j=1} (1-X_{i,j}) \cdot Y_{i,j}^{2}\right|

        Parameters
        ----------
        patch_size : patch size of image
        lambda_p : parameter to control the balance between regularization process
        eps: A small epsilon for numerical stability to avoid zero division error 
            (denominator will be always greater or equal to eps)

        Examples
        --------
        >>> criterion = DiceSplineLoss(alpha=0.5, patch_size=32)
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.ones(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.00777

        >>> criterion = DiceSplineLoss(alpha=0.5, patch_size=32)
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.zeros(2, 1, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.5

        References
        ----------
        https://www.kaggle.com/bigironsphere/loss-function-library-keras-pytorch

        https://openaccess.thecvf.com/content_CVPR_2019/papers/Chen_Learning_Active_Contour_Models_for_Medical_Image_Segmentation_CVPR_2019_paper.pdf
        """
        super(DiceSplineLoss, self).__init__()
        self.eps = eps
        self.alpha = alpha
        self.patch_size = patch_size

        self.dice = DiceLoss(mode='binary', reduction='mean', eps=self.eps)
        self.spline = SplineLoss(patch_size=self.patch_size)

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        logging.debug("Inside dice_spline loss forward routine")
        return (1 - self.alpha) * self.dice(y_pred, y_true) + \
            self.alpha * self.spline(y_pred, y_true)
