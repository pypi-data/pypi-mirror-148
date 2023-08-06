import os
import logging
from typing import Tuple
from phobos.dataset.streams import get_dataloaders

import torch
import torch.distributed as dist
from torch.autograd import Variable
from torch.utils.tensorboard import SummaryWriter

from phobos.models import get_model 
from phobos.dataset import get_dataloaders
from .utils import get_scheduler, get_optimizer
from .tracking import TrackingOutputCollection

__all__ = ["Runner"]


class Runner():
    """Runner class.

    Parameters
    ----------
    model : model to train or validate.
    device : device to move tensors to.
    train_loader : dataloader to load training dataset.
    val_loader : dataloader to load validation dataset.
    inputs : object representing model's inputs
    outputs : object representing model's outputs
    optimizer : optimizer string / instance. Details of phobos supported optimizers `here <phobos.runner.optimizers.map.html>`_
    mode : mode of model training, by default ``epoch``. runner supports ``epoch`` and ``batch`` modes
    verbose : flag to run model training in verbose / diagnostic mode
    scheduler : scheduler string / instance. Details of phobos supported schedulers `here <phobos.runner.schedulers.map.html>`_
    max_iters : maximum number of iterations for model training. represents number of
        * epochs to train for ``epoch`` mode training
        * train dataset batches to process for ``batch`` mode training
    frequency : train cycle frequency for ``batch`` mode training
    distributed : flag to represent if model is to train in distributed mode, by default ``False``
    polyaxon_exp : polyaxon experiment.
    tensorboard_logging : flag to represent if results are to be logged in Tensorboard, by default ``True``

    Examples
    --------
    Parse properties configured in metadata YAML using a Grain instance

    >>> grain = Grain()
    >>> args = grain.parse_args_from_yaml('metadata.yaml')
    >>>

    Retrieve InputCollection and OutputCollection instances from Grain instance

    >>> inputs, outputs = grain.get_inputs_outputs()

    refer to Grain documentation for more details

    Create and load a dummy model 

    >>> class Dummy(nn.Module):
    ...     def __init__(self, n_channels, n_classes):
    ...         super(Dummy, self).__init__()
    ...         self.linear = nn.Linear(n_channels, n_classes)
    ... 
    ...     def forward(self, x):
    ...         x = x['inp']
    ...         x = self.linear(x).permute(0, 3, 1, 2)
    ...         x = torch.abs(x)
    ... 
    ...         map = {'out': x }
    ...         return map
    >>>
    >>> device = torch.device('cuda',args.gpu)
    >>> model = Dummy(1, 1).to(device=device)

    and dummy train and val loaders

    >>> class DummyPreloader(data.Dataset):
    ...     def __init__(self, patch_size, n_channels, n_classes, n_samples):
    ...         self.patch_size = patch_size
    ...         self.n_channels = n_channels
    ...         self.n_classes = n_classes
    ...         self.samples = n_samples
    ... 
    ...     def __getitem__(self, index):
    ...         imap = { 'inp': np.random.rand(self.patch_size, self.patch_size,
    ...                                self.n_channels) }
    ...         omap = { 'out' : np.ones((self.patch_size, self.patch_size)) }
    ... 
    ...         return imap, omap
    ... 
    ...     def __len__(self):
    ...         return self.samples
    >>>
    >>> train_set = DummyPreloader(patch_size=32,
    ...                            n_channels=1,
    ...                            n_classes=1,
    ...                            n_samples=5)
    >>> val_set = DummyPreloader(patch_size=32,
    ...                          n_channels=1,
    ...                          n_classes=16,
    ...                          n_samples=2)
    
    Use datasets map to create dataloaders

    >>> datasets = {'train': train_set, 'val': val_set }
    >>> 
    >>> loaders = getDataLoaders(
    ...     datasets=datasets,
    ...     batch_size=2,
    ...     num_workers=2,
    ...     load='full'
    ... )

    ``Note`` 
    
    keys ``inp`` and ``out`` used in model and dataset should be specified in metadata

    refer to MNIST examples for more clarity
    
    1. Create Runner instance using parsed arguments

    >>> runner = Runner(model=model,
    ...                 device=device,
    ...                 train_loader=loaders['train'],
    ...                 val_loader=loaders['val'],
    ...                 inputs=inputs,
    ...                 outputs=outputs,
    ...                 mode='epoch',
    ...                 max_iters=args.max_iters,
    ...                 optimizer=args.optimizer,
    ...                 scheduler=args.scheduler,
    ...                 )

    2. Pass ``batch`` related arguments to create Runner instance to train in ``batch`` mode: 

    >>> mode = 'batch'
    >>> frequency = 10
    >>> max_iters = 100
    >>>
    >>> runner = Runner(model=model,
    ...                 device=device,
    ...                 train_loader=loaders['train'],
    ...                 val_loader=loaders['val'],
    ...                 inputs=inputs,
    ...                 outputs=outputs,
    ...                 mode=mode,
    ...                 frequency=frequency,
    ...                 max_iters=max_iters,
    ...                 optimizer=args.optimizer,
    ...                 scheduler=args.scheduler,
    ...                 )

    these arguments can be configured in metadata YAML

    3. Set ``distributed`` flag to create Runner instance for distributed training

    >>> runner = Runner(model=model,
    ...                 device=device,
    ...                 train_loader=loaders['train'],
    ...                 val_loader=loaders['val'],
    ...                 inputs=inputs,
    ...                 outputs=outputs,
    ...                 mode='epoch',
    ...                 distributed=True,
    ...                 max_iters=args.max_iters,
    ...                 optimizer=args.optimizer,
    ...                 scheduler=args.scheduler,
    ...                 )

    Details of optimizers and schedulers supported by phobos currently can be viewed `here <phobos.runner.optimizers.map.html>`_ and `here <phobos.runner.schedulers.map.html>`_ 
    
    Apart from this, custom optimizer (derived from :attr:`torch.optim`) and custom scheduler (derived from :attr:`torch.optim.lr_scheduler`) can also be passed for Runner instance creation.

    Runner instance created thus is used for model training and evaluation

    >>> for step, outputs in runner.trainer():
    ...     if runner.master():
    ...         print(f'step: {step}')
    ...         outputs.print()
    ... 
    ...         val_recall = outputs.headmap['out|val_metrics|recall']
    ...         if val_recall > best_val:
    ...             best_val = val_recall
    ...             cpt_path = os.path.join(args.weight_dir,
    ...                                     'checkpoint_epoch_'+ str(step) + '.pt')
    ...             state_dict = model.module.state_dict() if runner.distributed else model.state_dict()
    ...             torch.save(state_dict, cpt_path)

    """
    def __init__(
        self,
        args,
        polyaxon_exp=None            
     ): 
        self.device = args.device
        self.train_loader, self.val_loader = get_dataloaders(args)
        self.model = get_model(args)
        self.tracking = TrackingOutputCollection(args.output, self.device)
        self.args = args.run

        assert 'mode' in self.args, logging.error("Runner mode (batch/epoch) is required in metadata.yaml")
        assert self.args.mode == 'epoch' or self.args.mode == 'batch', logging.error('Enter the correct mode epoch/batch')
        if 'verbose' not in self.args:
            self.args["verbose"] = False

        self.polyaxon_exp = polyaxon_exp

        self.optimizer = get_optimizer(self.args.optimizer, self.model)
        self.scheduler = get_scheduler(self.args.scheduler, self.optimizer)

        self.tboards = None

        if 'frequency' not in self.args:
            self.args['frequency'] = 0 

        if 'distributed' not in args:
            self.args['distributed'] = False 

        if self.args.distributed:
            self.set_distributed_params()

        if 'tensorboard' in self.args and self.args.tensorboard:
            if polyaxon_exp:
                tensorboard_path = os.path.join(polyaxon_exp.get_artifacts_path(), 'outputs/tensorboard')
            else:
                tensorboard_path = os.path.join(os.curdir, 'outputs/tensorboard')
            for dir_ in [tensorboard_path, os.path.join(tensorboard_path, 'train'), os.path.join(tensorboard_path, 'val')]:
                if not os.path.exists(dir_):
                    os.makedirs(dir_)
            
            tboard_train = SummaryWriter(log_dir=os.path.join(tensorboard_path, 'train'))
            tboard_val = SummaryWriter(log_dir=os.path.join(tensorboard_path, 'val'))
            
            self.tboards = {'train': tboard_train, 'val': tboard_val}
        else: 
            self.args['tensorboard'] = False

    def set_distributed_params(self):
        self.rank = dist.get_rank()
        self.world_size = dist.get_world_size()

    @staticmethod
    def distributed():
        """Initialize process group, default is nccl backend.
        """
        dist.init_process_group(backend='nccl')

    @staticmethod
    def local_testing():
        if 'POLYAXON_NO_OP' in os.environ:
            if os.environ['POLYAXON_NO_OP'] == 'true':
                return True
        else:
            return False

    def master(self):
        return (
            not self.args.distributed or Runner.local_testing()
            ) or (
                self.args.distributed and self.rank == 0
                )

    def tensorize_batch(self, inputs, labels):
        """Tensorize batch of input images and labels, and move them to gpu.

        Parameters
        ----------
        inputs : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of input images batch
        labels : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of input labels batch

        Returns
        -------
        inputs : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of input images batch loaded in gpu
        labels : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of input labels batch loaded in gpu
        """
        logging.debug("Enter tensorize_batch routine")

        for key in inputs:
            input = inputs[key]

            input = Variable(input)
            input = input.to(device=self.device).float()

            inputs[key] = input

        for key in labels:
            label = labels[key]

            label = Variable(label)
            label = label.to(device=self.device)

            labels[key] = label

        logging.debug("Exit tensorize_batch routine")

        return inputs, labels        

    def train_forward_backward(self, inputs, labels):
        """Performs forward propagation, loss evaluation
        and backward propagation while training model.

        Parameters
        ----------
        inputs : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of tensorised batch of input images.
        labels : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of tensorised batch of input labels.
        """
        # Zero the gradient
        logging.debug("Enter train_forward_backward routine")
        self.optimizer.zero_grad()

        self.model.train()

        # Get model predictions, calculate loss, backprop
        predictions = self.model(inputs)
        hlossmap = {}

        for key in predictions:
            ptensor = predictions[key]
            ltensor = labels[key]

            head = self.tracking.track_outputs[key]
            
            tlossmap = head.train_losses
            tmetmap = head.train_metrics

            tlosses = tlossmap(ptensor, ltensor)
            tmetrics = tmetmap(ptensor, ltensor)

            lkey = list(tlosses.keys())[0]
            hloss = tlosses[lkey]

            hlossmap[key] = hloss

        lkey = list(hlossmap.keys())[0]
        loss = hlossmap[lkey]

        loss.backward()
        self.optimizer.step()
        logging.debug("Exit train_forward_backward routine")

    def eval_forward(self, inputs, labels):
        """Performs forward propagation while evaluating model.

        Parameters
        ----------
        inputs : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of tensorised batch of input images.
        labels : `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of tensorised batch of input labels.
        """
        # Get predictions and calculate loss
        logging.debug("Enter eval_forward routine")

        self.model.eval()

        predictions = self.model(inputs)

        hlossmap = {}

        for key in predictions:
            ptensor = predictions[key]
            ltensor = labels[key]

            head = self.tracking.track_outputs[key]
            
            vlossmap = head.val_losses
            vmetmap = head.val_metrics

            vlosses = vlossmap(ptensor, ltensor)
            vmetrics = vmetmap(ptensor, ltensor)

            
            lkey = list(vlosses.keys())[0]
            hloss = vlosses[lkey]

            hlossmap[key] = hloss

        lkey = list(hlossmap.keys())[0]
        loss = hlossmap[lkey]

        if self.scheduler:
            self.scheduler.step(loss)

        logging.debug("Exit eval_forward routine")
        
    def condRun(self, iteration):
        if iteration < self.args.max_iters:
            return True
        print("exiting")
        return False

    def train_epoch(self, iteration):
        """Executes a single training cycle

        Parameters
        ----------
        iteration : `int <https://docs.python.org/3/library/functions.html#int>`_
            current iteration

        Yields
        -------
        `int <https://docs.python.org/3/library/functions.html#int>`_
            next iteration
        """
        while self.condRun(iteration):
            for inputs, labels in self.train_loader:
                inputs, labels = self.tensorize_batch(inputs, labels)

                self.train_forward_backward(inputs, labels)

                with torch.no_grad():
                    if self.args.mode == 'batch':
                        iteration += 1

                        self.tracking.compute(mode='batch', phase='train')

                        self.reduce_outputs()

                        if self.args.verbose:
                            print(f'step: {iteration}')
                            self.tracking.print()

                        self.log_outputs(iteration)

                        self.tracking.reset()

                        if not iteration % self.args.frequency:
                            yield iteration

            if self.args.mode == 'epoch':
                iteration += 1
                yield iteration

    def eval_epoch(self):
        """Executes a single validation cycle

        """
        for inputs, labels in self.val_loader:
            inputs, labels = self.tensorize_batch(inputs, labels)
            
            self.eval_forward(inputs, labels)
    
    def reduce_outputs(self):
        if self.args.distributed:
            outlist = [None for _ in range(self.world_size)]
            dist.all_gather_object(outlist, self.tracking, group=dist.group.WORLD)
            self.tracking.reduce(outlist, wsize=self.world_size)
            dist.barrier()

    def log_outputs(self, iteration):
        self.tracking.setHeadMap()
        
        if self.master():
            if self.polyaxon_exp:
                self.tracking.logPolyaxon(
                                        step=iteration,
                                        exp=self.polyaxon_exp)
            if self.args.tensorboard:
                self.tracking.plotTensorboard(
                                            step=iteration,
                                            tboards=self.tboards)
        if self.args.distributed:
            dist.barrier()

    def trainer(self):
        """Trains model on dataset, and yields results for every cycle

        Yields
        ------
        `phobos.io.OutputCollection <https://github.com/granularai/phobos/blob/develop/phobos/io/output.py>`_
            OutputCollection instance containing cycle results
        """
        logging.debug("Enter train_model generator")

        iteration = 0

        for iteration in self.train_epoch(iteration):
            with torch.no_grad():
                self.eval_epoch()

                if self.args.mode == 'epoch':
                    self.tracking.compute(mode='epoch')
                elif self.args.mode == 'batch':
                    self.tracking.compute(mode='batch', phase='val')

                self.reduce_outputs()
                
                self.log_outputs(iteration)
                    
                if not self.args.distributed:
                    yield iteration, self.tracking
                elif self.rank == 0:
                    yield iteration, self.tracking

                self.tracking.reset()       

                if not self.condRun(iteration):
                    break