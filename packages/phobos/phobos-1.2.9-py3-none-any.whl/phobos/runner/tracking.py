import logging

from numpy import isin
from phobos.dataset import output 

from phobos.loss import LossCollection
from phobos.metrics import MetricCollection

__all__ = ["TrackingOutput", "TrackingOutputCollection"]


class TrackingOutput():
    """Class representing an output head of model

    Parameters
    ----------
    config : map containing model output(s) configs
    device : device on which metrics and losses should be computed
    
    Attributes
    ----------
    means : map containing crunched statistics after a batch/epoch cycle
    logits : flag representing type of input expected by MetricCollection instance, by default ``False``
    
        * ``True``  : logits based inputs
        * ``False`` : non logits based inputs

    num_classes : number of classes in output
    train_losses : object representing collection of training losses at output head
    train_metrics : object representing collection of training metrics at output head
    val_losses : object representing collection of validation losses at output head
    val_metrics : object representing collection of validation metrics at output head
    
    Examples
    --------
    Check OutputCollection examples
    """
    def __init__(
        self, 
        config: dict, 
        device: int
    ):  
        # TODO: Validate if the loss function and metrics are compatible with type
        assert isinstance(config, dict), logging.error("Tracking output config should be a dictionary or YACS")
        assert len(config.keys()) == 1, logging.error("Tracking output config can only have one output")
        self.name = list(config.keys())[0]
        output_properties = config[self.name]
        
        self.means = {}

        assert 'logits' in output_properties, logging.error(f"Please pass if model output {self.name} are logits or not")
        self.logits = output_properties['logits']

        assert 'type' in output_properties, logging.error(f"Please pass if model output {self.name} type (label/multilabels/mask/bbox)")
        if output_properties.type == 'multilabel':
            self.multilabel = True
        else:
            self.multilabel = False
            
        assert 'question' in output_properties, logging.error(f"Please provide question for model output {self.name}")
        self.num_classes = output_properties.num_classes
        
        assert 'loss' in output_properties, logging.error(f"Model output {self.name} should have one or more losses")
        self.train_losses  = LossCollection(
                                config=output_properties.loss,
                                common=self.getCommonParams()
                                )

        assert 'metrics' in output_properties, logging.error(f"Model output {self.name} should have metrics")
        self.train_metrics = MetricCollection(
                                config=output_properties.metrics,
                                common=self.getCommonParams(),
                                device=device,
                                logits=self.logits,
                                multilabel=self.multilabel
                                )

        self.val_losses    = LossCollection(
                                config=output_properties.loss,
                                common=self.getCommonParams()
                                )

        self.val_metrics   = MetricCollection(
                                config=output_properties.metrics,
                                common=self.getCommonParams(),
                                device=device,
                                logits=self.logits,
                                multilabel=self.multilabel
                                )

    def compute(
        self, 
        mode: str, 
        phase: str
    ):
        """Combines losses' and metrics' computation results for output head after a train/val cycle

        Parameters
        ----------
        mode : training mode. phobos supports following modes currently

            * ``epoch`` : epoch-wise model training
            * ``batch`` : batch-wise model training
        phase : phase of a training cycle. by default ``train``. can take following values

            * ``train`` : training phase
            * ``val``   : validation phase
        """
        if mode == 'epoch':
            params = [self.train_metrics, self.train_losses, self.val_metrics, self.val_losses]
            keys   = ['train_metrics', 'train_loss', 'val_metrics', 'val_loss']
        elif mode == 'batch':
            if phase == 'train':
                params = [self.train_metrics, self.train_losses]
                keys = ['train_metrics', 'train_loss']
            elif phase == 'val':
                params = [self.val_metrics, self.val_losses]
                keys = ['val_metrics', 'val_loss']

        for i in range(len(params)):
            pmeans = params[i].compute()
            self.means[keys[i]] = { k: float(v) for k, v in pmeans.items() }

    def reduce(
        self, 
        outputlist: list, 
        wsize: int
    ):
        """Reduces metrics and losses from similar output heads in multiple nodes during distributed model training

        Parameters
        ----------
        outputlist : list of similar output head instances in multiple nodes
        wsize : node pool's world size
        """
        for mkey in self.means:
            if 'metric' not in mkey:
                for pkey in self.means[mkey]:
                    psum = 0 
                    for output in outputlist:
                        psum += output.means[mkey][pkey]

                    self.means[mkey][pkey] = psum/wsize

    def reset(self):
        """Resets metrics and loss states for output head

        """
        params = [self.train_metrics, self.train_losses, self.val_metrics, self.val_losses]
        for param in params:
            param.reset()

        self.means = {}

    def getCommonParams(self):
        """Creates and returns a map of common parameters for all metrics and losses for output head

        Returns
        -------
        `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_
            map of common parameters
        """
        cparams = {
            'num_classes': self.num_classes
        }
        return cparams

    def print(self):
        """Prints current statistics for output head

        """
        for mkey in self.means:
            print(f'\t{mkey}:')
            for pkey, pmean in self.means[mkey].items():
                print(f'\t\t{pkey}: {pmean}')


