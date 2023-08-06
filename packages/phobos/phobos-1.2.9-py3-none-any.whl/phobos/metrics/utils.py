import logging
import inspect 
from pydoc import locate

import torch
import torch.nn as nn

__all__ = ["MetricCollection"]


class MetricCollection(nn.ModuleDict):
    """Class representing a collection of metrics

    Parameters
    ----------
    config : metrics collection as dictionary
    common : common properties for all the metrics
    device : device on which to compute all the metrics
    logits : flag representing type of input expected by MetricCollection instance, by default ``False``
        
        * ``True``  : logits based inputs
        * ``False`` : non logits based inputs
    multilabel : flag representing if this is a multilabel task output

    Examples
    --------
    Given a map of metric configs

    >>> config = {
    ...     'torchmetrics.Accuracy': None,
    ...     'torchmetrics.Precision': {
    ...         'num_classes': 3,
    ...         'average': 'macro'
    ...     },
    ...     'torchmetrics.Recall': {
    ...         'num_classes': 3,
    ...         'average': 'macro'
    ...     }
    ... }
    ... common = {}

    Use this to create a MetricCollection instance

    i. expecting non logits based inputs:

    >>> metrics = MetricCollection(config, common)
    >>> metrics
    MetricCollection(
    (accuracy): Accuracy()
    (precision): Precision()
    (recall): Recall()
    )
    >>> metrics.logits
    False

    ii. expecting logits based inputs:

    >>> metrics = MetricCollection(config, common, logits=True)
    >>> metrics
    MetricCollection(
    (accuracy): Accuracy()
    (precision): Precision()
    (recall): Recall()
    )
    >>> metrics.logits
    True

    Compute metrics for

    i. non logit based inputs

    >>> pred = torch.randint(0,3,size=(4,32,32))
    >>> targ = torch.randint(0,3,size=(4,32,32))
    >>> 
    >>> mmap = metrics(pred, targ)
    >>> mmap
    {'accuracy': tensor(0.3420), 'precision': tensor(0.3424), 'recall': tensor(0.3422)}   

    ii. logits based inputs

    >>> metrics = get_metric(config, common, logits=True)
    >>> pred = torch.rand(size=(4,3,32,32))
    >>> targ = torch.randint(0,3,size=(4,32,32))
    >>> 
    >>> mmap = metrics(pred, targ)
    >>> mmap
    {'accuracy': tensor(0.3337), 'precision': tensor(0.3340), 'recall': tensor(0.3338)}
    >>> 

    Combine metrics computations after a cycle

    >>> means = metrics.compute()

    Log compute results and reset metrics states after cycle completion

    >>> metrics.reset()

    """
    def __init__(
        self, 
        config: dict, 
        common: dict, 
        device: torch.device, 
        logits: bool = False, 
        multilabel: bool = False
    ):
        super().__init__()
        assert isinstance(config, dict), logging.error("Metrics config should be a dictionary")
        assert len(config.keys()) > 0, logging.error("Metrics config should have one or more metric keys")
        self.logits = logits
        self.device = device
        self.multilabel = multilabel

        self.add_metrics(config, common)

    def add_metrics(self, config: dict, common: dict):
        """Add metrics instances in metrics list to MetricCollection

        Parameters
        ----------
        config : metrics specific config
        common : common config for all metrics

        Raises
        ------
        ValueError
            MetricCollection should not have redundant entries
        """
        for metric_name in config:
            if locate(metric_name):
                args = {} if config[metric_name] is None else config[metric_name]

                metric_class = locate(metric_name)

                args_list = inspect.getfullargspec(metric_class.__init__).args
                for k in args:
                    assert k in args_list, logging.error(f"{k} is not a valid parameter for {metric_name}")

                for ckey in common:
                    if ckey in args_list:
                        args[ckey] = common[ckey]

                if not args:
                    metric = metric_class()
                else:
                    metric = metric_class(**args)
                
                metric.to(self.device)
                mkey = metric.__class__.__name__
                self[mkey.lower()] = metric 
            else:
                logging.error('Please provide correct key path as argument')
        
    def forward(self, predicted: torch.Tensor, target: torch.Tensor) -> dict:
        """Performs metrics computation for predicted and ground truth tensors

        Parameters
        ----------
        predicted : `torch.Tensor <https://pytorch.org/docs/stable/tensors.html#torch.Tensor>`_
            predicted tensor
        target : `torch.Tensor <https://pytorch.org/docs/stable/tensors.html#torch.Tensor>`_
            ground truth tensor

        Returns
        -------
        `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map containing metric computation results
        """
        fmap = {}

        pr = predicted.detach().squeeze().to(self.device)
        tg = target.detach().squeeze().to(self.device)

        if self.multilabel:
            assert pr.shape == tg.shape
            n = pr.shape[1]
            p = pr.transpose(0, 1).reshape(n, -1).transpose(0, 1).type(torch.float)
            t = tg.transpose(0, 1).reshape(n, -1).transpose(0, 1).type(torch.int)            
        elif not self.logits:
            assert pr.shape == tg.shape
            p = pr.reshape(-1)
            if 'float' in str(p.dtype):
                p = p.round().type(torch.int)
            t = tg.reshape(-1).type(torch.int)
        else:
            assert len(pr.shape) == len(tg.shape)+1
            n = pr.shape[1]
            p = pr.transpose(0, 1).reshape(n, -1).transpose(0, 1).type(torch.float)
            t = tg.reshape(-1).type(torch.int)

        for mkey, metric in self.items():
            if 'classification' in str(metric.__class__):
                fmap[mkey] = metric(p, t)
            else:
                fmap[mkey] = metric(pr, tg)

        return fmap

    def compute(self) -> dict:
        """Combines metric computation results after a train/val cycle

        Returns
        -------
        `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map summarising overall metrics after the cycle
        """
        return {k: m.compute() for k, m in self.items()}

    def reset(self):
        """Resets metric states. 
        
        """
        for _, m in self.items():
            m.reset()
