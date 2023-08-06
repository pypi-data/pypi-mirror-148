import logging
from re import A

__all__= ["Output", "OutputCollection"]


class Output():
    """Class representing an output head of model
    """
    def __init__(
        self, 
        name: str,
        config: dict
    ):  
        self.name = name
        
        assert isinstance(config, dict), logging.error(f"Output {name} config should be a dictionary")
        assert 'question' in config, logging.error(f"Output {name} should contain a question name")
        self.question = config.question

        assert 'type' in config, logging.error(f"Output {name} should contain how this output should be treated (label/multilabel/mask/bbox")
        self.type = config.type

class OutputCollection():
    """Class representing a collection of model's output heads
    """
    def __init__(
        self, 
        config: dict
    ):
        assert isinstance(config, dict), logging.error("Output configuration should be a dictionary")
        assert len(config.keys()) > 0, logging.error("One or more outputs should be defined")
        self.set_output_heads(config)

    def set_output_heads(
        self, 
        config: dict
    ):
        """Creates Output instances for each of the heads configured in ``ymeta``
        and populates ``heads`` with a map of head IDs and corresponding Output instance
        Parameters
        ----------
        config : map containing all output head configurations, retrieved from YAML
        """
        idict = {}
        for output_name in config:
            idict[output_name] = Output(output_name, config[output_name])

        self.outputs = idict