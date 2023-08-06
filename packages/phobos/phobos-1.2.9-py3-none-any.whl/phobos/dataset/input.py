import logging
from re import A

__all__= ["Input", "InputCollection"]


class Input():
    """Class representing an input head of model
    """
    def __init__(
        self, 
        name: str,
        config: dict
    ):  
        self.name = name
        
        assert isinstance(config, dict), logging.error(f"Input {name} config should be a dictionary")
        assert 'dates' in config, logging.error(f"Input {name} should contain dates property. This is used to identify which dates should be used from the dataset.")
        assert isinstance(config['dates'], list), logging.error("Dates should be a list")
        assert 'bands' in config, logging.error(f"Input {name} should contain bands property. This is used to identify which bands should be used from the dataset.")
        assert 'sensor' in config, logging.error(f"Input {name} should contain sensor from which the images were obtained")
        assert 'patch_size' in config, logging.error(f"Input {name} should contain patch_size property.")
        self.patch_size = config['patch_size']

        self.raster_keys = self.get_raster_keys(config)

    def get_raster_keys(
        self, 
        config: dict
    ) -> list:
        dates_sensor_bands = []

        for date in config.dates:
            for band in config.bands:
                dates_sensor_bands.append(f"{date}.{config.sensor}.{band}")
        
        return dates_sensor_bands

class InputCollection():
    """Class representing a collection of model's input heads
    """
    def __init__(
        self, 
        config: dict
    ):
        assert isinstance(config, dict), logging.error("Input configuration should be a dictionary")
        assert len(config.keys()) > 0, logging.error("One or more inputs should be defined")
        self.set_input_heads(config)

    def set_input_heads(
        self, 
        config: dict
    ):
        """Creates Input instances for each of the heads configured in ``ymeta``
        and populates ``heads`` with a map of head IDs and corresponding Input instance
        Parameters
        ----------
        config : map containing all input head configurations, retrieved from YAML
        """
        idict = {}
        for input_name in config:
            idict[input_name] = Input(input_name, config[input_name])

        self.inputs = idict