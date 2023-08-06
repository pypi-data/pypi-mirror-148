import logging


__all__ = ["Dataset"]


class Dataset():
    """Class representing dataset"""

    def __init__(
        self,
        config: dict
    ):  
        self.train_transforms = {}
        self.val_transforms = {}

        if 'transforms' in config:
            if 'val' in config.transforms:
                self.val_transforms = config.transforms.val
                if 'train' not in config.transforms:
                    logging.warning("You have validation augmentations, maybe you need training augmentations too")
            assert [x in ['train', 'val'] for x in config.transforms.keys()], logging.error('Only train and val keywords are supported.')
            if 'train' in config.transforms:
                self.train_transforms = config.transforms.train
        else:
            logging.warning("No transforms have been passed for the dataset")

        if 'task' in config:
            self.task = config.task 
        else:
            self.task = None
            logging.warning(f"Task name is not present in {config.yaml}")
        
        if 'datasource' in config:
            self.datasource = config.datasource
        else:
            self.datasource = None
            logging.warning(f"Datasource name is not present in {config.yaml}")
        
        assert 'dates' in config, logging.error(f"Number of dates is not present in {config.yaml}")
        self.dates = config.dates  

        assert 'train' in config, logging.error(f"Train shard information is not present in {config.yaml}")       
        self.train_shards = config.train

        assert 'val' in config, logging.error(f"Val shard information is not present in {config.yaml}")
        self.val_shards = config.val

        if 'sampling' in config:
            self.sampling = config.sampling 
        else:
            self.sampling = None 
            logging.warning(f"Sampling strategy of {config.yaml} is unkown")
        
        assert 'sensors' in config, logging.error(f"Sensors information is not present in {config.yaml}")
        assert 'shard_keys' in config, logging.error(f"Shard keys not present in {config.yaml}")
        self.raster_keys = self.get_raster_keys(config)
        self.vector_config = self.get_vector_config(config)
        self.input_raster_keys = self.get_raster_keys(config)

    def get_raster_keys(
        self, 
        config
    ) -> dict:
        sensors_bands = {}
        for sensor in config.sensors.keys():
            assert ('bands' in config.sensors[sensor]), logging.error(f"Sensor {sensor} should contain bands information in {config.yaml}")
            bands = config.sensors[sensor].bands
            for band in bands.keys():
                sensors_bands[f"{sensor}.{band}"] = bands[band]

        dates_sensors_bands = {}
        for k in config.shard_keys.keys():
            sensor_band = '.'.join(k.split('.')[1:])
            if k != 'GeoJSON':
                dates_sensors_bands[k] = {**config.shard_keys[k], **sensors_bands[sensor_band]}

        return dates_sensors_bands

    def get_vector_config(
        self, 
        config: dict
    ) -> dict:
        assert 'GeoJSON' in config.shard_keys, logging.error(f"GeoJSON shard key should be present in {config.yaml}")
        assert 'questions' in config.shard_keys.GeoJSON, logging.error(f"Questions information is not present in {config.yaml} shard key GeoJSON")
        questions = {}
        for question in config.shard_keys.GeoJSON.questions.keys():
            properties = config.shard_keys.GeoJSON.questions[question]
            assert 'response_options' in properties, logging.error(f"response_options for {config.yaml} shard key GeoJSON question {question} not present")
            assert 'temporal_scope' in properties, logging.error(f"temporal_scope for {config.yaml} shard key GeoJSON question {question} not present")
            assert 'structural_scope' in properties, logging.error(f"structural_scope for {config.yaml} shard key GeoJSON question {question} not present")
            assert 'type' in properties, logging.error(f"type for {config.yaml} shard key GeoJSON question {question} not present")
            assert 'reference_band' in properties, logging.error(f"reference_band for {config.yaml} shard key GeoJSON question {question} not present")
            assert 'response_location' in properties, logging.error(f"response_location for {config.yaml} shard key GeoJSON question {question} not present")
            questions[question] = properties
        
        return questions