class TrackingOutputCollection():
    """Class representing a collection of model's output heads

    Parameters
    ----------
    config : map containing all output head configurations, retrieved from YAML
    device : device on which all losses and metrics should be computed

    Attributes
    ----------
    lossmap : map of final losses after combination
    device : model device
    heads : map of Output instances and their head ids
    headmap : map with overall model output statistics

    Examples
    --------
    Use a sample config

    >>> config = {
    ...           'segmentation': {
    ...                'logits': True,
    ...                'num_classes': 10,
    ...                'metrics': {
    ...                     'torchmetrics.Precision': {
    ...                          'average': 'macro'
    ...                      },
    ...                     'torchmetrics.Recall': {
    ...                           'average': 'macro'
    ...                      }
    ...                 },
    ...                 'losses': {
    ...                      'torch.nn.CrossEntropyLoss': None
    ...                     },
    ...                 'factor': 0.5
    ...                 },
    ...               'detection': {
    ...                     'logits': True,
    ...                     'num_classes': 10,
    ...                     'metrics': {
    ...                         'torchmetrics.Precision': {
    ...                             'average': 'macro'
    ...                         },
    ...                         'torchmetrics.Recall': {
    ...                             'average': 'macro'
    ...                             }
    ...                         },
    ...                     'losses': {
    ...                         'nn.CrossEntropyLoss': None
    ...                     },
    ...                     'factor': 0.5
    ...                 }
    ...             }

    Model's device to create an OutputCollection instance

    >>> device = torch.device("cpu",0)
    >>> outputs = OutputCollection(config=config, device=device)
    >>>

    Combine output statistics (metrics and losses) at the end of a train/val cycle

    >>> outputs.compute(mode='epoch')

    At master node in case of distributed training,
    
    combine results in OutputCollection instances from worker nodes

    >>> wsize = 32
    >>> outlist = [None for _ in range(wsize)]
    >>> dist.all_gather_object(outlist, outputs, group=dist.group.WORLD)
    >>> outputs.reduce(outlist, wsize)
    >>>

    print final results of a cycle

    >>> outputs.print()

    summarise results of cycle 

    >>> outputs.setHeadMap()

    use a map of tensorboard writers to log cycle's results to tensorboard

    >>> twriter = SummaryWriter(log_dir='/tmp')
    >>> vwriter = SummaryWriter(log_dir='/tmp')
    >>> map = {'train': twriter, 'val': vwriter}
    >>> cycle = 10
    >>>
    >>> outputs.plotTensorBoard(map, cycle)
    >>>

    use a polyaxon experiment to log cycle's results to polyaxon

    >>> outputs.logPolyaxon(cycle, exp)

    reset results to cycle after computation, printing and logging

    >>> outputs.reset()

    """
    def __init__(
        self, 
        config: dict,
        device: int
    ):
        assert config, logging.error("Model output tracking needs to be passed.")
        assert len(config.keys()), logging.error("Track one or more output coming from model.")
        if len(config.keys()) == 1:
            assert 'factor' not in config[list(config.keys())[0]], logging.error(f"{list(config.keys())[0]} has multiplication factor and this model has single output.")
        if len(config.keys()) > 1:
            for k in config.keys():
                assert 'factor' in config[k], logging.error(f"{k} does not have a multiplication factor. This model has multiple outputs.")

        self.track_outputs = {}
        self.device = device
        self.factors = {}
        self.train_combined_loss = 0
        self.val_combined_loss = 0

        self.setOutputHeads(config)

    def setOutputHeads(
        self, 
        config: dict
    ):
        """Creates Output instances for each of the heads configured in ``ymeta``

        and populates ``heads`` with a map of head IDs and corresponding Output instance

        Parameters
        ----------
        config : map containing all output head configurations, retrieved from YAML
        """
        for output_name in config.keys():
            output_config = config[output_name]
            self.track_outputs[output_name] = TrackingOutput(
                                            config={output_name: output_config},
                                            device=self.device
                                            )
            if 'factor' in output_config:
                self.factors[output_name] = output_config['factor']

    def setHeadMap(self):
        """Internally summarises results of a cycle

        """
        map = {}
        for output_name, track_output in self.track_outputs.items():
            for mkey in track_output.means:
                for pkey, pmean in track_output.means[mkey].items():
                    key = f'{output_name}|{mkey}|{pkey}'
                    map[key] = pmean
        
        map['train_combined_loss'] = self.train_combined_loss
        map['val_combined_loss'] = self.val_combined_loss

        self.headmap = map

    def compute(self, mode, phase='train'):
        """Combines  model's output statistics(metrics and losses) for a train/val cycle

        Parameters
        ----------
        mode : training mode. phobos supports following modes currently

            * ``epoch`` : epoch-wise model training
            * ``batch`` : batch-wise model training
        phase : phase of a training cycle. by default ``train``. can take following values

            * ``train`` : training phase
            * ``val``   : validation phase
        """
        for output_name, track_output in self.track_outputs.items():
            track_output.compute(mode=mode, phase=phase)

            if output_name in self.factors:
                factor = self.factors[output_name]
            else:
                factor = 1

            if mode == 'epoch':
                if 'combined' in track_output.means['train_loss']:
                    self.train_combined_loss += factor * track_output.means['train_loss']['combined']
                else:
                    self.train_combined_loss += factor * list(track_output.means['train_loss'].values())[0]

                if 'combined' in track_output.means['val_loss']:
                    self.val_combined_loss += factor * track_output.means['val_loss']['combined']
                else:
                    self.val_combined_loss += factor * list(track_output.means['val_loss'].values())[0]
                
            elif mode == 'batch':
                if phase == 'train':
                    if 'combined' in track_output.means['train_loss']:
                        self.train_combined_loss += factor * track_output.means['train_loss']['combined']
                    else:
                        self.train_combined_loss += factor * list(track_output.means['train_loss'].values())[0]
                elif phase == 'val':
                    if 'combined' in track_output.means['val_loss']:
                        self.val_combined_loss += factor * track_output.means['val_loss']['combined']
                    else:
                        self.val_combined_loss += factor * list(track_output.means['val_loss'].values())[0]

    def reduce(
        self, 
        outputslist: list, 
        wsize: int
    ):
        """Reduces results in OutputCollection instances from worker nodes during distributed model training

        Parameters
        ----------
        outputslist : list of output collections from worker nodes
        wsize : node pool's world size
        """
        for output_name, track_output in self.track_outputs.items():
            outputlist = [track_outputs[output_name] for track_outputs in outputslist]
            track_output.reduce(outputlist, wsize)

        self.train_combined_loss = sum([track_outputs.train_combined_loss for track_outputs in outputlist]) / wsize
        self.val_combined_loss = sum([track_outputs.val_combined_loss for track_outputs in outputlist]) / wsize

    def reset(self):
        """Resets final results of a cycle

        """
        for _, track_output in self.track_outputs.items():
            track_output.reset()

        self.train_combined_loss = 0
        self.val_combined_loss = 0
        self.headmap = {}

    def print(self):
        """Prints final results of a cycle

        """
        for output_name, track_output in self.track_outputs.items():
            print(f'{output_name}:')
            track_output.print()

        print(f"train_combined_loss: {self.train_combined_loss}")
        print(f"val_combined_loss: {self.val_combined_loss}")

    def plotTensorboard(
        self, 
        tboards: dict, 
        step: int
    ):
        """Logs results of a cycle to Tensorboard

        Parameters
        ----------
        tboards : map of tensorboard writers
        step : current step/iteration number
        """
        for key in self.headmap:
            if 'train' in key:
                tboards['train'].add_scalar(key, self.headmap[key], step)
            elif 'val' in key:
                tboards['val'].add_scalar(key, self.headmap[key], step)

    def logPolyaxon(
        self, 
        exp, 
        step: int, 
        rank: int = -1
    ):
        """Logs results of a cycle to Polyaxon

        Parameters
        ----------
        exp : polyaxon experiment
        step : current step/iteration number
        rank : rank of node, by default -1
        """
        if rank == -1:
            exp.log_metrics(step=step, **self.headmap)
        else:
            exp.log_metrics(step=step, rank=rank, **self.headmap)