from pydoc import locate
import logging


def get_optimizer(oconfig, model):
    """Creates and returns a optimizer based on optimizer type and arguments. 

    Parameters
    ----------
    oconfig : path of optimizer to be used and its args
    model : model to train or validate.

    Returns
    -------
    optimizer instance.

    Examples
    --------
    Create an optimizer instance using a dummy model and SGD parameters

    >>> class Dummy(nn.Module):
    ...     def __init__(self, n_channels, n_classes):
    ...         super(Dummy, self).__init__()
    ...         self.linear = nn.Linear(n_channels, n_classes)
    ...
    ...     def forward(self, x):
    ...         x = self.linear(x).permute(0, 3, 1, 2)
    ...         return x
    >>> model = Dummy(1, 1)
    >>> oconfig = {'torch.optim.SGD': {'lr': 0.1}}
    >>> optimizer = get_optimizer(oconfig=oconfig, model=model)
    >>> optimizer
    SGD (
    Parameter Group 0
        dampening: 0
        lr: 0.1
        momentum: 0
        nesterov: False
        weight_decay: 0
    )

    This optimizer instance can be passed to runner for training.

    Click `here <phobos.runner.optimizers.map.html>`_ to view details of optimizers supported by phobos currently. 
    """
    logging.debug("Enter get_optimizer routine")
    assert len(oconfig.keys()), logging.error("No optimizer passed!")
    assert len(oconfig.keys()) == 1, logging.error("Only one optimizer can be used!")

    oname = list(oconfig.keys())[0]
    if locate(oname):
        optimizer_class = locate(oname)
        args = oconfig[oname]
    else:
        raise Exception('Please provide proper pytorch optim path as optimizer')
    
    args['params'] = model.parameters()
    
    logging.debug("Exit get_optimizer routine")

    return optimizer_class(**args)


def get_scheduler(sconfig, optimizer):
    """Creates and returns a scheduler based on scheduler type and arguments.

    Parameters
    ----------
    oconfig : path of scheduler to be used and its args
    optimizer :  optimizer instance.

    Returns
    -------
    scheduler instance.

    Examples
    --------
    Create an optimizer instance using a dummy model and SGD parameters

    >>> class Dummy(nn.Module):
    ...     def __init__(self, n_channels, n_classes):
    ...         super(Dummy, self).__init__()
    ...         self.linear = nn.Linear(n_channels, n_classes)
    ...
    ...     def forward(self, x):
    ...         x = self.linear(x).permute(0, 3, 1, 2)
    ...         return x
    >>> model = Dummy(1, 1)
    >>> oconfig = {'torch.optim.SGD': {'lr': 0.1}}
    >>> optimizer = get_optimizer(oconfig=oconfig, model=model)
    >>> optimizer
    SGD (
    Parameter Group 0
        dampening: 0
        lr: 0.1
        momentum: 0
        nesterov: False
        weight_decay: 0
    )

    Create a scheduler instance using optimizer instance and STEP scheduler parameters

    >>> sconfig = {'torch.optim.lr_scheduler.StepLR': {'step_size': 30, 'gamma': 0.1}}
    >>> scheduler = get_scheduler(sconfig=sconfig, optimizer=optimizer)
    >>> scheduler
    <torch.optim.lr_scheduler.StepLR object at 0x7f4597b94a60>

    This scheduler instance can be passed to runner for training.

    Click `here <phobos.scheduler.map.html>`_ to view details of schedulers supported by phobos currently.
    """
    logging.debug("Enter get_scheduler routine")
    if len(sconfig.keys()):
        logging.debug("No scheduler passed!")
        return None 
        
    assert len(sconfig.keys()) == 1, logging.error("Only one scheduler can be used!")

    sname = list(sconfig.keys())[0]
    if locate(sname):
        scheduler_class = locate(sname)
        args = sconfig[sname]
    else:
        raise Exception('Please provide proper pytorch optim path as scheduler')
    
    args['optimizer'] = optimizer
    
    logging.debug("Exit get_scheduler routine")

    return scheduler_class(**args)
