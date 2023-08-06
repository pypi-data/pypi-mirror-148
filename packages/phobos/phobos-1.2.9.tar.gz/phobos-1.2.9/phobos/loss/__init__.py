import logging
import torch.nn as nn

from .bce_jaccard import BCEJaccardLoss
from .dice_spline import DiceSplineLoss
from .dice import DiceLoss
from .focal import FocalLoss
from .jaccard import JaccardLoss
from .lovasz import LovaszLoss
from .soft_bce import SoftBCEWithLogitsLoss
from .soft_ce import SoftCrossEntropyLoss
from .spline import SplineLoss
from .tversky import TverskyLoss


from .utils import LossCollection


__all__ = ['BCEJaccardLoss', 'DiceSplineLoss', 'DiceLoss', 
           'FocalLoss', 'JaccardLoss', 'LovaszLoss',
           'SoftBCEWithLogitsLoss', 'SoftCrossEntropyLoss', 
           'SplineLoss', 'TverskyLoss', "LossCollection"]
