import logging
import inspect
from copy import copy

import torch
import torch.nn as nn

from pydoc import locate

__all__ = ["LossCollection"]


class LossCollection(nn.ModuleDict):
    """Class representing a collection of losses

    Parameters
    ----------
    config : all losses and their params
    common : commong parameters for all the losses

    Attributes
    ----------
    state : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
        state dictionary for individual losses

    Examples
    --------
    Given a map of loss configs

    >>> config = {
    ...     'phobos.loss.TverskyLoss': {
    ...         'mode': 'binary',
    ...         'alpha': 1,
    ...         'beta': 0.5,
    ...         'factor': 0.5
    ...     },
    ...     'phobos.loss.DiceLoss': {
    ...         'mode': 'binary',
    ...         'factor': 0.5
    ...     }
    ... } 
    ... common = {}


    Use lconfig and cconfig to create a LossCollection instance

    >>> losses = LossCollection(config, common)
    >>> losses
    LossCollection(
    (tverskyloss): TverskyLoss()
    (diceloss): DiceLoss()
    )

    Compute individual loss for every train/val pass

    >>> pred = torch.rand(size=(2, 1, 32, 32))
    >>> targ = torch.randint(0, 2, size=(2, 32, 32))
    >>> 
    >>> lmap = losses(pred, targ)
    >>> lmap
    {'tverskyloss': tensor(0.6058), 'diceloss': tensor(0.5070), 'combined': tensor(0.5564)}

    Combine loss combinations after a cycle

    >>> means = losses.compute()

    Log compute results and reset loss states after cycle completion

    >>> losses.reset()

    """
    def __init__(
        self, 
        config: dict, 
        common: dict
    ):
        super().__init__()
        assert isinstance(config, dict), logging.error("Losses config should be a dictionary")
        assert len(config.keys()) > 0, logging.error("Losses config should have one or more loss keys")
        if len(config.keys()) == 1:
            if config[list(config.keys())[0]]:
                assert 'factor' not in config[list(config.keys())[0]], logging.error(f"{list(config.keys())[0]} has multiplication factor and it is a single loss for the model output.")
        if len(config.keys()) > 1:
            for k in config.keys():
                if config[k]:
                    assert 'factor' not in config[k], logging.error(f"{k} does not have a multiplication factor. This model output has multiple losses.")
        self.state = {}
        self.factors = {}
        
        self.add_losses(config, common)

    def add_losses(self, config: dict, common: dict):
        """Add loss instances in loss list to LossCollection

        Parameters
        ----------
        config : all losses and their params
        common : commong parameters for all the losses 

        Raises
        ------
        ValueError
            LossCollection should not have redundant entries
        """
        for loss_name in config:
            if locate(loss_name):
                args = {} if config[loss_name] is None else copy(config[loss_name])
                if 'factor' in args:
                    del args['factor']
                
                loss_class = locate(loss_name)
                
                args_list = inspect.getfullargspec(loss_class.__init__).args
                for k in args:
                    assert k in args_list, logging.error(f"{k} is not a valid parameter for {loss_name}")

                for ckey in common:
                    if ckey in args_list:
                        args[ckey] = common[ckey]

                if not args:
                    criterion = loss_class()
                else:
                    criterion = loss_class(**args)

                lkey = criterion.__class__.__name__
                self[lkey.lower()] = criterion
                self.state[lkey.lower()] = []
                if config[loss_name] and 'factor' in config[loss_name]:
                    self.factors[lkey.lower()] = config[loss_name]['factor'] 
                    self.state['combined'] = []
            else:
                logging.error('Please provide correct loss name')
            
    def forward(self, predicted: torch.Tensor, target: torch.Tensor) -> dict:
        """Performs loss computation for predicted and ground truth tensors

        Parameters
        ----------
        predicted : `torch.Tensor <https://pytorch.org/docs/stable/tensors.html#torch.Tensor>`_
            predicted tensor
        target : `torch.Tensor <https://pytorch.org/docs/stable/tensors.html#torch.Tensor>`_
            ground truth tensor

        Returns
        -------
        `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map containing loss computation results
        """
        losses = {}
        for loss_name, criterion in self.items():
            loss_val = criterion(predicted, target)

            losses[loss_name] = loss_val
            self.state[loss_name].append(loss_val)
            
            if loss_name in self.factors:
                if 'combined' not in losses:
                    losses['combined'] = self.factors[loss_name] * loss_val
                else:
                    losses['combined'] += self.factors[loss_name] * loss_val

        if 'combined' in losses:
            self.state['combined'].append(losses['combined'])

        return losses

    def compute(self) -> dict:
        """Combines loss computation results after a train/val cycle

        Returns
        -------
        `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map summarising overall loss after the cycle
        """
        return { lkey: torch.mean(torch.tensor(self.state[lkey])) for lkey in self.state }

    def reset(self):
        """Resets loss states 
        
        """
        for lkey in self.state:
            self.state[lkey] = []