from typing import Optional, List
import logging

import torch
import torch.nn.functional as F
from torch.nn.modules.loss import _Loss

__all__ = ["SplineLoss"]


class SplineLoss(_Loss):
    
    def __init__(
        self, 
        patch_size: int, 
        lambda_p: Optional[int] = 1,
        eps: Optional[float] = 1e-7,
    ):
        r"""Creates a criterion that measures the Active Contour Error or Spline Error
        between predicted input :math:`U` and ground truth input :math:`V`.

        For :math:`X , Y \in \left[ 0 , 1 \right]^{m \times n}`, where :math:`m` and :math:`n` are the input dimensions,

        Active Contour Loss or Spline Loss is computed as:

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

        Shape
        -----
        **y_pred** - torch.Tensor of shape (N, H, W)
        **y_true** - torch.Tensor of shape (N, H, W) 

        Examples
        --------
        >>> criterion = SplineLoss(w=1, lambda_p=1, patch_size=32)
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.ones(2, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()
        0.0

        >>> criterion = SplineLoss(w=1, lambda_p=1, patch_size=32)
        >>> predicted = torch.ones(2, 1, 32, 32)
        >>> target = torch.zeros(2, 32, 32)
        >>> loss = criterion(predicted, target)
        >>> loss.item()    
        2.0

        References
        ----------
        https://openaccess.thecvf.com/content_CVPR_2019/papers/Chen_Learning_Active_Contour_Models_for_Medical_Image_Segmentation_CVPR_2019_paper.pdf
        """
        super(SplineLoss, self).__init__()
        self.patch_size = patch_size
        self.lambda_p = lambda_p
        self.eps = eps

    def forward(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:
        logging.debug("Inside spline loss forward routine")
        y_pred = y_pred.float()
        y_true = y_true.float()

        # horizontal and vertical directions
        x = y_pred[:, 1:, :] - y_pred[:, :-1, :]
        y = y_pred[:, :, 1:] - y_pred[:, :, :-1]

        delta_x = x[:, 1:, :-2]**2
        delta_y = y[:, :-2, 1:]**2
        delta_u = torch.abs(delta_x + delta_y)

        # equ.(11) in the paper
        length = torch.sum(torch.sqrt(delta_u + self.eps))

        c_1 = torch.ones((self.patch_size, self.patch_size))
        c_2 = torch.zeros((self.patch_size, self.patch_size))

        c_1 = c_1.to(y_pred.device)
        c_2 = c_2.to(y_pred.device)

        region_in = torch.abs(
            torch.sum(
                y_pred[:, :, :] * ((y_true[:, :, :] - c_1)**2)))  # equ.(12) in the paper
        region_out = torch.abs(
            torch.sum(
                (1 - y_pred[:, :, :]) * ((y_true[:, :, :] - c_2) ** 2)))  # equ.(12) in the paper

        loss = length + self.lambda_p * (region_in + region_out)

        return loss / y_true.nelement()
