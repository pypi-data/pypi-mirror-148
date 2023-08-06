import os
import random
import glob
import io
import json
import cv2

from PIL import Image
from rasterio.io import MemoryFile
import rasterio as rio
import numpy as np
import torch.nn as nn

from shapely.geometry import Polygon
from skimage.draw import polygon

import torch.utils.data as data
from . import getWebDataLoaders, getDataLoaders

import albumentations as A
from phobos.transforms import Normalize


__all__ = ["get_dataloaders"]

def preproc_band(band_byte):
    mfile = MemoryFile(band_byte)
    r = mfile.open()
    return r, r.read()[0]

def preproc_label(json_stream):
    mfile = io.BytesIO(json_stream)
    json_data = json.load(mfile)
    return json_data['properties']['responses'][0]["0"][0]

def preproc_mask(json_stream, r):
    mfile = io.BytesIO(json_stream)
    json_data = json.load(mfile)
    mask = np.zeros((r.shape[0], r.shape[1]), dtype=np.uint8)

    for feature in json_data['features']:
        try:
            poly = Polygon(feature['geometry']['coordinates'][0])
            label = feature['properties']['lbl']
            
            xs, ys = poly.exterior.coords.xy
            rc = rio.transform.rowcol(r.transform, xs, ys)
            poly = np.asarray(list(zip(rc[0], rc[1])))
            rr, cc = polygon(poly[:,0], poly[:,1], mask.shape)
            mask[rr,cc] = label + 1
        except:
            pass

    return mask


class ClassificationTransform(nn.Module):
    def __init__(self, transform, inp_name, out_name, raster_keys):
        super(ClassificationTransform, self).__init__()
        self.transform = transform 
        self.raster_keys = raster_keys
        self.inp_name = inp_name
        self.out_name = out_name

    def forward(self, stream):
        bands = []
        for raster_key in self.raster_keys:
            r, band = preproc_band(stream[f"{raster_key.lower()}.path"])
            bands.append(band)

        label = preproc_label(stream["geojson.path"])
        bands = np.asarray([bands]).astype(np.float32)

        return {self.inp_name: bands}, {self.out_name: label}


class SegmentationTransform(nn.Module):
    def __init__(self, transform, inp_name, out_name, raster_keys):
        super(SegmentationTransform, self).__init__()
        self.transform = transform 
        self.raster_keys = raster_keys
        self.inp_name = inp_name
        self.out_name = out_name

    def forward(self, stream):
        bands = []
        r = None
        for raster_key in self.raster_keys:
            r, band = preproc_band(stream[f"{raster_key.lower()}.path"])
            bands.append(band)

        mask = preproc_mask(stream["geojson.path"], r)
        bands = np.asarray([bands]).astype(np.float32)

        return {self.inp_name: bands}, {self.out_name: mask}


def get_dataloaders(args):
    """Get train and val dataloaders.
    Given user arguments, loads dataset metadata
    defines a preloader and returns train and val dataloaders.
    Parameters
    ----------
    args : basecamp.grain.grain.Grain
        Dictionary of argsions/flags
    Returns
    -------
    (DataLoader, DataLoader)
        returns train and val dataloaders
    """
    train_url = f"pipe:aws s3 cp {args.dataset.yaml.replace('metadata.yaml', f'train/{args.dataset.train.url}')} -"
    val_url = f"pipe:aws s3 cp {args.dataset.yaml.replace('metadata.yaml', f'val/{args.dataset.val.url}')} -"
    
    which_transform = None
    inp_name = list(args.input.keys())[0]
    raster_keys = []
    for date in args.input[inp_name].dates:
        for band in args.input[inp_name].bands:
            raster_keys.append(f"{date}.{args.input[inp_name].sensor}.{band}")

    for out_name in args.output:
        if args.output[out_name].type == 'label':
            which_transform = ClassificationTransform
        if args.output[out_name].type == 'mask':
            which_transform = SegmentationTransform
            break

    datasets = getWebDataLoaders(posixes={"train": train_url,
                                          "val": val_url},
                                 transforms={"train": which_transform(None, 
                                                                      inp_name,
                                                                      out_name,
                                                                      raster_keys),
                                             "val": which_transform(None, 
                                                                      inp_name,
                                                                      out_name,
                                                                      raster_keys)},
                                 batch_size=args.run.batch_size,
                                 num_workers=args.run.num_workers)

    return datasets["train"], datasets["val"]