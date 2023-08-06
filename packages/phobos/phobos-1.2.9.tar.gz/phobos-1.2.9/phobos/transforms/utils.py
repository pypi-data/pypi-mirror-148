from pydoc import locate
from threading import local 

from albumentations.core.composition import Compose

import logging


def build_pipeline(config):
    """Create train and val transforms pipelines from args.

    Parameters
    ----------
    config : Dictionary of transforms to be applied in training and validation pipeline.
    
    Returns
    -------
    train _aug_pipeline / val_aug_pipeline : train pipeline / val pipeline based on :attr:`dstype` passed

    Examples
    --------
    Create train and val transforms pipeline 

    >>> config = {
    ...             'train': [
    ...                         {'phobos.transforms.Normalize': {}},
    ...                         {'albumentations.VerticalFlip': {'p': 0.5}},
    ...                         {'albumentations..HorizontalFlip': {'p': 0.5}}
    ...                  ],
    ...             'val': [   
    ...                         {'phobos.transforms.Normalize': {}}
    ...                  ]
    ...         }
    >>> train_pipeline, val_pipeline = build_pipeline(config)
    >>> train_pipeline
    Compose([
        Normalize(always_apply=False, p=1.0, mean=[0.485 0.456 0.406], std=[0.229 0.224 0.225]),
        VerticalFlip(always_apply=False, p=0.5),
        HorizontalFlip(always_apply=False, p=0.5),
    ], p=1.0, bbox_params=None, keypoint_params=None, additional_targets={})
    >>> val_pipeline
    Compose([
        Normalize(always_apply=False, p=1.0, mean=[0.485 0.456 0.406], std=[0.229 0.224 0.225]),
    ], p=1.0, bbox_params=None, keypoint_params=None, additional_targets={})

    Use these pipelines to apply transforms to image and masks in dataloaders. We pass patches to pipeline below

    >>> img = full_load[key]['i']
    >>> msk = full_load[key]['m']
    >>>
    >>> img_crop = np.copy(img[:,x:x+w,y:y+w])
    >>> msk_crop = np.copy(msk[x:x+w,y:y+w])
    >>>
    >>> trns_out = train_pipeline(image=img_crop,mask=msk_crop)
    >>>
    >>> tr_img_crop = trns_out['image']
    >>> tr_msk_crop = trns_out['mask']

    Click `here <phobos.transform.map.html>`_ for details of transforms supported by phobos currently

    Custom transforms can also be added to transforms pipelines. Please check `here <phobos.transforms.html#phobos.transforms.utils.set_transform>`_ for more details.
 
    """
    logging.debug("Enter build_pipeline routine")
    if len(config.keys()) == 0:
        logging.debug("No input data transformation has been applied")
        return Compose([]), Compose([])

    assert [x in ['train', 'val'] for x in config.keys()], logging.error('Only train and val keywords are supported.')

    
    train_pipeline = Compose([])
    if len(config['train']):
        xforms = config['train']
        aug_list = []
        for aug, params in xforms:
            if locate(aug):
                aug_class = locate(aug)
                aug_list.append(aug_class(**params))
            else:
                raise Exception(f"{aug} does not exist. Please check for typo.")
        train_pipeline = Compose(aug_list)
    else:
        logging.warning('Empty train augs passed')

    val_pipeline = Compose([])
    if 'val' in config:
        if len(config['val']):
            xforms = config['val']
            aug_list = []
            for aug, params in xforms:
                if locate(aug):
                    aug_class = locate(aug)
                    aug_list.append(aug_class(**params))
                else:
                    raise Exception(f"{aug} does not exist. Please check for typo.")
            val_pipeline = Compose(aug_list)
        else:
            logging.warning('Empty val augs passed')

    return train_pipeline, val_pipeline
