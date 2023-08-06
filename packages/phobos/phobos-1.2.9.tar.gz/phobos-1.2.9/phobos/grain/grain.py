import logging
import re
import collections
import yaml
import copy
import boto3

from yacs.config import CfgNode as CN
from yacs import config

from polyaxon.tracking import Run

import torch

from phobos import __version__ as version

config._VALID_TYPES = config._VALID_TYPES.union({Run, torch.device})

_VALID_TYPES = config._VALID_TYPES

class Grain(CN):
    """A class derived from class CfgNode from yacs to be used for:

    - validating config yaml properties
    
    - creating a python yacs object from yaml config file
    
    The object formed thus is a nested YACS object wherein YAML keys are converted to multilevel keys/attributes.

    Parameters
    ----------
    polyaxon_exp : polyaxon experiment
    """

    def __init__(
        self, 
        yaml_file: str, 
        polyaxon_exp: Run = None, 
        *args, 
        **kwargs
    ):  

        # TODO: Check validity of yaml file 

        with open(yaml_file, 'r') as fp:
            project_meta = dict(yaml.safe_load(fp.read()))
            project_meta = expand(project_meta, project_meta)['project']

        # TODO: Check if yaml file specified
        # TODO: Check if access to file is possible and file exists
        # TODO: Check if the file path is valid path
        # TODO: Check validity of yaml file

        yaml_file = project_meta['dataset']['yaml'].replace('s3://', '')
        bucket_name = yaml_file.split("/")[0]
        object_key = '/'.join(yaml_file.split("/")[1:])
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        dataset_meta = dict(yaml.safe_load(response["Body"]))
        dataset_meta = expand(dataset_meta, dataset_meta)

        project_meta['dataset'] = {**dataset_meta, **project_meta['dataset']}

            
        project_meta = Grain._create_config_tree_from_dict(project_meta, key_list=[])
        super(Grain, self).__init__(init_dict = project_meta)
        self.version = version
        
        if polyaxon_exp:
            map = flatten(self, sep='-')
            polyaxon_exp.log_inputs(**map)

        self.polyaxon_exp = polyaxon_exp
        
        self.device = torch.device("cpu", 0)
        if torch.cuda.is_available() and self.run.num_gpus > 0:
            self.device = torch.device("cuda", 0)

    
    @classmethod
    def _create_config_tree_from_dict(
        cls, 
        project_meta: dict, 
        key_list: list
    ) -> dict:
        """
        Create a configuration tree using the given dict.
        Any dict-like objects inside dict will be treated as a new CfgNode.
        Args:
            dic (dict):
            key_list (list[str]): a list of names which index this CfgNode from the root.
                Currently only used for logging purposes.
        """
        project_meta = copy.deepcopy(project_meta)
        for k, v in project_meta.items():
            if isinstance(v, dict):
                # Convert dict to CfgNode
                project_meta[k] = CN(v, key_list=key_list + [k])
            else:
                # Check for valid leaf type or nested CfgNode
                _assert_with_logging(
                    _valid_type(v, allow_cfg_node=False),
                    "Key {} with value {} is not a valid type; valid types: {}".format(
                        ".".join(key_list + [str(k)]), type(v), _VALID_TYPES
                    ),
                )
        return project_meta

def flatten(
    meta: dict, 
    parent_key: str = '', 
    sep: str = '.'
) -> dict:
    items = []
    for k, v in meta.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, str(v)))
    return dict(items)

def _assert_with_logging(
    cond: str, 
    msg: str
):
    if not cond:
        logging.debug(msg)
    assert cond, msg

def _valid_type(
    value, 
    allow_cfg_node=False
):
    return (type(value) in _VALID_TYPES) or (
        allow_cfg_node and isinstance(value, CN)
    )

def replace(
    map: dict, 
    rkey: str
) -> str:
    ref = map

    keys = rkey.split('.')
    for key in keys:
        if type(ref) == dict:
            ref = ref[key]
        elif type(ref) == list:
            ref = ref[int(key)]
        
    return ref

def expand(
    block, 
    meta
):
    if isinstance(block, dict):
        for key in block:
            block[key] = expand(block[key], meta)
    elif isinstance(block, list):
        for idx in range(len(block)):
            block[idx] = expand(block[idx], meta)
    else:
        if type(block) == str:
            mlist = re.findall(r'\$\{.*?\}', block)
            mkeys = [m[2:-1] for m in mlist]
            for i in range(len(mkeys)):
                if not block.replace(mlist[i], ''):
                    block = replace(meta, mkeys[i])
                else:
                    kref = replace(meta, mkeys[i])
                    block = block.replace(mlist[i], str(kref))
        
    return block
