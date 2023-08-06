import logging 

import torch
from . import initialization as init


class SegmentationModel(torch.nn.Module):

    def initialize(self):
        init.initialize_decoder(self.decoder)
        init.initialize_head(self.segmentation_head)
        if self.classification_head is not None:
            init.initialize_head(self.classification_head)

    def forward(self, x: dict) -> dict:
        """Sequentially pass `x` trough model`s encoder, decoder and heads"""
        assert len(x.keys()) == len(self.input.keys()), logging.error("Input data does not have same number of head(s) as passed input dict during class intialization")
        assert x[list(x.keys())[0]].shape[1] == len(self.input[list(self.input.keys())[0]].dates), logging.error("Input data does not have same number of dates as passed in input dict during class initialization")
        assert x[list(x.keys())[0]].shape[2] == self.num_bands, logging.error("Input data does not have same number of bands as passed in input dict during class initialization")
        
        x = x[list(self.input.keys())[0]][:, 0, :, :, :]
        features = self.encoder(x)
        decoder_output = self.decoder(*features)

        masks = self.segmentation_head(decoder_output)

        # if self.classification_head is not None:
        #     labels = self.classification_head(features[-1])
        #     return masks, labels

        masks = {list(self.output.keys())[0]: masks}
        
        return masks